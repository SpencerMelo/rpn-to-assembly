from dataclasses import dataclass
from typing import override
from src.config.config import Operator, Scope


@dataclass(frozen=True)
class TokenInt:
    value: int

    @override
    def __repr__(self):
        return f"Int({self.value})"


@dataclass(frozen=True)
class TokenFloat:
    value: float

    @override
    def __repr__(self):
        return f"Float({self.value})"


@dataclass(frozen=True)
class TokenOp:
    value: Operator

    @override
    def __repr__(self):
        return f"Op({self.value.name})"


@dataclass(frozen=True)
class TokenScope:
    value: Scope

    @override
    def __repr__(self):
        return f"Scope({self.value.name})"


Token = TokenInt | TokenFloat | TokenOp | TokenScope


def lex(input: str) -> list[Token]:
    tokens: list[Token] = []
    _state_pending(input, 0, tokens)
    return tokens


def _state_pending(input: str, i: int, tokens: list[Token]) -> None:
    while i < len(input):
        if input[i].isspace():
            i += 1
        elif input[i].isdigit():
            i = _state_integer(input, i, tokens)
        elif Operator.from_str(input[i]) is not None:
            i = _state_operator(input, i, tokens)
        elif (scope := Scope.from_str(input[i])) is not None:
            tokens.append(TokenScope(scope))
            i += 1
        else:
            raise ValueError(f"Unexpected character: {input[i]}")


def _state_integer(input: str, i: int, tokens: list[Token]) -> int:
    start = i
    while i < len(input):
        if input[i].isdigit():
            i += 1
        elif input[i] == ".":
            return _state_float(input, i + 1, input[start:i + 1], tokens)
        elif input[i].isspace() or Scope.from_str(input[i]) is not None:
            break
        else:
            raise ValueError(f"Unexpected character: {input[i]}")
    tokens.append(TokenInt(int(input[start:i])))
    return i


def _state_float(input: str, i: int, buffer: str, tokens: list[Token]) -> int:
    start = i
    while i < len(input):
        if input[i].isdigit():
            i += 1
        elif input[i].isspace() or Scope.from_str(input[i]) is not None:
            break
        else:
            raise ValueError(f"Unexpected character: {input[i]}")
    tokens.append(TokenFloat(float(buffer + input[start:i])))
    return i


def _state_operator(input: str, i: int, tokens: list[Token]) -> int:
    start = i
    while i < len(input) and not input[i].isspace() and Scope.from_str(input[i]) is None:
        i += 1
        if Operator.from_str(input[start:i]) is None:
            raise ValueError(f"Unexpected operation: {input[start:i]}")
    op = Operator.from_str(input[start:i])
    if op is None:
        raise ValueError(f"Unexpected operation: {input[start:i]}")
    tokens.append(TokenOp(op))
    return i
