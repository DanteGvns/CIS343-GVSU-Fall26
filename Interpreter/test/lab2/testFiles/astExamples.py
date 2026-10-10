# --- start AI code --
from expression import Binary, Group, Literal, Unary
from src.token import Symbol


def getExamples():
    return [
        (
            "lecture slide example",
            Binary(
                Literal(1),
                Symbol(1, "+", "PLUS"),
                Binary(
                    Literal(2),
                    Symbol(1, "*", "STAR"),
                    Binary(
                        Literal(3),
                        Symbol(1, "-", "MINUS"),
                        Literal(4),
                    ),
                ),
            ),
            "(+ 1 (* 2 (- 3 4)))",
        ),
        (
            "assignment example",
            Binary(
                Unary(Symbol(1, "-", "MINUS"), Literal(123)),
                Symbol(1, "*", "STAR"),
                Group(Literal(45.67)),
            ),
            "(* (- 123) (group 45.67))",
        ),
        (
            "nested arithmetic",
            Binary(
                Binary(Literal(8), Symbol(1, "+", "PLUS"), Literal(4)),
                Symbol(1, "/", "SLASH"),
                Binary(Literal(5), Symbol(1, "-", "MINUS"), Literal(2)),
            ),
            "(/ (+ 8 4) (- 5 2))",
        ),
        (
            "booleans and negation",
            Binary(
                Unary(Symbol(1, "!", "BANG"), Literal(False)),
                Symbol(1, "==", "EQUAL_EQUAL"),
                Literal(True),
            ),
            "(== (! false) true)",
        ),
        (
            "word and nil inequality",
            Binary(Literal("hello world"), Symbol(1, "!=", "BANG_EQUAL"), Literal(None)),
            '(!= "hello world" nil)',
        ),
        (
            "less than",
            Binary(Literal(1), Symbol(1, "<", "LESS"), Literal(2)),
            "(< 1 2)",
        ),
        (
            "less than or equal",
            Binary(Literal(2), Symbol(1, "<=", "LESS_EQUAL"), Literal(2)),
            "(<= 2 2)",
        ),
        (
            "greater than",
            Binary(Literal(3), Symbol(1, ">", "GREATER"), Literal(2)),
            "(> 3 2)",
        ),
        (
            "greater than or equal",
            Binary(Literal(3), Symbol(1, ">=", "GREATER_EQUAL"), Literal(3)),
            "(>= 3 3)",
        ),
        ("nested grouping", Group(Group(Literal(0))), "(group (group 0))"),
        ("empty word", Literal(""), '""'),
        ("parentheses in word", Literal("(hello world)"), '"(hello world)"'),
        ("multiline word", Literal("first\nsecond"), '"first\\nsecond"'),
        ("nil literal", Literal(None), "nil"),
        ("false literal", Literal(False), "false"),
        ("true literal", Literal(True), "true"),
        ("zero literal", Literal(0), "0"),
        ("decimal literal", Literal(1.0), "1.0"),
        (
            "left nested subtraction",
            Binary(
                Binary(Literal(10), Symbol(1, "-", "MINUS"), Literal(3)),
                Symbol(1, "-", "MINUS"),
                Literal(2),
            ),
            "(- (- 10 3) 2)",
        ),
        (
            "right nested subtraction",
            Binary(
                Literal(10),
                Symbol(1, "-", "MINUS"),
                Binary(Literal(3), Symbol(1, "-", "MINUS"), Literal(2)),
            ),
            "(- 10 (- 3 2))",
        ),
    ]
# --- end AI code --