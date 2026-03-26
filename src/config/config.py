from enum import Enum, auto


class Operator(Enum):
    Add = auto()    # +
    Sub = auto()    # -
    Mul = auto()    # *
    Div = auto()    # /
    IntDiv = auto() # //
    Pow = auto()    # ^
    Mod = auto()    # %

    @staticmethod
    def from_str(s: str) -> "Operator | None":
        return {
            "+": Operator.Add,
            "-": Operator.Sub,
            "*": Operator.Mul,
            "/": Operator.Div,
            "//": Operator.IntDiv,
            "^": Operator.Pow,
            "%": Operator.Mod,
        }.get(s)


class Scope(Enum):
    Open = auto()   # (
    Close = auto()  # )

    @staticmethod
    def from_str(s: str) -> "Scope | None":
        return {
            "(": Scope.Open,
            ")": Scope.Close,
        }.get(s)
