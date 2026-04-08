from Syntactic import Const, Var, OpBin, ChamadaFuncao, CmdAtrib, CmdIf, CmdWhile, DeclFun, CmdReturn

class Generator:
    def __init__(self):
        self.instrucoes_main = []   # código do bloco main
        self.instrucoes_funs = []   # código das funções
        self.variaveis_globais = [] # nomes das variáveis globais (para .bss)
        self.label_count = 0

        # Contexto da função sendo gerada atualmente
        self._fun_params = []    # list[str]: nomes dos parâmetros na ordem
        self._fun_locals = []    # list[str]: nomes das vars locais na ordem
        self._fun_rbp_offset = {}  # nome -> offset relativo ao RBP
        self._epilogo_atual = None

    # ------------------------------------------------------------------
    # LABELS
    # ------------------------------------------------------------------
    def nova_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    # ------------------------------------------------------------------
    # PROGRAMA
    # ------------------------------------------------------------------
    def gera_programa(self, programa):
        # variáveis globais
        for decl in programa.decls_globais:
            self.variaveis_globais.append(decl.nome)

        # código das declarações globais (no main)
        for decl in programa.decls_globais:
            self.instrucoes_main.append(f"  # {decl.nome} = ...")
            self._gera_exp(decl.expressao, self.instrucoes_main)
            self.instrucoes_main.append(f"  mov %rax, {decl.nome}(%rip)")

        # comandos do main
        self._epilogo_atual = "end_main"
        self.instrucoes_main.append("  # comandos")
        for cmd in programa.comandos:
            self._gera_cmd(cmd, self.instrucoes_main)

        # return do main
        self.instrucoes_main.append("  # return")
        self._gera_exp(programa.retorno, self.instrucoes_main)
        self.instrucoes_main.append("end_main:")
        self._epilogo_atual = None

        # gerar código de cada função
        for fun in programa.decls_fun:
            self._gera_fun(fun)

    # ------------------------------------------------------------------
    # FUNÇÕES
    # ------------------------------------------------------------------
    def _gera_fun(self, fun):
        out = self.instrucoes_funs
        nome = fun.nome
        params = fun.params_formais      # list[str]
        locals_ = [d.nome for d in fun.vars_locais]  # list[str]
        nlocals = len(locals_)

        # ---- montar mapa de offsets ----
        # Layout da pilha após prólogo:
        #   RSP+0          .. RSP+(nlocals-1)*8   -> vars locais (índice 0..nlocals-1)
        #   RSP+nlocals*8                         -> RBP salvo
        #   RSP+(nlocals+1)*8                     -> endereço de retorno
        #   RSP+(nlocals+2)*8                     -> param[0]  (1º parâmetro)
        #   RSP+(nlocals+3)*8                     -> param[1]
        #   ...
        # Como RBP = RSP (após mov %rsp, %rbp):
        #   local[i]  -> RBP + i*8
        #   param[j]  -> RBP + (nlocals + 2 + j) * 8

        offsets = {}
        for i, nome_local in enumerate(locals_):
            offsets[nome_local] = i * 8
        for j, nome_param in enumerate(params):
            offsets[nome_param] = (nlocals + 2 + j) * 8

        self._fun_params = params
        self._fun_locals = locals_
        self._fun_rbp_offset = offsets

        # ---- prólogo ----
        label_epilogo = self.nova_label()
        self._epilogo_atual = label_epilogo
        out.append(f"{nome}:")
        out.append(f"  push %rbp")
        if nlocals > 0:
            out.append(f"  sub ${nlocals * 8}, %rsp")
        out.append(f"  mov %rsp, %rbp")

        # inicializar vars locais
        for decl in fun.vars_locais:
            out.append(f"  # {decl.nome} = ...")
            self._gera_exp(decl.expressao, out)
            off = offsets[decl.nome]
            out.append(f"  mov %rax, {off}(%rbp)")

        # comandos
        for cmd in fun.comandos:
            self._gera_cmd(cmd, out)

        # expressão de retorno
        out.append(f"  # return")
        self._gera_exp(fun.retorno, out)

        # ---- epílogo ----
        out.append(f"{label_epilogo}:")
        if nlocals > 0:
            out.append(f"  add ${nlocals * 8}, %rsp")
        out.append(f"  pop %rbp")
        out.append(f"  ret")
        out.append("")  # linha em branco para legibilidade

        # limpar contexto
        self._fun_params = []
        self._fun_locals = []
        self._fun_rbp_offset = {}

    # ------------------------------------------------------------------
    # COMANDOS
    # ------------------------------------------------------------------
    def _gera_cmd(self, cmd, out):
        if isinstance(cmd, CmdAtrib):
            out.append(f"  # {cmd.nome} = ...")
            self._gera_exp(cmd.expressao, out)
            self._gera_store(cmd.nome, out)

        elif isinstance(cmd, CmdReturn):
            out.append(f"  # return (early)")
            self._gera_exp(cmd.expressao, out)
            if self._epilogo_atual:
                out.append(f"  jmp {self._epilogo_atual}")

        elif isinstance(cmd, CmdIf):
            label_else = self.nova_label()
            label_end = self.nova_label()

            self._gera_exp(cmd.cond, out)
            out.append("  cmp $0, %rax")
            out.append(f"  jz {label_else}")

            for c in cmd.then_cmds:
                self._gera_cmd(c, out)
            out.append(f"  jmp {label_end}")

            out.append(f"{label_else}:")
            for c in cmd.else_cmds:
                self._gera_cmd(c, out)

            out.append(f"{label_end}:")

        elif isinstance(cmd, CmdWhile):
            label_inicio = self.nova_label()
            label_fim = self.nova_label()

            out.append(f"{label_inicio}:")
            self._gera_exp(cmd.cond, out)
            out.append("  cmp $0, %rax")
            out.append(f"  jz {label_fim}")

            for c in cmd.corpo:
                self._gera_cmd(c, out)

            out.append(f"  jmp {label_inicio}")
            out.append(f"{label_fim}:")

    # ------------------------------------------------------------------
    # EXPRESSÕES
    # ------------------------------------------------------------------
    def _gera_exp(self, node, out):
        if isinstance(node, Const):
            out.append(f"  mov ${node.valor}, %rax")

        elif isinstance(node, Var):
            self._gera_load(node.nome, out)

        elif isinstance(node, ChamadaFuncao):
            self._gera_chamada(node, out)

        elif isinstance(node, OpBin):
            # Avalia direito primeiro, depois esquerdo
            self._gera_exp(node.opDir, out)
            out.append("  push %rax")
            self._gera_exp(node.opEsq, out)
            out.append("  pop %rbx")

            if node.operador == '+':
                out.append("  add %rbx, %rax")
            elif node.operador == '-':
                out.append("  sub %rbx, %rax")
            elif node.operador == '*':
                out.append("  imul %rbx, %rax")
            elif node.operador == '/':
                out.append("  cqo")
                out.append("  idiv %rbx")
            elif node.operador == '%':
                out.append("  cqo")
                out.append("  idiv %rbx")
                out.append("  mov %rdx, %rax")
            elif node.operador in ('<', '>', '<=', '>=', '==', '!='):
                out.append("  cmp %rbx, %rax")
                if node.operador == '<':
                    out.append("  setl %al")
                elif node.operador == '>':
                    out.append("  setg %al")
                elif node.operador == '<=':
                    out.append("  setle %al")
                elif node.operador == '>=':
                    out.append("  setge %al")
                elif node.operador == '==':
                    out.append("  sete %al")
                elif node.operador == '!=':
                    out.append("  setne %al")
                out.append("  movzb %al, %rax")

    def _gera_chamada(self, node, out):
        """Gera código para chamada de função."""
        # empilhar parâmetros na ordem inversa
        for param in reversed(node.params):
            self._gera_exp(param, out)
            out.append("  push %rax")

        out.append(f"  call {node.nome}")

        # remover parâmetros da pilha
        n = len(node.params)
        if n > 0:
            out.append(f"  add ${n * 8}, %rsp")
        # resultado fica em %rax

    # ------------------------------------------------------------------
    # ACESSO A VARIÁVEIS (load / store)
    # ------------------------------------------------------------------
    def _is_local(self, nome):
        return nome in self._fun_rbp_offset

    def _gera_load(self, nome, out):
        if self._is_local(nome):
            off = self._fun_rbp_offset[nome]
            out.append(f"  mov {off}(%rbp), %rax")
        else:
            out.append(f"  mov {nome}(%rip), %rax")

    def _gera_store(self, nome, out):
        if self._is_local(nome):
            off = self._fun_rbp_offset[nome]
            out.append(f"  mov %rax, {off}(%rbp)")
        else:
            out.append(f"  mov %rax, {nome}(%rip)")

    # ------------------------------------------------------------------
    # SAÍDA
    # ------------------------------------------------------------------
    def get_codigo_bss(self):
        linhas = []
        for var in self.variaveis_globais:
            linhas.append(f"  .lcomm {var}, 8")
        return "\n".join(linhas)

    def get_codigo_main(self):
        return "\n".join(self.instrucoes_main)

    def get_codigo_funs(self):
        return "\n".join(self.instrucoes_funs)
