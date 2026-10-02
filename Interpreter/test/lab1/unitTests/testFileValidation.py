# --- start AI code ---
from niosTestCase import NiosTestCase


class FileValidationTests(NiosTestCase):
    def testRejectsNonNiosFile(self):
        output = self.runNios("notNiosFile.txt")

        self.assertEqual(output.strip(), "Error: Nios can only read .nios files.")
    # --- end AI code ---