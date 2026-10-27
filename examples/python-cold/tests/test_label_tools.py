"""Test the cold example's label-normalization behavior."""

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from label_tools import normalize_label  # noqa: E402


class NormalizeLabelTests(unittest.TestCase):
    def test_collapses_whitespace_and_casefolds(self) -> None:
        self.assertEqual(normalize_label("  Warm\t  BOOT  "), "warm boot")

    def test_normalizes_unicode_compatibility_forms(self) -> None:
        self.assertEqual(normalize_label("Ｆｕｌｌｗｉｄｔｈ"), "fullwidth")

    def test_uses_unicode_case_folding(self) -> None:
        self.assertEqual(normalize_label("Straße"), "strasse")

    def test_rejects_non_string_input(self) -> None:
        with self.assertRaisesRegex(TypeError, "^value must be str$"):
            normalize_label(42)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
