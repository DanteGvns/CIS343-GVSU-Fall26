class Statement:
    pass


class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression


class ShowStatement(Statement):
    def __init__(self, expression):
        self.expression = expression