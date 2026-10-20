from astPrinter import AstPrinter
from expression import Binary, Group, Literal, Unary


class EvaluationError(Exception):
    #lets nios print evaluation errors without a Python traceback
    pass


def is_truthy(value):
    #nil, false, and zero are false; other values are true
    return value is not None and value != 0


class Evaluator:
    def __init__(self, on_step=None):
        self.on_step = on_step


    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, Group):
            return self.evaluate(expression.expression)

        if isinstance(expression, Unary):
            operand = self.evaluate(expression.operand)
            operator = expression.operator
            if operator.symbol == "BANG":
                value = not is_truthy(operand)
            elif operator.symbol == "MINUS":
                if not isinstance(operand, (int, float)):
                    raise self.error(operator, "Operand must be a number.")
                value = -operand
            else:
                raise self.error(operator, "Unsupported operator.")

        elif isinstance(expression, Binary):
            #post order: finish both sides before applying this operator
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)
            operator = expression.operator
            symbol = operator.symbol

            if symbol == "COMMA":
                #both sides were evaluated, but comma returns the right side
                value = right
            elif symbol in ("PLUS", "MINUS", "STAR", "SLASH", "GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
                #bool counts as an int in Python, so true works as 1 and false as 0
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise self.error(operator, "Operands must be numbers.")
                if symbol == "PLUS":
                    value = left + right
                elif symbol == "MINUS":
                    value = left - right
                elif symbol == "STAR":
                    value = left * right
                elif symbol == "SLASH":
                    if right == 0:
                        raise self.error(operator, "Division by zero.")
                    value = left / right
                elif symbol == "GREATER":
                    value = left > right
                elif symbol == "GREATER_EQUAL":
                    value = left >= right
                elif symbol == "LESS":
                    value = left < right
                else:
                    value = left <= right
            elif symbol == "EQUAL_EQUAL":
                value = left == right
            elif symbol == "BANG_EQUAL":
                value = left != right
            else:
                raise self.error(operator, "Unsupported operator.")

        else:
            raise EvaluationError("Unsupported expression type.")

        #report the finished node for -a without changing its value or the original tree
        if self.on_step is not None:
            self.on_step(expression, value)
        return value


    def error(self, operator, message):
        return EvaluationError(
            f"[line {operator.lineNumber}] Error at {repr(operator.raw)}: {message}"
        )


class TracePrinter(AstPrinter):
    def __init__(self):
        #remember evaluated nodes separately so the original AST stays intact
        self.reduced = {}


    def print(self, expression):
        if expression in self.reduced:
            value = self.reduced[expression]
            if isinstance(value, float):
                #round only the displayed text, not the number used in later calculations
                text = f"{value:.3f}".rstrip("0").rstrip(".")
            else:
                text = super().print(Literal(value))
            return f"({text})"
        return super().print(expression)