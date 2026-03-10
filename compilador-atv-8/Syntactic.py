class Exp: pass

class Const(Exp):
    def __init__(self, valor):
        self.valor = int(valor)

class OpBin(Exp):
    def __init__(self, operador, opEsq, opDir):
        self.operador = operador
        self.opEsq = opEsq
        self.opDir = opDir

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.proximo_token()

    def comer(self, tipo):
        if self.token_atual.tipo == tipo:
            self.token_atual = self.lexer.proximo_token()
        else:
            raise Exception(f"Erro sintático: esperado {tipo}, recebido {self.token_atual.tipo}")

    # prim ::= num | '(' exp_a ')'
    def analisaPrim(self):
        tok = self.token_atual

        if tok.tipo == 'LITERAL_INTEIRO':
            self.comer('LITERAL_INTEIRO')
            return Const(tok.lexema)

        elif tok.tipo == 'ABRE_PARENTESE':
            self.comer('ABRE_PARENTESE')
            node = self.analisaExpA()
            self.comer('FECHA_PARENTESE')
            return node

        else:
            raise Exception("Erro sintático: esperado número ou '('")

    # exp_m ::= prim (('*' | '/') prim)*
    def analisaExpM(self):
        node = self.analisaPrim()

        while self.token_atual.tipo == 'OPERADOR' and self.token_atual.lexema in ('*', '/'):
            operador = self.token_atual.lexema
            self.comer('OPERADOR')
            direito = self.analisaPrim()
            node = OpBin(operador, node, direito)

        return node

    # exp_a ::= exp_m (('+' | '-') exp_m)*
    def analisaExpA(self):
        node = self.analisaExpM()

        while self.token_atual.tipo == 'OPERADOR' and self.token_atual.lexema in ('+', '-'):
            operador = self.token_atual.lexema
            self.comer('OPERADOR')
            direito = self.analisaExpM()
            node = OpBin(operador, node, direito)

        return node

    def parse(self):
        ast = self.analisaExpA()

        if self.token_atual.tipo != 'EOF':
            raise Exception("Erro sintático: conteúdo extra no final do arquivo")

        return ast