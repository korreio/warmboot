"""Small standard-library helpers for deterministic label comparison."""

import unicodedata


def normalize_label(value: str) -> str:
    """Return a comparison key; callers retain the original display label."""

    if not isinstance(value, str):
        raise TypeError("value must be str")

    compatible = unicodedata.normalize("NFKC", value)
    return " ".join(compatible.split()).casefold()
