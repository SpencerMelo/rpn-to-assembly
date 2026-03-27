# =======================================================
# Name: Spencer Melo
# GitHub: https://github.com/SpencerMelo
# Canvas Group: RA1 20
# =======================================================

import sys
from src.lexer.lexer import lex

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as file:
        content = file.read()

    for line in content.splitlines():
        line = line.strip()
        if line:
            tokens = lex(line)
            print(tokens)
