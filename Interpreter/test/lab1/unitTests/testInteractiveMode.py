# --- start AI code ---
from niosTestCase import NiosTestCase


class InteractiveModeTests(NiosTestCase):
    def testInteractiveModeRecoversAfterErrors(self):
        userInput = '@\n"missing end\nshow 42;\n/* missing end\nshow false;\n'
        output = self.runNios(userInput=userInput)

        self.assertIn("REPL mode", output)
        self.assertIn("[line 1] Error: Unexpected character '@'.", output)
        self.assertIn("[line 1] Error: Unterminated string.", output)
        self.assertIn("[line 1] Error: Unterminated block comment.", output)
        self.assertIn("KEYWORD(SHOW) raw='show' literal=None", output)
        self.assertIn("NUMBER raw='42' literal=42", output)
        self.assertIn("KEYWORD(FALSE) raw='false' literal=False", output)

        firstError = output.index("Unexpected character")
        recoveredToken = output.index("NUMBER raw='42'")
        lastError = output.index("Unterminated block comment")
        finalRecoveredToken = output.index("KEYWORD(FALSE)")
        self.assertLess(firstError, recoveredToken)
        self.assertLess(lastError, finalRecoveredToken)
    # --- end AI code ---