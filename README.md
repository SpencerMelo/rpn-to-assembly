# rpn-to-assembly

## Requirements

- Python 3.12+

## Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```sh
python3 main.py <file>
```

Each line of the input file is lexed independently and its token list is printed to stdout.

## Test

```sh
.venv/bin/pytest tests/
```

## Lexer DFA

The lexer is implemented as a Deterministic Finite Automaton (DFA) that tokenizes RPN expressions. Each line is processed independently.

### Token Types

| Token | Example | Description |
|-------|---------|-------------|
| `Int` | `42` | Integer literal |
| `Float` | `3.14` | Floating-point literal |
| `Op` | `+` `-` `*` `/` `//` `^` `%` | Arithmetic operator |
| `Scope` | `(` `)` | Grouping |
| `Command` | `RES` | Built-in command |
| `Variable` | `FOO` | Uppercase identifier |

### Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| `RES` | `(N RES)` | Returns the result of the expression `N` lines before the current one (`N` is a non-negative integer) |

### Alphabet

| Symbol | Description |
|--------|-------------|
| `d` | Digit (`0`–`9`) |
| `.` | Dot |
| `op` | Operator character (`+` `-` `*` `/` `^` `%`) |
| `sc` | Scope character (`(` `)`) |
| `A` | Uppercase letter (`A`–`Z`) |
| `ws` | Whitespace |
| `?` | Any other character (invalid) |

### States

| State | Description |
|-------|-------------|
| **Pending** | Initial state — waiting for next token |
| **Integer** | Reading digits of an integer |
| **Float** | Reading digits after a decimal point |
| **Operator** | Reading operator characters |
| **Command** | Reading an uppercase identifier (resolves to `Command` or `Variable`) |

### Transitions

| State | `d` | `.` | `op` | `sc` | `A` | `ws` | `?` |
|-------|-----|-----|------|------|-----|------|-----|
| **Pending** | → Integer | Error | → Operator | emit `Scope`, stay | → Command | stay | Error |
| **Integer** | stay | → Float | Error | emit `Int`, → Pending | Error | emit `Int`, → Pending | Error |
| **Float** | stay | Error | Error | emit `Float`, → Pending | Error | emit `Float`, → Pending | Error |
| **Operator** | Error | Error | stay (if valid prefix) | emit `Op`, → Pending | Error | emit `Op`, → Pending | Error |
| **Command** | Error | Error | Error | emit `Command`/`Variable`, → Pending | stay | emit `Command`/`Variable`, → Pending | Error |

### Accepting states

All states except **Error** are accepting at end of input, each emitting their buffered token. **Pending** accepts with no token emitted.
