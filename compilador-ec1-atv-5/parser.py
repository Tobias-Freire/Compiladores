from ast_ec1 import Const, OpBin
from models.Token import Token

class SyntaxError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def proximo_token(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def token_atual(self):
        return self.tokens[self.pos]

    def verificar(self, tipo_esperado):
        token = self.proximo_token()
        if token.tipo != tipo_esperado:
            raise SyntaxError(
                f"Esperado {tipo_esperado}, encontrado {token.tipo} "
                f"(linha {token.posicao[0]}, coluna {token.posicao[1]})"
            )

    # 🔹 NOVO MÉTODO
    def parse(self):
        expr = self.analisa_expressao()
        token = self.proximo_token()
        if token.tipo != "END_OF_FILE":
            raise SyntaxError("Tokens extras após o fim da expressão")
        return expr

    def analisa_expressao(self):
        token = self.proximo_token()

        if token.tipo == "NUMERO":
            return Const(int(token.lexema))

        elif token.tipo == "ABRE_PARENTESE":
            op_esq = self.analisa_expressao()
            operador = self.analisa_operador()
            op_dir = self.analisa_expressao()
            self.verificar("FECHA_PARENTESE")
            return OpBin(operador, op_esq, op_dir)

        else:
            raise SyntaxError(
                f"Token inesperado {token.tipo} "
                f"(linha {token.posicao[0]}, coluna {token.posicao[1]})"
            )

    def analisa_operador(self):
        token = self.proximo_token()
        if token.tipo in {
            "ADICAO",
            "SUBTRACAO",
            "MULTIPLICACAO",
            "DIVISAO",
        }:
            return token.tipo

        raise SyntaxError(
            f"Operador inválido {token.tipo} "
            f"(linha {token.posicao[0]}, coluna {token.posicao[1]})"
        )

