# Current task

This synthetic teaching snapshot is not a live assignment and grants no authority.

- Status: `REVIEW`
- Objective: deliver a deterministic label comparison-key package and CLI while
  keeping the original display value outside the normalizer.
- Coordinator and sole Git/remote holder: `example-coordinator`
- Exact implementation scope: `src/label_normalizer/**`, `tests/**`, package
  metadata, workspace task, and the linked example documentation.
- Runtime: Python standard library only; no network, service, database, or
  mutable global state.
- Git, installation, publication, and hosted release: `NOT AUTHORIZED`.

## Acceptance

- `normalize_label("  Warm   BOOT  ") == "warm boot"`.
- Unicode compatibility forms and case folding are covered by tests.
- Non-string input raises `TypeError` at the public boundary.
- The CLI prints one comparison key per input and writes no extra output.
- The cold and guided core functions have the same tested semantics.
- All local Markdown links resolve and the workspace JSON parses.
- Every human-authored code file follows the Python docstring rule; consequential logic
  carries adjacent rationale and an exact ADR-section link.
- An independent reviewer returns `CLEAN`, `FINDING`, or `BLOCKED`.

## Evidence

| Check | State | Result |
|---|---|---|
| cold native unit suite | `PROVED` | 4 tests passed with bytecode writes disabled |
| guided native unit suite | `PROVED` | 5 tests passed with bytecode writes disabled |
| core semantic equivalence | `PROVED` | 5 representative strings and the type-error boundary matched |
| CLI smoke | `PROVED` | printed `warm boot` and `strasse`, with no extra output |
| local links and metadata | `PROVED` | 6 local Markdown links resolved; workspace JSON and project TOML parsed |
| human-authored code orientation | `PROVED` | exact six-file source/test set parsed and each file has a module docstring; presence/syntax only |
| package installation | `UNPROVED` | not required for acceptance; installation is not authorized |

Changed paths: this synthetic example only.

Changed-source comprehension: Python docstrings are owned by this task and `AGENTS.md`.
The complete human-authored code set is `src/label_normalizer/__init__.py`,
`src/label_normalizer/__main__.py`, `src/label_normalizer/core.py`,
`tests/__init__.py`, `tests/test_cli.py`, and `tests/test_core.py`. The package/API,
CLI, test-package and test-module files are simple and oriented; `core.py` is
consequential and carries the local normalization invariant plus an exact link to
`docs/adr/0001-python-standard-library-core.md#decision`. There are no generated,
vendored or pure re-export exceptions and no known pre-existing source debt. The
bounded toolkit check proves Python syntax and module-docstring presence only, not
semantic adequacy.

Review: `NOT STARTED`. Results become stale if code, tests, interpreter, settings,
or task inputs change. On interruption, retain the filesystem, reread this record,
and rerun stale checks. Next authorized action: obtain independent review.
