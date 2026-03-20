from Token import Token

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.char_atual = self.texto[self.pos] if self.texto else None

    def avancar(self):
        self.pos += 1
        self.char_atual = self.texto[self.pos] if self.pos < len(self.texto) else None

    def pular_espacos(self):
        while self.char_atual is not None and self.char_atual.isspace():
            self.avancar()

    def olhar_proximo_token(self):
        """Retorna o próximo token sem consumir (lookahead)."""
        pos_salva = self.pos
        char_salvo = self.char_atual
        tok = self.proximo_token()
        self.pos = pos_salva
        self.char_atual = char_salvo
        return tok

    def proximo_token(self):
        while self.char_atual is not None:
            if self.char_atual.isspace():
                self.pular_espacos()
                continue

            # Números inteiros
            if self.char_atual.isdigit():
                num_str = ''
                while self.char_atual is not None and self.char_atual.isdigit():
                    num_str += self.char_atual
                    self.avancar()
                # Erro léxico: número seguido de letra (ex: 237axy)
                if self.char_atual is not None and self.char_atual.isalpha():
                    raise Exception(f"Erro léxico: sequência inválida '{num_str}{self.char_atual}' na posição {self.pos}")
                return Token('LITERAL_INTEIRO', num_str)

            # Identificadores (começam com letra)
            if self.char_atual.isalpha():
                ident_str = ''
                while self.char_atual is not None and (self.char_atual.isalpha() or self.char_atual.isdigit()):
                    ident_str += self.char_atual
                    self.avancar()
                return Token('IDENTIFICADOR', ident_str)

            if self.char_atual == '(':
                self.avancar()
                return Token('ABRE_PARENTESE', '(')

            if self.char_atual == ')':
                self.avancar()
                return Token('FECHA_PARENTESE', ')')

            if self.char_atual == ';':
                self.avancar()
                return Token('PONTO_VIRGULA', ';')

            if self.char_atual == '=':
                self.avancar()
                return Token('IGUAL', '=')

            if self.char_atual in ('+', '-', '*', '/'):
                op = self.char_atual
                self.avancar()
                return Token('OPERADOR', op)

            raise Exception(f"Erro léxico: caractere '{self.char_atual}' inesperado na posição {self.pos}")

        return Token('EOF', '')
