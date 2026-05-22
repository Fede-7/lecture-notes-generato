import sys
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from note_generator.main import main


class CliTests(unittest.TestCase):
    def test_cli_writes_output(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "lecture.txt"
            output_path = Path(temp_dir) / "notes.md"
            input_path.write_text("Il processo è schedulato.", encoding="utf-8")

            original_argv = sys.argv[:]
            sys.argv = [
                "main.py",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--format",
                "markdown",
            ]
            try:
                self.assertEqual(main(), 0)
            finally:
                sys.argv = original_argv

            self.assertTrue(output_path.exists())
            self.assertIn("Automated Lecture Notes", output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
