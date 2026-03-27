from dataclasses import dataclass
from typing import override
from src.config.config import Operator, Scope, Command


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


@dataclass(frozen=True)
class TokenCommand:
    value: Command

    @override
    def __repr__(self):
        return f"Command({self.value.name})"


@dataclass(frozen=True)
class TokenVariable:
    value: str

    @override
    def __repr__(self):
        return f"Variable({self.value})"


Token = TokenInt | TokenFloat | TokenOp | TokenScope | TokenCommand | TokenVariable


def lex(input: str) -> list[Token]:
    tokens: list[Token] = []
    _state_pending(input, 0, tokens)
    return tokens


def _state_pending(input: str, i: int, tokens: list[Token]) -> None:
    if i >= len(input):
        return
    if input[i].isspace():
        _state_pending(input, i + 1, tokens)
    elif input[i].isdigit():
        _state_integer(input, i, tokens)
    elif Operator.from_str(input[i]) is not None:
        _state_operator(input, i, tokens)
    elif Scope.from_str(input[i]) is not None:
        _state_scope(input, i, tokens)
    elif input[i].isalpha() and input[i].isupper():
        _state_command(input, i, tokens)
    else:
        raise ValueError(f"Unexpected character: {input[i]}")


def _state_integer(input: str, i: int, tokens: list[Token]) -> None:
    start = i
    while i < len(input):
        if input[i].isdigit():
            i += 1
        elif input[i] == ".":
            _state_float(input, i + 1, input[start:i + 1], tokens)
            return
        elif input[i].isspace() or Scope.from_str(input[i]) is not None:
            break
        else:
            raise ValueError(f"Unexpected character: {input[i]}")
    tokens.append(TokenInt(int(input[start:i])))
    _state_pending(input, i, tokens)


def _state_float(input: str, i: int, buffer: str, tokens: list[Token]) -> None:
    start = i
    while i < len(input):
        if input[i].isdigit():
            i += 1
        elif input[i].isspace() or Scope.from_str(input[i]) is not None:
            break
        else:
            raise ValueError(f"Unexpected character: {input[i]}")
    tokens.append(TokenFloat(float(buffer + input[start:i])))
    _state_pending(input, i, tokens)


def _state_operator(input: str, i: int, tokens: list[Token]) -> None:
    start = i
    while i < len(input) and not input[i].isspace() and Scope.from_str(input[i]) is None:
        i += 1
        if Operator.from_str(input[start:i]) is None:
            raise ValueError(f"Unexpected operation: {input[start:i]}")
    op = Operator.from_str(input[start:i])
    if op is None:
        raise ValueError(f"Unexpected operation: {input[start:i]}")
    tokens.append(TokenOp(op))
    _state_pending(input, i, tokens)


def _state_scope(input: str, i: int, tokens: list[Token]) -> None:
    scope = Scope.from_str(input[i])
    if scope is None:
        raise ValueError(f"Unexpected scope: {input[i]}")
    tokens.append(TokenScope(scope))
    _state_pending(input, i + 1, tokens)


def _state_command(input: str, i: int, tokens: list[Token]) -> None:
    start = i
    while i < len(input):
        if input[i].isalpha() and input[i].isupper():
            i += 1
        elif input[i].isspace() or Scope.from_str(input[i]) is not None:
            break
        else:
            raise ValueError(f"Unexpected character in command: {input[i]}")
    cmd = Command.from_str(input[start:i])
    if cmd is None:
        tokens.append(TokenVariable(input[start:i]))
    else:
        tokens.append(TokenCommand(cmd))
    _state_pending(input, i, tokens)
