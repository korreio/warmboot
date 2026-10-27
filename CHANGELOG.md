# Changelog

This file records Warmboot guidance and compatibility changes. A committed entry does
not claim publication, release, deployment or an installed-target upgrade.

## Unreleased

### 2026-10-26 — Python 3.11

- Minimum Python 3.11. CI tests Python 3.11 and 3.15 on Ubuntu and macOS.

### 2026-10-25 — route links

- The five routes live in `routes/` beside `WARMBOOT.md`, and the core links each one
  relatively, so the same links resolve in this checkout and under `.agent-warmboot/`
  in an installed target. The installed layout is the same nine files; existing
  installations keep passing `check` and are not upgraded.

### 2026-10-24 — licensing, rendered diagrams and CI

- MIT licence for code, documentation, templates and synthetic examples; the installed
  core carries the full notice within the nine-file payload.
- Rendered Mermaid diagrams with collapsed source, regenerated and checked by
  `tools/render_mermaid_docs.py` (`--check` verifies each wrapper's source digest,
  image and laptop readability).
- `check` rejects a manifest with a repeated JSON key, a non-JSON constant (`NaN`,
  `Infinity`) or nesting deep enough to exhaust the decoder as invalid JSON
  ([BUGFIXES.md](BUGFIXES.md) WB-006, WB-007).
- `check` and `init` print paths from the manifest, filesystem and command line with
  non-printable characters escaped, so a crafted name cannot start a new output line
  ([BUGFIXES.md](BUGFIXES.md) WB-008).
- CI on Ubuntu and macOS with Python 3.10 and 3.13.
- Maintainer guide in [docs/maintaining.md](docs/maintaining.md).

### 2026-10-18 — interrupted lanes and complete fix scope

- The [context route](routes/context.md) requires bounded lanes to report
  proved and unfinished work before their limit; unreported work counts only after
  recovery proves it. The [review route](routes/review.md) requires full-class
  repair within scope and records other owners. These installed-guidance changes do
  not upgrade existing installations; consumer outcomes remain unproved.

### 2026-10-11 — every code change is reviewed; fix rule; maintainer evidence ladder

- Every code change requires at least one independent non-author review. `NOT REQUIRED`
  remains only for small reversible no-code work. Core, routes, toolkit docs, seeds and
  the example reflect this; existing installations are not upgraded.
- The [review route](routes/review.md) retains stricter task-declared sizing
  and, for substantial code, one already-required round from another model family
  where reachable. Behavior claims name reachable triggers; unreachable claims are
  `REFUTED`, and the coordinator verifies claims before fixes.
- Fixes remove causes at their owner; symptom guards are not fixes. A second failed
  fix for the same component and defect kind restarts from the state before those
  fixes with a different writer and direction.
  The task seed records one review line per round.
- Declared this checkout's evidence ladder and review-round record. This maintainer
  guidance is not installed in target projects.

### 2026-09-05 — bounded corrections and adoption guidance

- Made independent source reconciliation conditional on material review, preserving
  writer assessment and a small-work review decision.
- Corrected directory-relocation guarantees and preservation warnings; rejected
  invalid OS manifest paths before inspection and stopped content reads of unexpected
  entries. Retained descriptor-relative preservation and variable route sets.
- Allowed equal mutable task/handoff receipts in the frozen comparison, distinct from
  immutable inputs and excluded from product review; no trial result is claimed.
- Added a disposable install/resume exercise and manual update/reconciliation example;
  documented single-account modes and the inherited/current platform-proof boundary.

### 2026-08 — initial guidance

- Added portable review and delegation-failure rules to the installed routes—digest-bound
  targets, verified claims, review independence and fallbacks, interrupted-lane recovery and
  evidence outages—plus conditional bootstrap and maintainer guidance.
- Made language-native source orientation and consequential adjacent rationale an
  implementation and independent-review gate rather than a planning aspiration.
- Required coordinator-attested candidate source sets and independent inventory
  reconciliation so an omitted authored file cannot silently escape review.
- Added a merge-first coded-project documentation floor and proportional current-
  quality control loop for materially complex projects.
- Added synthetic review cases for simple, missing, consequential and exact-ADR-link
  source contracts, including removal mutations.

These are unreleased changes. `init` remains create-only; no installed-target
upgrade, publication or compatibility-identifier change is implied, and the installer
and manifest identities are unchanged.
