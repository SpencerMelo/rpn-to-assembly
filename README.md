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
python3 main.py
```

## Test

```sh
.venv/bin/pytest tests/
```

## Lexer DFA

The lexer is implemented as a Deterministic Finite Automaton (DFA) that tokenizes RPN expressions.

### Alphabet

| Symbol | Description |
|--------|-------------|
| `d` | Digit (`0`–`9`) |
| `.` | Dot |
| `op` | Operator character (`+` `-` `*` `/` `^` `%`) |
| `sc` | Scope character (`(` `)`) |
| `ws` | Whitespace |
| `?` | Any other character (invalid) |

### States

| State | Description |
|-------|-------------|
| **Pending** | Initial state — waiting for next token |
| **Integer** | Reading digits of an integer |
| **Float** | Reading digits after a decimal point |
| **Operator** | Reading operator characters |

### Transitions

| State | `d` | `.` | `op` | `sc` | `ws` | `?` |
|-------|-----|-----|------|------|------|-----|
| **Pending** | → Integer | Error | → Operator | emit `Scope`, stay | stay | Error |
| **Integer** | stay | → Float | emit `Int`, → Operator | emit `Int`, → Pending | emit `Int`, → Pending | Error |
| **Float** | stay | Error | emit `Float`, → Operator | emit `Float`, → Pending | emit `Float`, → Pending | Error |
| **Operator** | Error | Error | stay (if valid prefix) | emit `Op`, → Pending | emit `Op`, → Pending | Error |

### Accepting states

All states except **Error** are accepting at end of input, each emitting their buffered token (`Int`, `Float`, or `Op`). **Pending** accepts with no token emitted.
