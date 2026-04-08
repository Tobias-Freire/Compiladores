# NÓS DA AST

class Exp:
    pass

class Const(Exp):
    def __init__(self, valor):
        self.valor = int(valor)

class Var(Exp):
    def __init__(self, nome):
        self.nome = nome

class ChamadaFuncao(Exp):
    def __init__(self, nome, params):
        self.nome = nome      # str: nome da função
        self.params = params  # list[Exp]: parâmetros reais

class OpBin(Exp):
    def __init__(self, operador, opEsq, opDir):
        self.operador = operador
        self.opEsq = opEsq
        self.opDir = opDir


# DECLARAÇÕES
class DeclVar:
    def __init__(self, nome, expressao):
        self.nome = nome
        self.expressao = expressao

class DeclFun:
    def __init__(self, nome, params_formais, vars_locais, comandos, retorno):
        self.nome = nome                  # str
        self.params_formais = params_formais  # list[str]
        self.vars_locais = vars_locais    # list[DeclVar]
        self.comandos = comandos          # list[Cmd]
        self.retorno = retorno            # Exp


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
    def __init__(self, decls_globais, decls_fun, comandos, retorno):
        self.decls_globais = decls_globais  # list[DeclVar]
        self.decls_fun = decls_fun          # list[DeclFun]
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
            raise Exception(f"Erro sintático: esperado {tipo}, recebido '{self.token_atual.lexema}' ({self.token_atual.tipo})")

    # EXPRESSÕES
    def analisaPrim(self):
        tok = self.token_atual

        if tok.tipo == 'LITERAL_INTEIRO':
            self.comer('LITERAL_INTEIRO')
            return Const(tok.lexema)

        elif tok.tipo == 'IDENTIFICADOR':
            self.comer('IDENTIFICADOR')
            # diferenciar variável de chamada de função
            if self.token_atual.tipo == 'ABRE_PARENTESE':
                return self.analisaChamadaFuncao(tok.lexema)
            return Var(tok.lexema)

        elif tok.tipo == 'ABRE_PARENTESE':
            self.comer('ABRE_PARENTESE')
            node = self.analisaExp()
            self.comer('FECHA_PARENTESE')
            return node

        else:
            raise Exception(f"Erro sintático: expressão primária esperada, recebido '{tok.lexema}' ({tok.tipo})")

    def analisaChamadaFuncao(self, nome):
        """Analisa a lista de parâmetros reais de uma chamada de função."""
        self.comer('ABRE_PARENTESE')
        params = []
        while self.token_atual.tipo != 'FECHA_PARENTESE' and self.token_atual.tipo != 'EOF':
            params.append(self.analisaExp())
            if self.token_atual.tipo == 'VIRGULA':
                self.comer('VIRGULA')
        self.comer('FECHA_PARENTESE')
        return ChamadaFuncao(nome, params)

    def analisaExpM(self):
        node = self.analisaPrim()
        while self.token_atual.tipo == 'OPERADOR' and self.token_atual.lexema in ('*', '/', '%'):
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

    def analisaExp(self):
        node = self.analisaExpA()
        if self.token_atual.tipo == 'OP_COMPARACAO':
            op = self.token_atual.lexema
            self.comer('OP_COMPARACAO')
            direito = self.analisaExpA()
            node = OpBin(op, node, direito)
        return node

    # DECLARAÇÃO DE VARIÁVEL  (var ident = exp ;)
    def analisaDeclVar(self):
        self.comer('VAR')
        nome = self.comer('IDENTIFICADOR').lexema
        self.comer('IGUAL')
        exp = self.analisaExp()
        self.comer('PONTO_VIRGULA')
        return DeclVar(nome, exp)

    # DECLARAÇÃO DE FUNÇÃO
    def analisaDeclFun(self):
        self.comer('FUN')
        nome = self.comer('IDENTIFICADOR').lexema
        self.comer('ABRE_PARENTESE')
        params_formais = self.analisaListaParamsFormais()
        self.comer('FECHA_PARENTESE')
        self.comer('ABRE_CHAVE')

        # variáveis locais
        vars_locais = []
        while self.token_atual.tipo == 'VAR':
            vars_locais.append(self.analisaDeclVar())

        # comandos
        comandos = []
        while self.token_atual.tipo not in ('RETURN', 'EOF'):
            comandos.append(self.analisaCmd())

        self.comer('RETURN')
        retorno = self.analisaExp()
        self.comer('PONTO_VIRGULA')
        self.comer('FECHA_CHAVE')

        return DeclFun(nome, params_formais, vars_locais, comandos, retorno)

    def analisaListaParamsFormais(self):
        """Retorna lista de nomes (str) dos parâmetros formais."""
        params = []
        while self.token_atual.tipo != 'FECHA_PARENTESE' and self.token_atual.tipo != 'EOF':
            if self.token_atual.tipo == 'IDENTIFICADOR':
                params.append(self.comer('IDENTIFICADOR').lexema)
                if self.token_atual.tipo == 'VIRGULA':
                    self.comer('VIRGULA')
            else:
                raise Exception(f"Erro sintático: identificador esperado na lista de parâmetros, recebido '{self.token_atual.lexema}'")
        return params

    # COMANDOS
    def analisaCmd(self):
        if self.token_atual.tipo == 'IDENTIFICADOR':
            nome = self.comer('IDENTIFICADOR').lexema
            if self.token_atual.tipo == 'IGUAL':
                self.comer('IGUAL')
                exp = self.analisaExp()
                self.comer('PONTO_VIRGULA')
                return CmdAtrib(nome, exp)
            elif self.token_atual.tipo == 'OP_ATRIB_COMPOSTA':
                op_composto = self.comer('OP_ATRIB_COMPOSTA').lexema
                op_simples = op_composto[0]
                exp = self.analisaExp()
                self.comer('PONTO_VIRGULA')
                return CmdAtrib(nome, OpBin(op_simples, Var(nome), exp))
            else:
                raise Exception(f"Erro sintático: operacao de atribuicao esperada, recebido '{self.token_atual.lexema}' ({self.token_atual.tipo})")

        elif self.token_atual.tipo == 'RETURN':
            self.comer('RETURN')
            exp = self.analisaExp()
            self.comer('PONTO_VIRGULA')
            return CmdReturn(exp)

        elif self.token_atual.tipo == 'IF':
            return self.analisaIf()

        elif self.token_atual.tipo == 'WHILE':
            return self.analisaWhile()

        else:
            raise Exception(f"Erro sintático: comando esperado, recebido '{self.token_atual.lexema}' ({self.token_atual.tipo})")

    def analisaBloco(self):
        self.comer('ABRE_CHAVE')
        comandos = []
        while self.token_atual.tipo not in ('FECHA_CHAVE', 'EOF'):
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
        decls_globais = []
        decls_fun = []

        # sequência de declarações (var ou fun) até 'main'
        while self.token_atual.tipo not in ('MAIN', 'EOF'):
            if self.token_atual.tipo == 'VAR':
                decls_globais.append(self.analisaDeclVar())
            elif self.token_atual.tipo == 'FUN':
                decls_fun.append(self.analisaDeclFun())
            else:
                raise Exception(f"Erro sintático: declaração esperada (var ou fun), recebido '{self.token_atual.lexema}'")

        self.comer('MAIN')
        self.comer('ABRE_CHAVE')

        comandos = []
        while self.token_atual.tipo not in ('RETURN', 'EOF'):
            comandos.append(self.analisaCmd())

        self.comer('RETURN')
        retorno = self.analisaExp()
        self.comer('PONTO_VIRGULA')
        self.comer('FECHA_CHAVE')

        if self.token_atual.tipo != 'EOF':
            raise Exception("Erro: conteúdo extra após o bloco main")

        return Programa(decls_globais, decls_fun, comandos, retorno)
