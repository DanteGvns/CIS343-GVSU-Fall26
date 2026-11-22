# Dante Givens - CIS 343 01 - 11/21/26

## Nios - Lab 5 Variable Report

## New Statements

For this lab I added a variable declaration/assignment statement to Nios. My language uses `let` to initialize a variable. When using `let` you can either just initialize the variable with the default value of `nil`, or initialize the variable and assign a value to it. In Nios, to assign a new value to an already initialized variable, you have to drop the `let` keyword and simply do `variableName = newValue`. If you try to assign a value to a variable by using `let`, and that variable has already been initialized with `let` Nios will throw a `Variable already declared in this scope` error.

### New Statement Grammar

```text
program        -> declaration* EOF ;
declaration    -> letDecl | statement ;
letDecl        -> "let" LABEL ("=" expression)? ";" ;
statement      -> showStmt | block | expressionStmt ;
showStmt       -> "show" expression ";" ;
block          -> "{" declaration* "}" ;
expressionStmt -> expression ";" ;
```

In Nios `LABEL` is a variable name, the `?` means the initializer is optional. Both `let count;` and `let count = 2;` are valid declarations. An assignment like `count = 3;` is an expression statement and does not use `let`.

## Block Scope Added

In this lab I've also added blocks and block scope. Nios now uses curly braces `{ }` to group statements into a block. Each block has its own scope, so a variable declared with `let` inside a block is not available outside of it's block. Blocks can also be nested in Nios. Inner blocks can access the variables defined in the outer block, but outer block cannot access the variables defined in the inner blocks. If an inner block declares a variable with the same name as an outer one, the variable will use that new definition inside the inner block, but retain it's original value inside the outer block.

The evaluator maintains a stack of dictionaries, starting with the global scope. When a block starts, the evaluator adds a new dictionary to the stack. When the block ends, that dictionary is removed from the stack even if a runtime error occurs. A `let` declaration adds the name to the current dictionary. Reads and assignments search from the innermost scope outward, so an assignment without `let` updates the nearest variable that already exists.

## Design Choices

- **Declaration:** `let name = value;` declares a variable.
- **Access before declaration:** Declarations take effect when they run, not at the start of the scope. Reading or assigning a name with no visible declaration is a runtime error. A declaration's initializer runs before the new variable is added. For example, `let x = x;` is an error unless there is already a visible `x` in an outer scope.
- **Missing initializer:** `let x;` starts `x` at `nil`. `let x = ;` is an error because the `=` needs an expression after it.
- **Redeclaration:** Declaring the same name twice in one scope is a runtime error. An inner block can declare its own variable with the same name. That variable shadows the outer one until the block ends.
- **Assignment:** `name = expression` updates the nearest visible declaration and returns the assigned value. Only a `LABEL` can go on the left of `=`. Assignment groups from right to left, so `a = b = 9` sets `b` first. Assignment has lower precedence than equality and higher precedence than the comma operator.

The Nios scanner already knew about `let`, labels, `=`, and braces. The parser now uses those tokens for declarations, assignments, and blocks. The new nodes are in expression.py and statement.py.

# Setup

Nios runs on Python and does not need any third-party packages. These examples were run with Python 3.15.0 on Windows 11 using powershell. 

From the repository root enter the `Interpreter` folder, then to run a nios file you call python, then nios, then a .nios file.
For example:
```powershell
cd Interpreter
python src\nios.py test\lab5\variables.nios
python src\nios.py test\lab5\blockScope.nios
```

Run `python src\nios.py` with no file to start REPL mode. Variables stay defined between REPL lines, but a block has to fit on one REPL line.

# Testing

### Declaration, Access, and Assignment
Test File: test\lab5\variables.nios
```text
let count = 2;
show count;
count = count + 3;
show count;
let saved;
show saved;
show saved = count = 9;
show count;
show saved;
```
Run:
```powershell
python src\nios.py test\lab5\variables.nios
```
Output:

```text
2
5
nil
9
9
9
```

`count` starts at `2` and is updated to `5`. `saved` starts at `nil` because it has no initializer. The chained assignment sets both variables to `9` and also returns `9` to `show`.

### Textbook Block Scope Example
Test File: test\lab5\blockScope.nios
```text
let a = "global a";
let b = "global b";
let c = "global c";
{
    let a = "outer a";
    let b = "outer b";
    {
        let a = "inner a";
        show a;
        show b;
        show c;
    }
    show a;
    show b;
    show c;
}
show a;
show b;
show c;
```
Run:
```powershell
python src\nios.py test\lab5\blockScope.nios
```
Output:

```text
inner a
outer b
global c
outer a
outer b
global c
global a
global b
global c
```

This version uses Nios' `let` and `show` in place of the textbook's `var` and `print`. The inner block finds `a` in its own scope, `b` in the enclosing block, and `c` in the global scope. After the inner block ends, the enclosing block finds its own `a` and `b` and still gets `c` from the global scope. After both blocks end, all three reads use the global scope.

## Error Examples

The parser reports syntax errors with line numbers and tries to continue at semicolons, braces, declarations, or `show` statements. If any syntax error was found, normal mode does not run the input. A runtime error stops the rest of the current input, but output from statements that already ran is kept.

### Unmatched Opening Brace
Test File: test\lab5\unmatchedOpen.nios
```text
{
    let count = 1;
```
Run:
```powershell
python src\nios.py test\lab5\unmatchedOpen.nios
```
Output:

```text
[line 3] Error at end of input: Expected '}' to close block.
```

Error Explanation: The file ends before the block is closed.

### Unmatched Closing Brace
Test File: test\lab5\unmatchedClose.nios
```text
}
show 1;
```
Run:
```powershell
python src\nios.py test\lab5\unmatchedClose.nios
```
Output:

```text
[line 1] Error at '}': Unmatched '}'.
```

Error Explanation: The `}` has no opening block, so `show 1;` does not run.

### Invalid Assignment Targets
Test File: test\lab5\invalidTargets.nios
```text
1 = 2;
let name = 3;
(name) = 4;
name + 1 = 5;
```
Run:
```powershell
python src\nios.py test\lab5\invalidTargets.nios
```
Output:

```text
[line 1] Error at '=': Invalid assignment target.
[line 3] Error at '=': Invalid assignment target.
[line 4] Error at '=': Invalid assignment target.
```
Error Explanation: Only a bare variable name can go on the left side of `=`. The literal `1`, the grouped name `(name)`, and the expression `name + 1` are all invalid assignment targets.
### Missing Name, Expression, or Semicolon
Test File: test\lab5\badDeclarations.nios
```text
let 123;
let count = ;
let next = 1
show next;
next = ;
```
Run:
```powershell
python src\nios.py test\lab5\badDeclarations.nios
```
Output:

```text
[line 1] Error at '123': Expected a variable name.
[line 2] Error at ';': Expected an expression.
[line 4] Error at 'show': Expected ';' after variable declaration.
[line 5] Error at ';': Expected an expression.
```

Error Explanation: `123` is a number, not a variable name. `let count = ;` and `next = ;` both need an expression after `=`. `let next = 1` is missing its semicolon, which the parser notices when it reaches `show` on the next line.

### Undefined Variables Before Declaration
Test Input: REPL (enter one line at a time)
```text
show x; let x = 1;
x = 1; let x;
let x = x;
```
Run:
```powershell
python src\nios.py
```
Output:

```text
REPL mode
[line 1] Error at 'x': Undefined variable.
[line 1] Error at 'x': Undefined variable.
[line 1] Error at 'x': Undefined variable.
```

Error Explanation: The first input reads `x` before its declaration. The second tries to assign to `x` before declaring it. The third reads `x` in its own initializer, before the declaration takes effect.

### Undefined Variable After a Block
Test File: test\lab5\scopeErrors.nios
```text
{
    let local = "inside";
    show local;
}
show local;
```
Run:
```powershell
python src\nios.py test\lab5\scopeErrors.nios
```
Output:

```text
inside
[line 5] Error at 'local': Undefined variable.
```

Error Explanation: The first read works because it is inside the block. The second fails because the block's scope is gone.

### Same-Scope Redeclaration
Test File: test\lab5\redeclaration.nios
```text
let count = 1;
let count = 2;
```
Run:
```powershell
python src\nios.py test\lab5\redeclaration.nios
```
Output:

```text
[line 2] Error at 'count': Variable already declared in this scope.
```

Error Explanation: The second `let` tries to declare `count` again in the same scope. To update the existing variable, use `count = 2;` without `let`.

## Automated Testing

The Lab 5 automated tests and additional test files were AI-generated. The tests run Nios with `.nios` files and REPL input, then compare the actual output and error messages with the expected results.

Run just Lab 5:

```powershell
python test\lab5\runAllUnitTests.py
```

Run all current lab suites and the shared end-to-end tests:

```powershell
python test\runAllUnitTests.py
```

The Lab 5 tests cover:

- Declaring variables with `let`, reading and updating them, and defaulting to `nil` without an initializer.
- Chained assignments and assignment precedence.
- Nested block scope, shadowing, and assignment to the nearest visible variable.
- The expected output from the textbook block scope example.
- Syntax errors for unmatched braces, invalid assignment targets, and incomplete declarations.
- Runtime errors for undefined variables and same-scope redeclarations.
- Keeping global variables between REPL inputs and restoring the outer scope after an error inside a block.