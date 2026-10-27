# Label Normalizer — guided example

This synthetic Label Normalizer project is the guided half of a small teaching
pair. It has the same comparison-key semantics as `../python-cold`, while adding
a package boundary, CLI, target-owned instructions, one architecture decision,
and evidence and release records.

## Try it

Prerequisite: Python 3.11 or newer. No installation is required.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m label_normalizer "  Warm   BOOT  " "Straße"
```

Expected output:

```text
warm boot
strasse
```

Normalization uses Unicode compatibility forms, whitespace collapse, and
Unicode-aware case folding. It is suitable for comparison keys, not preserved
display text, transliteration, slug generation, or locale-specific collation.

## Project map

- `src/label_normalizer/core.py` owns comparison-key policy.
- `src/label_normalizer/__main__.py` owns only command-line input and output.
- `tests/` holds local behavior evidence; `TASK.md` records its current limits.
- `docs/adr/` preserves the accepted design rationale.

## Read by need

- [`TASK.md`](TASK.md) — current objective, authority, and actual evidence
- [`AGENTS.md`](AGENTS.md) — concise working and recovery contract
- [`docs/adr/0001-python-standard-library-core.md`](docs/adr/0001-python-standard-library-core.md)
  — the accepted trade-off and reversal triggers
- [`CHANGELOG.md`](CHANGELOG.md) — user-visible behavior and release boundary
- [`BUGFIXES.md`](BUGFIXES.md) — escaped defects and regression evidence

`pyproject.toml` declares package metadata and a console entry point. Installing
it is optional and may require separately authorized build tooling; the commands
above remain the required offline path.
