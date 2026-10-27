# ADR 0001 — Python standard-library core and thin CLI

- Status: `ACCEPTED FOR THIS SYNTHETIC EXAMPLE`
- Decision owner: `example-coordinator`
- Related task: [`TASK.md`](../../TASK.md)

## Context

The project needs one deterministic transformation from display labels to
comparison keys and a command-line adapter. It has no service, persistence,
concurrency, UI, or performance requirement. The required path must run offline
without installing runtime dependencies.

## Options

1. A shell pipeline would use fewer source files, but Unicode compatibility and
   case-folding behavior would vary with platform tools.
2. Python's standard library provides the required Unicode normalization,
   argument parsing, and tests. A pure function can own policy while a thin CLI
   owns process I/O.
3. A third-party normalization or CLI library could add policies and richer
   output, but no accepted caller needs them; it would add installation and
   update cost.

## Decision

Choose option 2. Require Python 3.11 or newer for this example. Keep
`normalize_label(str) -> str` as the only behavior owner, use a thin CLI, and
keep runtime dependencies empty. Treat package installation, network access,
version changes, tags, and publication as separate decisions and permissions.

The normalized result is destructive comparison data. Callers retain the
original display label. Transliteration, punctuation removal, URL slugging, and
locale-specific collation are non-goals.

## Consequences and reversal

The native tests and source CLI run with the standard library. Optional packaging
metadata exposes a console entry point but does not prove installation or a
release. This design should be replaced when a real caller needs stable keys
across Unicode database versions, a different runtime, locale-aware collation,
bulk performance evidence, or a third-party policy.
