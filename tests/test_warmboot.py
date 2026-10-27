"""Tests installer safety first, then synthetic guidance-contract decisions."""

from __future__ import annotations

import ast
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

SOURCE_SCRIPT = Path(__file__).resolve().parents[1] / "bin" / "warmboot"
ROOT = SOURCE_SCRIPT.parent.parent
EXAMPLE_ROOT = ROOT / "examples" / "python-guided"


def load_cli_module():
    loader = importlib.machinery.SourceFileLoader("warmboot_cli_under_test", str(SOURCE_SCRIPT))
    specification = importlib.util.spec_from_loader(loader.name, loader)
    if specification is None:
        raise RuntimeError("could not load warmboot CLI for unit testing")
    module = importlib.util.module_from_spec(specification)
    loader.exec_module(module)
    return module


CLI_MODULE = load_cli_module()


def review_java_fixture(source: str, adr: str = "", assessment: str = "") -> list[str]:
    """Apply the source-comprehension review rule to bounded synthetic Java examples.

    This is deliberately not a source linter: it recognizes only the fixtures below.
    Real changed-source review remains a language-aware human judgment.
    """

    findings: list[str] = []
    declaration = re.search(r"\b(?:class|record|enum)\s+(\w+)", source)
    if declaration is None:
        return ["fixture has no reviewed type"]
    type_name = declaration.group(1)
    leading = source[: declaration.start()]
    if not re.search(r"/\*\*.+?\*/\s*(?:public\s+)?(?:final\s+)?$", leading, re.DOTALL):
        findings.append("missing language-native type orientation")

    consequential = any(signal in source for signal in ("compareAndSet", "retry", "Duration"))
    if consequential:
        for label in ("Why:", "Invariant:", "Failure:"):
            if label not in source:
                findings.append(f"missing adjacent {label[:-1].lower()} rationale")
        if "Duration" in source and "Units:" not in source:
            findings.append("missing units")

        # Why: the review route lets an exact ADR section supplement, never replace,
        # the local contract, so a link is optional but must resolve when present.
        reference = re.search(r"See:\s+(\S+)", source)
        link = None
        if reference:
            link = re.fullmatch(r"([^\s#]+)#([a-z0-9-]+)", reference.group(1))
        if reference and link is None:
            findings.append("ADR link lacks an exact section")
        elif link is not None:
            heading = " ".join(link.group(2).split("-")).lower()
            adr_headings = {
                re.sub(r"[^a-z0-9]+", " ", line[3:].strip().lower()).strip()
                for line in adr.splitlines()
                if line.startswith("## ")
            }
            if heading not in adr_headings:
                findings.append("linked ADR section is absent")

        if not re.search(
            rf"(?im)^\s*{re.escape(type_name)}\.java\s*:\s*consequential\s*:\s*pass\s*$",
            assessment,
        ):
            findings.append("changed-source assessment is absent")
    return findings


def example_python_orientation_findings(sources: dict[str, str]) -> list[str]:
    """Check only syntax and module-docstring presence in the bounded Python example."""

    findings: list[str] = []
    for relative_path, source in sorted(sources.items()):
        try:
            module = ast.parse(source, filename=relative_path)
        except SyntaxError:
            findings.append(f"{relative_path}: invalid Python syntax")
            continue
        if ast.get_docstring(module, clean=False) is None:
            findings.append(f"{relative_path}: missing module orientation")
    return findings


def source_inventory_findings(candidate: set[str], writer_inventory: set[str]) -> list[str]:
    """Reconcile a frozen synthetic candidate set with its writer assessment."""

    missing = sorted(candidate - writer_inventory)
    unexpected = sorted(writer_inventory - candidate)
    return [
        *(f"omitted authored source: {path}" for path in missing),
        *(f"non-candidate source: {path}" for path in unexpected),
    ]


class WarmbootCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.toolkit = root / "toolkit"
        self.target = root / "target"
        (self.toolkit / "bin").mkdir(parents=True)
        (self.toolkit / "routes").mkdir(parents=True)
        self.target.mkdir()
        shutil.copy2(SOURCE_SCRIPT, self.toolkit / "bin" / "warmboot")
        (self.toolkit / "WARMBOOT.md").write_text("# Test core\n", encoding="utf-8")
        (self.toolkit / "SOURCE_REVISION").write_text("test-revision\n", encoding="utf-8")
        (self.toolkit / "routes" / "review.md").write_text("# Review route\n", encoding="utf-8")
        (self.toolkit / "routes" / "work.md").write_text("# Work route\n", encoding="utf-8")
        self.script = self.toolkit / "bin" / "warmboot"

    def run_cli(self, *arguments: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.script), *arguments],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def apply(self) -> subprocess.CompletedProcess[str]:
        return self.run_cli("init", str(self.target), "--apply")

    def test_installed_payload_has_exact_nine_file_allowlist(self) -> None:
        expected = {
            ".agent-warmboot/core.md",
            ".agent-warmboot/manifest.json",
            ".agent-warmboot/routes/context.md",
            ".agent-warmboot/routes/evidence.md",
            ".agent-warmboot/routes/handoff.md",
            ".agent-warmboot/routes/review.md",
            ".agent-warmboot/routes/rotation.md",
            "AGENTS.md",
            "CLAUDE.md",
        }
        observed = CLI_MODULE.expected_install(ROOT, self.target)
        self.assertEqual(set(observed), expected)
        self.assertEqual(len(observed), 9)

    def assert_final_structure_race_is_preserved(
        self, inject, expected_failure: str, expected_check: str
    ) -> None:
        original_create = CLI_MODULE.atomic_create
        injected = False
        warnings = io.StringIO()
        output = io.StringIO()

        def inject_after_last_create(destination: Path, data: bytes, parent_handle=None):
            nonlocal injected
            receipt = original_create(destination, data, parent_handle)
            if destination.name == "CLAUDE.md":
                inject()
                injected = True
            return receipt

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(CLI_MODULE, "atomic_create", side_effect=inject_after_last_create),
            mock.patch.object(
                CLI_MODULE.os, "unlink", side_effect=AssertionError("unlink forbidden")
            ) as unlink,
            mock.patch.object(
                CLI_MODULE.os, "rmdir", side_effect=AssertionError("rmdir forbidden")
            ) as rmdir,
            redirect_stderr(warnings),
            redirect_stdout(output),
        ):
            with self.assertRaises(CLI_MODULE.WarmbootError) as caught:
                CLI_MODULE.init_command(str(self.target), apply=True)

        self.assertTrue(injected)
        self.assertIn(expected_failure, str(caught.exception))
        self.assertNotIn("APPLIED", output.getvalue())
        self.assertIn("install stopped without rollback", warnings.getvalue())
        self.assertIn(expected_failure, warnings.getvalue())
        unlink.assert_not_called()
        rmdir.assert_not_called()

        checked = io.StringIO()
        with redirect_stdout(checked):
            self.assertEqual(CLI_MODULE.check_command(str(self.target)), 1)
        self.assertIn(expected_check, checked.getvalue())

    def test_preview_lists_exact_changes_without_mutation(self) -> None:
        result = self.run_cli("init", str(self.target))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                f"PREVIEW {self.target.resolve()} (agent review required; target semantics not inferred)",
                "CREATE-DIR .agent-warmboot",
                "CREATE-DIR .agent-warmboot/routes",
                "CREATE-FILE .agent-warmboot/core.md",
                "CREATE-FILE .agent-warmboot/manifest.json",
                "CREATE-FILE .agent-warmboot/routes/review.md",
                "CREATE-FILE .agent-warmboot/routes/work.md",
                "CREATE-FILE AGENTS.md",
                "CREATE-FILE CLAUDE.md",
                CLI_MODULE.WORKSPACE_NOTICE,
            ],
        )
        self.assertEqual(list(self.target.iterdir()), [])

    def test_apply_installs_core_routes_loaders_and_manifest(self) -> None:
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (self.target / ".agent-warmboot" / "core.md").read_text(encoding="utf-8"),
            "# Test core\n",
        )
        self.assertEqual(
            (self.target / ".agent-warmboot" / "routes" / "review.md").read_text(encoding="utf-8"),
            "# Review route\n",
        )
        self.assertEqual(
            (self.target / "AGENTS.md").read_bytes(),
            (self.target / "CLAUDE.md").read_bytes(),
        )
        self.assertFalse((self.target / "target.code-workspace").exists())
        manifest = json.loads(
            (self.target / ".agent-warmboot" / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["schema"], 1)
        self.assertEqual(manifest["toolkit"], "agent-warmboot")
        self.assertEqual(manifest["source_revision"], "test-revision")
        core = (self.target / ".agent-warmboot" / "core.md").read_bytes()
        self.assertEqual(
            manifest["files"][".agent-warmboot/core.md"], hashlib.sha256(core).hexdigest()
        )
        self.assertFalse(any(path.endswith(".code-workspace") for path in manifest["files"]))
        self.assertIn(CLI_MODULE.WORKSPACE_NOTICE, result.stdout)

    def test_source_revision_absence_never_calls_subprocess_or_git(self) -> None:
        (self.toolkit / "SOURCE_REVISION").unlink()
        with mock.patch("subprocess.run", side_effect=AssertionError("subprocess forbidden")):
            self.assertEqual(CLI_MODULE.source_revision(self.toolkit), "UNCOMMITTED")

    def test_source_revision_rejects_unsafe_format(self) -> None:
        for value in ("embedded\tcontrol\n", "x" * 257 + "\n"):
            with self.subTest(value_length=len(value)):
                (self.toolkit / "SOURCE_REVISION").write_text(value, encoding="utf-8")
                with self.assertRaisesRegex(
                    CLI_MODULE.WarmbootError, "one non-empty printable line"
                ):
                    CLI_MODULE.source_revision(self.toolkit)

    def test_check_passes_after_apply(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        result = self.run_cli("check", str(self.target))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("manifest-declared content and structure matched", result.stdout)
        self.assertIn(
            "source_revision is informational/self-declared, not authenticated", result.stdout
        )
        self.assertIn(CLI_MODULE.WORKSPACE_NOTICE, result.stdout)

    def test_check_uses_frozen_manifest_after_source_revision_changes(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        (self.toolkit / "SOURCE_REVISION").write_text("later-revision\n", encoding="utf-8")
        (self.toolkit / "WARMBOOT.md").write_text("# Later source core\n", encoding="utf-8")
        result = self.run_cli("check", str(self.target))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_check_does_not_authenticate_manifest_declared_source_revision(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["source_revision"] = "coherently-tampered-metadata"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        result = self.run_cli("check", str(self.target))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("manifest-declared content and structure matched", result.stdout)
        self.assertIn("informational/self-declared, not authenticated", result.stdout)
        self.assertNotIn("provenance", result.stdout.lower())

    def test_check_rejects_boolean_manifest_schema(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["schema"] = True
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        result = self.run_cli("check", str(self.target))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("manifest.json: unsupported schema", result.stdout)

    def test_check_rejects_duplicate_key_manifest(self) -> None:
        """Installed-state duplicate-key manifests must fail closed, not last-wins.

        WB-006: the import-free CLI parses `manifest.json` itself, so a repeated object
        key, top-level or nested, must be rejected at parse rather than silently
        resolved to its last value. A bogus first block (a 0*64 digest for a frozen
        path) shadowed by the real block would otherwise let a tampered install pass
        `check` at exit 0. `json.dumps` cannot emit a repeated key, so each manifest is
        assembled as raw text.
        """
        self.assertEqual(self.apply().returncode, 0)
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        real = json.loads(manifest_path.read_text(encoding="utf-8"))
        frozen_path = min(real["files"])

        def render(pairs: list, indent: int) -> str:
            pad = " " * indent
            body = ",\n".join(f"{pad}{json.dumps(key)}: {value}" for key, value in pairs)
            return "{\n" + body + "\n" + " " * (indent - 2) + "}"

        bogus_files = {
            path: ("0" * 64 if path == frozen_path else digest)
            for path, digest in real["files"].items()
        }
        nested_files = render(
            [(frozen_path, json.dumps("0" * 64))]
            + [(path, json.dumps(digest)) for path, digest in sorted(real["files"].items())],
            4,
        )
        scalars = [
            ("schema", json.dumps(real["schema"])),
            ("source_revision", json.dumps(real["source_revision"])),
            ("toolkit", json.dumps(real["toolkit"])),
        ]
        duplicate_manifests = {
            "top-level duplicate files key": render(
                [
                    ("files", json.dumps(bogus_files, sort_keys=True)),
                    ("files", json.dumps(real["files"], sort_keys=True)),
                    *scalars,
                ],
                2,
            ),
            "nested duplicate managed-file key": render([("files", nested_files), *scalars], 2),
        }
        for name, raw in sorted(duplicate_manifests.items()):
            with self.subTest(manifest=name):
                manifest_path.write_text(raw + "\n", encoding="utf-8")
                result = self.run_cli("check", str(self.target))
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("manifest.json: invalid JSON", result.stdout)

    def test_check_rejects_deeply_nested_manifest_as_invalid_json(self) -> None:
        """Nesting deep enough to exhaust the decoder's recursion must fail as invalid JSON.

        WB-007: the decoder raises RecursionError, which is not a ValueError, so without an
        explicit catch `check` would stop with a traceback instead of a clean FAIL line.
        """
        self.assertEqual(self.apply().returncode, 0)
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        manifest_path.write_text("[" * 200000 + "]" * 200000 + "\n", encoding="utf-8")

        result = self.run_cli("check", str(self.target))

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("manifest.json: invalid JSON", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_check_rejects_non_json_numeric_constants(self) -> None:
        """`NaN`, `Infinity` and `-Infinity` are not JSON and must fail as invalid JSON.

        WB-007: the standard decoder accepts these tokens by default, so a manifest could
        carry values no other JSON reader accepts.
        """
        self.assertEqual(self.apply().returncode, 0)
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        original = manifest_path.read_text(encoding="utf-8")
        for token in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(token=token):
                manifest_path.write_text(
                    original.replace('"schema": 1', f'"schema": {token}', 1),
                    encoding="utf-8",
                )
                result = self.run_cli("check", str(self.target))
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("manifest.json: invalid JSON", result.stdout)

    def test_check_rejects_invalid_os_paths_without_traceback(self) -> None:
        # Valid JSON can still carry names rejected by filesystem APIs. These pins
        # reach manifest filenames, unlike the schema/source-revision cases above.
        self.assertEqual(self.apply().returncode, 0)
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        original = json.loads(manifest_path.read_text(encoding="utf-8"))
        with self.assertRaises(UnicodeEncodeError):
            os.fsencode("bad\ud800name")
        for name in ("bad\x00name", "bad\ud800name"):
            with self.subTest(name=repr(name)):
                manifest = dict(original, files=dict(original["files"]))
                manifest["files"][name] = "0" * 64
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                before = {
                    path.relative_to(self.target): path.read_bytes()
                    for path in self.target.rglob("*")
                    if path.is_file()
                }

                checked = self.run_cli("check", str(self.target))

                self.assertEqual(checked.returncode, 1)
                self.assertIn("FAIL", checked.stdout)
                self.assertIn("invalid managed file entry", checked.stdout)
                self.assertNotIn("Traceback", checked.stderr)
                self.assertEqual(
                    before,
                    {
                        path.relative_to(self.target): path.read_bytes()
                        for path in self.target.rglob("*")
                        if path.is_file()
                    },
                )

    def test_check_reports_unexpected_manifest_entry_without_opening_it(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        unmanaged = self.target / "unmanaged.txt"
        sentinel = b"harmless project-owned content\n"
        unmanaged.write_bytes(sentinel)
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        # A correct hash makes allowlist membership, not a content mismatch, the
        # reason for refusal. Observe real os.open without replacing filesystem I/O.
        manifest["files"]["unmanaged.txt"] = hashlib.sha256(sentinel).hexdigest()
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        before = {
            path.relative_to(self.target): path.read_bytes()
            for path in self.target.rglob("*")
            if path.is_file()
        }
        output = io.StringIO()
        with (
            mock.patch.object(CLI_MODULE.os, "open", wraps=os.open) as opened,
            redirect_stdout(output),
        ):
            result = CLI_MODULE.main(["check", str(self.target)])

        self.assertEqual(result, 1)
        self.assertIn("unexpected entries: unmanaged.txt", output.getvalue())
        self.assertFalse(any(call.args[0] == "unmanaged.txt" for call in opened.call_args_list))
        self.assertEqual(
            before,
            {
                path.relative_to(self.target): path.read_bytes()
                for path in self.target.rglob("*")
                if path.is_file()
            },
        )

    def test_check_displays_surrogateescape_manifest_key_with_strict_stdout(self) -> None:
        # StringIO and the runner's inherited encoding can hide this failure. The
        # name is OS-encodable, so preserve validation and escape only its diagnostic.
        self.assertEqual(self.apply().returncode, 0)
        self.assertEqual(os.fsencode("x\udc80name"), b"x\x80name")
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        original = json.loads(manifest_path.read_text(encoding="utf-8"))
        cases = (
            ("x\udc80name", r"x\udc80name", "unexpected entries:"),
            (
                ".agent-warmboot/routes/r\udc80.md",
                r".agent-warmboot/routes/r\udc80.md",
                "missing managed path(s):",
            ),
        )
        for name, displayed_name, reason in cases:
            with self.subTest(name=repr(name)):
                manifest = dict(original, files=dict(original["files"]))
                manifest["files"][name] = "0" * 64
                manifest["files"]["café"] = "0" * 64
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                before = {
                    path.relative_to(self.target): path.read_bytes()
                    for path in self.target.rglob("*")
                    if path.is_file()
                }

                checked = subprocess.run(
                    [sys.executable, str(self.script), "check", str(self.target)],
                    env={**os.environ, "PYTHONIOENCODING": "utf-8:strict"},
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertEqual(checked.returncode, 1)
                self.assertIn("FAIL", checked.stdout)
                self.assertIn(reason, checked.stdout)
                self.assertIn(displayed_name, checked.stdout)
                self.assertIn("café", checked.stdout)
                self.assertNotIn("invalid managed file entry", checked.stdout + checked.stderr)
                self.assertNotIn("Traceback", checked.stderr)
                self.assertEqual(
                    before,
                    {
                        path.relative_to(self.target): path.read_bytes()
                        for path in self.target.rglob("*")
                        if path.is_file()
                    },
                )

    def test_check_preserves_variable_unicode_route_sets(self) -> None:
        # Installed route declarations are frozen independently of this helper's
        # current checkout. A valid non-ASCII name must not be rejected as malformed.
        self.assertEqual(self.apply().returncode, 0)
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for name in ("review.md", "work.md"):
            relative = f".agent-warmboot/routes/{name}"
            (self.target / relative).unlink()
            del manifest["files"][relative]
        relative = ".agent-warmboot/routes/résumé.md"
        route = b"# Optional installed route\n"
        (self.target / relative).write_bytes(route)
        manifest["files"][relative] = hashlib.sha256(route).hexdigest()
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        checked = self.run_cli("check", str(self.target))

        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("PASS", checked.stdout)
        self.assertEqual((self.target / relative).read_bytes(), route)

    def test_apply_is_idempotent(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        before = {
            path.relative_to(self.target): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in self.target.rglob("*")
            if path.is_file()
        }
        second = self.apply()
        after = {
            path.relative_to(self.target): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in self.target.rglob("*")
            if path.is_file()
        }
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("0 file(s) created", second.stdout)
        self.assertEqual(before, after)

    def test_loader_conflict_fails_before_any_mutation(self) -> None:
        (self.target / "AGENTS.md").write_text(
            "# Project-specific instructions\n", encoding="utf-8"
        )
        result = self.apply()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("is not the Warmboot loader", result.stderr)
        self.assertIn("BOOTSTRAP.md#existing-agent-instructions", result.stderr)
        self.assertFalse((self.target / ".agent-warmboot").exists())
        self.assertFalse((self.target / "CLAUDE.md").exists())
        self.assertEqual(
            (self.target / "AGENTS.md").read_text(encoding="utf-8"),
            "# Project-specific instructions\n",
        )

    def test_target_named_workspace_is_unmanaged_and_preserved(self) -> None:
        workspace = self.target / "target.code-workspace"
        sentinel = b'{"folders": [], "settings": {"sentinel": true}}\n'
        workspace.write_bytes(sentinel)
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(workspace.read_bytes(), sentinel)
        check = self.run_cli("check", str(self.target))
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual(workspace.read_bytes(), sentinel)

    def test_preexisting_binary_under_managed_root_fails_before_mutation(self) -> None:
        managed = self.target / ".agent-warmboot"
        managed.mkdir()
        preexisting = managed / "preexisting.bin"
        preexisting.write_bytes(b"preserve me\x00")

        result = self.apply()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unexpected managed path(s): .agent-warmboot/preexisting.bin", result.stderr)
        self.assertEqual(preexisting.read_bytes(), b"preserve me\x00")
        self.assertEqual(sorted(path.name for path in managed.iterdir()), ["preexisting.bin"])
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertFalse((self.target / "CLAUDE.md").exists())
        self.assertFalse((self.target / "target.code-workspace").exists())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_fifo_under_managed_root_is_always_unexpected(self) -> None:
        managed = self.target / ".agent-warmboot"
        managed.mkdir()
        fifo = managed / "preexisting.fifo"
        os.mkfifo(fifo)

        refused = self.apply()

        self.assertNotEqual(refused.returncode, 0)
        self.assertIn(
            "unexpected managed path(s): .agent-warmboot/preexisting.fifo", refused.stderr
        )
        self.assertFalse((self.target / "AGENTS.md").exists())
        fifo.unlink()
        self.assertEqual(self.apply().returncode, 0)
        extra_fifo = managed / "unexpected.fifo"
        os.mkfifo(extra_fifo)

        checked = self.run_cli("check", str(self.target))

        self.assertNotEqual(checked.returncode, 0)
        self.assertIn("unexpected managed path(s): .agent-warmboot/unexpected.fifo", checked.stdout)

    def test_unexpected_managed_directory_and_symlink_fail_before_mutation(self) -> None:
        routes = self.target / ".agent-warmboot" / "routes"
        routes.mkdir(parents=True)
        unexpected_directory = self.target / ".agent-warmboot" / "cache"
        unexpected_directory.mkdir()
        (unexpected_directory / "state.bin").write_bytes(b"state")
        sentinel = self.target / "sentinel.txt"
        sentinel.write_text("keep\n", encoding="utf-8")
        unexpected_symlink = self.target / ".agent-warmboot" / "sentinel-link"
        unexpected_symlink.symlink_to("../sentinel.txt")

        result = self.apply()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(".agent-warmboot/cache", result.stderr)
        self.assertIn(".agent-warmboot/sentinel-link", result.stderr)
        self.assertTrue(unexpected_directory.is_dir())
        self.assertEqual((unexpected_directory / "state.bin").read_bytes(), b"state")
        self.assertTrue(unexpected_symlink.is_symlink())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep\n")
        self.assertEqual(list(routes.iterdir()), [])
        self.assertFalse((self.target / ".agent-warmboot" / "core.md").exists())
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertFalse((self.target / "CLAUDE.md").exists())
        self.assertFalse((self.target / "target.code-workspace").exists())

    def test_empty_expected_managed_parent_directories_are_preserved(self) -> None:
        routes = self.target / ".agent-warmboot" / "routes"
        routes.mkdir(parents=True)
        managed_identity = (routes.parent.stat().st_dev, routes.parent.stat().st_ino)
        routes_identity = (routes.stat().st_dev, routes.stat().st_ino)

        result = self.apply()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(routes.is_dir())
        self.assertEqual(
            (routes.parent.stat().st_dev, routes.parent.stat().st_ino), managed_identity
        )
        self.assertEqual((routes.stat().st_dev, routes.stat().st_ino), routes_identity)
        check = self.run_cli("check", str(self.target))
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_differently_named_workspace_survives_preview_apply_rerun_and_check(self) -> None:
        other = self.target / "existing.code-workspace"
        sentinel = (
            b'{"folders": [{"path": "existing"}], "settings": {"sentinel": true}, '
            b'"tasks": {"version": "2.0.0", "tasks": []}}\n'
        )
        other.write_bytes(sentinel)

        preview = self.run_cli("init", str(self.target))
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(other.read_bytes(), sentinel)

        applied = self.apply()
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertEqual(other.read_bytes(), sentinel)
        rerun = self.apply()
        self.assertEqual(rerun.returncode, 0, rerun.stderr)
        self.assertEqual(other.read_bytes(), sentinel)
        check = self.run_cli("check", str(self.target))
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual(other.read_bytes(), sentinel)
        self.assertFalse((self.target / "target.code-workspace").exists())

    def test_multiple_invalid_and_symlink_workspaces_are_unmanaged_and_preserved(self) -> None:
        backing = self.target / "workspace-source.json"
        backing.write_text('{"folders": []}\n', encoding="utf-8")
        invalid = self.target / "target.code-workspace"
        invalid_bytes = b"not-json\n"
        invalid.write_bytes(invalid_bytes)
        workspace = self.target / "linked.code-workspace"
        workspace.symlink_to(backing.name)
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(invalid.read_bytes(), invalid_bytes)
        self.assertTrue(workspace.is_symlink())
        self.assertEqual(os.readlink(workspace), backing.name)
        check = self.run_cli("check", str(self.target))
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual(invalid.read_bytes(), invalid_bytes)
        self.assertTrue(workspace.is_symlink())

    def test_workspace_edit_after_apply_does_not_fail_managed_check(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        workspace = self.target / "target.code-workspace"
        workspace.write_text('{"folders": [{"path": ".", "name": "Target"}]}\n', encoding="utf-8")
        first = self.run_cli("check", str(self.target))
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        workspace.write_text(
            '{"folders": [{"path": ".", "name": "Target project"}], '
            '"settings": {"editor.formatOnSave": true}}\n',
            encoding="utf-8",
        )
        second = self.run_cli("check", str(self.target))
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertIn(CLI_MODULE.WORKSPACE_NOTICE, second.stdout)

    def test_final_rescan_rejects_concurrent_unexpected_managed_path(self) -> None:
        extra = self.target / ".agent-warmboot" / "concurrent-extra.bin"

        self.assert_final_structure_race_is_preserved(
            lambda: extra.write_bytes(b"concurrent managed content\n"),
            "unexpected managed path(s): .agent-warmboot/concurrent-extra.bin",
            "unexpected managed path(s): .agent-warmboot/concurrent-extra.bin",
        )

        self.assertEqual(extra.read_bytes(), b"concurrent managed content\n")
        self.assertTrue((self.target / ".agent-warmboot" / "manifest.json").is_file())

    def test_final_rescan_rejects_concurrent_root_stage(self) -> None:
        stage_name = f".{CLI_MODULE.MANAGED_DIR}.{'0' * 24}.create"
        stage = self.target / stage_name

        self.assert_final_structure_race_is_preserved(
            stage.mkdir,
            f"preserved staged path(s) require inspection: {stage_name}",
            f"preserved staged path(s) require inspection: {stage_name}",
        )

        self.assertTrue(stage.is_dir())
        self.assertTrue((self.target / "CLAUDE.md").is_file())

    def test_create_failure_preserves_compatible_progress_for_rerun(self) -> None:
        sentinel = self.target / "TASK.md"
        sentinel.write_bytes(b"existing task\n")
        original_create = CLI_MODULE.atomic_create
        call_count = 0
        warnings = io.StringIO()

        def fail_on_second_create(destination: Path, data: bytes, parent_handle=None):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise OSError("injected second-create failure")
            return original_create(destination, data, parent_handle)

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(CLI_MODULE, "atomic_create", side_effect=fail_on_second_create),
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(OSError, "injected second-create failure"):
                CLI_MODULE.init_command(str(self.target), apply=True)

        core = self.target / ".agent-warmboot" / "core.md"
        self.assertEqual(sentinel.read_bytes(), b"existing task\n")
        self.assertEqual(core.read_bytes(), b"# Test core\n")
        self.assertTrue((self.target / ".agent-warmboot" / "routes").is_dir())
        self.assertFalse((self.target / ".agent-warmboot" / "manifest.json").exists())
        self.assertIn("install stopped without rollback", warnings.getvalue())
        self.assertIn(str(core), warnings.getvalue())

        recovered = self.apply()
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        self.assertEqual(core.read_bytes(), b"# Test core\n")
        self.assertEqual(self.run_cli("check", str(self.target)).returncode, 0)

    def test_managed_parent_symlink_swap_cannot_redirect_creation(self) -> None:
        managed = self.target / ".agent-warmboot"
        routes = managed / "routes"
        routes.mkdir(parents=True)
        detached = self.target / "detached-managed"
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        original_create = CLI_MODULE.atomic_create
        swapped = False
        warnings = io.StringIO()

        def swap_then_create(destination: Path, data: bytes, parent_handle=None):
            nonlocal swapped
            if CLI_MODULE.MANAGED_DIR in destination.parts and not swapped:
                managed.rename(detached)
                managed.symlink_to(outside, target_is_directory=True)
                swapped = True
            return original_create(destination, data, parent_handle)

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(CLI_MODULE, "atomic_create", side_effect=swap_then_create),
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(
                CLI_MODULE.WarmbootError, "directory containment changed during install"
            ):
                CLI_MODULE.init_command(str(self.target), apply=True)

        self.assertTrue(swapped)
        self.assertTrue(managed.is_symlink())
        self.assertEqual(list(outside.iterdir()), [])
        self.assertEqual([routes for routes in detached.rglob("*") if routes.is_file()], [])
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertFalse((self.target / "CLAUDE.md").exists())
        self.assertFalse((self.target / "target.code-workspace").exists())
        self.assertIn("preserved observed state", warnings.getvalue())

    def test_late_parent_rename_preserves_inode_and_warns_paths_may_have_moved(self) -> None:
        # The swap tests above inject before atomic_create's validation; this one injects
        # in the later syscall window, proving the warning rather than promising
        # containment across hostile renames. Real descriptor-relative creation is used.
        managed = self.target.resolve() / ".agent-warmboot"
        moved = self.target.resolve().parent / "moved-original"
        original_open = os.open
        original_identity = None
        injected = False

        def move_before_create(name, flags, *args, **kwargs):
            nonlocal original_identity, injected
            if name == "core.md" and flags & os.O_CREAT and not injected:
                identity = managed.stat()
                original_identity = (identity.st_dev, identity.st_ino)
                managed.rename(moved)
                managed.mkdir()
                injected = True
            return original_open(name, flags, *args, **kwargs)

        output, warnings = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(CLI_MODULE.os, "open", side_effect=move_before_create),
            redirect_stdout(output),
            redirect_stderr(warnings),
        ):
            result = CLI_MODULE.main(["init", str(self.target), "--apply"])

        self.assertTrue(injected)
        self.assertEqual(result, 1)
        self.assertNotIn("APPLIED", output.getvalue())
        self.assertEqual(original_identity, (moved.stat().st_dev, moved.stat().st_ino))
        self.assertEqual(list(managed.iterdir()), [])
        # This outside write is the documented limit: a rename after validation moves it.
        self.assertEqual((moved / "core.md").read_bytes(), b"# Test core\n")
        self.assertIn("preservation", warnings.getvalue())
        self.assertIn("recorded paths may have moved", warnings.getvalue())

    def test_target_replacement_after_preflight_cannot_receive_install(self) -> None:
        sentinel = self.target / "TASK.md"
        sentinel.write_bytes(b"original target\n")
        detached = self.target.parent / "detached-original"
        original_preflight = CLI_MODULE.preflight_install
        swapped = False
        warnings = io.StringIO()

        def replace_target_after_preflight(target, expected, handles=None):
            nonlocal swapped
            creates = original_preflight(target, expected, handles)
            target.rename(detached)
            target.mkdir()
            swapped = True
            return creates

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(
                CLI_MODULE,
                "preflight_install",
                side_effect=replace_target_after_preflight,
            ),
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(
                CLI_MODULE.WarmbootError, "directory containment changed during install"
            ):
                CLI_MODULE.init_command(str(self.target), apply=True)

        self.assertTrue(swapped)
        self.assertEqual(list(self.target.iterdir()), [])
        self.assertEqual((detached / "TASK.md").read_bytes(), b"original target\n")
        self.assertFalse((detached / ".agent-warmboot").exists())
        self.assertFalse((detached / "AGENTS.md").exists())
        self.assertIn("preserved observed state", warnings.getvalue())

    def test_created_managed_root_replacement_is_not_adopted(self) -> None:
        managed = self.target / CLI_MODULE.MANAGED_DIR
        original_mkdir = CLI_MODULE.os.mkdir
        replacement_inode: int | None = None
        injected = False
        warnings = io.StringIO()

        def inject_final_after_staged_mkdir(path, *args, **kwargs):
            nonlocal replacement_inode, injected
            result = original_mkdir(path, *args, **kwargs)
            if str(path).startswith("..agent-warmboot.") and not injected:
                original_mkdir(CLI_MODULE.MANAGED_DIR, dir_fd=kwargs["dir_fd"])
                (managed / "replacement.txt").write_bytes(b"preserve replacement\n")
                replacement_inode = managed.stat().st_ino
                injected = True
            return result

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(CLI_MODULE.os, "mkdir", side_effect=inject_final_after_staged_mkdir),
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(
                CLI_MODULE.WarmbootError,
                "could not publish created directory safely: .agent-warmboot",
            ):
                CLI_MODULE.init_command(str(self.target), apply=True)

        staged = list(self.target.glob("..agent-warmboot.*.create"))
        self.assertTrue(injected)
        self.assertEqual(managed.stat().st_ino, replacement_inode)
        self.assertEqual((managed / "replacement.txt").read_bytes(), b"preserve replacement\n")
        self.assertEqual(len(staged), 1)
        self.assertEqual(CLI_MODULE.stat.S_IMODE(staged[0].stat().st_mode), 0o700)
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertIn("staged directory publication is uncertain", warnings.getvalue())

    def test_staged_directory_fails_closed_when_no_replace_is_unavailable(self) -> None:
        parent = CLI_MODULE.open_directory_handle(self.target)
        warnings = io.StringIO()
        try:
            with (
                mock.patch.object(CLI_MODULE.sys, "platform", "unsupported-platform"),
                redirect_stderr(warnings),
            ):
                with self.assertRaisesRegex(
                    CLI_MODULE.WarmbootError,
                    "could not publish created directory safely: .agent-warmboot",
                ):
                    CLI_MODULE.create_staged_directory(
                        self.target,
                        CLI_MODULE.MANAGED_DIR,
                        parent,
                        CLI_MODULE.MANAGED_DIR,
                    )
        finally:
            CLI_MODULE.close_directory_handles([parent])

        staged = list(self.target.glob("..agent-warmboot.*.create"))
        self.assertEqual(len(staged), 1)
        self.assertFalse((self.target / CLI_MODULE.MANAGED_DIR).exists())
        self.assertIn("atomic no-replace rename is unavailable", warnings.getvalue())
        self.assertIn("preserved final/staged state", warnings.getvalue())

        with mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit):
            with self.assertRaisesRegex(
                CLI_MODULE.WarmbootError,
                "preserved staged path.*require inspection before install",
            ):
                CLI_MODULE.init_command(str(self.target), apply=True)
        checked = io.StringIO()
        with redirect_stdout(checked):
            self.assertEqual(CLI_MODULE.check_command(str(self.target)), 1)
        self.assertIn("preserved staged path(s) require inspection", checked.getvalue())

    def test_created_routes_replacement_is_not_adopted(self) -> None:
        original_mkdir = CLI_MODULE.os.mkdir
        replacement_inode: int | None = None
        injected = False
        warnings = io.StringIO()

        def inject_final_after_staged_mkdir(path, *args, **kwargs):
            nonlocal replacement_inode, injected
            result = original_mkdir(path, *args, **kwargs)
            if str(path).startswith(".routes.") and not injected:
                original_mkdir("routes", dir_fd=kwargs["dir_fd"])
                managed = self.target / CLI_MODULE.MANAGED_DIR
                routes = managed / "routes"
                (routes / "replacement.txt").write_bytes(b"preserve replacement\n")
                replacement_inode = routes.stat().st_ino
                injected = True
            return result

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(CLI_MODULE.os, "mkdir", side_effect=inject_final_after_staged_mkdir),
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(
                CLI_MODULE.WarmbootError,
                "could not publish created directory safely: .agent-warmboot/routes",
            ):
                CLI_MODULE.init_command(str(self.target), apply=True)

        managed = self.target / CLI_MODULE.MANAGED_DIR
        routes = managed / "routes"
        self.assertTrue(injected)
        self.assertTrue(managed.is_dir())
        self.assertEqual(routes.stat().st_ino, replacement_inode)
        self.assertEqual(
            (routes / "replacement.txt").read_bytes(),
            b"preserve replacement\n",
        )
        staged = list(managed.glob(".routes.*.create"))
        self.assertEqual(len(staged), 1)
        self.assertEqual(CLI_MODULE.stat.S_IMODE(staged[0].stat().st_mode), 0o700)
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertIn("staged directory publication is uncertain", warnings.getvalue())
        self.assertIn("install stopped without rollback", warnings.getvalue())

    def test_created_managed_root_inspection_failure_is_reported_and_preserved(self) -> None:
        original_mkdir = CLI_MODULE.os.mkdir
        original_stat = CLI_MODULE.os.stat
        staged_name: str | None = None
        failed = False
        warnings = io.StringIO()

        def record_mkdir(path, *args, **kwargs):
            nonlocal staged_name
            result = original_mkdir(path, *args, **kwargs)
            if str(path).startswith("..agent-warmboot."):
                staged_name = str(path)
            return result

        def fail_created_stat(path, *args, **kwargs):
            nonlocal failed
            if path == staged_name and kwargs.get("dir_fd") is not None and not failed:
                failed = True
                raise OSError("injected managed identity failure")
            return original_stat(path, *args, **kwargs)

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(CLI_MODULE.os, "mkdir", side_effect=record_mkdir),
            mock.patch.object(CLI_MODULE.os, "stat", side_effect=fail_created_stat),
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(
                CLI_MODULE.WarmbootError,
                "could not publish created directory safely: .agent-warmboot",
            ):
                CLI_MODULE.init_command(str(self.target), apply=True)

        self.assertTrue(failed)
        staged = list(self.target.glob("..agent-warmboot.*.create"))
        self.assertEqual(len(staged), 1)
        self.assertEqual(CLI_MODULE.stat.S_IMODE(staged[0].stat().st_mode), 0o700)
        self.assertFalse((self.target / CLI_MODULE.MANAGED_DIR).exists())
        self.assertIn("injected managed identity failure", warnings.getvalue())
        self.assertIn("preserved final/staged state", warnings.getvalue())

    def test_created_routes_inspection_failure_is_reported_and_preserved(self) -> None:
        original_mkdir = CLI_MODULE.os.mkdir
        original_stat = CLI_MODULE.os.stat
        staged_name: str | None = None
        failed = False
        warnings = io.StringIO()

        def record_mkdir(path, *args, **kwargs):
            nonlocal staged_name
            result = original_mkdir(path, *args, **kwargs)
            if str(path).startswith(".routes."):
                staged_name = str(path)
            return result

        def fail_created_stat(path, *args, **kwargs):
            nonlocal failed
            if path == staged_name and kwargs.get("dir_fd") is not None and not failed:
                failed = True
                raise OSError("injected routes identity failure")
            return original_stat(path, *args, **kwargs)

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(CLI_MODULE.os, "mkdir", side_effect=record_mkdir),
            mock.patch.object(CLI_MODULE.os, "stat", side_effect=fail_created_stat),
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(
                CLI_MODULE.WarmbootError,
                "could not publish created directory safely: .agent-warmboot/routes",
            ):
                CLI_MODULE.init_command(str(self.target), apply=True)

        managed = self.target / CLI_MODULE.MANAGED_DIR
        self.assertTrue(failed)
        self.assertTrue(managed.is_dir())
        staged = list(managed.glob(".routes.*.create"))
        self.assertEqual(len(staged), 1)
        self.assertEqual(CLI_MODULE.stat.S_IMODE(staged[0].stat().st_mode), 0o700)
        self.assertFalse((managed / "routes").exists())
        self.assertIn("injected routes identity failure", warnings.getvalue())
        self.assertIn("preserved final/staged state", warnings.getvalue())
        self.assertIn("install stopped without rollback", warnings.getvalue())

    def test_existing_leaf_symlink_swap_after_preflight_prevents_applied(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        (self.target / "CLAUDE.md").unlink()
        outside = self.target.parent / "outside-loader.md"
        outside.write_bytes(b"outside\n")
        original_preflight = CLI_MODULE.preflight_install
        swapped = False
        warnings = io.StringIO()

        def swap_loader_after_preflight(target, expected, handles=None):
            nonlocal swapped
            creates = original_preflight(target, expected, handles)
            agents = target / "AGENTS.md"
            agents.unlink()
            agents.symlink_to(outside)
            swapped = True
            return creates

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(
                CLI_MODULE,
                "preflight_install",
                side_effect=swap_loader_after_preflight,
            ),
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(
                CLI_MODULE.WarmbootError, "install result changed before completion"
            ):
                CLI_MODULE.init_command(str(self.target), apply=True)

        self.assertTrue(swapped)
        self.assertTrue((self.target / "AGENTS.md").is_symlink())
        self.assertEqual(outside.read_bytes(), b"outside\n")
        self.assertEqual(
            (self.target / "CLAUDE.md").read_bytes(), CLI_MODULE.LOADER.encode("utf-8")
        )
        self.assertIn(str(self.target / "CLAUDE.md"), warnings.getvalue())
        rerun = self.apply()
        self.assertNotEqual(rerun.returncode, 0)
        self.assertIn("AGENTS.md is a symlink", rerun.stderr)
        self.assertTrue((self.target / "AGENTS.md").is_symlink())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_preflight_fifo_swap_is_rejected_without_blocking(self) -> None:
        agents = self.target / "AGENTS.md"
        agents.write_bytes(CLI_MODULE.LOADER.encode("utf-8"))
        original_open = CLI_MODULE.os.open
        swapped = False

        def swap_to_fifo_before_open(path, flags, *args, **kwargs):
            nonlocal swapped
            if path == "AGENTS.md" and kwargs.get("dir_fd") is not None and not swapped:
                agents.unlink()
                os.mkfifo(agents)
                swapped = True
            return original_open(path, flags, *args, **kwargs)

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(CLI_MODULE.os, "open", side_effect=swap_to_fifo_before_open),
        ):
            with self.assertRaisesRegex(CLI_MODULE.WarmbootError, "file changed"):
                CLI_MODULE.init_command(str(self.target), apply=True)

        self.assertTrue(swapped)
        self.assertTrue(CLI_MODULE.stat.S_ISFIFO(agents.stat(follow_symlinks=False).st_mode))
        self.assertFalse((self.target / ".agent-warmboot").exists())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_check_fifo_swap_is_rejected_without_pass(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        agents = self.target.resolve() / "AGENTS.md"
        original_open = CLI_MODULE.os.open
        swapped = False

        def swap_to_fifo_before_open(path, flags, *args, **kwargs):
            nonlocal swapped
            if path == "AGENTS.md" and kwargs.get("dir_fd") is not None and not swapped:
                agents.unlink()
                os.mkfifo(agents)
                swapped = True
            return original_open(path, flags, *args, **kwargs)

        with mock.patch.object(CLI_MODULE.os, "open", side_effect=swap_to_fifo_before_open):
            with self.assertRaisesRegex(CLI_MODULE.WarmbootError, "file changed"):
                CLI_MODULE.check_command(str(self.target))

        self.assertTrue(swapped)
        self.assertTrue(CLI_MODULE.stat.S_ISFIFO(agents.stat(follow_symlinks=False).st_mode))

    def test_atomic_create_uses_final_name_without_any_delete_boundary(self) -> None:
        destination = self.target / "direct-final.txt"

        with (
            mock.patch.object(
                CLI_MODULE.os, "unlink", side_effect=AssertionError("unlink forbidden")
            ) as unlink,
            mock.patch.object(
                CLI_MODULE.os, "rmdir", side_effect=AssertionError("rmdir forbidden")
            ) as rmdir,
        ):
            receipt = CLI_MODULE.atomic_create(destination, b"direct content\n")

        self.assertEqual(receipt.path, destination)
        self.assertEqual(receipt.inode, destination.stat().st_ino)
        self.assertEqual(destination.read_bytes(), b"direct content\n")
        self.assertEqual(list(self.target.iterdir()), [destination])
        unlink.assert_not_called()
        rmdir.assert_not_called()

    def test_atomic_create_never_overwrites_an_existing_final_path(self) -> None:
        destination = self.target / "existing-final.txt"
        destination.write_bytes(b"concurrent content\n")

        with self.assertRaisesRegex(
            CLI_MODULE.WarmbootError, "destination appeared during install"
        ):
            CLI_MODULE.atomic_create(destination, b"managed content\n")

        self.assertEqual(destination.read_bytes(), b"concurrent content\n")

    def test_atomic_create_preserves_final_file_after_receipt_failure(self) -> None:
        destination = self.target / "receipt-failure.txt"
        warnings = io.StringIO()

        with (
            mock.patch.object(
                CLI_MODULE, "sha256", side_effect=OSError("injected receipt hash failure")
            ),
            mock.patch.object(
                CLI_MODULE.os, "unlink", side_effect=AssertionError("unlink forbidden")
            ) as unlink,
            mock.patch.object(
                CLI_MODULE.os, "rmdir", side_effect=AssertionError("rmdir forbidden")
            ) as rmdir,
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(OSError, "injected receipt hash failure"):
                CLI_MODULE.atomic_create(destination, b"new content\n")

        self.assertEqual(destination.read_bytes(), b"new content\n")
        self.assertIn(str(destination), warnings.getvalue())
        self.assertIn("preserved the final path without cleanup", warnings.getvalue())
        unlink.assert_not_called()
        rmdir.assert_not_called()

    def test_atomic_create_preserves_replacement_after_postflight_failure(self) -> None:
        destination = self.target / "replaced-before-receipt.txt"
        original_stat = CLI_MODULE.os.stat
        replaced = False
        warnings = io.StringIO()

        def replace_then_fail(path, *args, **kwargs):
            nonlocal replaced
            result = original_stat(path, *args, **kwargs)
            if path == destination.name and kwargs.get("dir_fd") is not None and not replaced:
                destination.unlink()
                destination.write_bytes(b"replacement content\n")
                replaced = True
                raise OSError("injected receipt stat failure")
            return result

        with (
            mock.patch.object(CLI_MODULE.os, "stat", new=replace_then_fail),
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(OSError, "injected receipt stat failure"):
                CLI_MODULE.atomic_create(destination, b"original content\n")

        self.assertTrue(replaced)
        self.assertEqual(destination.read_bytes(), b"replacement content\n")
        self.assertIn("preserved the final path without cleanup", warnings.getvalue())

    def test_atomic_create_preserves_modified_inode_after_postflight_failure(self) -> None:
        destination = self.target / "modified-before-receipt.txt"
        original_stat = CLI_MODULE.os.stat
        modified_inode: int | None = None
        warnings = io.StringIO()

        def modify_then_fail(path, *args, **kwargs):
            nonlocal modified_inode
            result = original_stat(path, *args, **kwargs)
            if (
                path == destination.name
                and kwargs.get("dir_fd") is not None
                and modified_inode is None
            ):
                modified_inode = result.st_ino
                destination.write_bytes(b"modified content\n")
                raise OSError("injected receipt stat failure")
            return result

        with (
            mock.patch.object(CLI_MODULE.os, "stat", new=modify_then_fail),
            redirect_stderr(warnings),
        ):
            with self.assertRaisesRegex(OSError, "injected receipt stat failure"):
                CLI_MODULE.atomic_create(destination, b"original content\n")

        self.assertIsNotNone(modified_inode)
        self.assertEqual(destination.stat().st_ino, modified_inode)
        self.assertEqual(destination.read_bytes(), b"modified content\n")
        self.assertIn("preserved the final path without cleanup", warnings.getvalue())

    def test_partial_final_file_is_preserved_without_delete_and_blocks_rerun(self) -> None:
        original_write = CLI_MODULE.os.write
        write_calls = 0
        warnings = io.StringIO()
        output = io.StringIO()

        def fail_after_partial_write(descriptor, data):
            nonlocal write_calls
            write_calls += 1
            if write_calls == 1:
                return original_write(descriptor, data[:1])
            raise OSError("injected write failure")

        with (
            mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit),
            mock.patch.object(CLI_MODULE.os, "write", side_effect=fail_after_partial_write),
            mock.patch.object(
                CLI_MODULE.os, "unlink", side_effect=AssertionError("unlink forbidden")
            ) as unlink,
            mock.patch.object(
                CLI_MODULE.os, "rmdir", side_effect=AssertionError("rmdir forbidden")
            ) as rmdir,
            redirect_stderr(warnings),
            redirect_stdout(output),
        ):
            with self.assertRaisesRegex(OSError, "injected write failure"):
                CLI_MODULE.init_command(str(self.target), apply=True)

        partial = self.target / ".agent-warmboot" / "core.md"
        self.assertEqual(partial.read_bytes(), b"#")
        self.assertTrue((self.target / ".agent-warmboot" / "routes").is_dir())
        self.assertIn(str(partial), warnings.getvalue())
        self.assertIn("preserved the final path without cleanup", warnings.getvalue())
        self.assertNotIn("APPLIED", output.getvalue())
        unlink.assert_not_called()
        rmdir.assert_not_called()

        with mock.patch.object(CLI_MODULE, "toolkit_root", return_value=self.toolkit):
            with self.assertRaisesRegex(
                CLI_MODULE.WarmbootError,
                r"\.agent-warmboot/core\.md differs from the managed content",
            ):
                CLI_MODULE.init_command(str(self.target), apply=True)
        self.assertEqual(partial.read_bytes(), b"#")
        self.assertFalse((self.target / "AGENTS.md").exists())

    def test_install_source_has_no_destructive_cleanup_path(self) -> None:
        source = SOURCE_SCRIPT.read_text(encoding="utf-8")

        self.assertNotIn("os.unlink(", source)
        self.assertNotIn("os.rmdir(", source)
        self.assertNotIn("def rollback_", source)
        self.assertNotIn(".tmp", source)

    def test_check_detects_tampering(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        (self.target / ".agent-warmboot" / "core.md").write_text("# Tampered\n", encoding="utf-8")
        result = self.run_cli("check", str(self.target))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("content/hash mismatch", result.stdout)

    def test_check_detects_missing_and_extra_managed_routes(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        routes = self.target / ".agent-warmboot" / "routes"
        (routes / "extra.md").write_text("# Extra\n", encoding="utf-8")
        (routes / "review.md").unlink()
        result = self.run_cli("check", str(self.target))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unexpected managed path(s): .agent-warmboot/routes/extra.md", result.stdout)
        self.assertIn("missing managed path(s): .agent-warmboot/routes/review.md", result.stdout)

    # Each pair is a raw name tail and the escaped form the output must show instead:
    # a newline that would start a forged line, and a carriage return plus a terminal
    # erase-line sequence that would visually overwrite the real line on a terminal.
    FORGED_TAILS = (
        ("\nPASS forged", "\\nPASS forged"),
        ("\r\x1b[2KPASS forged", "\\r\\x1b[2KPASS forged"),
    )

    def assert_output_lines_are_unforgeable(
        self, output: str, first_word: str, *escaped_lines: str
    ) -> None:
        """Every line stays printable, so no raw name can start or overwrite a line."""
        self.assertTrue(output.startswith(first_word), ascii(output))
        lines = output.split("\n")
        self.assertEqual(lines[-1], "", ascii(output))
        self.assertTrue(all(line.isprintable() for line in lines), ascii(output))
        self.assertFalse(
            [line for line in output.splitlines() if line.startswith(("PASS", "APPLIED"))],
            ascii(output),
        )
        for line in escaped_lines:
            self.assertIn(line, lines, ascii(output))

    def test_printable_path_escapes_only_what_could_forge_or_blur_a_line(self) -> None:
        cases = {
            ".agent-warmboot/routes/café.md": ".agent-warmboot/routes/café.md",
            "a\nb": "a\\nb",
            "a\rb": "a\\rb",
            "a\tb": "a\\tb",
            "a\x1b[2Kb": "a\\x1b[2Kb",
            "a\x85b": "a\\x85b",
            "a\u2028b": "a\\u2028b",
            "a" + os.fsdecode(b"\xff") + "b": "a\\udcffb",
            # A literal backslash is doubled, so it never reads like an escape.
            "a\\nb": "a\\\\nb",
        }
        for raw, shown in cases.items():
            with self.subTest(raw=ascii(raw)):
                self.assertEqual(CLI_MODULE.printable_path(raw), shown)
                self.assertTrue(CLI_MODULE.printable_path(raw).isprintable())
        self.assertEqual(CLI_MODULE.printable_path(Path("/tmp") / "x\ny"), "/tmp/x\\ny")

    def test_check_output_cannot_be_forged_by_a_newline_in_a_manifest_key(self) -> None:
        """A manifest key is printed escaped in every failure family that carries it."""
        self.assertEqual(self.apply().returncode, 0)
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        original = json.loads(manifest_path.read_text(encoding="utf-8"))
        tails = (
            (
                "\nPASS " + str(self.target) + ": forged",
                "\\nPASS " + str(self.target) + ": forged",
            ),
            *self.FORGED_TAILS,
        )
        for raw, escaped in tails:
            with self.subTest(tail=ascii(raw)):
                # The key's parent is not the routes directory, so it is both an
                # unexpected manifest entry and a missing managed path.
                manifest = dict(original, files=dict(original["files"]))
                manifest["files"][".agent-warmboot/routes/x.md" + raw] = "0" * 64
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

                result = self.run_cli("check", str(self.target))

                self.assertEqual(result.returncode, 1, ascii(result.stdout + result.stderr))
                shown = ".agent-warmboot/routes/x.md" + escaped
                self.assert_output_lines_are_unforgeable(
                    result.stdout,
                    "FAIL ",
                    f"- .agent-warmboot/manifest.json: unexpected entries: {shown}",
                    f"- missing managed path(s): {shown}",
                )

    def test_check_escapes_manifest_route_keys_in_missing_path_failures(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        manifest_path = self.target / ".agent-warmboot" / "manifest.json"
        original = json.loads(manifest_path.read_text(encoding="utf-8"))
        for raw, escaped in self.FORGED_TAILS:
            with self.subTest(tail=ascii(raw)):
                # A declared route that is absent reaches both the structure and the
                # per-file content failure.
                manifest = dict(original, files=dict(original["files"]))
                manifest["files"][f".agent-warmboot/routes/x{raw}.md"] = "0" * 64
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

                result = self.run_cli("check", str(self.target))

                self.assertEqual(result.returncode, 1, ascii(result.stdout + result.stderr))
                shown = f".agent-warmboot/routes/x{escaped}.md"
                self.assert_output_lines_are_unforgeable(
                    result.stdout,
                    "FAIL ",
                    f"- missing managed path(s): {shown}",
                    f"- {shown}: missing or not a regular file",
                )

    def test_check_escapes_filesystem_names_in_unexpected_managed_paths(self) -> None:
        self.assertEqual(self.apply().returncode, 0)
        managed = self.target / ".agent-warmboot"
        for raw, escaped in self.FORGED_TAILS:
            with self.subTest(tail=ascii(raw)):
                (managed / f"x{raw}").write_text("planted\n", encoding="utf-8")
                (managed / f"d{raw}").mkdir()
                try:
                    result = self.run_cli("check", str(self.target))
                finally:
                    (managed / f"x{raw}").unlink()
                    (managed / f"d{raw}").rmdir()

                self.assertEqual(result.returncode, 1, ascii(result.stdout + result.stderr))
                self.assert_output_lines_are_unforgeable(
                    result.stdout,
                    "FAIL ",
                    f"- unexpected managed path(s): .agent-warmboot/x{escaped}",
                    f"- unexpected managed directory(s): .agent-warmboot/d{escaped}",
                )

    def test_check_escapes_the_target_path_in_its_verdict_line(self) -> None:
        for index, (raw, escaped) in enumerate(self.FORGED_TAILS):
            with self.subTest(tail=ascii(raw)):
                target = Path(self.temporary.name) / f"t{index}{raw}"
                target.mkdir()
                applied = self.run_cli("init", str(target), "--apply")
                self.assertEqual(applied.returncode, 0, ascii(applied.stdout + applied.stderr))
                (target / ".agent-warmboot" / "routes" / "review.md").unlink()

                result = self.run_cli("check", str(target))

                self.assertEqual(result.returncode, 1, ascii(result.stdout + result.stderr))
                self.assert_output_lines_are_unforgeable(
                    result.stdout,
                    "FAIL ",
                    f"FAIL {target.parent.resolve()}/t{index}{escaped}",
                )

    def test_init_escapes_filesystem_and_route_names_in_output(self) -> None:
        for raw, escaped in self.FORGED_TAILS:
            with self.subTest(tail=ascii(raw), command="refused apply"):
                planted = self.target / ".agent-warmboot" / f"x{raw}"
                planted.parent.mkdir(exist_ok=True)
                planted.write_text("planted\n", encoding="utf-8")
                try:
                    result = self.apply()
                finally:
                    planted.unlink()

                self.assertEqual(result.returncode, 1, ascii(result.stdout + result.stderr))
                self.assertEqual(result.stdout, "")
                self.assertFalse((self.target / "AGENTS.md").exists())
                self.assert_output_lines_are_unforgeable(
                    result.stderr,
                    "FAIL: ",
                    f"FAIL: unexpected managed path(s): .agent-warmboot/x{escaped}",
                )
        (self.target / ".agent-warmboot").rmdir()

        for raw, escaped in self.FORGED_TAILS:
            with self.subTest(tail=ascii(raw), command="preview"):
                route = self.toolkit / "routes" / f"x{raw}.md"
                route.write_text("# Planted route\n", encoding="utf-8")
                try:
                    result = self.run_cli("init", str(self.target))
                finally:
                    route.unlink()

                self.assertEqual(result.returncode, 0, ascii(result.stdout + result.stderr))
                self.assertEqual(list(self.target.iterdir()), [])
                self.assert_output_lines_are_unforgeable(
                    result.stdout,
                    "PREVIEW ",
                    f"CREATE-FILE .agent-warmboot/routes/x{escaped}.md",
                )

    def test_core_and_rotation_route_carry_the_exact_review_authority_and_absence_rules(
        self,
    ) -> None:
        """Each sentence is pinned whole: dropping one qualifier must fail this test."""
        core = " ".join((ROOT / "WARMBOOT.md").read_text(encoding="utf-8").split())
        rotation = " ".join((ROOT / "routes/rotation.md").read_text(encoding="utf-8").split())
        for sentence in (
            "Every code change, however small, gets an independent non-author reviewer",
            "and an independent non-author reviewer repeats that reconciliation",
            (
                "Only an agent granted the work may append itself as coordinator when none is"
                " recorded or the coordinator is demonstrably absent, recording why; a delegated"
                " lane never does. Other holders change only by rotation"
            ),
            (
                "installing packages, and other external effects need separate explicit user"
                " authorization"
            ),
        ):
            with self.subTest(sentence=sentence[:40]):
                self.assertIn(sentence, core)
        self.assertEqual(core.count("independent non-author reviewer"), 2)
        self.assertIn(
            "When the outgoing holder is demonstrably absent and cannot freeze, the"
            " coordinator records the absence, the evidence for it, and the user's direction"
            " in place of this step; the replacement then continues from section 2, the"
            " independent replacement preflight. Nothing the absent holder left is discarded"
            " without inspection.",
            rotation,
        )

    def test_relative_target_is_refused(self) -> None:
        result = self.run_cli("init", "target", "--apply", cwd=Path(self.temporary.name))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be absolute", result.stderr)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_existing_task_file_is_preserved(self) -> None:
        task = self.target / "TASK.md"
        task.write_text("keep this task\n", encoding="utf-8")
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(task.read_text(encoding="utf-8"), "keep this task\n")
        self.assertFalse((self.target / "HANDOFF.md").exists())


class WarmbootQualityContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def headings(self, relative_path: str) -> set[str]:
        return {
            line.strip() for line in self.read(relative_path).splitlines() if line.startswith("##")
        }

    def consequential_fixture(self) -> tuple[str, str, str]:
        source = """/** Coordinates the durable retry budget; owns its deadline decision. */
final class RecoveryBudget {
    // Why: monotonic elapsed time avoids wall-clock jumps during recovery.
    // Invariant: a retry is allowed only before the one shared deadline.
    // Units: Duration values are converted to monotonic milliseconds.
    // Failure: an expired or unreadable deadline fails closed.
    // See: docs/adr/recovery.md#deadline-order
    boolean retry(Duration elapsed) { return compareAndSet(elapsed); }
}
"""
        adr = """# Recovery decision

## Deadline order

Use one monotonic deadline so every retry observes the same exhaustion boundary.
"""
        assessment = "RecoveryBudget.java: consequential: PASS\n"
        return source, adr, assessment

    def test_source_review_fixture_accepts_simple_native_orientation(self) -> None:
        source = "/** Identifies one immutable label. */\nrecord LabelId(String value) {}\n"

        self.assertEqual(review_java_fixture(source), [])

    def test_source_review_fixture_rejects_missing_orientation(self) -> None:
        source = "final class LabelId {}\n"

        self.assertIn("missing language-native type orientation", review_java_fixture(source))

    def test_source_review_fixture_rejects_tests_or_unlinked_adr_as_substitutes(self) -> None:
        source = """/** Coordinates retry decisions. Tests cover every branch. */
final class RecoveryBudget {
    boolean retry(Duration elapsed) { return compareAndSet(elapsed); }
}
"""

        findings = review_java_fixture(
            source,
            "# Recovery decision\n\n## Deadline order\n\nThe rationale exists elsewhere.\n",
            "RecoveryBudget.java: consequential: PASS\n",
        )

        self.assertIn("missing adjacent why rationale", findings)

    def test_source_review_fixture_accepts_local_contract_without_adr_link(self) -> None:
        source, _, assessment = self.consequential_fixture()
        source = source.replace("    // See: docs/adr/recovery.md#deadline-order\n", "")

        self.assertEqual(review_java_fixture(source, "", assessment), [])

    def test_source_review_fixture_accepts_local_contract_and_exact_adr_link(self) -> None:
        source, adr, assessment = self.consequential_fixture()

        self.assertEqual(review_java_fixture(source, adr, assessment), [])

    def test_source_review_fixture_mutations_are_rejected(self) -> None:
        source, adr, assessment = self.consequential_fixture()
        mutations = {
            "class contract": (source.split("\n", 1)[1], adr, assessment),
            "units": (
                source.replace(
                    "    // Units: Duration values are converted to monotonic milliseconds.\n", ""
                ),
                adr,
                assessment,
            ),
            "failure": (
                source.replace(
                    "    // Failure: an expired or unreadable deadline fails closed.\n", ""
                ),
                adr,
                assessment,
            ),
            "fragment": (
                source.replace("docs/adr/recovery.md#deadline-order", "docs/adr/recovery.md"),
                adr,
                assessment,
            ),
            "ADR heading": (
                source,
                adr.replace("## Deadline order", "## Retry ownership"),
                assessment,
            ),
            "assessment": (source, adr, ""),
        }

        for name, inputs in mutations.items():
            with self.subTest(name=name):
                self.assertTrue(review_java_fixture(*inputs))

    def test_guided_example_has_complete_oriented_python_source_set(self) -> None:
        paths = sorted(
            path
            for owner in (EXAMPLE_ROOT / "src", EXAMPLE_ROOT / "tests")
            for path in owner.rglob("*.py")
        )
        sources = {
            path.relative_to(EXAMPLE_ROOT).as_posix(): path.read_text(encoding="utf-8")
            for path in paths
        }
        expected = {
            "src/label_normalizer/__init__.py",
            "src/label_normalizer/__main__.py",
            "src/label_normalizer/core.py",
            "tests/__init__.py",
            "tests/test_cli.py",
            "tests/test_core.py",
        }

        self.assertEqual(set(sources), expected)
        self.assertEqual(example_python_orientation_findings(sources), [])

        mutated = dict(sources)
        mutated["tests/test_core.py"] = mutated["tests/test_core.py"].split("\n", 1)[1]
        self.assertEqual(
            example_python_orientation_findings(mutated),
            ["tests/test_core.py: missing module orientation"],
        )

    def test_writer_inventory_must_equal_frozen_candidate_source_set(self) -> None:
        candidate = {
            "examples/python-guided/src/label_normalizer/core.py",
            "examples/python-guided/tests/test_core.py",
            "tests/test_warmboot.py",
        }

        self.assertEqual(source_inventory_findings(candidate, set(candidate)), [])
        mutated = set(candidate)
        mutated.remove("examples/python-guided/tests/test_core.py")
        self.assertEqual(
            source_inventory_findings(candidate, mutated),
            ["omitted authored source: examples/python-guided/tests/test_core.py"],
        )

    def test_coded_project_floor_and_source_gate_have_living_owners(self) -> None:
        required_sections = {
            "BOOTSTRAP.md": {
                "### Adopt the coded-project floor",
                "### Prove changed-source comprehension",
            },
            "routes/review.md": {"## Source-comprehension release gate"},
            "routes/context.md": {"## Candidate source-set attestation"},
            "routes/handoff.md": {"## Durable comprehension route"},
            "templates/project-docs/engineering-standards.md": {
                "## Source-file comprehension contract"
            },
            "templates/TASK.md": {"## Changed-source comprehension"},
            "templates/HANDOFF.md": {"## Source routes"},
            "examples/python-guided/AGENTS.md": {"## Source comprehension"},
            "examples/python-guided/README.md": {"## Project map"},
            "BUGFIXES.md": {
                "## WB-001 — Plans and tests did not produce locally comprehensible source"
            },
            "CHANGELOG.md": {"## Unreleased"},
        }

        for relative_path, expected in required_sections.items():
            with self.subTest(relative_path=relative_path):
                self.assertTrue(expected.issubset(self.headings(relative_path)))

        bootstrap = self.read("BOOTSTRAP.md")
        for role in (
            "root README",
            "source/engineering rules",
            "changelog",
            "bug-fix record",
            "active task",
        ):
            with self.subTest(role=role):
                self.assertIn(role, bootstrap)
        architecture = self.read("docs/documentation-architecture.md")
        self.assertIn("project-docs/CHANGELOG.md", architecture)
        self.assertIn("project-docs/BUGFIXES.md", architecture)
        self.assertIn("neither can judge semantic adequacy or self-close acceptance", architecture)

    def test_plan_or_automation_cannot_self_close_source_comprehension(self) -> None:
        core = self.read("WARMBOOT.md")
        review = self.read("routes/review.md")
        evidence = self.read("routes/evidence.md")
        normalized_review = " ".join(review.split())

        self.assertIn(
            "Tests and distant plans do not replace this local contract",
            " ".join(core.split()),
        )
        self.assertIn("independent non-author reviewer", " ".join(core.lower().split()))
        self.assertIn("not only the task plan", normalized_review)
        self.assertIn("even if tests pass", normalized_review)
        self.assertIn("coordinator-attested frozen candidate source set", normalized_review)
        self.assertIn("An omitted authored code file is a `FINDING`", normalized_review)
        self.assertIn("cannot prove that a human can", evidence)
        self.assertIn("not a source linter", review_java_fixture.__doc__ or "")

    def test_example_consequential_source_has_local_rationale_and_exact_link(self) -> None:
        core = self.read("examples/python-guided/src/label_normalizer/core.py")

        self.assertIn("Why:", core)
        self.assertIn("Invariant:", core)
        self.assertIn("docs/adr/0001-python-standard-library-core.md#decision", core)
        self.assertIn("[`BUGFIXES.md`](BUGFIXES.md)", self.read("examples/python-guided/README.md"))

    def test_quality_responsibilities_have_stable_document_owners(self) -> None:
        required_sections = {
            "WARMBOOT.md": {"## Invariants", "## Finish"},
            "BOOTSTRAP.md": {"### Select target-owned quality practices", "## 6. Validate"},
            "routes/context.md": {"## Choose topology", "## Scope and lane continuity"},
            "routes/evidence.md": {"## Assertion and tier quality", "## Regression pins"},
            "routes/review.md": {
                "## Maintainability and test-quality lens",
                "## Fix and stop rule",
            },
            "templates/project-docs/engineering-standards.md": {
                "## Human inspectability",
                "## Boundaries",
            },
            "templates/project-docs/testing.md": {
                "## Assertion and fixture quality",
                "## Evidence tiers",
            },
            "templates/TASK.md": {"## Ownership", "## Context and hazards", "## Work and evidence"},
            "templates/HANDOFF.md": {"## State worth carrying", "## Evidence freshness"},
            "templates/capabilities/testing-feedback.md": {
                "## Adoption decision",
                "## Target record",
            },
        }

        for relative_path, expected in required_sections.items():
            with self.subTest(relative_path=relative_path):
                self.assertTrue(expected.issubset(self.headings(relative_path)))

    def test_current_core_and_routes_are_the_installed_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "target"
            target.mkdir()
            result = subprocess.run(
                [sys.executable, str(SOURCE_SCRIPT), "init", str(target), "--apply"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                (target / ".agent-warmboot" / "core.md").read_bytes(),
                (ROOT / "WARMBOOT.md").read_bytes(),
            )
            routes = sorted((ROOT / "routes").glob("*.md"))
            self.assertTrue(routes)
            for route in routes:
                with self.subTest(route=route.name):
                    self.assertEqual(
                        (target / ".agent-warmboot" / "routes" / route.name).read_bytes(),
                        route.read_bytes(),
                    )

    def test_installed_sources_are_self_contained_markdown(self) -> None:
        # Why: the core and routes are copied into targets without this checkout's
        # images or diagram helper, so a Mermaid fence, render wrapper or relative
        # image link there would arrive as a broken or unrendered reference.
        sources = [ROOT / "WARMBOOT.md", *sorted((ROOT / "routes").glob("*.md"))]
        for path in sources:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIsNone(
                    re.search(r"^ {0,3}(?:`{3,}|~{3,})\s*mermaid", text, re.MULTILINE)
                )
                self.assertNotIn("mermaid-render:", text)
                self.assertIsNone(
                    re.search(r"!\[[^\]\n]*\]\((?![A-Za-z][A-Za-z0-9+.-]*:)[^)\n]*\)", text)
                )

    def test_quality_contract_has_no_mechanical_count_mandates(self) -> None:
        contract_paths = (
            "WARMBOOT.md",
            "WHY.md",
            "BOOTSTRAP.md",
            "README.md",
            "routes/context.md",
            "routes/evidence.md",
            "routes/handoff.md",
            "routes/review.md",
            "docs/documentation-architecture.md",
            "templates/TASK.md",
            "templates/HANDOFF.md",
            "templates/project-docs/engineering-standards.md",
            "templates/project-docs/testing.md",
            "templates/capabilities/quality-evaluation.md",
            "templates/capabilities/testing-feedback.md",
        )
        prohibited = (
            r"(?:at least|minimum(?: of)?) \d+ (?:comments?|javadoc blocks?|tests?)",
            r"coverage (?:must|shall) (?:be|reach|exceed) \d+%",
            r"(?:files?|methods?|classes?) (?:must|shall) (?:be )?(?:under|below|no more than) \d+ (?:lines?|sloc)",
            r"(?:exactly|at least|minimum(?: of)?) \d+ (?:agents?|turns?|tokens?)",
        )

        for relative_path in contract_paths:
            normalized = " ".join(self.read(relative_path).lower().split())
            for pattern in prohibited:
                with self.subTest(relative_path=relative_path, pattern=pattern):
                    self.assertIsNone(re.search(pattern, normalized))

    def test_product_brand_is_distinct_from_installed_protocol_identity(self) -> None:
        self.assertTrue(CLI_MODULE.LOADER.startswith("# Warmboot Loader\n"))
        self.assertEqual(CLI_MODULE.TOOLKIT_NAME, "agent-warmboot")
        self.assertEqual(CLI_MODULE.MANAGED_DIR, ".agent-warmboot")
        self.assertEqual((ROOT / "SOURCE_REVISION").read_text().strip(), "warmboot-l0")

    def test_installed_loader_title_and_manifest_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "target"
            target.mkdir()

            applied = subprocess.run(
                [sys.executable, str(SOURCE_SCRIPT), "init", str(target), "--apply"],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertTrue(
                (target / "AGENTS.md").read_text(encoding="utf-8").startswith("# Warmboot Loader\n")
            )
            self.assertIn(
                "This loader is managed by agent-warmboot.",
                (target / "AGENTS.md").read_text(encoding="utf-8"),
            )
            manifest = json.loads(
                (target / ".agent-warmboot" / "manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["toolkit"], "agent-warmboot")
            self.assertEqual(manifest["source_revision"], "warmboot-l0")

            checked = subprocess.run(
                [sys.executable, str(SOURCE_SCRIPT), "check", str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_workflow_actions_are_pinned_and_checkout_keeps_no_credentials(self) -> None:
        """Every action is pinned to a full commit SHA; every checkout keeps no token."""
        workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
        self.assertTrue(workflows)
        for workflow in workflows:
            with self.subTest(workflow=workflow.name):
                text = workflow.read_text(encoding="utf-8")
                pinned = 0
                # Each list item starts a chunk, so a step's `with:` block stays in its chunk.
                for step in re.split(r"^\s*- ", text, flags=re.MULTILINE):
                    for action in re.findall(r"^\s*uses:\s*(\S+)", step, re.MULTILINE):
                        pinned += 1
                        self.assertRegex(action, r"^[\w.-]+/[\w./-]+@[0-9a-f]{40}$")
                        if action.startswith("actions/checkout@"):
                            self.assertRegex(step, r"(?m)^\s*persist-credentials: false$")
                self.assertGreater(pinned, 0)


if __name__ == "__main__":
    unittest.main()
