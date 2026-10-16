# --- start AI code --
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


LAB3_FOLDER = Path(__file__).resolve().parents[1]
INTERPRETER_FOLDER = Path(__file__).resolve().parents[3]
NIOS_FILE = INTERPRETER_FOLDER / "src" / "nios.py"
TEST_FOLDER = LAB3_FOLDER / "testFiles"
sys.path.insert(0, str(TEST_FOLDER))

from expressionCases import (
    associativityCases,
    groupingCases,
    lexicalErrorCases,
    literalCases,
    multilineCases,
    operatorCases,
    precedenceCases,
    syntaxErrorCases
)


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.tempFolder = tempfile.TemporaryDirectory(dir=TEST_FOLDER)
        self.addCleanup(self.tempFolder.cleanup)
        self.inputFile = Path(self.tempFolder.name) / "expression.nios"


    def runNios(self, fileName=None, userInput=None):
        command = [sys.executable, "-B", str(NIOS_FILE)]
        if fileName is not None:
            command.append(str(fileName))


        result = subprocess.run(
            command,
            cwd=INTERPRETER_FOLDER,
            input=userInput,
            text=True,
            capture_output=True,
            timeout=10
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout


    def checkBothModes(self, cases):
        for source, expected in cases:
            with self.subTest(source=source, mode="file"):
                self.inputFile.write_text(source, encoding="utf-8")
                actual = self.runNios(fileName=self.inputFile)
                self.assertEqual(actual, expected + "\n")

            with self.subTest(source=source, mode="interactive"):
                actual = self.runNios(userInput=source + "\n")
                self.assertEqual(actual, "REPL mode\n" + expected + "\n")


    def testLiteralTypes(self):
        self.checkBothModes(literalCases)


    def testEveryOperator(self):
        self.checkBothModes(operatorCases)


    def testPrecedence(self):
        self.checkBothModes(precedenceCases)


    def testAssociativity(self):
        self.checkBothModes(associativityCases)


    def testNestedGrouping(self):
        self.checkBothModes(groupingCases)


    def testSyntaxErrors(self):

        self.checkBothModes(syntaxErrorCases)


    def testLexicalErrors(self):
        self.checkBothModes(lexicalErrorCases)


    def testMultilineFiles(self):
        for source, expected in multilineCases:
            with self.subTest(source=source):
                self.inputFile.write_text(source, encoding="utf-8")
                actual = self.runNios(fileName=self.inputFile)
                self.assertEqual(actual, expected + "\n")


    def testInteractiveRecovery(self):
        inputs = ["2 * 3"]
        expected = ["REPL mode", "(* 2 3)"]

        for source, error in syntaxErrorCases + lexicalErrorCases:
            inputs.append(source)
            expected.append(error)
            inputs.append("1 + 2")
            expected.append("(+ 1 2)")

        userInput = "\n".join(inputs) + "\n"
        actual = self.runNios(userInput=userInput)
        self.assertEqual(actual, "\n".join(expected) + "\n")


    def testInteractiveInputEndsAtEachLine(self):
        actual = self.runNios(userInput="(1 +\n2\n3 * 4\n")
        expected = (
            "REPL mode\n"
            "[line 1] Error at end of input: Expected an expression.\n"
            "2\n"
            "(* 3 4)\n"
        )
        self.assertEqual(actual, expected)


    def testInteractiveEndOfInput(self):
        self.assertEqual(self.runNios(userInput=""), "REPL mode\n")
        self.assertEqual(self.runNios(userInput="1 + 2"), "REPL mode\n(+ 1 2)\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
# --- end AI code --