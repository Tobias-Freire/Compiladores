from lex import LexAnalyzer

if __name__ == "__main__":
    file = open("inputs/input_4.txt", "r")
    analyzer = LexAnalyzer()
    tokens, errors = analyzer.analyze(file)
    for token in tokens:
        print(f"<{token.tipo}, '{token.lexema}', {token.posicao}>")
    for error in errors:
        error.show()