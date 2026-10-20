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


    def runNios(self, fileName=None, userInput=None, flags=()):
        command = [sys.executable, "-B", str(NIOS_FILE)]
        if fileName is not None:
            command.append(str(fileName))
        command.extend(flags)


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
                actual = self.runNios(fileName=self.inputFile, flags=("-p",))
                self.assertEqual(actual, expected + "\n")

            with self.subTest(source=source, mode="interactive"):
                actual = self.runNios(userInput=source + "\n", flags=("-p",))
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


    def testInvalidNumberLiteral(self):
        source = "\u00b2"
        error = f"[line 1] Error: Invalid number literal {repr(source)}."
        self.checkBothModes([(source, error)])

        actual = self.runNios(userInput=source + "\n1 + 2\n")
        self.assertEqual(actual, "REPL mode\n" + error + "\n3\n")


    def testMultilineFiles(self):
        for source, expected in multilineCases:
            with self.subTest(source=source):
                self.inputFile.write_text(source, encoding="utf-8")
                actual = self.runNios(fileName=self.inputFile, flags=("-p",))
                self.assertEqual(actual, expected + "\n")


    def testInteractiveRecovery(self):
        inputs = ["2 * 3"]
        expected = ["REPL mode", "6"]

        for source, error in syntaxErrorCases + lexicalErrorCases:
            inputs.append(source)
            expected.append(error)
            inputs.append("1 + 2")
            expected.append("3")

        userInput = "\n".join(inputs) + "\n"
        actual = self.runNios(userInput=userInput)
        self.assertEqual(actual, "\n".join(expected) + "\n")


    def testInteractiveInputEndsAtEachLine(self):
        actual = self.runNios(userInput="(1 +\n2\n3 * 4\n")
        expected = (
            "REPL mode\n"
            "[line 1] Error at end of input: Expected an expression.\n"
            "2\n"
            "12\n"
        )
        self.assertEqual(actual, expected)


    def testInteractiveEndOfInput(self):
        self.assertEqual(self.runNios(userInput=""), "REPL mode\n")
        self.assertEqual(self.runNios(userInput="1 + 2"), "REPL mode\n3\n")


    def testEvaluation(self):
        cases = [
            ("1 + 2 / 3 * 4 == 23", "False"),
            ("true == 1", "True"),
            ("false == 0", "True"),
            ("nil", "nil"),
            ('"hello"', '"hello"'),
            ("!0", "True"),
            ("!2", "False"),
            ("!nil", "True"),
            ("!(1 < 2)", "False"),
            ("(3 + 4) * 2", "14"),
            ("1, 2 + 3", "5"),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.inputFile.write_text(source, encoding="utf-8")
                self.assertEqual(self.runNios(fileName=self.inputFile), expected + "\n")


    def testEvaluationTrace(self):
        source = "1 + 2 / 3 * 4 == 23"
        self.inputFile.write_text(source, encoding="utf-8")
        expected = (
            source + "\n"
            "(== (+ 1 (* (/ 2 3) 4)) 23)\n"
            "(== (+ 1 (* (0.667) 4)) 23)\n"
            "(== (+ 1 (2.667)) 23)\n"
            "(== (3.667) 23)\n"
            "False\n"
        )
        self.assertEqual(self.runNios(fileName=self.inputFile, flags=("-a",)), expected)
        self.assertEqual(self.runNios(fileName=self.inputFile), "False\n")


    def testEvaluationErrors(self):
        cases = [
            ("1 / 0", "[line 1] Error at '/': Division by zero."),
            ('"hello" + 1', "[line 1] Error at '+': Operands must be numbers."),
            ('-"hello"', "[line 1] Error at '-': Operand must be a number."),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.inputFile.write_text(source, encoding="utf-8")
                self.assertEqual(self.runNios(fileName=self.inputFile), expected + "\n")


    def testOutputModes(self):
        cases = [
            ("1 + 2 / 3 * 4 == 23", "-p", "(== (+ 1 (* (/ 2 3) 4)) 23)"),
            ("1 + 2 / 3 * 4 == 23", "-s", "NUM ADD NUM DIV NUM MUL NUM EQ NUM"),
            ("1 / 0", "-p", "(/ 1 0)"),
            ("1 +", "-s", "NUM ADD"),
            ('(true != false), nil, "hello", name', "-s",
             "LEFT_PAREN TRUE NE FALSE RIGHT_PAREN COMMA NIL COMMA WORD COMMA LABEL"),
            ("1 /* comment */ + 2", "-s", "NUM ADD NUM"),
            ("", "-s", ""),
            ("@", "-s", "[line 1] Error: Unexpected character '@'."),
        ]
        for source, flag, expected in cases:
            with self.subTest(source=source, flag=flag):
                self.inputFile.write_text(source, encoding="utf-8")
                self.assertEqual(
                    self.runNios(fileName=self.inputFile, flags=(flag,)), expected + "\n"
                )
                self.assertEqual(
                    self.runNios(userInput=source + "\n", flags=(flag,)),
                    "REPL mode\n" + expected + "\n"
                )


    def testConflictingOutputModes(self):
        for flags in (("-a", "-p"), ("-p", "-s"), ("-a", "-s"), ("-p", "-p")):
            with self.subTest(flags=flags):
                self.assertEqual(
                    self.runNios(userInput="", flags=flags),
                    "Error: use only one of -a, -p, or -s.\n"
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
# --- end AI code --