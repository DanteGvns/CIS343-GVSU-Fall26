# --- start AI code --
import sys
import unittest
from pathlib import Path


LAB2_FOLDER = Path(__file__).resolve().parents[1]
INTERPRETER_FOLDER = Path(__file__).resolve().parents[3]
SOURCE_FOLDER = INTERPRETER_FOLDER / "src"
sys.path.insert(0, str(SOURCE_FOLDER))
sys.path.insert(0, str(INTERPRETER_FOLDER))
sys.path.insert(0, str(LAB2_FOLDER))

from astPrinter import AstPrinter
from expression import Binary, Expression, Group, Literal, Unary
from src.token import Symbol
from testFiles.astExamples import getExamples


class AstTestCase(unittest.TestCase):
    def testExampleOutputs(self):
        printer = AstPrinter()
        for name, expression, expected in getExamples():
            with self.subTest(example=name):
                actual = printer.print(expression)
                self.assertEqual(actual, expected)


    def testNodeFields(self):
        number = Literal(123)
        minus = Symbol(1, "-", "MINUS")
        negative = Unary(minus, number)
        decimal = Literal(45.67)
        group = Group(decimal)
        star = Symbol(1, "*", "STAR")
        expression = Binary(negative, star, group)

        self.assertEqual(number.value, 123)
        self.assertEqual(decimal.value, 45.67)
        self.assertIs(negative.operator, minus)
        self.assertIs(negative.operand, number)
        self.assertIs(group.expression, decimal)
        self.assertIs(expression.left, negative)
        self.assertIs(expression.operator, star)
        self.assertIs(expression.right, group)
        self.assertEqual(star.raw, "*")
        self.assertEqual(star.lineNumber, 1)
        for node in (number, negative, group, expression):
            self.assertIsInstance(node, Expression)


    def testLiteralTypes(self):
        for value in (123, 45.67, "hello", True, False, None):
            with self.subTest(value=value):
                expression = Literal(value)
                self.assertIs(expression.value, value)
                self.assertIs(type(expression.value), type(value))


    def testPrintingDoesNotChangeTree(self):
        printer = AstPrinter()
        expression = getExamples()[1][1]
        nodes = (
            expression,
            expression.left,
            expression.left.operand,
            expression.left.operator,
            expression.operator,
            expression.right,
            expression.right.expression,
        )
        fields = [vars(node).copy() for node in nodes]

        self.assertEqual(printer.print(expression), "(* (- 123) (group 45.67))")
        self.assertEqual(printer.print(expression), "(* (- 123) (group 45.67))")
        for node, original in zip(nodes, fields):
            self.assertEqual(vars(node), original)
            for name, value in original.items():
                self.assertIs(getattr(node, name), value)


    def testUnsupportedExpression(self):
        with self.assertRaisesRegex(TypeError, "Unsupported expression type"):
            AstPrinter().print(Expression())


    def testUnsupportedLiteral(self):
        with self.assertRaisesRegex(TypeError, "Unsupported literal type"):
            AstPrinter().print(Literal([]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
# --- end AI code --