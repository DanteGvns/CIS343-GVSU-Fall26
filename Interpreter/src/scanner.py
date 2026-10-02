from token import Token, Number, Word, Label, Keyword, Symbol


class Scanner:
    # "raw input" : "token type"
    keywords = {
        "and": "AND",
        "else": "ELSE",
        "false": "FALSE",
        "if": "IF",
        "let": "LET",
        "nil": "NIL",
        "or": "OR",
        "show": "SHOW",
        "true": "TRUE",
        "while": "WHILE"
    }

    singleTokens = {
        "(": "LEFT_PAREN",
        ")": "RIGHT_PAREN",
        "{": "LEFT_BRACE",
        "}": "RIGHT_BRACE",
        ",": "COMMA",
        ".": "DOT",
        ";": "SEMICOLON",
        "+": "PLUS",
        "-": "MINUS",
        "*": "STAR"
    }


    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.errors = []
        self.start = 0
        self.current = 0
        self.line = 1


    def scanTokens(self):
        #scan until the end of code
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(self.line, "EOF", "", None))
        return self.tokens


    def scanToken(self):
        #character is what we are currently looking at while self.checkNextForSymbols() checks the next character
        character = self.advance()

        #check for symbol tokens first
        if character in self.singleTokens:
            self.addSymbol(self.singleTokens[character])
        elif character == "!":
            if self.checkNextForSymbols("="):
                self.addSymbol("BANG_EQUAL")
            else:
                self.addSymbol("BANG")
        elif character == "=":
            if self.checkNextForSymbols("="):
                self.addSymbol("EQUAL_EQUAL")
            else:
                self.addSymbol("EQUAL")
        elif character == "<":
            if self.checkNextForSymbols("="):
                self.addSymbol("LESS_EQUAL")
            else:
                self.addSymbol("LESS")
        elif character == ">":
            if self.checkNextForSymbols("="):
                self.addSymbol("GREATER_EQUAL")
            else:
                self.addSymbol("GREATER")
        elif character == "/":
            self.scanSlash()

        #ignore whitespace characters
        elif character in " \r\t":
            return

        #ignore newline characters, but add to the line number for errors
        elif character == "\n":
            self.line += 1

        #scan words(string literals)
        elif character == '"':
            self.scanWord()

        #scan numeric literals
        elif character.isdigit():
            self.scanNumber()

        #scan labels or keywords
        elif character.isalpha() or character == "_":
            self.scanLabelOrKeyword()

        #catch all for things that don't match any known token
        else:
            self.errors.append(f"[line {self.line}] Error: Unexpected character {repr(character)}.")


    #unlike most symbols, we have to scan slashes since they can be the start of comments
    def scanSlash(self):
        #// is the start of a single line comment so check to see if char is a /
        if self.checkNextForSymbols("/"):
            #advance while doing nothing to ignore until the line ends
            while self.peek() != "\n" and not self.isAtEnd():
                self.advance()
        #/* is the start of a block comment so check to see if char is a *
        elif self.checkNextForSymbols("*"):
            #scan the block comment
            self.scanBlockComment()
        #if it's not a comment, it's just a slash symbol
        else:
            self.addSymbol("SLASH")


    #scan block comments, handling nested comments correctly
    def scanBlockComment(self):
        #must remember the line where the block comment incase this is a multi-line block comment that ends up being unterminated
        opening_line = self.line

        #represents layer of nested block comments
        depth = 1

        #keep scanning until we back out of all nested block comment layers or reach the end of the file
        while depth > 0 and not self.isAtEnd():
            #check for the start of a nested block comment
            if self.peek() == "/" and self.peekNext() == "*":
                self.advance()
                self.advance()
                #go a layer deeper
                depth += 1
            #check for the end of a block comment
            elif self.peek() == "*" and self.peekNext() == "/":
                self.advance()
                self.advance()
                #back out a layer
                depth -= 1

            #check for newline characters to update the line number
            elif self.advance() == "\n":
                self.line += 1
        #if we reach here and depth is still greater than 0, it means we have an unterminated block comment
        if depth > 0:
            self.errors.append(f"[line {opening_line}] Error: Unterminated block comment.")


    def scanWord(self):
        #must remember the line since string can be multi-line
        opening_line = self.line

        #keep scanning until we find the closing quote or reach the end of the line/file
        while self.peek() != '"' and self.peek() != "\n" and not self.isAtEnd():
            self.advance()

        #if we reach the end of the line or file without finding a closing quote, it's an unterminated string
        if self.isAtEnd() or self.peek() == "\n":
            self.errors.append(f"[line {opening_line}] Error: Unterminated string.")
            return

        #consume the closing quote
        self.advance() 

        #extract the raw string including quotes and the literal value without quotes
        raw = self.source[self.start:self.current]
        literal = self.source[self.start + 1:self.current - 1]

        #add the string token to the list of tokens
        self.tokens.append(Word(self.line, raw, literal))


    def scanNumber(self):

        #scan until next non-digit character or the end of the file
        while self.peek().isdigit():
            self.advance()
        
        #if next character is a dot and followed by a digit, it's a floating-point number
        if self.peek() == "." and self.peekNext().isdigit():
            #consume the dot only once
            self.advance()
            #keep looking for digits after the dot
            while self.peek().isdigit():
                self.advance()

        #get the value of everything scanned and make the token
        #the Number class will handle floating point vs integer by itself
        raw = self.source[self.start:self.current]
        self.tokens.append(Number(self.line, raw))


    #these are together since they are both full words
    def scanLabelOrKeyword(self):
        #keep scanning until we find a non-alphanumeric character or _ since _ is allowed in labels
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        #check if the raw input is a defined keyword
        raw = self.source[self.start:self.current]
        if raw in self.keywords:
            literal = None

            #determine the literal value for boolean keywords
            if raw == "true":
                literal = True
            elif raw == "false":
                literal = False

            #for other keywords, the literal value remains None
            self.tokens.append(Keyword(self.line, raw, literal))

        else:
            #if it's not a keyword, treat it as a label
            self.tokens.append(Label(self.line, raw))


    def addSymbol(self, symbolType):
        raw = self.source[self.start:self.current]
        self.tokens.append(Symbol(self.line, raw, symbolType))


    def checkNextForSymbols(self, expected):
        #if the next character does not match the expected one or is end do nothing
        if self.isAtEnd() or self.source[self.current] != expected:
            return False
        
        #advance the current position since the next character matches so we'll consumed it
        self.current += 1
        return True


    #check the current character without consuming it
    def peek(self):
        #if we are at the end of the source, return the null character
        if self.isAtEnd():
            return "\0"
        
        #return the character without consuming it
        return self.source[self.current]

    #check the next character without consuming it
    def peekNext(self):
        #if the next character is beyond the end of the source, return the null character
        if self.current + 1 >= len(self.source):
            return "\0"
        
        #return the next character without consuming it
        return self.source[self.current + 1]


    #consume the current character and return it
    def advance(self):
        character = self.source[self.current]
        self.current += 1
        return character


    #check if we have reached the end of the source
    def isAtEnd(self):
        return self.current >= len(self.source)
