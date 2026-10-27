# Bug fixes

This ledger records observed Warmboot operating defects, why prior evidence missed them,
and the smallest retained recurrence check. Dated runs below are historical evidence,
not executions of the current checkout. Later corrections supersede obsolete policy
descriptions. IDs are per edition; the sibling edition's ledger numbers its own defects.
Defects in the shared installer are recorded in both ledgers, each under its own ID.

## WB-001 — Plans and tests did not produce locally comprehensible source

- Status and owner: corrected in Warmboot; toolkit maintainer owns the rule and
  regression fixture.
- Observed failure: earlier versions of the protocol let plans, tests, ADRs and review
  machinery pass while changed source files still lacked immediate purpose, operative
  rationale and invariants.
- Root cause: source comprehension was an aspiration but neither writer handoff nor
  independent review had to inspect and account for every changed authored source file;
  a writer-declared inventory also had no independent completeness source.
- RED evidence: the focused `WarmbootQualityContractTests` run on 2026-08-14 reported
  nine failures and three missing-file errors before the doctrine and living owners
  were added; synthetic missing-orientation and mutation cases establish the intended
  reviewer decisions.
- Fix: bootstrap adopts the target-native rule and coded-project floor; the coordinator
  attests a frozen candidate set, writers reconcile the full set, and non-author
  reviewers independently reconcile and block omissions or missing, stale or
  decorative explanation even when tests pass; existing debt is risk-inventoried.
- Remaining limit: the fixture proves only its bounded examples. Semantic adequacy in
  real code remains language-aware human review, and existing installations require a
  reviewed reconciliation because the helper is create-only.

## WB-002 — Small-work review decision contradicted the completion gate

- Status/owner: corrected; toolkit maintainer owns policy reconciliation.
- Observed defect: core Finish and bootstrap required a fresh reviewer for every
  changed source path while the core/context selected single-agent work below material
  risk. A small reversible source change had incompatible completion instructions.
- Rule: every code change gets independent review. `NOT REQUIRED` applies only to
  small reversible work that changes no code, with a scope/risk reason and subject to
  stricter target/user rules; it is a task state, never a reviewer verdict. Complete
  candidate inventory and writer assessment apply to every change.
- Evidence/reach: the 2026-09-05 assessment confirmed the conflicting complete semantic
  units by inspection. Acceptance walks both small and material changes through core,
  routes, bootstrap and seeds; this does not prove real agent adherence. No prose pin
  or recurring benchmark was added.

## WB-003 — Recovery comparison excluded the live receipt

- Status/owner: protocol corrected; toolkit maintainer owns comparison design;
  historical correction assessed on 2026-09-05; no consumer trial claimed.
- Observed defect: the comparison protocol allowed only three product paths, disabling
  the task-state update that Warmboot normally uses across interruption. This changed
  the treatment being measured; no result from this protocol is published.
- Correction: both conditions permit mutable `TASK.md` and optional `HANDOFF.md`, with
  immutable input separately named `BRIEF.md`. Product review excludes the receipts,
  scans their names for leakage and reports receipt use as process evidence.
- Evidence/reach: confirmed by comparing the frozen write boundary with the handoff
  route. Inspect both conditions and product-bundle boundaries before any run; change
  no controls mid-run. Outcome benefit remains unproved; no permanent pin.

## WB-004 — Parent relocation exceeded the stated containment guarantee

- Status/owner: guarantee and warning corrected; toolkit maintainer owns the helper
  and late-window regression; historical native GREEN verified on 2026-09-05.
- Observed defect: a rename after parent validation but before descriptor-relative
  creation wrote the core to the moved original directory outside the target. The
  helper already refused `APPLIED` and preserved the replacement, but the warning
  omitted that recorded paths could have moved.
- RED: coordinator replay on the baseline reached real `os.open(O_CREAT)`, observed
  outside core bytes, exit 1, no `APPLIED`, untouched replacement and absent moved-path
  warning. RED belongs to that warning/guarantee gap, not existing refusal behavior.
- Correction/pin: `test_late_parent_rename_preserves_inode_and_warns_paths_may_have_moved`
  retains the real late-boundary write and checks the accurate warning and preservation.
  Earlier parent-swap coverage detects changes before this last create window.
- GREEN: the coordinator ran the new native late-window case on the corrected
  candidate: preservation and refusal still hold, with the moved-path warning now
  present. Continuous containment is neither asserted nor proved.
- Reach/cost/deletion: one deterministic local filesystem interleaving in the native
  suite; it cannot prove continuous pathname containment, arbitrary scheduling or
  power-loss durability. No added dependency/service. Fold it into ordinary creation
  coverage when that coverage reaches the same late window and warning; remove it if
  the descriptor-relative creation boundary is replaced and no longer applies.
- Note: the sibling edition records this defect as WB-055.

## WB-005 — Manifest validation inspected invalid and unmanaged paths

- Status/owner: validation/read boundary corrected; toolkit maintainer owns helper
  and focused cases; historical native GREEN verified on 2026-09-05.
- Observed defect: JSON keys with embedded NUL or a host-unencodable surrogate reached
  OS inspection and escaped as tracebacks. An unexpected regular-file entry was also
  opened before its normal rejection. No false `PASS` or mutation was observed.
- RED: coordinator baseline replay failed the NUL, host-proven U+D800 and unmanaged-read
  expectations. A variable Unicode route case already passed and remains compatibility
  evidence, not an invented failing-before case.
- Correction/cases: `test_check_rejects_invalid_os_paths_without_traceback` checks normal
  refusal; `test_check_reports_unexpected_manifest_entry_without_opening_it` uses a
  real harmless file, correct digest and an open-boundary spy;
  `test_check_preserves_variable_unicode_route_sets` retains compatible route sets.
- GREEN: coordinator native runs passed invalid-path refusal without traceback,
  no unmanaged content open, and variable Unicode-route compatibility. The latter
  also passed against baseline; it is not a newly repaired failure.
- Related diagnostic defect: valid surrogateescape names are OS-encodable, but raw failure
  diagnostics raised `UnicodeEncodeError` under strict UTF-8 stdout. The coordinator
  reproduced the root manifest key `x\udc80name` before the diagnostic correction with
  `PYTHONIOENCODING=utf-8:strict`; the target was unchanged. This was inherited
  diagnostic debt, not a regression introduced by input validation.
- Narrow correction: escape surrogate display in accumulated `check` failure lines,
  retaining original lookup names, ordinary Unicode and caller-owned streams.
  `test_check_displays_surrogateescape_manifest_key_with_strict_stdout` exercises
  an unexpected root key and a missing declared route under strict UTF-8, with a
  literal `café` control, normal refusal and unchanged-byte assertions. This adds one
  standard-library subprocess test method. Historical native replay on 2026-09-05
  failed both subtests before the diagnostic correction and passed the corrected
  method. Fold it into ordinary diagnostic coverage when that coverage reaches these
  same strict-output cases.
- Remaining display debt, owner toolkit maintainer: physical undecodable-byte names
  were not created on this macOS filesystem (errno 92), so their diagnostic behavior
  remains unproved. Raw target-path headers, other CLI output and non-UTF-8 stream
  behavior are outside this narrow fix. Revisit when a consumer requires those paths
  or encodings; no all-CLI encoding guarantee is made.
- Reach/cost/deletion: local path encoding and managed-read boundaries only, not all
  operating systems or manifest provenance; small native-suite cases with no added
  dependency. These ordinary behavior tests own the recurrence; no duplicate phrase
  pin. Retire or replace them if the manifest/read boundary they exercise is removed.
- Note: the sibling edition records this defect as WB-049.

## WB-006 — Manifest check accepted duplicate JSON keys last-value-wins

- Status/owner: corrected; toolkit maintainer owns the helper's manifest parse and
  its regression case.
- Observed defect: `check` decoded `manifest.json` with the standard `json.loads`,
  which keeps only the last of repeated object keys. A manifest whose first
  `.agent-warmboot/core.md` entry carried an all-zero digest, shadowed by the real
  entry, passed `check` with exit 0, as did a repeated top-level `files` block. No
  installed file was changed; the gap was in what the manifest could hide.
- RED: on 2026-10-24 the new `test_check_rejects_duplicate_key_manifest` failed both
  subtests (nested managed-file key and top-level `files` key) against the unfixed
  helper: `check` printed `PASS` and exited 0.
- Correction/pin: `loads_rejecting_duplicate_keys` decodes the manifest with an
  `object_pairs_hook` that raises on any repeated key at any depth, before schema or
  digest checks; the failure reports `manifest.json: invalid JSON`. The same test
  owns the recurrence.
- GREEN: the corrected helper rejects both manifests with a non-zero exit; the full
  native suite passed on macOS with Python 3.14.7, 3.13.15 and 3.10.21.
- Reach/cost/deletion: the installed-manifest parse only; it does not authenticate
  the manifest, which remains a consistency check. One native test method, no added
  dependency. Retire it if the manifest moves to a parser that cannot represent
  duplicate keys.
- Note: the sibling edition records this defect as WB-046 and corrected it earlier; the
  dates here are when Light's copy was found and fixed.

## WB-007 — Manifest parse escaped as a traceback or accepted non-JSON constants

- Status/owner: corrected; toolkit maintainer owns the helper's manifest parse and its
  regression cases.
- Observed defect: a manifest nested deep enough to exhaust the decoder raised
  `RecursionError`, which is not a `ValueError`, so `check` stopped with a traceback
  instead of a `FAIL` line. The standard decoder also accepted `NaN`, `Infinity` and
  `-Infinity`, which are not JSON, so such a manifest reached the field checks and
  failed only as an unsupported schema.
- RED: on 2026-10-24 `test_check_rejects_deeply_nested_manifest_as_invalid_json` failed
  (no `manifest.json: invalid JSON` line) and `test_check_rejects_non_json_numeric_constants`
  failed all three subtests (reported `unsupported schema`) against the unfixed helper.
- Correction/pin: the manifest parse rejects the three constants through
  `parse_constant` and catches `RecursionError` with `ValueError`, so both cases report
  `manifest.json: invalid JSON` and exit 1. The two tests own the recurrence.
- GREEN: both tests and the full native suite passed on macOS with Python 3.14.7,
  3.13.15 and 3.10.21.
- Reach/cost/deletion: the installed-manifest parse only. Two native test methods, no
  added dependency. Retire them if the manifest moves to a parser that cannot
  represent these inputs.
- Note: the sibling edition records these defects as WB-052 and WB-053.

## WB-008 — A newline in a manifest key could forge a `PASS` line

- Status/owner: corrected; toolkit maintainer owns the helper's output rendering and
  its regression cases.
- Observed defect: `check` printed manifest-derived paths raw. A manifest key holding a
  newline followed by `PASS <target>: forged` produced two lines starting with `PASS`
  inside a failing report, one after the unexpected-entries line and one after the
  missing-paths line. The exit code stayed 1; the risk was a misleading report.
- RED: on 2026-10-24 `test_check_output_cannot_be_forged_by_a_newline_in_a_manifest_key`
  failed against the unfixed helper with both forged lines in its output.
- Correction/pin: `printable_path` renders every manifest-, filesystem-, route- and
  target-derived path with non-printable characters and the backslash escaped as
  `repr` writes them, so each message stays on one line. It generalizes the narrower
  surrogate escaping from WB-005, whose test still passes. The recurrence is owned by
  `test_printable_path_escapes_only_what_could_forge_or_blur_a_line` and the CLI cases
  `test_check_output_cannot_be_forged_by_a_newline_in_a_manifest_key`,
  `test_check_escapes_manifest_route_keys_in_missing_path_failures`,
  `test_check_escapes_filesystem_names_in_unexpected_managed_paths`,
  `test_check_escapes_the_target_path_in_its_verdict_line` and
  `test_init_escapes_filesystem_and_route_names_in_output`, each run with a newline
  tail and a carriage-return plus terminal-erase tail. A mutation that lets the
  carriage return and escape character through fails eight of these cases.
- GREEN: the test, the WB-005 strict-stdout test and the full native suite passed on
  macOS with Python 3.14.7, 3.13.15 and 3.10.21.
- Reach/cost/deletion: helper output only; lookups use the original names. A literal
  backslash in a name now prints doubled. Six native test methods, no added dependency.
  Retire it if the helper stops printing manifest-derived names.
- Note: the sibling edition records this defect as WB-054.

Current executions and review verdicts belong to [TASK.md](TASK.md); Linux execution
is covered by the CI workflow. Editor opening and autonomous resume remain unproved. Passing checks do not
substitute for an independent verdict, upgrade existing installations or establish
workflow superiority.
