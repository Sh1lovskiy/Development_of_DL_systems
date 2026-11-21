import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "test.py"


class CompareImagesTest(unittest.TestCase):
    def test_only_equal_pixels_pass(self):
        cases = [
            ((2, 2), 50, 0),
            ((2, 2), 51, 1),
            ((2, 2), 49, 1),
            ((3, 2), 50, 1),
        ]
        with tempfile.TemporaryDirectory() as temp:
            expected = Path(temp) / "expected.png"
            actual = Path(temp) / "actual.png"
            Image.new("RGB", (2, 2), (50, 50, 50)).save(expected)
            for size, intensity, status in cases:
                with self.subTest(size=size, intensity=intensity):
                    Image.new("RGB", size, (intensity,) * 3).save(actual)
                    result = subprocess.run(
                        [sys.executable, str(SCRIPT), str(expected), str(actual)],
                        capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(result.returncode, status, result.stderr)
                    if status:
                        self.assertIn("Images differ", result.stderr)
