#nios expression grammar
#each rule calls the next one to handle higher priority operators first
#program       -> declaration* EOF ;
#declaration   -> varDecl | statement ;
#varDecl       -> ("let" | "var") LABEL ("=" expression)? ";" ;
#statement     -> showStmt | block | expressionStmt ;
#showStmt      -> "show" expression ";" ;
#block         -> "{" declaration* "}" ;
#expressionStmt -> expression ";" ;
#expression -> comma ;
#comma      -> assignment ( "," assignment )* ;
#assignment -> equality ( "=" assignment )? ; only a LABEL can go before "="
#equality   -> comparison ( ("==" | "!=") comparison )* ;
#comparison -> term ( (">" | ">=" | "<" | "<=") term )* ;
#term       -> factor ( ("+" | "-") factor )* ;
#factor     -> unary ( ("*" | "/") unary )* ;
#unary      -> ("!" | "-") unary | primary ;
#primary    -> NUMBER | WORD | LABEL | "true" | "false" | "nil"
#            | "(" expression ")" ;

#operators at the same binary level group from left to right, like (8 - 3) - 1

from expression import Assign, Binary, Group, Literal, Unary, Variable
from statement import BlockStatement, ExpressionStatement, ShowStatement, VarStatement

class ParseError(Exception):
    #separate error type so we can catch parser errors in main
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.errors = []


    def parse(self):
        return self.parseStatements()

    def parseStatements(self, inBlock=False):
        statements = []

        while not self.isAtEnd():
            if self.checkSymbols("RIGHT_BRACE"):
                if inBlock:
                    break
                self.errors.append(str(self.error("Unmatched '}'.")))
                self.advance()
                continue

            try:
                statements.append(self.declaration())
            except ParseError as error:
                self.errors.append(str(error))
                self.fallbackMode()

        return statements

    def fallbackMode(self):
        while not self.isAtEnd():
            token = self.peek()

            #leave braces for the statement loop so recovery doesn't change the scope
            if self.checkSymbols("LEFT_BRACE", "RIGHT_BRACE"):
                return

            if token.type == "KEYWORD" and token.keyword in ("SHOW", "LET", "VAR"):
                return

            self.advance()

            if token.type == "SYMBOL" and token.symbol == "SEMICOLON":
                return

    def declaration(self):
        token = self.peek()
        if token.type == "KEYWORD" and token.keyword in ("LET", "VAR"):
            self.advance()
            return self.varDeclaration()
        return self.statement()

    def varDeclaration(self):
        if self.peek().type != "LABEL":
            raise self.error("Expected a variable name.")
        name = self.advance()

        initializer = None
        if self.matchSymbols("EQUAL"):
            initializer = self.expression()

        if not self.matchSymbols("SEMICOLON"):
            raise self.error("Expected ';' after variable declaration.")
        return VarStatement(name, initializer)

    def statement(self):
        token = self.peek()

        if token.type == "KEYWORD" and token.keyword == "SHOW":
            self.advance()
            return self.showStatement()

        if self.matchSymbols("LEFT_BRACE"):
            statements = self.parseStatements(inBlock=True)
            if not self.matchSymbols("RIGHT_BRACE"):
                raise self.error("Expected '}' to close block.")
            return BlockStatement(statements)

        return self.expressionStatement()

    def showStatement(self):
        expression = self.expression()

        if not self.matchSymbols("SEMICOLON"):
            raise self.error("Expected ';' after SHOW statement.")

        return ShowStatement(expression)

    def expressionStatement(self):
        expression = self.expression()

        if not self.matchSymbols("SEMICOLON"):
            raise self.error("Expected ';' after expression.")

        return ExpressionStatement(expression)



    def expression(self):
        #comma has the lowest priority
        return self.comma()


    def comma(self):
        expression = self.assignment()

        #keep combining from the left so 1, 2, 3 becomes (, (, 1 2) 3)
        while self.matchSymbols("COMMA"):
            operator = self.previous()
            right = self.assignment()
            expression = Binary(expression, operator, right)
        return expression


    def assignment(self):
        expression = self.equality()
        if self.matchSymbols("EQUAL"):
            operator = self.previous()
            #recurse on the right so a = b = 3 assigns b before a
            value = self.assignment()
            if not isinstance(expression, Variable):
                raise self.error("Invalid assignment target.", operator)
            return Assign(expression.name, value)
        return expression


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

        if token.type == "LABEL":
            return Variable(self.advance())

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
            "COMMA", "PLUS", "STAR", "SLASH", "EQUAL_EQUAL", "BANG_EQUAL",
            "GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"
        ):
            raise self.error(f"Missing left operand before {repr(token.raw)}.")

        #catch anything that can't start an expression, including EOF if an operand is missing
        raise self.error("Expected an expression.")


    def matchSymbols(self, *symbolTypes):
        if self.checkSymbols(*symbolTypes):
            self.advance()
            return True
        return False


    def checkSymbols(self, *symbolTypes):
        token = self.peek()
        return token.type == "SYMBOL" and token.symbol in symbolTypes


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


    def error(self, message, token=None):
        if token is None:
            token = self.peek()

        #EOF has no text, so say end of input instead
        if token.type == "EOF":
            location = "end of input"
        else:
            location = repr(token.raw)

        return ParseError(f"[line {token.lineNumber}] Error at {location}: {message}")