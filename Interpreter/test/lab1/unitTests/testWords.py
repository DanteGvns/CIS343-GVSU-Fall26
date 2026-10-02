# --- start AI code ---
from niosTestCase import NiosTestCase


class WordTests(NiosTestCase):
    def testWordCanSpanMultipleLines(self):
        output = self.runNios("multilineWord.nios")

        self.assertIn(
            "WORD raw='\"first line\\nsecond line\"' "
            "literal='first line\\nsecond line' line=1",
            output
        )
        self.assertIn("LABEL raw='afterWord' literal=None line=3", output)
        self.assertNotIn("Unterminated string", output)
    # --- end AI code ---