class Token:
    def __init__(self, lineNumber, type, raw="", literal=None):
        self.lineNumber = lineNumber
        self.type = type
        self.raw = raw
        self.literal = literal

    def getLineNumber(self):
        return f"This is at line: {self.lineNumber}."

    def getType(self):
        return f"{self.type}"

    def __str__(self):
        return f"{self.type} raw={repr(self.raw)} literal={repr(self.literal)} line={self.lineNumber}"

    def showError(error):
        print(error)


class Number(Token):
    def __init__(self, lineNumber, value):
        self.type = "NUMBER"
        raw = str(value)
        if "." in raw:
            self.value = float(raw)
        else:
            self.value = int(raw)
        super().__init__(lineNumber, self.type, raw, self.value)


class Word(Token):
    def __init__(self, lineNumber, raw, value=None):
        self.type = "WORD"
        if value is None:
            value = raw
        super().__init__(lineNumber, self.type, raw, value)
        self.value = value


class Label(Token):
    def __init__(self, lineNumber, value):
        self.type = "LABEL"
        super().__init__(lineNumber, self.type, value, None)
        self.value = value


class Keyword(Token):
    def __init__(self, lineNumber, value, literal=None):
        self.type = "KEYWORD"
        self.keyword = value.upper()
        super().__init__(lineNumber, self.type, value, literal)
        self.value = value


class Symbol(Token):
    def __init__(self, lineNumber, value, symbolType=None):
        self.type = "SYMBOL"
        if symbolType is None:
            symbolType = value
        self.symbol = symbolType
        super().__init__(lineNumber, self.type, value, None)
        self.value = value