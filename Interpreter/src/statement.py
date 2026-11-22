class Statement:
    pass


class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression


class ShowStatement(Statement):
    def __init__(self, expression):
        self.expression = expression


class LetStatement(Statement):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer


class BlockStatement(Statement):
    def __init__(self, statements):
        self.statements = statements