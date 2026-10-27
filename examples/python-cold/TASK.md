# Current task

This synthetic teaching snapshot is not a live assignment and grants no authority.

- Status: `COMPLETE`
- Objective: provide one deterministic label-to-comparison-key helper.
- Scope: `src/label_tools.py` and `tests/test_label_tools.py`.
- Runtime boundary: Python standard library only; no network or persistence.
- External effects: `NONE`; Git and publication are not authorized.

## Acceptance

- Normalize Unicode compatibility forms before comparison.
- Collapse whitespace and apply Unicode-aware case folding.
- Reject non-string input with `TypeError`.
- Preserve display labels outside this helper.
- Pass the native test command in `README.md`.
