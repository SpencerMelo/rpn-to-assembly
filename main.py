from src.lexer.lexer import lex

if __name__ == "__main__":
    input = "(10 (4 2 *) +)"
    tokens = lex(input)
    print(tokens)
