"""Pure standard-library comparison-key normalization."""

import unicodedata


def normalize_label(value: str) -> str:
    """Return a comparison key; callers retain the original display label."""

    if not isinstance(value, str):
        raise TypeError("value must be str")

    # Why: NFKC makes compatibility-equivalent labels comparable before whitespace
    # collapse and case folding. Invariant: this destructive key is never display text.
    # See: docs/adr/0001-python-standard-library-core.md#decision
    compatible = unicodedata.normalize("NFKC", value)
    return " ".join(compatible.split()).casefold()
