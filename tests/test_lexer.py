import pytest
from src.lexer.lexer import lex, Token, TokenInt, TokenFloat, TokenOp, TokenScope, TokenCommand, TokenVariable
from src.config.config import Operator, Scope, Command

# executarExpressao (casos validos)
@pytest.mark.parametrize("input, expected", [
    ("42",              [TokenInt(42)]),
    ("3.50",            [TokenFloat(3.50)]),
    ("3 4 5",           [TokenInt(3), TokenInt(4), TokenInt(5)]),
    ("1.5 2.5 3.5",     [TokenFloat(1.5), TokenFloat(2.5), TokenFloat(3.5)]),
    ("3 4.5 2 1.0",     [TokenInt(3), TokenFloat(4.5), TokenInt(2), TokenFloat(1.0)]),
    ("123 4567",        [TokenInt(123), TokenInt(4567)]),
    ("350.14159",       [TokenFloat(350.14159)]),
    ("0 0.0 000.000",   [TokenInt(0), TokenFloat(0.0), TokenFloat(0.0)]),
    ("3   4",           [TokenInt(3), TokenInt(4)]),
    ("  3  4  ",        [TokenInt(3), TokenInt(4)]),
    ("",                []),
    ("   ",             []),
    ("+",               [TokenOp(Operator.Add)]),
    ("-",               [TokenOp(Operator.Sub)]),
    ("*",               [TokenOp(Operator.Mul)]),
    ("/",               [TokenOp(Operator.Div)]),
    ("//",              [TokenOp(Operator.IntDiv)]),
    ("^",               [TokenOp(Operator.Pow)]),
    ("%",               [TokenOp(Operator.Mod)]),
    ("3 + 4",           [TokenInt(3), TokenOp(Operator.Add), TokenInt(4)]),
    ("10 - 5",          [TokenInt(10), TokenOp(Operator.Sub), TokenInt(5)]),
    ("2 * 3",           [TokenInt(2), TokenOp(Operator.Mul), TokenInt(3)]),
    ("8 / 2",           [TokenInt(8), TokenOp(Operator.Div), TokenInt(2)]),
    ("9 // 2",          [TokenInt(9), TokenOp(Operator.IntDiv), TokenInt(2)]),
    ("2 ^ 3",           [TokenInt(2), TokenOp(Operator.Pow), TokenInt(3)]),
    ("10 % 3",          [TokenInt(10), TokenOp(Operator.Mod), TokenInt(3)]),
    ("1.5 + 2.5",       [TokenFloat(1.5), TokenOp(Operator.Add), TokenFloat(2.5)]),
    ("1 + 2 - 3",       [TokenInt(1), TokenOp(Operator.Add), TokenInt(2), TokenOp(Operator.Sub), TokenInt(3)]),
    ("(",               [TokenScope(Scope.Open)]),
    (")",               [TokenScope(Scope.Close)]),
    ("(1 + 2)",         [TokenScope(Scope.Open), TokenInt(1), TokenOp(Operator.Add), TokenInt(2), TokenScope(Scope.Close)]),
    ("(10 2 /) 5 /",    [TokenScope(Scope.Open), TokenInt(10), TokenInt(2), TokenOp(Operator.Div), TokenScope(Scope.Close), TokenInt(5), TokenOp(Operator.Div)]),
    ("(4 (5 2 +) *)",   [TokenScope(Scope.Open), TokenInt(4), TokenScope(Scope.Open), TokenInt(5), TokenInt(2), TokenOp(Operator.Add), TokenScope(Scope.Close), TokenOp(Operator.Mul), TokenScope(Scope.Close)]),
    ("(())",            [TokenScope(Scope.Open), TokenScope(Scope.Open), TokenScope(Scope.Close), TokenScope(Scope.Close)]),
    ("(3)",             [TokenScope(Scope.Open), TokenInt(3), TokenScope(Scope.Close)]),
    ("(1.5)",           [TokenScope(Scope.Open), TokenFloat(1.5), TokenScope(Scope.Close)]),
    ("3\t4",            [TokenInt(3), TokenInt(4)]),
    ("3\n4",            [TokenInt(3), TokenInt(4)]),
    ("3 4 + 5 *",       [TokenInt(3), TokenInt(4), TokenOp(Operator.Add), TokenInt(5), TokenOp(Operator.Mul)]),
    ("RES",             [TokenCommand(Command.Res)]),
    ("(RES)",           [TokenScope(Scope.Open), TokenCommand(Command.Res), TokenScope(Scope.Close)]),
    ("(10 RES)",        [TokenScope(Scope.Open), TokenInt(10), TokenCommand(Command.Res), TokenScope(Scope.Close)]),
    ("(VARIABLE)",      [TokenScope(Scope.Open), TokenVariable("VARIABLE"), TokenScope(Scope.Close)]),
    ("(15 VARIABLE)",   [TokenScope(Scope.Open), TokenInt(15), TokenVariable("VARIABLE"), TokenScope(Scope.Close)]),
    ("(15.5 SPENCER)", [TokenScope(Scope.Open), TokenFloat(15.5), TokenVariable("SPENCER"), TokenScope(Scope.Close)]),
    ("(15.5 SPEN RES CER)", [TokenScope(Scope.Open), TokenFloat(15.5), TokenVariable("SPEN"), TokenCommand(Command.Res), TokenVariable("CER"), TokenScope(Scope.Close)]),
])
def test_lex(input: str, expected: list[Token]):
    assert lex(input) == expected

# executarExpressao (casos invalidos)
@pytest.mark.parametrize("input, match", [
    ("3 a 4",    "Unexpected character"),
    (".5",       "Unexpected character"),
    ("3.5.2",    "Unexpected character"),
    ("!",        "Unexpected character"),
    ("3 ++ 4",   "Unexpected operation"),
    ("3 //// 4", "Unexpected operation"),
    ("3 +- 4",   "Unexpected operation"),
    ("3+4",      "Unexpected character"),
    ("1.5+2",    "Unexpected character"),
    ("(res)",    "Unexpected character"),
    ("(15 S!P)", "Unexpected character"),
])
def test_lex_raises(input: str, match: str):
    with pytest.raises(ValueError, match=match):
        _ = lex(input)
