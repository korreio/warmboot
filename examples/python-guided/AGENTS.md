# Working contract — Label Normalizer

This is the target-owned operating contract for this synthetic project. Read
`TASK.md` first. `CLAUDE.md` points here and adds no separate policy.

## Boundaries

- The coordinator named in `TASK.md` owns the task record and is the only Git,
  remote, or publication operator. Local source and test edits require an exact
  task assignment; package installation and network access require separate
  authorization.
- Preserve unrelated work. Stop when ownership overlaps or the requested change
  needs an excluded effect.
- Keep the runtime standard-library-only. `core.py` owns normalization;
  `__main__.py` only parses arguments and prints results.
- A normalized value is a comparison key, never display text. Do not add
  transliteration, punctuation stripping, slugging, persistence, or services
  without a changed requirement and a superseding decision.

## Evidence and review

Start with the smallest relevant test, then close with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m label_normalizer "  Warm   BOOT  "
```

Record what actually ran and what remains unproved. A passing test proves only
its assertions. Every code change needs a reviewer who did not author the change;
the verdict is `CLEAN`, `FINDING`, or `BLOCKED`.

## Source comprehension

Python module and public-callable docstrings are the adopted language-native form.
Every human-authored code file starts with an accurate purpose; one sentence is
enough for a simple adapter. Put why and operative invariants beside consequential
normalization logic, with an exact ADR-section link for extended rationale. Tests and
the ADR do not replace the local source contract. Generated, vendored and pure
re-export files would need a recorded exception; this example has none.

Before handoff, the coordinator attests the frozen candidate source set and the writer
reconciles every path and records whether it is simple or consequential in `TASK.md`.
The non-author reviewer independently repeats that reconciliation, reads every path,
and returns `FINDING` for an omission or missing, stale or code-restating explanation
even when tests pass. The attestation and writer assessment remain mandatory.

## Recovery and release

On resume, reread `TASK.md` and inspect current files before trusting inherited
results. Rerun evidence when source, tests, interpreter, settings, or task inputs
changed. Preserve the filesystem at interruption and describe which evidence was
rerun rather than silently treating it as current.

Update `CHANGELOG.md` only for user-visible behavior or compatibility changes.
A version in `pyproject.toml`, a local checkpoint, a tag, package publication,
and a hosted release are separate actions and permissions.

Finish by updating `TASK.md` with changed paths, commands and results, skipped
proof, review state, and the next authorized action.
