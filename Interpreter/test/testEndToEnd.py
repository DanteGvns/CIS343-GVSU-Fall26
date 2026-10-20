# --- start AI code --
import subprocess
import sys
import unittest
from pathlib import Path


INTERPRETER_FOLDER = Path(__file__).resolve().parents[1]
NIOS_FILE = INTERPRETER_FOLDER / "src" / "nios.py"
MIDTERM_FILE = INTERPRETER_FOLDER / "test" / "lab3" / "testFiles" / "midtermExample.nios"


class EndToEndTestCase(unittest.TestCase):
    def runNios(self, arguments=(), userInput=""):
        result = subprocess.run(
            [sys.executable, "-B", str(NIOS_FILE), *map(str, arguments)],
            cwd=INTERPRETER_FOLDER,
            input=userInput,
            text=True,
            capture_output=True,
            timeout=10
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout


    def testMidtermFileAllModes(self):
        cases = [
            ((), "False\n"),
            (("-s",), "NUM ADD NUM DIV NUM MUL NUM EQ NUM\n"),
            (("-p",), "(== (+ 1 (* (/ 2 3) 4)) 23)\n"),
            (("-a",),
             "1 + 2 / 3 * 4 == 23\n"
             "(== (+ 1 (* (/ 2 3) 4)) 23)\n"
             "(== (+ 1 (* (0.667) 4)) 23)\n"
             "(== (+ 1 (2.667)) 23)\n"
             "(== (3.667) 23)\n"
             "False\n"),
        ]
        for flags, expected in cases:
            with self.subTest(flags=flags):
                self.assertEqual(self.runNios((MIDTERM_FILE, *flags)), expected)


    def testInteractiveRecovery(self):
        source = "1 + 2\n@\n1 +\n1 / 0\n(3 + 4) * 2\ntrue == 1\nfalse == 0\n!0\n!-2\n"
        expected = (
            "REPL mode\n"
            "3\n"
            "[line 1] Error: Unexpected character '@'.\n"
            "[line 1] Error at end of input: Expected an expression.\n"
            "[line 1] Error at '/': Division by zero.\n"
            "14\nTrue\nTrue\nTrue\nFalse\n"
        )
        self.assertEqual(self.runNios(userInput=source), expected)


    def testOutputModesStopAtTheirStage(self):
        self.assertEqual(
            self.runNios(("-s",), "1 +\n"),
            "REPL mode\nNUM ADD\n"
        )
        self.assertEqual(
            self.runNios(("-p",), "1 / 0\n"),
            "REPL mode\n(/ 1 0)\n"
        )


    def testTraceDoesNotRoundCalculation(self):
        self.assertEqual(
            self.runNios(("-a",), "2 / 3 * 3 == 2\n"),
            "REPL mode\n"
            "2 / 3 * 3 == 2\n"
            "(== (* (/ 2 3) 3) 2)\n"
            "(== (* (0.667) 3) 2)\n"
            "(== (2) 2)\n"
            "True\n"
        )


    def testRejectsConflictingFlags(self):
        self.assertEqual(
            self.runNios((MIDTERM_FILE, "-p", "-s")),
            "Error: use only one of -a, -p, or -s.\n"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
# --- end AI code --