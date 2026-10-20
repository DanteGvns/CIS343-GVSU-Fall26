import sys
from scanner import Scanner
from parser import Parser, ParseError
from astPrinter import AstPrinter
from evaluator import EvaluationError, Evaluator, TracePrinter
from expression import Literal

def main():
    #skip the program name and separate output flags from the file path
    arguments = sys.argv[1:]
    showAst = "-a" in arguments
    parseOnly = "-p" in arguments
    scanOnly = "-s" in arguments
    flags = [argument for argument in arguments if argument in ("-a", "-p", "-s")]
    files = [argument for argument in arguments if argument not in ("-a", "-p", "-s")]

    if len(files) > 1:
        print("Error: too many args")
        print("Correct usage of nios: python src/nios.py file.nios [-a | -p | -s]")
        return

    if len(flags) > 1:
        print("Error: use only one of -a, -p, or -s.")
        return

    if not files:
        print("REPL mode")
        try:
            #loop always getting user input
            while True:
                userInput = input()
                scanSource(userInput, showAst, parseOnly, scanOnly)

        #exit the program with Ctrl + C
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

    else:
        scanFile(files[0], showAst, parseOnly, scanOnly)


def scanSource(source, showAst=False, parseOnly=False, scanOnly=False):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    #don't parse if the scanner found errors
    if scanner.errors:
        for error in scanner.errors:
            print(error)
        return

    #scanner mode shows token types even when the expression would not parse
    if scanOnly:
        printTokens(tokens)
        return

    try:
        parser = Parser(tokens)
        expression = parser.parse()
    except ParseError as error:
        print(error)
        return

    #parser mode shows the tree without evaluating it
    if parseOnly:
        print(AstPrinter().print(expression))
        return

    #show the starting expression and tree before evaluating anything
    if showAst:
        print(source.strip())
        print(AstPrinter().print(expression))
        trace = TracePrinter()

        def show_step(node, value):
            trace.reduced[node] = value
            #the root is the final answer, so don't print it twice
            if node is not expression:
                print(trace.print(expression))

        evaluator = Evaluator(on_step=show_step)
    else:
        evaluator = Evaluator()

    try:
        result = evaluator.evaluate(expression)
        #keep nil and quoted words in Nios format, but print booleans as True or False
        if result is None or isinstance(result, str):
            print(AstPrinter().print(Literal(result)))
        else:
            print(result)
    except EvaluationError as error:
        print(error)


def scanFile(inputFile, showAst=False, parseOnly=False, scanOnly=False):
    if not inputFile.endswith(".nios"):
        print("Error: Nios can only read .nios files.")
        return

    try:
        #match the test files so characters like superscript two are read correctly
        with open(inputFile, "r", encoding="utf-8") as file:
            content = file.read()
            scanSource(content, showAst, parseOnly, scanOnly)
    except FileNotFoundError:
        print("Error: That file does not exist, please check your file path.")


def printTokens(tokens):
    shortNames = {
        "NUMBER": "NUM",
        "PLUS": "ADD",
        "MINUS": "SUB",
        "STAR": "MUL",
        "SLASH": "DIV",
        "EQUAL_EQUAL": "EQ",
        "BANG_EQUAL": "NE",
        "LESS": "LT",
        "LESS_EQUAL": "LE",
        "GREATER": "GT",
        "GREATER_EQUAL": "GE",
        "BANG": "NOT"
    }
    names = []
    for token in tokens:
        #EOF is only a marker for the parser, not part of the source
        if token.type == "EOF":
            continue
        if token.type == "SYMBOL":
            name = token.symbol
        elif token.type == "KEYWORD":
            name = token.keyword
        else:
            name = token.type
        names.append(shortNames.get(name, name))
    print(" ".join(names))

#run main
if __name__ == "__main__":
    main()
