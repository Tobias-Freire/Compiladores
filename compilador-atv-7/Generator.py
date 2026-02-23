from Syntactic import Const, OpBin

class Generator:
    def __init__(self):
        self.instrucoes = []

    def gera(self, node):
        if isinstance(node, Const):
            self.instrucoes.append(f"  mov ${node.valor}, %rax")
        
        elif isinstance(node, OpBin):
            # 1. Incluir o código gerado para o operando direito
            self.gera(node.opDir)
            # 2. Salvar RAX na pilha
            self.instrucoes.append("  push %rax")
            # 3. Incluir o código gerado para o operando esquerdo
            self.gera(node.opEsq)
            # 4. Desempilhar o resultado do lado direito em RBX
            self.instrucoes.append("  pop %rbx")
            
            # 5. Executar a operação adequada em RAX
            if node.operador == '+':
                self.instrucoes.append("  add %rbx, %rax")
            elif node.operador == '-':
                self.instrucoes.append("  sub %rbx, %rax")
            elif node.operador == '*':
                self.instrucoes.append("  imul %rbx, %rax")
            elif node.operador == '/':
                self.instrucoes.append("  cqo") # Extende o sinal de RAX para RDX:RAX (necessário no x86-64)
                self.instrucoes.append("  idiv %rbx")

    def get_codigo(self):
        return "\n".join(self.instrucoes)