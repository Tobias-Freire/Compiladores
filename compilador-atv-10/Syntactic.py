
# NÓS DA AST

class Exp:
    pass

class Const(Exp):
    def __init__(self, valor):
        self.valor = int(valor)

class Var(Exp):
    def __init__(self, nome):
        self.nome = nome

class OpBin(Exp):
    def __init__(self, operador, opEsq, opDir):
        self.operador = operador
        self.opEsq = opEsq
        self.opDir = opDir


# DECLARAÇÃO
class Decl:
    def __init__(self, nome, expressao):
        self.nome = nome
        self.expressao = expressao


# COMANDOS
class Cmd:
    pass

class CmdAtrib(Cmd):
    def __init__(self, nome, expressao):
        self.nome = nome
        self.expressao = expressao

class CmdIf(Cmd):
    def __init__(self, cond, then_cmds, else_cmds):
        self.cond = cond
        self.then_cmds = then_cmds
        self.else_cmds = else_cmds

class CmdWhile(Cmd):
    def __init__(self, cond, corpo):
        self.cond = cond
        self.corpo = corpo

class CmdReturn(Cmd):
    def __init__(self, expressao):
        self.expressao = expressao


# PROGRAMA
class Programa:
    def __init__(self, declaracoes, comandos, retorno):
        self.declaracoes = declaracoes
        self.comandos = comandos
        self.retorno = retorno


# PARSER
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
            raise Exception(f"Erro sintático: esperado {tipo}, recebido {self.token_atual.tipo}")

    # EXPRESSÕES
    def analisaPrim(self):
        tok = self.token_atual

        if tok.tipo == 'LITERAL_INTEIRO':
            self.comer('LITERAL_INTEIRO')
            return Const(tok.lexema)

        elif tok.tipo == 'IDENTIFICADOR':
            self.comer('IDENTIFICADOR')
            return Var(tok.lexema)

        elif tok.tipo == 'ABRE_PARENTESE':
            self.comer('ABRE_PARENTESE')
            node = self.analisaExp()
            self.comer('FECHA_PARENTESE')
            return node

        else:
            raise Exception("Erro sintático")

    def analisaExpM(self):
        node = self.analisaPrim()

        while self.token_atual.tipo == 'OPERADOR' and self.token_atual.lexema in ('*', '/'):
            op = self.token_atual.lexema
            self.comer('OPERADOR')
            node = OpBin(op, node, self.analisaPrim())

        return node

    def analisaExpA(self):
        node = self.analisaExpM()

        while self.token_atual.tipo == 'OPERADOR' and self.token_atual.lexema in ('+', '-'):
            op = self.token_atual.lexema
            self.comer('OPERADOR')
            node = OpBin(op, node, self.analisaExpM())

        return node

    #  NOVO: comparação
    def analisaExp(self):
        node = self.analisaExpA()

        if self.token_atual.tipo == 'OP_COMPARACAO':
            op = self.token_atual.lexema
            self.comer('OP_COMPARACAO')
            direito = self.analisaExpA()
            node = OpBin(op, node, direito)

        return node

    # DECLARAÇÃO
    def analisaDecl(self):
        nome = self.comer('IDENTIFICADOR').lexema
        self.comer('IGUAL')
        exp = self.analisaExp()
        self.comer('PONTO_VIRGULA')
        return Decl(nome, exp)

    # COMANDOS
    def analisaCmd(self):
        if self.token_atual.tipo == 'IDENTIFICADOR':
            nome = self.comer('IDENTIFICADOR').lexema
            self.comer('IGUAL')
            exp = self.analisaExp()
            self.comer('PONTO_VIRGULA')
            return CmdAtrib(nome, exp)

        elif self.token_atual.tipo == 'IF':
            return self.analisaIf()

        elif self.token_atual.tipo == 'WHILE':
            return self.analisaWhile()

        else:
            raise Exception("Erro sintático")

    def analisaBloco(self):
        self.comer('ABRE_CHAVE')
        comandos = []

        while self.token_atual.tipo not in ('FECHA_CHAVE', 'RETURN'):
            comandos.append(self.analisaCmd())

        return comandos

    def analisaIf(self):
        self.comer('IF')
        cond = self.analisaExp()

        then_cmds = self.analisaBloco()
        self.comer('FECHA_CHAVE')

        self.comer('ELSE')
        else_cmds = self.analisaBloco()
        self.comer('FECHA_CHAVE')

        return CmdIf(cond, then_cmds, else_cmds)

    def analisaWhile(self):
        self.comer('WHILE')
        cond = self.analisaExp()

        corpo = self.analisaBloco()
        self.comer('FECHA_CHAVE')

        return CmdWhile(cond, corpo)

    # PROGRAMA
    def parse(self):
        declaracoes = []

        while self.token_atual.tipo == 'IDENTIFICADOR':
            declaracoes.append(self.analisaDecl())

        self.comer('ABRE_CHAVE')

        comandos = []
        while self.token_atual.tipo != 'RETURN':
            comandos.append(self.analisaCmd())

        self.comer('RETURN')
        retorno = self.analisaExp()
        self.comer('PONTO_VIRGULA')

        self.comer('FECHA_CHAVE')

        if self.token_atual.tipo != 'EOF':
            raise Exception("Erro: conteúdo extra")

        return Programa(declaracoes, comandos, retorno)