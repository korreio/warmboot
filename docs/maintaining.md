# Maintaining Warmboot Light

This guide governs maintaining this toolkit checkout; it is not installed into target
projects.

Adopt guidance on this repository's own hazards. Record any compression of shared
text and preserve its meaning and evidence boundary. State rule duties by role.
Before calling a rule change done, re-read the complete changed semantic unit from
the perspective of a coordinating platform other than the writer's, give the reviewer
the same instruction, and check intentionally shared text as a whole
whitespace-normalized unit, never a prefix.

The parts shared with Warmboot Full are the same bytes in both editions: `bin/warmboot`
(including the installed loader text), the five routes under `routes/`, the text of
`WARMBOOT.md` outside its marked edition block, `LICENSE`, `templates/TASK.md` and
`templates/HANDOFF.md`, the three shared README pictures (session loop, stale evidence,
edition), the "Which edition?" text, the shared part of BOOTSTRAP's "Existing agent
instructions", the README section headings, `tools/render_mermaid_docs.py` with
`tests/test_render_mermaid_docs.py`, `.ruff.toml`, `.editorconfig`, `.gitattributes`,
and `.github/SECURITY.md`, `.github/CONTRIBUTING.md` and `.github/ISSUE_TEMPLATE/`.
They are aligned by hand and compared byte for byte: the core after removing its edition
block, the rendered PNGs by hash after a clean render. The remaining differences are each
core's edition block, Full's extra tooling and documents, and each edition's own
BOOTSTRAP sections, tests, ledgers and changelogs.

## Evidence ladder for this checkout

A row is required when the change touches what it names; the evidence route still
decides any hazard no row reaches. The coordinator records each result in
[`TASK.md`](../TASK.md) with its command, host and `PROVED`, `UNPROVED` or `BLOCKED`.
Every required tier that an available host can run is run before the local checkpoint.

| Tier | Command or observation | Required when the change touches | What a pass proves |
|---|---|---|---|
| 1. Native suite | The README's [validate command](../README.md#validate-this-checkout): `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`. | Anything in this checkout. | The helper behavior its assertions name (create-only preview, apply and check, refusals, residue preserved under injected faults), the diagram helper's ownership and batch-safety cases, on the host and Python that ran it, and the pinned headings, phrases and installed projection of the living documents. Not agent behavior, guidance quality or workspace usability. |
| 2. Install exercise | The [disposable install/resume example](../BOOTSTRAP.md#disposable-install-and-resume-example). | `bin/warmboot`, `WARMBOOT.md`, a route, the loader text or that example. | The real helper installs and checks this checkout's actual payload in a new target. |
| 3. Source reading | The coordinator freezes and attests the candidate source set; the writer reconciles its assessment against it; an independent non-author reviewer repeats the reconciliation and reads every resulting path ([context route](../routes/context.md#candidate-source-set-attestation)). An omitted file is a `FINDING`. | `bin/warmboot`, `tools/`, `tests/` or example source. | A reader can recover purpose and consequential intent from the file itself. No test pass replaces it. |
| 4. Second platform | Tiers 1 and 2 on a Linux host. | The helper's filesystem, descriptor or encoding behavior. | The same assertions on that host. |
| 5. Diagrams | `python3 -B tools/render_mermaid_docs.py --root . --check`; regenerate without `--check` when a fence changes. | A Mermaid fence, its wrapper or a diagram image. | Each wrapper matches its source digest and render policy and its image exists. It does not render or inspect pixels; look at a regenerated image before accepting it. |

The hosted CI workflow pins every action to a full 40-character commit SHA and checks
out with `persist-credentials: false`; the native suite fails on an action referenced
by tag or branch, or on a checkout that keeps credentials.

When no Linux host is available, tier 4 stays `UNPROVED`: the macOS result is recorded
as macOS-only and is never relabelled. A review round is recorded in the same task, one
line per round: reviewers by role and model family, claims raised, confirmed, downgraded
and refuted, minutes, unproved tiers and the terminal verdict. The line reads:

```text
review <package> r<N> <YYYY-MM-DD>: reviewers=<role@family, …> raised=<n> confirmed=<n> downgraded=<n> refuted=<n> minutes=<n> unproved=<tier or none> result=<CLEAN|FINDING|BLOCKED>
```

When the next task starts, it replaces `TASK.md`; version control keeps the previous
record.
