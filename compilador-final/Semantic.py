from Syntactic import (
    Const, Var, OpBin, ChamadaFuncao,
    DeclVar, DeclFun, Programa,
    CmdAtrib, CmdIf, CmdWhile, CmdReturn
)

class AnalisadorSemantico:
    def __init__(self):
        # tabela global: nome -> {'tipo': 'var'} ou {'tipo': 'fun', 'nparams': N, 'locals': set}
        self.tabela_global = {}
        self.tabela_local = None   # set de nomes visíveis dentro da função atual
        self.nome_funcao_atual = None  # para permitir recursão direta

    # -----------------------------------------------------------------
    # PROGRAMA
    # -----------------------------------------------------------------
    def verificar(self, programa):
        # 1) registrar variáveis globais
        for decl in programa.decls_globais:
            self.verificar_expressao(decl.expressao)
            self.tabela_global[decl.nome] = {'tipo': 'var'}

        # 2) registrar e verificar funções
        for fun in programa.decls_fun:
            # pré-registrar para permitir recursão direta
            self.tabela_global[fun.nome] = {
                'tipo': 'fun',
                'nparams': len(fun.params_formais),
                'locals': set()
            }
            self._verificar_fun(fun)

        # 3) bloco main
        for cmd in programa.comandos:
            self.verificar_cmd(cmd)
        self.verificar_expressao(programa.retorno)

    def _verificar_fun(self, fun):
        """Verifica o corpo de uma função usando tabela local."""
        self.nome_funcao_atual = fun.nome

        # tabela local = parâmetros + vars locais
        local = set(fun.params_formais)

        for decl in fun.vars_locais:
            # a expressão inicial pode referenciar parâmetros e vars já declaradas
            self._verificar_expressao_fun(decl.expressao, local)
            local.add(decl.nome)

        # atualizar locals na tabela global
        self.tabela_global[fun.nome]['locals'] = local

        self.tabela_local = local
        for cmd in fun.comandos:
            self._verificar_cmd_fun(cmd)
        self._verificar_expressao_fun(fun.retorno, local)

        self.tabela_local = None
        self.nome_funcao_atual = None

    # -----------------------------------------------------------------
    # Resolução de nome (local tem prioridade sobre global)
    # -----------------------------------------------------------------
    def _resolve_var(self, nome, tabela_local=None):
        """Retorna True se nome é uma variável visível no contexto."""
        if tabela_local and nome in tabela_local:
            return True
        if nome in self.tabela_global and self.tabela_global[nome]['tipo'] == 'var':
            return True
        return False

    # -----------------------------------------------------------------
    # Verificação dentro de funções
    # -----------------------------------------------------------------
    def _verificar_expressao_fun(self, node, local):
        if isinstance(node, Const):
            return
        elif isinstance(node, Var):
            if not self._resolve_var(node.nome, local):
                raise Exception(f"Erro semântico: variável '{node.nome}' não declarada")
        elif isinstance(node, OpBin):
            self._verificar_expressao_fun(node.opEsq, local)
            self._verificar_expressao_fun(node.opDir, local)
        elif isinstance(node, ChamadaFuncao):
            self._verificar_chamada(node)

    def _verificar_cmd_fun(self, cmd):
        if isinstance(cmd, CmdAtrib):
            if not self._resolve_var(cmd.nome, self.tabela_local):
                raise Exception(f"Erro semântico: variável '{cmd.nome}' não declarada")
            self._verificar_expressao_fun(cmd.expressao, self.tabela_local)
        elif isinstance(cmd, CmdIf):
            self._verificar_expressao_fun(cmd.cond, self.tabela_local)
            for c in cmd.then_cmds:
                self._verificar_cmd_fun(c)
            for c in cmd.else_cmds:
                self._verificar_cmd_fun(c)
        elif isinstance(cmd, CmdWhile):
            self._verificar_expressao_fun(cmd.cond, self.tabela_local)
            for c in cmd.corpo:
                self._verificar_cmd_fun(c)
        elif isinstance(cmd, CmdReturn):
            self._verificar_expressao_fun(cmd.expressao, self.tabela_local)

    # -----------------------------------------------------------------
    # Verificação no escopo global (bloco main)
    # -----------------------------------------------------------------
    def verificar_cmd(self, cmd):
        if isinstance(cmd, CmdAtrib):
            if cmd.nome not in self.tabela_global or self.tabela_global[cmd.nome]['tipo'] != 'var':
                raise Exception(f"Erro semântico: variável '{cmd.nome}' não declarada")
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
        elif isinstance(cmd, CmdReturn):
            self.verificar_expressao(cmd.expressao)

    def verificar_expressao(self, node):
        if isinstance(node, Const):
            return
        elif isinstance(node, Var):
            if node.nome not in self.tabela_global or self.tabela_global[node.nome]['tipo'] != 'var':
                raise Exception(f"Erro semântico: variável '{node.nome}' não declarada")
        elif isinstance(node, OpBin):
            self.verificar_expressao(node.opEsq)
            self.verificar_expressao(node.opDir)
        elif isinstance(node, ChamadaFuncao):
            self._verificar_chamada(node)

    def _verificar_chamada(self, node):
        if node.nome not in self.tabela_global:
            raise Exception(f"Erro semântico: função '{node.nome}' não declarada")
        entrada = self.tabela_global[node.nome]
        if entrada['tipo'] != 'fun':
            raise Exception(f"Erro semântico: '{node.nome}' não é uma função")
        if len(node.params) != entrada['nparams']:
            raise Exception(
                f"Erro semântico: função '{node.nome}' espera {entrada['nparams']} parâmetro(s), "
                f"recebeu {len(node.params)}"
            )
        # verificar cada parâmetro real
        for p in node.params:
            if self.tabela_local is not None:
                self._verificar_expressao_fun(p, self.tabela_local)
            else:
                self.verificar_expressao(p)
