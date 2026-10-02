import sys
from scanner import Scanner

def main():
    #remove 1 since 0 is the program itself
    arg_count = len(sys.argv) - 1

    if arg_count == 0:
        print("REPL mode")
        try:
            #loop always getting user input
            while True:
                userInput = input()
                scanSource(userInput)

        #exit the program with Ctrl + C
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

    elif arg_count == 1:
        #try to look for a file by the name of the second Arg
        fileName = sys.argv[1]
        scanFile(fileName)

    elif arg_count > 1:
        print("Error: too many args")
        print("Correct usage of nios: python src/nios.py file.nios")


def scanSource(source):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    for token in tokens:
        print(token)

    for error in scanner.errors:
        print(error)


def scanFile(inputFile):
    if not inputFile.endswith(".nios"):
        print("Error: Nios can only read .nios files.")
        return

    try:
        with open(inputFile, "r") as file:
            content = file.read()
            scanSource(content)
    except FileNotFoundError:
        print("Error: That file does not exist, please check your file path.")

#run main
if __name__ == "__main__":
    main()
