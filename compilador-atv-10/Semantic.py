from Syntactic import (
    Const, Var, OpBin,
    Decl, Programa,
    CmdAtrib, CmdIf, CmdWhile
)

class AnalisadorSemantico:
    def __init__(self):
        self.tabela_simbolos = set()

    # PROGRAMA
    def verificar(self, programa):
        # declarações
        for decl in programa.declaracoes:
            self.verificar_expressao(decl.expressao)
            self.tabela_simbolos.add(decl.nome)

        # comandos
        for cmd in programa.comandos:
            self.verificar_cmd(cmd)

        # return
        self.verificar_expressao(programa.retorno)

    # COMANDOS
    def verificar_cmd(self, cmd):
        if isinstance(cmd, CmdAtrib):
            # variável deve existir
            if cmd.nome not in self.tabela_simbolos:
                raise Exception(f"Erro semântico: variável '{cmd.nome}' não foi declarada")

            self.verificar_expressao(cmd.expressao)

        elif isinstance(cmd, CmdIf):
            self.verificar_expressao(cmd.cond)

            for c in cmd.then_cmds:
                self.verificar_cmd(c)

            for c in cmd.else_cmds:
                self.verificar_cmd(c)

        elif isinstance(cmd, CmdWhile):
            self.verificar_expressao(cmd.cond)

            for c in cmd.corpo:
                self.verificar_cmd(c)

    # EXPRESSÕES
    def verificar_expressao(self, node):
        if isinstance(node, Const):
            return

        elif isinstance(node, Var):
            if node.nome not in self.tabela_simbolos:
                raise Exception(f"Erro semântico: variável '{node.nome}' não foi declarada")

        elif isinstance(node, OpBin):
            self.verificar_expressao(node.opEsq)
            self.verificar_expressao(node.opDir)