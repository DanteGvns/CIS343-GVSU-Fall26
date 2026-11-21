# --- start AI code --
import subprocess
import sys
import unittest
from pathlib import Path


LAB_FOLDER = Path(__file__).resolve().parents[1]
NIOS_FILE = LAB_FOLDER.parents[1] / "src" / "nios.py"


class VariablesTestCase(unittest.TestCase):
    def runNios(self, *arguments, userInput=""):
        result = subprocess.run(
            [sys.executable, "-B", str(NIOS_FILE), *map(str, arguments)],
            input=userInput,
            text=True,
            capture_output=True,
            timeout=10
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def checkFile(self, name, expected):
        self.assertEqual(self.runNios(LAB_FOLDER / (name + ".nios")), expected)

    def testVariables(self):
        self.checkFile("variables", "2\n5\nnil\n9\n9\n9\n")

    def testShowIsTheOutputKeyword(self):
        self.assertEqual(
            self.runNios(userInput="print 2;\nlet print = 3; show print;\n"),
            "REPL mode\n[line 1] Error at '2': Expected ';' after expression.\n3\n"
        )

    def testTextbookBlockScope(self):
        self.checkFile(
            "blockScope",
            "inner a\nouter b\nglobal c\n"
            "outer a\nouter b\nglobal c\n"
            "global a\nglobal b\nglobal c\n"
        )

    def testAssignmentUsesNearestScope(self):
        output = self.runNios(
            userInput="let a = 1; let b = 2;\n"
            "{ let a = a + 1; { a = 3; b = 4; } show a; }\n"
            "show a; show b;\n"
        )
        self.assertEqual(output, "REPL mode\n3\n1\n4\n")

    def testAssignmentPrecedence(self):
        output = self.runNios(userInput="var a; show a = 2 + 3, a == 5;\nshow a;\n")
        self.assertEqual(output, "REPL mode\ntrue\n5\n")

    def testSyntaxErrors(self):
        cases = {
            "invalidTargets": "".join(
                f"[line {line}] Error at '=': Invalid assignment target.\n"
                for line in (1, 3, 4)
            ),
            "badDeclarations": (
                "[line 1] Error at '123': Expected a variable name.\n"
                "[line 2] Error at ';': Expected an expression.\n"
                "[line 4] Error at 'show': Expected ';' after variable declaration.\n"
                "[line 5] Error at ';': Expected an expression.\n"
            ),
            "unmatchedOpen": "[line 3] Error at end of input: Expected '}' to close block.\n",
            "unmatchedClose": "[line 1] Error at '}': Unmatched '}'.\n"
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                self.checkFile(name, expected)

    def testRecoveryKeepsBlockBoundaries(self):
        self.assertEqual(
            self.runNios("-p", userInput="{ let a = } show 2;\n"),
            "REPL mode\n[line 1] Error at '}': Expected an expression.\n"
            "(block)\n(show 2)\n"
        )

    def testRuntimeErrors(self):
        self.checkFile(
            "redeclaration",
            "[line 2] Error at 'count': Variable already declared in this scope.\n"
        )
        self.checkFile("scopeErrors", "inside\n[line 5] Error at 'local': Undefined variable.\n")
        for source in ("show x; var x = 1;", "var x = x;", "x = 1; var x;"):
            with self.subTest(source=source):
                self.assertEqual(
                    self.runNios(userInput=source + "\n"),
                    "REPL mode\n[line 1] Error at 'x': Undefined variable.\n"
                )

    def testBlockScopeIsCleanedUpAfterError(self):
        self.assertEqual(
            self.runNios(userInput="let x = 1;\n{ let x = 2; show missing; }\nshow x;\n"),
            "REPL mode\n[line 1] Error at 'missing': Undefined variable.\n1\n"
        )

    def testAstAndTraceModes(self):
        self.assertEqual(
            self.runNios("-p", userInput="let a; { a = 2; show a; }\n"),
            "REPL mode\n(var a)\n(block (expr (= a 2)) (show a))\n"
        )
        self.assertEqual(
            self.runNios("-a", userInput="var a = 1; show a;\n"),
            "REPL mode\nvar a = 1; show a;\n(var a 1)\n(show a)\n(show (1))\n1\n"
        )


if __name__ == "__main__":
    unittest.main()

# --- end AI code ---