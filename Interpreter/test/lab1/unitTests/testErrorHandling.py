# --- start AI code ---
from niosTestCase import NiosTestCase


class ErrorHandlingTests(NiosTestCase):
    def testEveryLexicalErrorFromFile(self):
        output = self.runNios("errorTest.nios")
        wordOutput = self.runNios("unterminatedWord.nios")

        self.assertIn("[line 2] Error: Unexpected character '@'.", output)
        self.assertIn("[line 3] Error: Unterminated block comment.", output)
        self.assertIn("[line 1] Error: Unterminated string.", wordOutput)
    # --- end AI code ---