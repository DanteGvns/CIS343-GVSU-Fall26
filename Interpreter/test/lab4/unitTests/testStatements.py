# --- start AI code --
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


LAB4_FOLDER = Path(__file__).resolve().parents[1]
INTERPRETER_FOLDER = Path(__file__).resolve().parents[3]
NIOS_FILE = INTERPRETER_FOLDER / "src" / "nios.py"


class StatementsTestCase(unittest.TestCase):
    def setUp(self):
        self.tempFolder = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempFolder.cleanup)
        self.inputFile = Path(self.tempFolder.name) / "statements.nios"

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

    def runSource(self, source, flags=()):
        self.inputFile.write_text(source, encoding="utf-8")
        return self.runNios((self.inputFile, *flags))

    def checkBothModes(self, source, expected, flags=()):
        with self.subTest(mode="file"):
            self.assertEqual(self.runSource(source, flags), expected)
        with self.subTest(mode="REPL"):
            self.assertEqual(
                self.runNios(flags, source + "\n"), "REPL mode\n" + expected
            )

    def testRequiredValidFile(self):
        self.assertEqual(
            self.runNios((LAB4_FOLDER / "statements.nios",)),
            'one\ntrue\n3\nnil\n'
        )

    def testRequiredInvalidFile(self):
        source = (LAB4_FOLDER / "requiredErrors.nios").read_text(encoding="utf-8")
        eofLine = source.count("\n") + 1
        self.assertEqual(
            self.runNios((LAB4_FOLDER / "requiredErrors.nios",)),
            "[line 2] Error at 'true': Expected ';' after expression.\n"
            f"[line {eofLine}] Error at end of input: Expected an expression.\n"
        )

    def testExistingBadStatementsFile(self):
        source = (LAB4_FOLDER / "badStatements.nios").read_text(encoding="utf-8")
        eofLine = source.count("\n") + 1
        self.assertEqual(
            self.runNios((LAB4_FOLDER / "badStatements.nios",)),
            "[line 2] Error at 'false': Expected ';' after expression.\n"
            f"[line {eofLine}] Error at end of input: Expected an expression.\n"
        )

    def testLiteralPrinting(self):
        cases = [
            ("12", "12"), ("12.5", "12.5"), ("true", "true"),
            ("false", "false"), ("nil", "nil"), ('"yes"', "yes"),
            ('""', ""), ('"a\\nb"', 'a\\nb'),
            ('"test"', "test"), ('"  spaced  "', "  spaced  "),
            ('("grouped")', "grouped"), ('1, "last"', "last")
        ]
        for expression, expected in cases:
            with self.subTest(expression=expression):
                self.checkBothModes(f"show {expression};", expected + "\n")

    def testExpressionStatementsAreSilent(self):
        for expression in ("2 + 2", "true", "nil", '"yes"', "(2 + 3) >= 2"):
            with self.subTest(expression=expression):
                self.checkBothModes(expression + ";", "")

    def testMixedStatementsExecuteInOrder(self):
        self.checkBothModes(
            '1 + 2; show 4; false; show "last"; nil;',
            '4\nlast\n'
        )

    def testAllExpressionOperatorsStillWork(self):
        cases = [
            ("1 + 2 * 3", "7"), ("(1 + 2) * 3", "9"),
            ("8 - 3 - 1", "4"), ("8 / 4 / 2", "1.0"),
            ("-2 * 3", "-6"), ("!false", "true"),
            ("1 < 2", "true"), ("2 <= 2", "true"),
            ("3 > 4", "false"), ("3 >= 3", "true"),
            ("1 == 2", "false"), ("1 != 2", "true"),
            ("1, 2 + 3", "5"), ("true == 3", "true"),
            ("false == 0", "true"), ("!nil", "true")
        ]
        for expression, expected in cases:
            with self.subTest(expression=expression):
                self.checkBothModes(f"show {expression};", expected + "\n")

    def testEmptyPrograms(self):
        for source in ("", "   ", "// comment", "/* comment */"):
            for flags in ((), ("-p",)):
                with self.subTest(source=source, flags=flags):
                    self.checkBothModes(source, "", flags)

    def testMultilineStatementsAndComments(self):
        source = 'show (1 +\n2) * 3;\n// next\n4;\nshow /* comment */ true;'
        self.assertEqual(self.runSource(source), "9\ntrue\n")
        self.assertEqual(
            self.runSource(source, ("-p",)),
            "(show (* (group (+ 1 2)) 3))\n(expr 4)\n(show true)\n"
        )

    def testMultilineStringPreservesNewlines(self):
        self.assertEqual(self.runSource('show "a\nb";'), 'a\nb\n')

    def testManyStatementsPreserveOrder(self):
        source = " ".join(f"{number}; show {number};" for number in range(100))
        expected = "".join(f"{number}\n" for number in range(100))
        self.assertEqual(self.runSource(source), expected)

    def testErrorsAreReportedInSourceOrder(self):
        self.assertEqual(
            self.runSource("show ;\nshow 1;\nshow 2 +\n", ("-p",)),
            "[line 1] Error at ';': Expected an expression.\n"
            "[line 4] Error at end of input: Expected an expression.\n"
            "(show 1)\n"
        )

    def testReplResetsLineNumbers(self):
        self.assertEqual(
            self.runNios(userInput="show ;\nshow ;\n"),
            "REPL mode\n"
            "[line 1] Error at ';': Expected an expression.\n"
            "[line 1] Error at ';': Expected an expression.\n"
        )

    def testMissingSemicolons(self):
        for source, message in (
            ("2 + 2", "Expected ';' after expression."),
            ("show 12", "Expected ';' after SHOW statement.")
        ):
            with self.subTest(source=source):
                self.checkBothModes(
                    source, f"[line 1] Error at end of input: {message}\n"
                )

    def testKeywordCaseAndUnquotedWords(self):
        for source, token in (("SHOW 12;", "SHOW"), ("show yes;", "yes")):
            with self.subTest(source=source):
                self.checkBothModes(
                    source, f"[line 1] Error at '{token}': Expected an expression.\n"
                )

    def testUnsupportedAssignmentAndImplicitMultiplication(self):
        for source, token in (("1 = 1;", "="), ("1(2 * 4);", "(")):
            with self.subTest(source=source):
                self.checkBothModes(
                    source,
                    f"[line 1] Error at '{token}': Expected ';' after expression.\n"
                )

    def testRuntimeErrors(self):
        cases = [
            ("1 / 0;", "[line 1] Error at '/': Division by zero.\n"),
            ("show 1 / 0;", "[line 1] Error at '/': Division by zero.\n"),
            ('show "yes" + 12;', "[line 1] Error at '+': Operands must be numbers.\n"),
            ('show -"yes";', "[line 1] Error at '-': Operand must be a number.\n")
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.checkBothModes(source, expected)

    def testRuntimeErrorStopsRemainingStatements(self):
        self.assertEqual(
            self.runSource("show 1; 1 / 0; show 2;"),
            "1\n[line 1] Error at '/': Division by zero.\n"
        )

    def testSyntaxErrorPreventsAllExecution(self):
        self.checkBothModes(
            "show 1; show 2 + ; show 3;",
            "[line 1] Error at ';': Expected an expression.\n"
        )

    def testScannerErrorPreventsAllExecution(self):
        self.checkBothModes(
            "show 1; @ show 2;",
            "[line 1] Error: Unexpected character '@'.\n"
        )

    def testRecoveryAtSemicolons(self):
        expectedErrors = (
            "[line 1] Error at ';': Expected an expression.\n"
            "[line 3] Error at ';': Expected an expression.\n"
        )
        file = LAB4_FOLDER / "recovery.nios"
        self.assertEqual(self.runNios((file,)), expectedErrors)
        self.assertEqual(
            self.runNios((file, "-p")),
            expectedErrors + "(show 2)\n(show 4)\n"
        )

    def testRecoveryPreservesNextShow(self):
        file = LAB4_FOLDER / "missingSemicolon.nios"
        self.assertEqual(
            self.runNios((file, "-p")),
            "[line 2] Error at 'show': Expected ';' after SHOW statement.\n"
            "(show 2)\n"
        )

    def testMissingExpressionBeforeNextShow(self):
        self.checkBothModes(
            "show show 2;",
            "[line 1] Error at 'show': Expected an expression.\n(show 2)\n",
            ("-p",)
        )

    def testRecoveryPreservesExpressionAfterSemicolon(self):
        self.checkBothModes(
            "show 1 + ; 2 + 3; show 4;",
            "[line 1] Error at ';': Expected an expression.\n"
            "(expr (+ 2 3))\n(show 4)\n",
            ("-p",)
        )

    def testRecoverySkipsDamagedTokens(self):
        self.checkBothModes(
            "show 1 + * 9 10; show 2;",
            "[line 1] Error at '*': Missing left operand before '*'.\n"
            "(show 2)\n",
            ("-p",)
        )

    def testRecoveryFromGroupingError(self):
        self.checkBothModes(
            "show (1 + 2; show 3;",
            "[line 1] Error at ';': Expected ')' after expression.\n(show 3)\n",
            ("-p",)
        )

    def testRecoveryTerminatesAtEof(self):
        for source, expected in (
            ("show", "Expected an expression."),
            ("show 1 +", "Expected an expression."),
            ("show (1", "Expected ')' after expression."),
            ("1", "Expected ';' after expression.")
        ):
            with self.subTest(source=source):
                self.checkBothModes(
                    source, f"[line 1] Error at end of input: {expected}\n", ("-p",)
                )

    def testRepeatedBadTokensMakeProgress(self):
        source = "; " * 100 + "show 7;"
        output = self.runSource(source, ("-p",))
        self.assertEqual(
            output,
            "[line 1] Error at ';': Expected an expression.\n" * 100
            + "(show 7)\n"
        )

    def testRepeatedShowKeywordsMakeProgress(self):
        output = self.runSource("show " * 100 + "7;", ("-p",))
        self.assertEqual(
            output,
            "[line 1] Error at 'show': Expected an expression.\n" * 99
            + "(show 7)\n"
        )

    def testReplRecoversOnNextInputLine(self):
        self.assertEqual(
            self.runNios(userInput="show 1 + ;\nshow 2;\n@\nshow 3;\n"),
            "REPL mode\n[line 1] Error at ';': Expected an expression.\n"
            "2\n[line 1] Error: Unexpected character '@'.\n3\n"
        )

    def testParserModeShowsStatementTypesWithoutExecuting(self):
        self.checkBothModes(
            "4 + 2; show 1 / 0; show nil;",
            "(expr (+ 4 2))\n(show (/ 1 0))\n(show nil)\n",
            ("-p",)
        )

    def testScannerModeDoesNotParse(self):
        self.checkBothModes(
            "show 2 +",
            "SHOW NUM ADD\n",
            ("-s",)
        )
        self.checkBothModes(
            "show true; 2;",
            "SHOW TRUE SEMICOLON NUM SEMICOLON\n",
            ("-s",)
        )

    def testTraceShowsSilentExpressionReduction(self):
        self.checkBothModes(
            "1 + 2;",
            "1 + 2;\n(expr (+ 1 2))\n(expr (3))\n",
            ("-a",)
        )

    def testTraceIsResetBetweenStatements(self):
        self.checkBothModes(
            "show 1 + 2; show 3 * 4;",
            "show 1 + 2; show 3 * 4;\n"
            "(show (+ 1 2))\n(show (3))\n3\n"
            "(show (* 3 4))\n(show (12))\n12\n",
            ("-a",)
        )

    def testTraceDoesNotExecuteSyntaxInvalidProgram(self):
        self.checkBothModes(
            "show 1; show 2 + ;",
            "[line 1] Error at ';': Expected an expression.\n",
            ("-a",)
        )

    def testConflictingFlags(self):
        for flags in (("-a", "-p"), ("-p", "-s"), ("-a", "-s"), ("-p", "-p")):
            with self.subTest(flags=flags):
                self.assertEqual(
                    self.runNios(flags),
                    "Error: use only one of -a, -p, or -s.\n"
                )

    def testMissingFileAndUnsupportedExtension(self):
        self.assertEqual(
            self.runNios((Path(self.tempFolder.name) / "missing.nios",)),
            "Error: That file does not exist, please check your file path.\n"
        )
        self.assertEqual(
            self.runNios((Path(self.tempFolder.name) / "input.txt",)),
            "Error: Nios can only read .nios files.\n"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
# --- end AI code --
