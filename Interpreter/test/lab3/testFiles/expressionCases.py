# --- start AI code --
literalCases = [
    ("0", "0"),
    ("123", "123"),
    ("45.67", "45.67"),
    ("0.0", "0.0"),
    ('"hello world"', '"hello world"'),
    ('""', '""'),
    ('"+ ! ( ) /* text */"', '"+ ! ( ) /* text */"'),
    ("true", "true"),
    ("false", "false"),
    ("nil", "nil")
]

operatorCases = [
    ("1, 2", "(, 1 2)"),
    ("1 + 2", "(+ 1 2)"),
    ("1 - 2", "(- 1 2)"),
    ("1 * 2", "(* 1 2)"),
    ("1 / 2", "(/ 1 2)"),
    ("1 == 2", "(== 1 2)"),
    ("1 != 2", "(!= 1 2)"),
    ("1 < 2", "(< 1 2)"),
    ("1 <= 2", "(<= 1 2)"),
    ("1 > 2", "(> 1 2)"),
    ("1 >= 2", "(>= 1 2)"),
    ("-123", "(- 123)"),
    ("!false", "(! false)")
]

precedenceCases = [
    ("1 + 2, 3 * 4", "(, (+ 1 2) (* 3 4))"),
    ("1, 2 + 3", "(, 1 (+ 2 3))"),
    ("1, 2 == 3", "(, 1 (== 2 3))"),
    ("1 + 2 * 3", "(+ 1 (* 2 3))"),
    ("2 * 3 + 1", "(+ (* 2 3) 1)"),
    ("8 - 6 / 2", "(- 8 (/ 6 2))"),
    ("6 / 2 - 1", "(- (/ 6 2) 1)"),
    ("1 + 2 < 4 - 1", "(< (+ 1 2) (- 4 1))"),
    ("1 < 2 == 3 >= 2", "(== (< 1 2) (>= 3 2))"),
    ("-2 * 3", "(* (- 2) 3)"),
    ("2 * -3", "(* 2 (- 3))"),
    ("!false == true", "(== (! false) true)"),
    ("-1 + 2 * 3 < 8 == !false", "(== (< (+ (- 1) (* 2 3)) 8) (! false))")
]

associativityCases = [
    ("1, 2, 3", "(, (, 1 2) 3)"),
    ("8 - 3 - 1", "(- (- 8 3) 1)"),
    ("8 / 4 / 2", "(/ (/ 8 4) 2)"),
    ("8 + 3 - 1", "(- (+ 8 3) 1)"),
    ("8 / 4 * 2", "(* (/ 8 4) 2)"),
    ("1 < 2 <= 3", "(<= (< 1 2) 3)"),
    ("true == false != nil", "(!= (== true false) nil)"),
    ("!!true", "(! (! true))"),
    ("--1", "(- (- 1))"),
    ("!-1", "(! (- 1))")
]

groupingCases = [
    ("(1, 2) * 3", "(* (group (, 1 2)) 3)"),
    ("1, (2, 3)", "(, 1 (group (, 2 3)))"),
    ("(1)", "(group 1)"),
    ("(((1)))", "(group (group (group 1)))"),
    ("(1 + 2) * 3", "(* (group (+ 1 2)) 3)"),
    ("8 - (3 - 1)", "(- 8 (group (- 3 1)))"),
    ("(1 + (2 * (3 - 4)))", "(group (+ 1 (group (* 2 (group (- 3 4))))))"),
    ("-123 * (45.67)", "(* (- 123) (group 45.67))"),
    ("!(true == false)", "(! (group (== true false)))")
]

syntaxErrorCases = [
    ("(1 + 2", "[line 1] Error at end of input: Expected ')' after expression."),
    ("((1)", "[line 1] Error at end of input: Expected ')' after expression."),
    ("(1 2)", "[line 1] Error at '2': Expected ')' after expression."),
    ("1)", "[line 1] Error at ')': Unexpected token after expression."),
    ("()", "[line 1] Error at ')': Expected an expression."),
    ("1 +", "[line 1] Error at end of input: Expected an expression."),
    ("!", "[line 1] Error at end of input: Expected an expression."),
    ("-", "[line 1] Error at end of input: Expected an expression."),
    ("(1 + )", "[line 1] Error at ')': Expected an expression."),
    (", 1", "[line 1] Error at ',': Missing left operand before ','."),
    ("1,,2", "[line 1] Error at ',': Missing left operand before ','."),
    ("(, 1)", "[line 1] Error at ',': Missing left operand before ','."),
    ("1,", "[line 1] Error at end of input: Expected an expression."),
    ("+ 2", "[line 1] Error at '+': Missing left operand before '+'."),
    ("* 2", "[line 1] Error at '*': Missing left operand before '*'."),
    ("/ 2", "[line 1] Error at '/': Missing left operand before '/'."),
    ("== 2", "[line 1] Error at '==': Missing left operand before '=='."),
    ("!= 2", "[line 1] Error at '!=': Missing left operand before '!='."),
    ("> 2", "[line 1] Error at '>': Missing left operand before '>'."),
    (">= 2", "[line 1] Error at '>=': Missing left operand before '>='."),
    ("< 2", "[line 1] Error at '<': Missing left operand before '<'."),
    ("<= 2", "[line 1] Error at '<=': Missing left operand before '<='."),
    ("1 + * 2", "[line 1] Error at '*': Missing left operand before '*'."),
    ("(* 2)", "[line 1] Error at '*': Missing left operand before '*'."),
    ("! == 2", "[line 1] Error at '==': Missing left operand before '=='."),
    ("*", "[line 1] Error at '*': Missing left operand before '*'."),
    ("name", "[line 1] Error at 'name': Expected an expression."),
    ("show 1", "[line 1] Error at 'show': Expected an expression."),
    ("1 2", "[line 1] Error at '2': Unexpected token after expression."),
    ("1;", "[line 1] Error at ';': Unexpected token after expression."),
    ("1 = 2", "[line 1] Error at '=': Unexpected token after expression."),
    ("true and false", "[line 1] Error at 'and': Unexpected token after expression."),
    ("true or false", "[line 1] Error at 'or': Unexpected token after expression."),
    ("", "[line 1] Error at end of input: Expected an expression."),
    ("   ", "[line 1] Error at end of input: Expected an expression."),
    ("// only a comment", "[line 1] Error at end of input: Expected an expression.")
]

lexicalErrorCases = [
    ("1 @", "[line 1] Error: Unexpected character '@'."),
    ("1 + @", "[line 1] Error: Unexpected character '@'."),
    ('"unfinished', "[line 1] Error: Unterminated string."),
    ("1 /* unfinished", "[line 1] Error: Unterminated block comment."),
    ("1 @ #", "[line 1] Error: Unexpected character '@'.\n[line 1] Error: Unexpected character '#'.")
]


multilineCases = [
    ("1,\n2", "(, 1 2)"),
    ("1,\n,2", "[line 2] Error at ',': Missing left operand before ','."),
    ("(1 +\n2) * 3", "(* (group (+ 1 2)) 3)"),
    ('"hello\nworld"', '"hello\\nworld"'),
    ("1 /* outer\n/* inner */ done */ + 2 // done", "(+ 1 2)"),
    ("1 +\n* 2", "[line 2] Error at '*': Missing left operand before '*'."),
    ("(1 +\n2", "[line 2] Error at end of input: Expected ')' after expression."),
    ("1\n2", "[line 2] Error at '2': Unexpected token after expression."),
    ("1 +\n@ 2", "[line 2] Error: Unexpected character '@'."),
    ('\n"unfinished', "[line 2] Error: Unterminated string."),
    ("1\n/* unfinished", "[line 2] Error: Unterminated block comment.")
]
# --- end AI code --