# Dante Givens - Lab 1 Scanner Test Report - CIS 343 01 - 10/02/26

## My language is named Nios.

## Regular expressions:
Number literal (Number): `[0-9]+(\.[0-9]+)?`  
String literal (Word): `"[^"]*"`  
Identifier (Label): `[A-Za-z_][A-Za-z0-9_]*`  
<br>

## in Nios a string literal is the "Word" token.  
Strings are surrounded by double quotes. The raw input includes the quotes, while the literal value does not. Strings can continue across lines in source files but do not currently support escape sequences.  
<br>

## identifiers are the "Label" tokens.  
Identifiers may begin with a letter or underscore. Later characters may also be digits. After scanning an identifier, the scanner checks whether it is one of these case-sensitive keywords: `and`, `else`, `false`, `if`, `let`, `nil`, `or`, `show`, `true`, or `while`.  
<br>

## "Number" tokens are ints or floats.  
A decimal point is included in a number only when at least one digit follows it.  
For example, `3.14` is one number token, while `12.` is a number token followed by a dot token.  
<br>

## White space rules:
Spaces, carriage returns, and tabs are ignored. Newlines are ignored as tokens but increase the line number. 

## Optional Extra Credit: Nested Block Comments

**Feature and effort:** Nios supports nested `/* ... */` block comments by tracking comment depth. The depth increases for each inner `/*` and decreases for each `*/`; scanning resumes only when it returns to zero. The scanner also tracks newlines and reports the outer comment's opening line if EOF is reached first.

**Value:** Code already containing block comments can now easily be commented out.

**Test evidence:** `unit test: testCommentsAreIgnored` verifies that the nested comment in `allTokens.nios` is skipped and scanning resumes.
`unit test: testEveryLexicalErrorFromFile` verifies that the unterminated block comment in `errorTest.nios` reports an error. Please see the Test section later in the report for more about these tests.

### Design Choices Relative to Lox

- Nios uses a character by character scanner design like Lox.
- Nios uses `let` instead of Lox's `var` and `show` instead of Lox's `print`.
- Nios groups tokens into object-oriented classes: `Number`, `Word`, `Label`, `Keyword`, and `Symbol`.
- Nios calls string tokens `Word` and identifier tokens `Label`.
- Symbols retain both a broad `SYMBOL` category and a specific type such as `PLUS` or `GREATER_EQUAL`.
- Like Lox, a decimal point becomes part of a number only when followed by a digit.
- Like the Lox scanner, Nios Word tokens/strings can span multiple lines.
- Nios adds nested block comments in addition to line comments.
- The scanner collects lexical errors and prints them after the tokens instead of stopping at the first error.  
<br>

### - The interpreter will only run .nios files  
<br>

# Dependencies and Setup

The scanner only requires Python and uses no third-party packages. It was tested with Python 3.14 on Windows.

From the repository root, enter the interpreter folder:
```
cd Interpreter
```

Run the scanner with a source file:
```
python src/nios.py test/lab1/testFiles/allTokens.nios
```

Run interactive mode without a file argument:
```
python src/nios.py
```

Exit interactive mode with `Ctrl+C` or `Ctrl+Z` followed by Enter on Windows.  
<br>
<br>

# Testing
### *Please note, the tests in test\unitTests are almost enitrely AI generated and self reviewed
### *The test files in test\testFiles are also almost enitrely AI generated and self reviewed  
<br>

## Run one test manually:
```
python src/nios.py test/lab1/testFiles/"FileName".nios
```

## Run all automated tests:
```
python test/lab1/runAllUnitTests.py
```

The test runner discovers the tests in `test/lab1/unitTests`. Test source files are stored in `test/lab1/testFiles`.  
<br>

## Test Cases


### 1 - Every Supported Token Type &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Automated Test Name: `testEveryTokenTypeFromFile`

```
python src/nios.py test/lab1/testFiles/allTokens.nios
```

**Purpose:** Verify every supported keyword, identifier form, number, string, operator, punctuation token, comment form, and EOF. It also checks case sensitivity, an identifier beginning with a keyword, an empty string, a trailing decimal point, and symbols inside a string.

**Source input (`allTokens.nios`):**

```nios
and else false if let nil or show true while
identifier _private label123 anderson True _
0 42 3.14 12.
"" "hello world" "! @ 123"
( ) { } , . ;
+ - * /
! != = == < <= > >=
// lineCommentText @ "ignored"
/* outerCommentText
	/* nestedCommentText */
	stillInsideComment
*/
afterComments
```

**Expected:** Every keyword and symbol receives its specific token type. Identifiers remain labels, numbers have numeric literal values, strings have values without quotes, comments produce no tokens, and scanning ends with EOF.

**Actual scanner output:**

```text
KEYWORD(AND) raw='and' literal=None line=1
KEYWORD(ELSE) raw='else' literal=None line=1
KEYWORD(FALSE) raw='false' literal=False line=1
KEYWORD(IF) raw='if' literal=None line=1
KEYWORD(LET) raw='let' literal=None line=1
KEYWORD(NIL) raw='nil' literal=None line=1
KEYWORD(OR) raw='or' literal=None line=1
KEYWORD(SHOW) raw='show' literal=None line=1
KEYWORD(TRUE) raw='true' literal=True line=1
KEYWORD(WHILE) raw='while' literal=None line=1
LABEL raw='identifier' literal=None line=2
LABEL raw='_private' literal=None line=2
LABEL raw='label123' literal=None line=2
LABEL raw='anderson' literal=None line=2
LABEL raw='True' literal=None line=2
LABEL raw='_' literal=None line=2
NUMBER raw='0' literal=0 line=3
NUMBER raw='42' literal=42 line=3
NUMBER raw='3.14' literal=3.14 line=3
NUMBER raw='12' literal=12 line=3
SYMBOL(DOT) raw='.' literal=None line=3
WORD raw='""' literal='' line=4
WORD raw='"hello world"' literal='hello world' line=4
WORD raw='"! @ 123"' literal='! @ 123' line=4
SYMBOL(LEFT_PAREN) raw='(' literal=None line=5
SYMBOL(RIGHT_PAREN) raw=')' literal=None line=5
SYMBOL(LEFT_BRACE) raw='{' literal=None line=5
SYMBOL(RIGHT_BRACE) raw='}' literal=None line=5
SYMBOL(COMMA) raw=',' literal=None line=5
SYMBOL(DOT) raw='.' literal=None line=5
SYMBOL(SEMICOLON) raw=';' literal=None line=5
SYMBOL(PLUS) raw='+' literal=None line=6
SYMBOL(MINUS) raw='-' literal=None line=6
SYMBOL(STAR) raw='*' literal=None line=6
SYMBOL(SLASH) raw='/' literal=None line=6
SYMBOL(BANG) raw='!' literal=None line=7
SYMBOL(BANG_EQUAL) raw='!=' literal=None line=7
SYMBOL(EQUAL) raw='=' literal=None line=7
SYMBOL(EQUAL_EQUAL) raw='==' literal=None line=7
SYMBOL(LESS) raw='<' literal=None line=7
SYMBOL(LESS_EQUAL) raw='<=' literal=None line=7
SYMBOL(GREATER) raw='>' literal=None line=7
SYMBOL(GREATER_EQUAL) raw='>=' literal=None line=7
LABEL raw='afterComments' literal=None line=13
EOF raw='' literal=None line=13
```

**Result:** Matches expectations.

### 2 - Comments Are Ignored &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Automated Test Name: `testCommentsAreIgnored`

```
python src/nios.py test/lab1/testFiles/allTokens.nios
```

**Purpose:** Verify line comments, block comments, nested block comments, and continued scanning after comments.

**Source input:** The comment section of `allTokens.nios`:

```nios
// lineCommentText @ "ignored"
/* outerCommentText
	/* nestedCommentText */
	stillInsideComment
*/
afterComments
```

**Expected:** No token contains `lineCommentText`, `outerCommentText`, `nestedCommentText`, or `stillInsideComment`. The scanner resumes with `afterComments`.

**Actual scanner output:**

```text
LABEL raw='afterComments' literal=None line=13
EOF raw='' literal=None line=13
```

None of the comment text appeared in the output.

**Result:** Matches expectations.

### 3 - Line Comment at EOF &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Automated Test Name: `testLineCommentCanEndAtEof`

```
python src/nios.py test/lab1/testFiles/commentAtEnd.nios
```

**Purpose:** Verify that a line comment does not require a final newline.

**Source input (`commentAtEnd.nios`):**

```nios
// comment reaches end of file
```

The file has no newline after the comment.

**Expected:** Only EOF.

**Actual scanner output:**

```text
EOF raw='' literal=None line=1
```

**Result:** Matches expectations.

### 4 - Empty Source File &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Automated Test Name: `testEmptyFileProducesEof`

```
python src/nios.py test/lab1/testFiles/emptyTest.nios
```

**Purpose:** Verify scanner behavior when the source contains no characters.

**Source input (`emptyTest.nios`):** Empty file.

**Expected:** Only EOF on line 1.

**Actual scanner output:**

```text
EOF raw='' literal=None line=1
```

**Result:** Matches expectations.

### 5 - Lexical Errors and Line Numbers &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Automated Test Name: `testEveryLexicalErrorFromFile`

```
python src/nios.py test/lab1/testFiles/errorTest.nios
python src/nios.py test/lab1/testFiles/unterminatedWord.nios
```

**Purpose:** Verify unexpected-character, unterminated-string, and unterminated-block-comment errors. It also verifies that each diagnostic reports the correct line.

**Source input (`errorTest.nios`):**

```nios
let good = 1;
@
/* missing end
```

**Source input (`unterminatedWord.nios`):**

```nios
"missing end
still missing
```

**Expected:** `errorTest.nios` produces valid tokens from line 1, an unexpected `@` error on line 2, and an unterminated block comment error on line 3. `unterminatedWord.nios` reports an unterminated string using its opening line, line 1.

**Actual scanner output for `errorTest.nios`:**

```text
KEYWORD(LET) raw='let' literal=None line=1
LABEL raw='good' literal=None line=1
SYMBOL(EQUAL) raw='=' literal=None line=1
NUMBER raw='1' literal=1 line=1
SYMBOL(SEMICOLON) raw=';' literal=None line=1
EOF raw='' literal=None line=3
[line 2] Error: Unexpected character '@'.
[line 3] Error: Unterminated block comment.
```

**Actual scanner output for `unterminatedWord.nios`:**

```text
EOF raw='' literal=None line=2
[line 1] Error: Unterminated string.
```

**Result:** Matches expectations.

### 6 - Reject Non-Nios Files &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Automated Test Name: `testRejectsNonNiosFile`

```
python src/nios.py test/lab1/testFiles/notNiosFile.txt
```

**Purpose:** Verify that source-file mode accepts only files ending in `.nios` and does not scan rejected file contents.

**Source input (`notNiosFile.txt`):**

```text
show "This file should not be scanned";
```

**Expected:** A file-extension error and no tokens.

**Actual scanner output:**

```text
Error: Nios can only read .nios files.
```

**Result:** Matches expectations.

### 7 - Interactive Recovery After Errors &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Automated Test Name: `testInteractiveModeRecoversAfterErrors`

```
python src/nios.py
```

**Purpose:** Verify interactive mode reports every supported lexical error and remains usable afterward.

**Interactive input, entered one line at a time:**
```
@
"missing end
show 42;
/* missing end
show false;
```

**Expected:**  
`@` would report an unexpected-character.  
 `"missing end` would report an unterminated-string error.  
`show 42;` should scans successfully.  
`/* missing end` should report an unterminated block comment.  
`show false;` should also scan successfully.

**Actual scanner output:**

```nios
PS C:\Users\US242028\Documents\GitHub\CIS343-GVSU-Fall26\Interpreter> python src/nios.py
REPL mode
@
EOF raw='' literal=None line=1
[line 1] Error: Unexpected character '@'.
"missing end
EOF raw='' literal=None line=1
[line 1] Error: Unterminated string.
show 42;
KEYWORD(SHOW) raw='show' literal=None line=1
NUMBER raw='42' literal=42 line=1
SYMBOL(SEMICOLON) raw=';' literal=None line=1
EOF raw='' literal=None line=1
/* missing end
EOF raw='' literal=None line=1
[line 1] Error: Unterminated block comment.
show flase
KEYWORD(SHOW) raw='show' literal=None line=1
LABEL raw='flase' literal=None line=1
EOF raw='' literal=None line=1
PS C:\Users\US242028\Documents\GitHub\CIS343-GVSU-Fall26\Interpreter> 
```

**Result:** Matches expectations.

### 8 - Multiline Word Tokens &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Automated Test Name: `testWordCanSpanMultipleLines`

```
python src/nios.py test/lab1/testFiles/multilineWord.nios
```

**Purpose:** Verify that one Word token can contain newlines, keeps the line where it opened, and updates the line number for following tokens.

**Source input (`multilineWord.nios`):**

```nios
"first line
second line"
afterWord
```

**Expected:** One Word token beginning on line 1 with a newline in its raw and literal values, followed by `afterWord` on line 3 with no errors.

**Actual scanner output:**

```text
WORD raw='"first line\nsecond line"' literal='first line\nsecond line' line=1
LABEL raw='afterWord' literal=None line=3
EOF raw='' literal=None line=3
```

**Result:** Matches expectations.  
<br>


# Automated Test Result

Command:

```powershell
python test/lab1/runAllUnitTests.py
```

Result on October 2, 2026:

```
PS C:\Users\US242028\Documents\GitHub\CIS343-GVSU-Fall26\Interpreter> python test/lab1/runAllUnitTests.py
testEveryTokenTypeFromFile (testAllTokens.AllTokenTests.testEveryTokenTypeFromFile) ... ok
testCommentsAreIgnored (testComments.CommentTests.testCommentsAreIgnored) ... ok
testLineCommentCanEndAtEof (testComments.CommentTests.testLineCommentCanEndAtEof) ... ok
testEmptyFileProducesEof (testEndOfFile.EndOfFileTests.testEmptyFileProducesEof) ... ok
testEveryLexicalErrorFromFile (testErrorHandling.ErrorHandlingTests.testEveryLexicalErrorFromFile) ... ok
testRejectsNonNiosFile (testFileValidation.FileValidationTests.testRejectsNonNiosFile) ... ok
testInteractiveModeRecoversAfterErrors (testInteractiveMode.InteractiveModeTests.testInteractiveModeRecoversAfterErrors) ... ok
testWordCanSpanMultipleLines (testWords.WordTests.testWordCanSpanMultipleLines) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.309s

OK
PS C:\Users\US242028\Documents\GitHub\CIS343-GVSU-Fall26\Interpreter> 
```

All eight tests passed.

## Known Limitations

- String escape sequences such as `\"` and `\n` are not supported.
- Interactive mode scans each entered line separately, so a string or block comment cannot begin on one REPL line and end on a later REPL line.
- Errors contain line numbers but not column numbers/line position.
- The `.nios` extension check is case-sensitive, so `.NIOS` is rejected.
- The implementation uses Python's `isalpha`, `isalnum`, and `isdigit` methods, which may accept some Unicode characters beyond the ASCII forms shown in the regular expressions.
- So far this lab implements lexical scanning only; parsing and execution are not included.
