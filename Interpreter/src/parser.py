#nios expression grammar
#each rule calls the next one to handle higher priority operators first
#expression -> equality ;
#equality   -> comparison ( ("==" | "!=") comparison )* ;
#comparison -> term ( (">" | ">=" | "<" | "<=") term )* ;
#term       -> factor ( ("+" | "-") factor )* ;
#factor     -> unary ( ("*" | "/") unary )* ;
#unary      -> ("!" | "-") unary | primary ;
#primary    -> NUMBER | WORD | "true" | "false" | "nil"
#            | "(" expression ")" ;

#operators at the same binary level group from left to right, like (8 - 3) - 1

from expression import Binary, Group, Literal, Unary


class ParseError(Exception):
    #separate error type so we can catch parser errors in main
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0


    def parse(self):
        expression = self.expression()

        #we only want one expression, so there should be nothing left except EOF
        if not self.isAtEnd():
            raise self.error("Unexpected token after expression.")
        return expression


    def expression(self):
        #equality has the lowest priority so just return self
        return self.equality()


    def equality(self):
        expression = self.comparison()

        #keep putting the tree we already made on the left side of the next operator
        while self.matchSymbols("EQUAL_EQUAL", "BANG_EQUAL"):
            operator = self.previous()
            right = self.comparison()
            expression = Binary(expression, operator, right)
        return expression


    def comparison(self):
        #check the math before comparing the two sides
        expression = self.term()
        while self.matchSymbols("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self.previous()
            right = self.term()
            expression = Binary(expression, operator, right)
        return expression


    def term(self):
        #multiplication and division before addition and subtraction
        expression = self.factor()
        while self.matchSymbols("PLUS", "MINUS"):
            operator = self.previous()
            right = self.factor()
            expression = Binary(expression, operator, right)
        return expression


    def factor(self):
        #check for ! or a negative sign before looking for * or /
        expression = self.unary()
        while self.matchSymbols("STAR", "SLASH"):
            operator = self.previous()
            right = self.unary()
            expression = Binary(expression, operator, right)
        return expression


    def unary(self):
        if self.matchSymbols("BANG", "MINUS"):
            operator = self.previous()

            #there could be another unary operator after this one, like !!true
            operand = self.unary()
            return Unary(operator, operand)
        return self.primary()


    def primary(self):
        token = self.peek()

        #scanner already got the value for numbers and words
        if token.type in ("NUMBER", "WORD"):
            self.advance()
            return Literal(token.literal)

        #true, false, and nil have literal values too, but the other keywords don't belong here
        if token.type == "KEYWORD" and token.keyword in ("TRUE", "FALSE", "NIL"):
            self.advance()
            return Literal(token.literal)

        #start over with expression so anything inside parentheses stays together
        if self.matchSymbols("LEFT_PAREN"):
            expression = self.expression()

            #we consumed the opening parenthesis so there must be a closing one
            if not self.matchSymbols("RIGHT_PAREN"):
                raise self.error("Expected ')' after expression.")
            return Group(expression)

        #these operators need something on their left, but - can be unary so leave it out
        if token.type == "SYMBOL" and token.symbol in (
            "PLUS", "STAR", "SLASH", "EQUAL_EQUAL", "BANG_EQUAL",
            "GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"
        ):
            raise self.error(f"Missing left operand before {repr(token.raw)}.")

        #catch anything that can't start an expression, including EOF if an operand is missing
        raise self.error("Expected an expression.")


    def matchSymbols(self, *symbolTypes):
        token = self.peek()

        #type only says SYMBOL, so check symbol to see which operator it actually is
        if token.type == "SYMBOL" and token.symbol in symbolTypes:
            self.advance()
            return True
        return False


    #check the current token without consuming it
    def peek(self):
        return self.tokens[self.current]


    def previous(self):
        return self.tokens[self.current - 1]


    def advance(self):
        token = self.peek()

        #don't move past EOF or we would go outside the token list
        if not self.isAtEnd():
            self.current += 1
        return token


    def isAtEnd(self):
        return self.peek().type == "EOF"


    def error(self, message):
        token = self.peek()

        #EOF has no text, so say end of input instead
        if self.isAtEnd():
            location = "end of input"
        else:
            location = repr(token.raw)

        return ParseError(f"[line {token.lineNumber}] Error at {location}: {message}")