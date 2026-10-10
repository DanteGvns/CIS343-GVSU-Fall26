class Expression:
    """Base type shared by every expression node."""
    pass


class Literal(Expression):
    #literals are already complete values, so they have no child nodes
    def __init__(self, value):
        self.value = value


class Unary(Expression):
    #a unary expression has one operator and one operand
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand


class Binary(Expression):
    #left and right can be any expression, including another Binary
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Group(Expression):
    #keep grouping in the tree so the printer can show the hierarchy
    def __init__(self, expression):
        self.expression = expression
