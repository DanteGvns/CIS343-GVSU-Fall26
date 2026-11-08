# Dante Givens - CIS 343 01 - 11/08/26

## Nios - Lab 4 Statements Report

## Statements

For this lab I added expression statements and print statements to Nios. My language uses `show` instead of `print`. Before this change, the interpreter read one expression and automatically printed its result. Now it reads a list of statements and only prints a value when the statement uses `show`.

For example, `2 + 2;` calculates the result but does not print anything. `show 2 + 2;` calculates the same expression and prints `4`. Both statements need a semicolon, including in the REPL.

### Statement Grammar

```text
statement      -> showStmt | expressionStmt ;
showStmt       -> "show" expression ";" ;
expressionStmt -> expression ";" ;
```

The expression rules from the previous lab are still used inside each statement. Precedence, grouping, unary operators, comparisons, and the comma operator still work the same way.

### AST and Execution

I added `ExpressionStatement` and `ShowStatement` in [statement.py](../src/statement.py). Both store an expression, but the class tells the evaluator what to do with it.

- `ExpressionStatement` evaluates its expression and discards the result.
- `ShowStatement` evaluates its expression and prints the result.

In [parser.py](../src/parser.py), `parse()` now loops until EOF and returns a list of statements. `statement()` checks for the `show` keyword. If it is not there, the parser tries an expression statement. Each statement method checks for its ending semicolon.

In [evaluator.py](../src/evaluator.py), `execute()` handles the statement types and reuses `evaluate()` for the expression inside them. Words print directly without the surrounding quotes, so `show "test";` prints `test`. Spaces and newlines inside a word are preserved. Other values reuse the AST printer's literal formatting, so booleans print as `true` or `false`, and `nil` prints as `nil`.

The main program, [nios.py](../src/nios.py), processes the statement list instead of automatically printing each expression's result. I also updated [astPrinter.py](../src/astPrinter.py) to support the new statement nodes.

I reused the [scanner](../src/scanner.py), [token classes](../src/token.py), and [expression classes](../src/expression.py). The scanner already recognized `show` and semicolons.

<br>

## Panic-Mode Error Recovery

Before this lab, a syntax error stopped parsing the input. I changed the statement loop so each statement has its own `try` and `except ParseError`. If a statement fails, the parser saves the error message in `parser.errors` and calls `fallbackMode()`.

`fallbackMode()` skips tokens until it finds a place to resume:

- If it reaches a semicolon, it consumes it and returns.
- If it reaches `show`, it returns without consuming that keyword.
- If it reaches EOF, it stops.

Leaving `show` unconsumed matters when the previous statement is missing a semicolon. Otherwise, recovery could skip the beginning of the next valid statement. The next call to `statement()` consumes `show` normally.

The parser then continues through the rest of the input. Only successfully parsed statements are added to the statement list. The main program prints all collected syntax errors in order.

I kept parsing and execution separate. If the program has syntax errors, the interpreter reports them without executing any of its statements. Recovery lets the parser check the rest of the input without running a partially valid program.

<br>

## Dependencies and Setup

Nios uses Python and does not need any third-party packages. These results were checked with Python 3.15.0 on Windows.

From the repository root, enter the interpreter folder:

```powershell
cd Interpreter
```

All commands below are run from that folder.

Run a source file:

```powershell
python src\nios.py test\lab4\statements.nios
```

Run the REPL:

```powershell
python src\nios.py
```

REPL mode processes one line at a time, and can be exited with `Ctrl+C`. 

<br>

## Required Test Cases

These are the two inputs from the assignment, using `show` as the Nios equivalent of `print`. The outputs below are the actual results.

### Test 1: Invalid Statements

Input: [requiredErrors.nios](../test/lab4/requiredErrors.nios)

```text
"one"
true;
show 2 +
```

Run:

```powershell
python src\nios.py test\lab4\requiredErrors.nios
```

Actual output:

```text
[line 2] Error at 'true': Expected ';' after expression.
[line 4] Error at end of input: Expected an expression.
```

The first error happens because `"one"` is missing a semicolon. The parser notices this when it reaches `true`. Recovery skips through `true;` and then resumes at `show`. The second error happens because `show 2 +` is missing its right operand. EOF is reported on line 4 because the file has a newline after the last line.

**Result:** Both errors are reported in one run, so the first syntax error does not stop the parser from reaching the later statement.

### Test 2: Valid Statements

Input: [statements.nios](../test/lab4/statements.nios)

```text
4 + 2;
show "one";
show true;
show 1 + 2;
show nil;
```

Run:

```powershell
python src\nios.py test\lab4\statements.nios
```

Actual output:

```text
one
true
3
nil
```

**Result:** The four `show` statements print their values. There is no `6` in the output because `4 + 2;` is an expression statement and its result is discarded.

<br>

## Additional Recovery Tests

### Recovering After a Semicolon

Input: [recovery.nios](../test/lab4/recovery.nios)

```text
show 1 + ;
show 2;
3 + ;
show 4;
```

Run:

```powershell
python src\nios.py test\lab4\recovery.nios
```

Actual output:

```text
[line 1] Error at ';': Expected an expression.
[line 3] Error at ';': Expected an expression.
```

Both incomplete expressions are reported in one run. The error on line 3 shows that parsing continued after the error on line 1. Nothing is executed because the input contains syntax errors.

### Recovering at the Next `show`

Input: [missingSemicolon.nios](../test/lab4/missingSemicolon.nios)

```text
show 1
show 2;
```

Run:

```powershell
python src\nios.py test\lab4\missingSemicolon.nios
```

Actual output:

```text
[line 2] Error at 'show': Expected ';' after SHOW statement.
```

The first statement fails, but recovery leaves the second `show` available for the parser. The second statement is valid and does not add another error. Its value is not printed because the input contains a syntax error.

<br>

## Automated Testing

The Lab 4 automated tests and additional test files were AI-generated. The tests run the command-line interpreter and check its actual output against the expected output.

Run just Lab 4:

```powershell
python test\lab4\runAllUnitTests.py
```

Run all current lab suites and the shared end-to-end tests:

```powershell
python test\runAllUnitTests.py
```

The Lab 4 tests cover:

- The required valid and invalid inputs.
- Silent expression statements and printed values.
- Operators, grouping, multiline input, and statement order.
- Missing semicolons and invalid expressions.
- Recovery at semicolons, at `show`, and at EOF.
- Repeated bad tokens to check that recovery makes progress instead of looping forever.
- Scanner errors, runtime errors, and recovery between REPL inputs.

<br>

## Limitations

- Strings need quotes. Variable lookup and assignment are not implemented.
- Multiplication needs `*`; an expression like `1(2 + 3)` is not supported.
- The `+` operator currently requires numbers, so `"yes" + 12` is an error.
- Panic-mode recovery handles parser errors. Scanner errors still stop processing before parsing begins.
- A runtime error stops execution of the remaining statements in that input.
- Recovery skips damaged input; it does not repair it or guarantee that every intended statement is preserved.
