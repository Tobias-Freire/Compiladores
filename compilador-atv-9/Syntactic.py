class Exp:
    """Classe base para expressões."""
    pass

class Const(Exp):
    """Constante inteira."""
    def __init__(self, valor):
        self.valor = int(valor)

class Var(Exp):
    """Referência a uma variável."""
    def __init__(self, nome):
        self.nome = nome

class OpBin(Exp):
    """Operação binária."""
    def __init__(self, operador, opEsq, opDir):
        self.operador = operador
        self.opEsq = opEsq
        self.opDir = opDir

class Decl:
    """Declaração de variável: nome = expressão;"""
    def __init__(self, nome, expressao):
        self.nome = nome
        self.expressao = expressao

class Programa:
    """Nó raiz: lista de declarações + expressão final."""
    def __init__(self, declaracoes, resultado):
        self.declaracoes = declaracoes
        self.resultado = resultado

# ==========================================
# Parser (Analisador Sintático)
# ==========================================

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.proximo_token()

    def comer(self, tipo):
        if self.token_atual.tipo == tipo:
            tok = self.token_atual
            self.token_atual = self.lexer.proximo_token()
            return tok
        else:
            raise Exception(f"Erro sintático: esperado {tipo}, recebido {self.token_atual.tipo} ('{self.token_atual.lexema}')")

    # <prim> ::= <num> | <ident> | '(' <exp> ')'
    def analisaPrim(self):
        tok = self.token_atual

        if tok.tipo == 'LITERAL_INTEIRO':
            self.comer('LITERAL_INTEIRO')
            return Const(tok.lexema)

        elif tok.tipo == 'IDENTIFICADOR':
            self.comer('IDENTIFICADOR')
            return Var(tok.nome if hasattr(tok, 'nome') else tok.lexema)

        elif tok.tipo == 'ABRE_PARENTESE':
            self.comer('ABRE_PARENTESE')
            node = self.analisaExpA()
            self.comer('FECHA_PARENTESE')
            return node

        else:
            raise Exception(f"Erro sintático: esperado número, identificador ou '(', recebido {tok.tipo}")

    # <exp_m> ::= <prim> (('*' | '/') <prim>)*
    def analisaExpM(self):
        node = self.analisaPrim()

        while self.token_atual.tipo == 'OPERADOR' and self.token_atual.lexema in ('*', '/'):
            operador = self.token_atual.lexema
            self.comer('OPERADOR')
            direito = self.analisaPrim()
            node = OpBin(operador, node, direito)

        return node

    # <exp_a> ::= <exp_m> (('+' | '-') <exp_m>)*
    def analisaExpA(self):
        node = self.analisaExpM()

        while self.token_atual.tipo == 'OPERADOR' and self.token_atual.lexema in ('+', '-'):
            operador = self.token_atual.lexema
            self.comer('OPERADOR')
            direito = self.analisaExpM()
            node = OpBin(operador, node, direito)

        return node

    # <decl> ::= <ident> '=' <exp> ';'
    def analisaDecl(self):
        tok_nome = self.comer('IDENTIFICADOR')
        self.comer('IGUAL')
        expressao = self.analisaExpA()
        self.comer('PONTO_VIRGULA')
        return Decl(tok_nome.lexema, expressao)

    # <result> ::= '=' <exp>
    def analisaResult(self):
        self.comer('IGUAL')
        return self.analisaExpA()

    # <programa> ::= <decl>* <result>
    def parse(self):
        declaracoes = []

        # Enquanto o token atual for um IDENTIFICADOR, reconhecer uma declaração
        while self.token_atual.tipo == 'IDENTIFICADOR':
            dec = self.analisaDecl()
            declaracoes.append(dec)

        # A expressão final deve começar com '='
        if self.token_atual.tipo != 'IGUAL':
            raise Exception(f"Erro sintático: esperado '=' para expressão final, recebido {self.token_atual.tipo}")

        resultado = self.analisaResult()

        if self.token_atual.tipo != 'EOF':
            raise Exception("Erro sintático: conteúdo extra no final do arquivo")

        return Programa(declaracoes, resultado)
