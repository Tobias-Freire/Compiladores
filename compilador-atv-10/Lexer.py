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

    def olhar_proximo_char(self):
        if self.pos + 1 < len(self.texto):
            return self.texto[self.pos + 1]
        return None

    def olhar_proximo_token(self):
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

            # NÚMEROS
            if self.char_atual.isdigit():
                num_str = ''
                while self.char_atual is not None and self.char_atual.isdigit():
                    num_str += self.char_atual
                    self.avancar()

                if self.char_atual is not None and self.char_atual.isalpha():
                    raise Exception(f"Erro léxico: sequência inválida '{num_str}{self.char_atual}' na posição {self.pos}")

                return Token('LITERAL_INTEIRO', num_str)

            # IDENTIFICADORES / KEYWORDS
            if self.char_atual.isalpha():
                ident_str = ''
                while self.char_atual is not None and (self.char_atual.isalnum()):
                    ident_str += self.char_atual
                    self.avancar()

                # palavras-chave
                if ident_str == "if":
                    return Token('IF', ident_str)
                elif ident_str == "else":
                    return Token('ELSE', ident_str)
                elif ident_str == "while":
                    return Token('WHILE', ident_str)
                elif ident_str == "return":
                    return Token('RETURN', ident_str)

                return Token('IDENTIFICADOR', ident_str)

            # PONTUAÇÃO
            if self.char_atual == '{':
                self.avancar()
                return Token('ABRE_CHAVE', '{')

            if self.char_atual == '}':
                self.avancar()
                return Token('FECHA_CHAVE', '}')

            if self.char_atual == '(':
                self.avancar()
                return Token('ABRE_PARENTESE', '(')

            if self.char_atual == ')':
                self.avancar()
                return Token('FECHA_PARENTESE', ')')

            if self.char_atual == ';':
                self.avancar()
                return Token('PONTO_VIRGULA', ';')

            # OPERADORES

            # == (igualdade)
            if self.char_atual == '=' and self.olhar_proximo_char() == '=':
                self.avancar()
                self.avancar()
                return Token('OP_COMPARACAO', '==')

            # = (atribuição)
            if self.char_atual == '=':
                self.avancar()
                return Token('IGUAL', '=')

            # < ou >
            if self.char_atual in ('<', '>'):
                op = self.char_atual
                self.avancar()
                return Token('OP_COMPARACAO', op)

            # + - * /
            if self.char_atual in ('+', '-', '*', '/'):
                op = self.char_atual
                self.avancar()
                return Token('OPERADOR', op)

            # ERRO
            raise Exception(f"Erro léxico: caractere '{self.char_atual}' inesperado na posição {self.pos}")

        return Token('EOF', '')