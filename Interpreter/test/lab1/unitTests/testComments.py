# --- start AI code ---
from niosTestCase import NiosTestCase


class CommentTests(NiosTestCase):
    def testCommentsAreIgnored(self):
        output = self.runNios("allTokens.nios")

        self.assertNotIn("lineCommentText", output)
        self.assertNotIn("outerCommentText", output)
        self.assertNotIn("nestedCommentText", output)
        self.assertNotIn("stillInsideComment", output)
        self.assertIn("LABEL raw='afterComments'", output)

    def testLineCommentCanEndAtEof(self):
        output = self.runNios("commentAtEnd.nios")

        self.assertEqual(output.strip(), "EOF raw='' literal=None line=1")
    # --- end AI code ---