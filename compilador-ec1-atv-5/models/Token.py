class Token:
    """
    Representa um token para análise léxica.

    Attributes:
        tipo (str): O tipo do token.
        lexema (str): O lexema do token.
        posicao (tuple[int, int]): A posição do token no código-fonte (linha, coluna).
    """
    def __init__(self, tipo: str, lexema: str, posicao: tuple[int, int]):
        self.tipo = tipo
        self.lexema = lexema
        self.posicao = posicao

PONTUACOES = {
    "(": {
        "tipo": "ABRE_PARENTESE",
        "lexema": "(",
    },
    ")": {
        "tipo": "FECHA_PARENTESE",
        "lexema": ")",
    },
    "EOF": {
        "tipo": "END_OF_FILE",
        "lexema": "EOF",
    },
}

OPERADORES = {
    "+": {
        "tipo": "ADICAO",
        "lexema": "+",
    },
    "-": {
        "tipo": "SUBTRACAO",
        "lexema": "-",
    },
    "*": {
        "tipo": "MULTIPLICACAO",
        "lexema": "*",
    },
    "/": {
        "tipo": "DIVISAO",
        "lexema": "/",
    },
}