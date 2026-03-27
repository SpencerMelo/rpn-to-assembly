import sys
from src.lexer.lexer import lex

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as file:
        content = file.read()

    tokens = lex(content)
    print(tokens)
