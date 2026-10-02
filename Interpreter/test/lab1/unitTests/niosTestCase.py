# --- start AI code ---
import subprocess
import sys
import unittest
from pathlib import Path


LAB1_TEST_FOLDER = Path(__file__).resolve().parents[1]
INTERPRETER_FOLDER = Path(__file__).resolve().parents[3]
NIOS_FILE = INTERPRETER_FOLDER / "src" / "nios.py"
TEST_FOLDER = LAB1_TEST_FOLDER / "testFiles"


class NiosTestCase(unittest.TestCase):
    def runNios(self, fileName=None, userInput=None):
        command = [sys.executable, str(NIOS_FILE)]
        if fileName is not None:
            command.append(str(TEST_FOLDER / fileName))

        result = subprocess.run(
            command,
            cwd=INTERPRETER_FOLDER,
            input=userInput,
            text=True,
            capture_output=True
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout
# --- end AI code ---