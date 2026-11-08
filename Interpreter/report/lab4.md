# Dante Givens - CIS 343 01 - 11/06/26

## Nios - Lab 4 Statements Report

## Automated Testing

The Lab 4 automated tests are AI-generated and exercise statement parsing and
execution through the command-line interpreter. They cover the required valid
and invalid inputs, silent expression statements, printed literals and operators,
semicolon enforcement, panic-mode recovery, EOF and progress checks, runtime and
scanner errors, REPL recovery, and the `-p`, `-s`, and `-a` modes.

From the repository root, run just Lab 4:

```powershell
python -B Interpreter\test\lab4\runAllUnitTests.py
```

Run all current lab suites and the shared end-to-end tests:

```powershell
python -B Interpreter\test\runAllUnitTests.py
```

The all-tests runner discovers Lab 4 automatically and returns a nonzero exit
status if any suite fails. It retains the existing Lab 1 skip because those tests
expect the old detailed scanner output. Lab 2 AST tests remain unchanged; Lab 3
tests now use semicolon-terminated statements and explicit `show` for output.

Recovery tests verify that later valid statements appear in parser-only output.
Normal execution is blocked if the program contains any syntax errors.