import json

from expression import Assign, Binary, Group, Literal, Unary, Variable
from statement import ExpressionStatement, ShowStatement, VarStatement

class AstPrinter:
    def print(self, expression):
        if isinstance(expression, ExpressionStatement):
            return self.parenthesize("expr", expression.expression)

        if isinstance(expression, ShowStatement):
            return self.parenthesize("show", expression.expression)

        if isinstance(expression, VarStatement):
            name = "var " + expression.name.raw
            if expression.initializer is None:
                return self.parenthesize(name)
            return self.parenthesize(name, expression.initializer)

        if isinstance(expression, Variable):
            return expression.name.raw

        if isinstance(expression, Assign):
            return self.parenthesize("= " + expression.name.raw, expression.value)

        #use the operator text instead of the full token output
        if isinstance(expression, Binary):
            return self.parenthesize(
                expression.operator.raw, expression.left, expression.right
            )

        if isinstance(expression, Unary):
            return self.parenthesize(expression.operator.raw, expression.operand)

        if isinstance(expression, Group):
            return self.parenthesize("group", expression.expression)

        if isinstance(expression, Literal):
            value = expression.value

            #use the Nios names instead of Python's None, True, and False
            if value is None:
                return "nil"

            #check bool first since Python also treats it as a number
            if isinstance(value, bool):
                return "true" if value else "false"

            if isinstance(value, (int, float)):
                return str(value)

            if isinstance(value, str):
                #keep quotes around words and show newlines without breaking the output
                return json.dumps(value)

            raise TypeError("Unsupported literal type.")

        raise TypeError("Unsupported expression type.")


    def parenthesize(self, name, *expressions):
        parts = [name]

        #print each child first so nested expressions keep their parentheses
        for expression in expressions:
            parts.append(self.print(expression))

        return "(" + " ".join(parts) + ")"
