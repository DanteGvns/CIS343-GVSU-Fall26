# Dante Givens - CIS 343 01 - 10/09/26

## Nios - Lab 2 AST Printer Test Report

## Expression Grammar:

```text
expression  -> literal
             | unary
             | binary
             | grouping ;

literal     -> NUMBER | WORD | "true" | "false" | "nil" ;
grouping    -> "(" expression ")" ;
unary       -> ( "-" | "!" ) expression ;
binary      -> expression operator expression ;
operator    -> "==" | "!=" | "<" | "<=" | ">" | ">="
             | "+" | "-" | "*" | "/" ;
```

## Literal Types:

Nios supports integer and decimal Number literals, Word literals, the Boolean literals `true` and `false`, and `nil`. A Word is the Nios name for a string. The AST stores these as Python integers, floats, strings, Booleans, and `None`. The AST printer changes the Python representations `True`, `False`, and `None` back into the Nios representations `true`, `false`, and `nil`.  
<br>

## Supported Operators:

The unary operators are `-` for negative numbers and `!` for logical negation. The binary arithmetic operators are `+`, `-`, `*`, and `/`. The equality operators are `==` and `!=`. The comparison operators are `<`, `<=`, `>`, and `>=`. Nios reuses the `Symbol` token class from Lab 1 to store operators in the AST.  
<br>

### Design Choices Relative to Lox

- Nios uses the same four expression forms as Lox: Literal, Unary, Binary, and grouping. Nios names its grouping class `Group` instead of `Grouping`.
- The `Expression` class is the common parent. `Literal` stores a value, `Unary` stores an operator and operand, `Binary` stores left and right expressions with an operator, and `Group` stores one expression.
- Nios reuses the `Symbol` token class from Lab 1. The printer uses its raw operator text, such as `*`.
- The printer calls itself on each child expression and adds parentheses so it is easy to see which parts belong together. Instead of adding Lox's Visitor classes, it checks which of the four expression classes it receives.
- Word values are printed inside double quotes. `json.dumps` keeps empty or multiline Words readable without breaking the AST output across lines.
- `and` and `or` are not included in this grammar. This lab constructs trees directly and does not parse or execute expressions.  
<br>

# Dependencies and Setup

The AST printer only requires Python and uses no third-party packages. It was tested with Python 3.15.0 on Windows.

From the repository root, enter the interpreter folder:

```powershell
cd Interpreter
```

The implementation files are `src/expression.py`, `src/astPrinter.py`, and `src/printAst.py`. Automated tests are stored in `test/lab2/unitTests`, and additional hard-coded inputs are stored in `test/lab2/testFiles`. All commands are listed in the Testing section below.  
<br>
<br>

# Testing

### *Please note, the Lab 2 tests and test files are almost entirely AI generated and self reviewed.
<br>

## Run each test manually:

```powershell
python src/printAst.py assignment example
python src/printAst.py operator example
python src/printAst.py literal example
```

## Run all three manual examples:

```powershell
python src/printAst.py
```

## Run all automated tests:

```powershell
python test/lab2/runAllUnitTests.py
```

The test runner discovers tests in `test/lab2/unitTests`. Additional hard-coded AST inputs and expected outputs are stored in `test/lab2/testFiles/astExamples.py`.  
<br>

## Test Cases


### 1 - Assignment Example and Every Expression Class

```powershell
python src/printAst.py assignment example
```

**Purpose:** Verify Literal, Unary, Binary, and Group nodes in one nested AST. This also tests an integer Number, a decimal Number, unary minus, multiplication, and grouping. It reproduces the example required by the assignment.

**Hard-coded AST:**

```python
assignmentExample = Binary(
    Unary(Symbol(1, "-", "MINUS"), Literal(123)),
    Symbol(1, "*", "STAR"),
    Group(Literal(45.67))
)
```

The root is multiplication. Its left child is unary negation of `123`, and its right child groups `45.67`.

**Expected output:**

```text
(* (- 123) (group 45.67))
```

**Actual printer output:**

```text
(* (- 123) (group 45.67))
```

**Result:** Matches expectations.


### 2 - Every Binary Operator

```powershell
python src/printAst.py operator example
```

**Purpose:** Verify every supported binary operator and several layers of nested Binary nodes. Together with Test 1, this tree covers `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `<=`, `>`, and `>=`. Test 1 contains `*`, while this example contains all of the remaining binary operators.

**Hard-coded AST:**

```python
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
```

**Expected output:**

```text
(== (/ (+ 8 4) (- 5 2)) (!= (< 1 2) (> (<= 2 2) (>= 3 3))))
```

**Actual printer output:**

```text
(== (/ (+ 8 4) (- 5 2)) (!= (< 1 2) (> (<= 2 2) (>= 3 3))))
```

**Result:** Matches expectations.


### 3 - Every Remaining Literal Type and Logical Negation

```powershell
python src/printAst.py literal example
```

**Purpose:** Verify the Word, Boolean, and nil literal types, unary `!`, equality, inequality, and nested expressions. Numbers were tested in Tests 1 and 2. This confirms that Python values are printed using Nios spelling.

**Hard-coded AST:**

```python
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
```

**Expected output:**

```text
(== (! false) (!= true (== "hello world" nil)))
```

**Actual printer output:**

```text
(== (! false) (!= true (== "hello world" nil)))
```

**Result:** Matches expectations.


### Additional Automated Tests

The automated tests also verify the lecture-slide hierarchy, empty and multiline Words, nested grouping, left- and right-nested subtraction, stored node fields and types, repeated printing without changing the AST, and errors for unsupported expressions or literal values. All of these checks passed.  
<br>


# Automated Test Result

Command:

```powershell
python test/lab2/runAllUnitTests.py
```

Result on October 9, 2026:

```text
testExampleOutputs (testAstPrinter.AstTestCase.testExampleOutputs) ... ok
testLiteralTypes (testAstPrinter.AstTestCase.testLiteralTypes) ... ok
testNodeFields (testAstPrinter.AstTestCase.testNodeFields) ... ok
testPrintingDoesNotChangeTree (testAstPrinter.AstTestCase.testPrintingDoesNotChangeTree) ... ok
testUnsupportedExpression (testAstPrinter.AstTestCase.testUnsupportedExpression) ... ok
testUnsupportedLiteral (testAstPrinter.AstTestCase.testUnsupportedLiteral) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.003s

OK
```

All six Lab 2 automated tests passed.

## Known Limitations

- This lab constructs ASTs directly in Python. It does not parse `.nios` files yet.
- The AST printer represents expressions but does not evaluate them.
- The expression grammar does not define precedence or associativity because parsing wasn't needed for this lab.
- Expression constructors assume that their operands and child nodes are valid. They do not perform runtime grammar validation.
- `src/printAst.py` must be run from the `Interpreter` folder so its sibling imports resolve correctly.