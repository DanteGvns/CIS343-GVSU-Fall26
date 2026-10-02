# --- start AI code ---
from niosTestCase import NiosTestCase


class EndOfFileTests(NiosTestCase):
    def testEmptyFileProducesEof(self):
        output = self.runNios("emptyTest.nios")

        self.assertEqual(output.strip(), "EOF raw='' literal=None line=1")
    # --- end AI code ---