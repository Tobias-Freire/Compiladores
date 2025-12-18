from lex import LexAnalyzer

if __name__ == "__main__":
    file_name = str(input("Digite o nome do arquivo (que deve estar dentro de /inputs): "))
    file = open("inputs/" + file_name, "r")
    analyzer = LexAnalyzer()
    tokens, errors = analyzer.analyze(file)
    for token in tokens:
        print(f"<{token.tipo}, '{token.lexema}', {token.posicao}>")
    for error in errors:
        error.show()