# --- start AI code ---
from niosTestCase import NiosTestCase


class AllTokenTests(NiosTestCase):
    def testEveryTokenTypeFromFile(self):
        output = self.runNios("allTokens.nios")

        expectedKeywords = [
            "AND", "ELSE", "FALSE", "IF", "LET", "NIL", "OR", "SHOW",
            "TRUE", "WHILE"
        ]
        expectedSymbols = [
            "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE",
            "COMMA", "DOT", "SEMICOLON", "PLUS", "MINUS", "STAR",
            "SLASH", "BANG", "BANG_EQUAL", "EQUAL", "EQUAL_EQUAL",
            "LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL"
        ]

        for keyword in expectedKeywords:
            self.assertIn(f"KEYWORD({keyword})", output)

        for symbol in expectedSymbols:
            self.assertIn(f"SYMBOL({symbol})", output)

        self.assertIn("LABEL raw='identifier' literal=None", output)
        self.assertIn("LABEL raw='_private' literal=None", output)
        self.assertIn("LABEL raw='label123' literal=None", output)
        self.assertIn("LABEL raw='anderson' literal=None", output)
        self.assertIn("LABEL raw='True' literal=None", output)
        self.assertIn("LABEL raw='_' literal=None", output)
        self.assertIn("NUMBER raw='0' literal=0", output)
        self.assertIn("NUMBER raw='42' literal=42", output)
        self.assertIn("NUMBER raw='3.14' literal=3.14", output)
        self.assertIn("NUMBER raw='12' literal=12", output)
        self.assertIn("WORD raw='\"\"' literal=''", output)
        self.assertIn("WORD raw='\"hello world\"' literal='hello world'", output)
        self.assertIn("WORD raw='\"! @ 123\"' literal='! @ 123'", output)
        self.assertIn("KEYWORD(FALSE) raw='false' literal=False", output)
        self.assertIn("KEYWORD(TRUE) raw='true' literal=True", output)
        self.assertIn("EOF raw='' literal=None", output)
    # --- end AI code ---