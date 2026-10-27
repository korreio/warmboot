"""Exercises the label normalizer's process-level command-line contract."""

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LabelNormalizerCliTests(unittest.TestCase):
    def test_prints_one_comparison_key_per_argument(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run(
            [sys.executable, "-m", "label_normalizer", " Warm  BOOT ", "Straße"],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "warm boot\nstrasse\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
