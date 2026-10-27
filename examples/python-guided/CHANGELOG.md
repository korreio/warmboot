# Changelog

This file records user-visible behavior and compatibility changes. A version
entry does not claim a tag, package publication, or hosted release.

## 0.1.0 — synthetic local example

- Added Unicode compatibility normalization, whitespace collapse, and
  Unicode-aware case folding behind one pure function.
- Added a thin CLI that emits one comparison key per input.
- Defined output as destructive comparison data; callers retain display text.
- Kept the required run path offline and free of runtime dependencies.
