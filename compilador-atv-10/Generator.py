from Syntactic import Const, Var, OpBin, CmdAtrib, CmdIf, CmdWhile

class Generator:
    def __init__(self):
        self.instrucoes = []
        self.variaveis = []
        self.label_count = 0  #contador de labels

    # LABELS
    def nova_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    # PROGRAMA
    def gera_programa(self, programa):
        # coletar variáveis
        for decl in programa.declaracoes:
            self.variaveis.append(decl.nome)

        # declarações
        for decl in programa.declaracoes:
            self.instrucoes.append(f"  # {decl.nome} = ...")
            self.gera_exp(decl.expressao)
            self.instrucoes.append(f"  mov %rax, {decl.nome}")

        # comandos
        self.instrucoes.append("  # comandos")
        for cmd in programa.comandos:
            self.gera_cmd(cmd)

        # return
        self.instrucoes.append("  # return")
        self.gera_exp(programa.retorno)

    # COMANDOS
    def gera_cmd(self, cmd):
        if isinstance(cmd, CmdAtrib):
            self.instrucoes.append(f"  # {cmd.nome} = ...")
            self.gera_exp(cmd.expressao)
            self.instrucoes.append(f"  mov %rax, {cmd.nome}")

        elif isinstance(cmd, CmdIf):
            label_else = self.nova_label()
            label_end = self.nova_label()

            # condição
            self.gera_exp(cmd.cond)
            self.instrucoes.append("  cmp $0, %rax")
            self.instrucoes.append(f"  jz {label_else}")

            # THEN
            for c in cmd.then_cmds:
                self.gera_cmd(c)

            self.instrucoes.append(f"  jmp {label_end}")

            # ELSE
            self.instrucoes.append(f"{label_else}:")
            for c in cmd.else_cmds:
                self.gera_cmd(c)

            self.instrucoes.append(f"{label_end}:")

        elif isinstance(cmd, CmdWhile):
            label_inicio = self.nova_label()
            label_fim = self.nova_label()

            self.instrucoes.append(f"{label_inicio}:")

            # condição
            self.gera_exp(cmd.cond)
            self.instrucoes.append("  cmp $0, %rax")
            self.instrucoes.append(f"  jz {label_fim}")

            # corpo
            for c in cmd.corpo:
                self.gera_cmd(c)

            self.instrucoes.append(f"  jmp {label_inicio}")
            self.instrucoes.append(f"{label_fim}:")

    # EXPRESSÕES
    def gera_exp(self, node):
        if isinstance(node, Const):
            self.instrucoes.append(f"  mov ${node.valor}, %rax")

        elif isinstance(node, Var):
            self.instrucoes.append(f"  mov {node.nome}, %rax")

        elif isinstance(node, OpBin):
            # direito
            self.gera_exp(node.opDir)
            self.instrucoes.append("  push %rax")

            # esquerdo
            self.gera_exp(node.opEsq)
            self.instrucoes.append("  pop %rbx")

            # aritméticos
            if node.operador == '+':
                self.instrucoes.append("  add %rbx, %rax")

            elif node.operador == '-':
                self.instrucoes.append("  sub %rbx, %rax")

            elif node.operador == '*':
                self.instrucoes.append("  imul %rbx, %rax")

            elif node.operador == '/':
                self.instrucoes.append("  cqo")
                self.instrucoes.append("  idiv %rbx")

            # 🔥 COMPARAÇÕES
            elif node.operador in ('<', '>', '=='):
                self.instrucoes.append("  cmp %rbx, %rax")

                if node.operador == '<':
                    self.instrucoes.append("  setl %al")
                elif node.operador == '>':
                    self.instrucoes.append("  setg %al")
                elif node.operador == '==':
                    self.instrucoes.append("  sete %al")

                self.instrucoes.append("  movzb %al, %rax")

    # BSS
    def get_codigo_bss(self):
        linhas = []
        for var in self.variaveis:
            linhas.append(f"  .lcomm {var}, 8")
        return "\n".join(linhas)

    # TEXT
    def get_codigo_text(self):
        return "\n".join(self.instrucoes)