from Syntactic import Const, Var, OpBin

class Generator:
    def __init__(self):
        self.instrucoes = []      # Código da seção .text
        self.variaveis = []       # Nomes das variáveis (para seção .bss)

    def gera_programa(self, programa):
        """Gera código para o programa inteiro (declarações + resultado)."""
        # 1. Coletar todas as variáveis declaradas
        for decl in programa.declaracoes:
            self.variaveis.append(decl.nome)

        # 2. Gerar código para cada declaração
        for decl in programa.declaracoes:
            self.instrucoes.append(f"  # {decl.nome} = ...")
            self.gera_exp(decl.expressao)
            self.instrucoes.append(f"  mov %rax, {decl.nome}")

        # 3. Gerar código para a expressão final (resultado)
        self.instrucoes.append("  # = expressao final")
        self.gera_exp(programa.resultado)

    def gera_exp(self, node):
        """Gera código para uma expressão (recursivamente)."""
        if isinstance(node, Const):
            self.instrucoes.append(f"  mov ${node.valor}, %rax")

        elif isinstance(node, Var):
            self.instrucoes.append(f"  mov {node.nome}, %rax")

        elif isinstance(node, OpBin):
            # 1. Código para o operando direito
            self.gera_exp(node.opDir)
            # 2. Salvar RAX na pilha
            self.instrucoes.append("  push %rax")
            # 3. Código para o operando esquerdo
            self.gera_exp(node.opEsq)
            # 4. Desempilhar o resultado do lado direito em RBX
            self.instrucoes.append("  pop %rbx")

            # 5. Executar a operação adequada
            if node.operador == '+':
                self.instrucoes.append("  add %rbx, %rax")
            elif node.operador == '-':
                self.instrucoes.append("  sub %rbx, %rax")
            elif node.operador == '*':
                self.instrucoes.append("  imul %rbx, %rax")
            elif node.operador == '/':
                self.instrucoes.append("  cqo")
                self.instrucoes.append("  idiv %rbx")

    def get_codigo_bss(self):
        """Retorna as diretivas .lcomm para a seção BSS."""
        linhas = []
        for var in self.variaveis:
            linhas.append(f"  .lcomm {var}, 8")
        return "\n".join(linhas)

    def get_codigo_text(self):
        """Retorna o código assembly gerado para a seção TEXT."""
        return "\n".join(self.instrucoes)
