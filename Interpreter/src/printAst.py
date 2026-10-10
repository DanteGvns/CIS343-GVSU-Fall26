import sys

from astPrinter import AstPrinter
from expression import Binary, Group, Literal, Unary
from token import Symbol



def getExamples():
    #example from the slides
    assignmentExample = Binary(
        Unary(Symbol(1, "-", "MINUS"), Literal(123)),
        Symbol(1, "*", "STAR"),
        Group(Literal(45.67))
    )

    #nested example containing the rest of the binary operators
    operatorExample = Binary(
        Binary(
            Binary(Literal(8), Symbol(1, "+", "PLUS"), Literal(4)),
            Symbol(1, "/", "SLASH"),
            Binary(Literal(5), Symbol(1, "-", "MINUS"), Literal(2))
        ),
        Symbol(1, "==", "EQUAL_EQUAL"),
        Binary(
            Binary(Literal(1), Symbol(1, "<", "LESS"), Literal(2)),
            Symbol(1, "!=", "BANG_EQUAL"),
            Binary(
                Binary(Literal(2), Symbol(1, "<=", "LESS_EQUAL"), Literal(2)),
                Symbol(1, ">", "GREATER"),
                Binary(Literal(3), Symbol(1, ">=", "GREATER_EQUAL"), Literal(3))
            )
        )
    )

    #word, boolean, and nil literals with logical negation
    literalExample = Binary(
        Unary(Symbol(1, "!", "BANG"), Literal(False)),
        Symbol(1, "==", "EQUAL_EQUAL"),
        Binary(
            Literal(True),
            Symbol(1, "!=", "BANG_EQUAL"),
            Binary(
                Literal("hello world"),
                Symbol(1, "==", "EQUAL_EQUAL"),
                Literal(None)
            )
        )
    )

    return {
        "assignment example": assignmentExample,
        "operator example": operatorExample,
        "literal example": literalExample
    }


def main():
    examples = getExamples()
    printer = AstPrinter()

    #print all three examples when no name is given
    if len(sys.argv) == 1:
        for expression in examples.values():
            print(printer.print(expression))
        return

    requestedName = " ".join(sys.argv[1:]).lower()

    if requestedName == "--list":
        for name in examples:
            print(name)
        return

    if requestedName in examples:
        print(printer.print(examples[requestedName]))
        return

    print(f"Error: No AST example named {requestedName!r}.")
    print("Use --list to see the available example names.")
    sys.exit(1)


if __name__ == "__main__":
    main()
