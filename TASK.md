# Toolkit validation status

Status: IDLE — no active task. The next task replaces this record.

## Acceptance

The toolkit checkout is accepted when the native suite and both example suites pass, the
guided CLI prints its documented output, BOOTSTRAP's disposable install/resume exercise
installs and checks nine files and reruns on changed input, the installed core is
byte-identical to `WARMBOOT.md` and its full MIT notice, every diagram wrapper passes
its check, local Markdown links resolve, and changed human-authored code receives
independent review (per [docs/maintaining.md](docs/maintaining.md)).

## Validation

Commands run from the toolkit or respective example directory:

- Toolkit: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`.
- Diagrams: `python3 -B tools/render_mermaid_docs.py --root . --check`.
- Each example: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`.
- Guided CLI: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m label_normalizer "  Warm   BOOT  " "Straße"`.
- The three shell blocks in BOOTSTRAP's disposable install/resume example, checking
  preview non-mutation, nine installed files, `PASS` and input freshness.
- Installed-core identity with `WARMBOOT.md`, including its MIT notice, is asserted by
  `test_current_core_and_routes_are_the_installed_projection` in the toolkit suite.

2026-10-24, macOS: PROVED — on Python 3.14.7, 3.13.15 and 3.10.21, 90 toolkit tests (75
installer and document, 15 diagram helper) and 4 cold-example tests passed and the
diagram check confirmed 8 wrappers; on 3.14.7 and 3.13.15, 5 guided-example tests passed
and the guided CLI printed its documented output (the guided example requires Python
3.11+). BOOTSTRAP's three blocks, extracted as the CI workflow extracts them, left the
preview target empty, applied nine files, passed `check` and reran on changed input. All
83 local Markdown links and anchors and all 8 diagram images resolved. Linux evidence
comes from the CI workflow's run records.

2026-10-25, CI (Ubuntu and macOS, Python 3.10 and 3.13): PROVED — on all four jobs 90
toolkit tests (75 installer and document, 15 diagram helper) and 4 cold-example tests
passed, the diagram check confirmed 8 wrappers and BOOTSTRAP's three blocks passed; on
3.13 the 5 guided-example tests and the guided CLI passed (the guided example requires
Python 3.11+). No test was skipped.

2026-10-25, macOS with Python 3.14.7 and 3.13.15, for the `routes/` layout beside
`WARMBOOT.md`: PROVED with the commands above — the toolkit suite ran 90 tests and the
examples 4 and 5; a fresh `init --apply` into an empty directory created the nine files
and `check` passed; an installation created before this layout also passed `check`; all
7 relative links in the installed core and routes resolved from their own files, and all
91 local Markdown links and anchors in the checkout resolved; the diagram check
confirmed 8 wrappers and BOOTSTRAP's three blocks passed. CI on Ubuntu and macOS with
Python 3.10 and 3.13 passed all four jobs for this layout.

2026-10-26, CI: PROVED — the workflow runs five jobs, the four test jobs above and a
style job on Ubuntu with Python 3.13 that runs ruff 0.17.1 `check` and `format --check`
with `--no-cache`. All five passed; the test jobs ran the same 90 toolkit, 4 cold-example
and 5 guided-example tests (the last on 3.13 only) and confirmed 8 diagram wrappers.

2026-10-26, macOS with Python 3.11.17, 3.13.15, 3.14.7 and 3.15.0, for the Python 3.11
minimum: PROVED — each version ran the CI test job's steps: 90 toolkit tests, 4
cold-example and 5 guided-example tests passed with none skipped, the guided CLI printed
its documented output, the diagram check confirmed 8 wrappers and BOOTSTRAP's three
blocks passed. Ruff 0.17.1 with target `py311` reported nothing.

2026-10-26, CI (Ubuntu and macOS, Python 3.11 and 3.15): PROVED — all five jobs passed;
each test job ran 90 toolkit, 4 cold-example and 5 guided-example tests, the guided CLI
printed its documented output, the diagram check confirmed 8 wrappers and BOOTSTRAP's
three blocks passed; the style job ran on Python 3.15.

2026-10-27, macOS with Python 3.11.17, 3.13.15, 3.14.7 and 3.15.0: PROVED — each version
ran the CI test job's steps: 94 toolkit tests (76 installer and document, 18 diagram
helper), 4 cold-example and 5 guided-example tests passed, the guided CLI printed its
documented output, the diagram check confirmed 8 wrappers and BOOTSTRAP's three blocks
passed. Ruff 0.17.1 reported nothing; all 99 local Markdown links and anchors resolved
and all 8 diagram images are referenced.

## Review

Rows r1 to r15 record reviewer roles; the model family of each reviewer and the minutes
per round, which the format in [docs/maintaining.md](docs/maintaining.md) asks for, were
not recorded for them. Later rows show the family where known and mark unknown minutes.

```text
review documentation-diagrams-ci r1 2026-10-24: reviewers=reviewer-deep,reviewer-wide,other-family-reviewer,verifier raised=14 confirmed=13 downgraded=1 refuted=0 unproved=linux-ci result=FINDING
review documentation-diagrams-ci r2 2026-10-24: reviewers=reviewer-deep,other-family-reviewer raised=2 confirmed=2 downgraded=0 refuted=0 unproved=linux-ci result=FINDING
review documentation-diagrams-ci r3 2026-10-24: reviewers=cold-readers(same-family+other-family),verifier raised=22 confirmed=16 downgraded=6 refuted=0 unproved=linux-ci result=FINDING
review documentation-diagrams-ci r4 2026-10-24: reviewers=cold-readers(same-family+other-family),reviewer-wide raised=8 confirmed=8 downgraded=0 refuted=0 unproved=linux-ci result=FINDING
review documentation-diagrams-ci r5 2026-10-24: reviewers=reviewer-wide,other-family-reviewer raised=3 confirmed=2 downgraded=1 refuted=0 unproved=linux-ci result=FINDING
review documentation-diagrams-ci r6 2026-10-24: reviewers=independent-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 unproved=linux-ci result=CLEAN
review documentation-diagrams-ci r7 2026-10-24: reviewers=cold-readers(same-family+other-family),reviewer-deep raised=3 confirmed=3 downgraded=0 refuted=0 unproved=linux-ci result=FINDING
review documentation-diagrams-ci r8 2026-10-24: reviewers=independent-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 unproved=linux-ci result=CLEAN
review documentation-diagrams-ci r9 2026-10-24: reviewers=cold-readers(same-family+other-family) raised=4 confirmed=4 downgraded=0 refuted=0 unproved=none result=FINDING
review documentation-diagrams-ci r10 2026-10-24: reviewers=reviewer-deep,other-family-reviewer raised=4 confirmed=4 downgraded=0 refuted=0 unproved=none result=FINDING
review documentation-diagrams-ci r11 2026-10-24: reviewers=reviewer-deep,reviewer-wide,other-family-reviewer,verifier raised=6 confirmed=6 downgraded=0 refuted=0 unproved=none result=FINDING
review documentation-diagrams-ci r12 2026-10-24: reviewers=reviewer-deep,other-family-reviewer raised=4 confirmed=4 downgraded=0 refuted=0 unproved=none result=FINDING
review documentation-diagrams-ci r13 2026-10-25: reviewers=independent-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 unproved=none result=CLEAN
review documentation-diagrams-ci r14 2026-10-25: reviewers=cold-readers(same-family) raised=4 confirmed=4 downgraded=0 refuted=0 unproved=none result=FINDING
review documentation-diagrams-ci r15 2026-10-25: reviewers=independent-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 unproved=none result=CLEAN
review documentation-diagrams-ci r16 2026-10-25: reviewers=reviewer-wide(same-family),verifier(same-family) raised=3 confirmed=0 downgraded=1 refuted=2 minutes=unknown unproved=none result=FINDING
review documentation-diagrams-ci r17 2026-10-25: reviewers=independent-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review documentation-diagrams-ci r18 2026-10-25: reviewers=other-family-reviewer raised=1 confirmed=1 downgraded=0 refuted=0 minutes=unknown unproved=none result=FINDING
review route-links r1 2026-10-25: reviewers=reviewer-wide(same-family),other-family-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=linux-ci result=CLEAN
review documentation-closeout r1 2026-10-26: reviewers=reviewer-wide(same-family),other-family-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review community-files r1 2026-10-26: reviewers=reviewer-wide(same-family),other-family-reviewer raised=5 confirmed=3 downgraded=1 refuted=1 minutes=unknown unproved=none result=FINDING
review community-files r2 2026-10-26: reviewers=other-family-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review code-style r1 2026-10-26: reviewers=reviewer-wide(same-family),other-family-reviewer raised=2 confirmed=1 downgraded=0 refuted=1 minutes=unknown unproved=none result=FINDING
review code-style r2 2026-10-26: reviewers=other-family-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review code-style r3 2026-10-26: reviewers=reviewer-wide(same-family),other-family-reviewer raised=1 confirmed=0 downgraded=1 refuted=0 minutes=unknown unproved=windows-checkout result=CLEAN
review code-style r4 2026-10-26: reviewers=reviewer-wide(same-family),other-family-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review payload-docstring r1 2026-10-26: reviewers=reviewer-wide(same-family) raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review status-wording r1 2026-10-26: reviewers=reviewer-wide(same-family) raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review backlog-batch r1 2026-10-26: reviewers=reviewer-wide(same-family) raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review python-311 r1 2026-10-26: reviewers=reviewer-wide(same-family),other-family-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=python-3.10-run result=CLEAN
review rotation-wording r1 2026-10-26: reviewers=reviewer-wide(same-family) raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review ci-pins r1 2026-10-26: reviewers=reviewer-wide(same-family) raised=1 confirmed=1 downgraded=0 refuted=0 minutes=unknown unproved=none result=FINDING
review ci-pins r2 2026-10-26: reviewers=reviewer-wide(same-family) raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review render-walk r1 2026-10-27: reviewers=reviewer-wide(same-family) raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review render-nodes r1 2026-10-27: reviewers=reviewer-wide(same-family) raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
review final-sweep r1 2026-10-27: reviewers=4×reviewer-wide(same-family) raised=26 confirmed=18 downgraded=8 refuted=0 minutes=unknown unproved=none result=FINDING
review final-sweep r2 2026-10-27: reviewers=reviewer-wide(same-family),other-family-reviewer raised=0 confirmed=0 downgraded=0 refuted=0 minutes=unknown unproved=none result=CLEAN
```

## Limits

Checks prove their assertions on the host that runs them; Linux evidence lives in the
CI workflow's run records. Hosted rendering, real editor/workspace use, live-agent
adherence, cross-provider behavior, production use and general productivity, cost or
defect-rate improvements remain unproved. Manifest consistency does not authenticate
provenance; no release is claimed.
