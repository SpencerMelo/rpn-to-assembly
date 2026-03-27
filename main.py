# =======================================================
# Name: Spencer Melo
# GitHub: https://github.com/SpencerMelo
# Canvas Group: RA1 20
# =======================================================

import sys
from src.lexer.lexer import lex

# lerArquivo
def read_lines(path: str) -> list[str]:
    with open(path, 'r') as file:
        return [line.strip() for line in file if line.strip()]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    for line in read_lines(sys.argv[1]):
        print(lex(line))

    # Sem codegen, nao tenho dominio de Assembly, mesmo utilizando IA pra gerar e funcionando,
    # nao sou capacitado suficiente em assembly pra revisar e responder perguntas com confianca sobre codigo gerado.
