from io import StringIO
import sys

from lex import LexAnalyzer
from parser import Parser
from errors import LexicalError


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 main.py \"<expressao>\"")
        sys.exit(1)

    source = sys.argv[1]

    lex = LexAnalyzer()
    tokens, errors = lex.analyze(StringIO(source))

    if errors:
        for error in errors:
            error.show()
        sys.exit(1)

    parser = Parser(tokens)

    try:
        tree = parser.parse()
    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        sys.exit(1)

    print("Árvore sintática:")
    print(tree.imprimir())

    print("\nValor da expressão:")
    print(tree.avaliar())

    print("Árvore sintática (estrutura):")
    print(tree.pretty("", False))


if __name__ == "__main__":
    main()
