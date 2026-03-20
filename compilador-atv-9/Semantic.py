from Syntactic import Const, Var, OpBin, Decl, Programa

class AnalisadorSemantico:
    def __init__(self):
        # Tabela de símbolos: conjunto de nomes de variáveis declaradas
        self.tabela_simbolos = set()

    def verificar(self, programa):
        """Verifica o programa inteiro: declarações e expressão final."""
        for decl in programa.declaracoes:
            # Primeiro, verificar se a expressão da declaração usa apenas variáveis já declaradas
            self.verificar_expressao(decl.expressao)
            # Se passou, adicionar a variável à tabela de símbolos
            self.tabela_simbolos.add(decl.nome)

        # Verificar a expressão final (resultado)
        self.verificar_expressao(programa.resultado)

    def verificar_expressao(self, node):
        """Verifica recursivamente se todas as variáveis referenciadas foram declaradas."""
        if isinstance(node, Const):
            # Constantes não precisam de verificação
            return

        elif isinstance(node, Var):
            if node.nome not in self.tabela_simbolos:
                raise Exception(f"Erro semântico: variável '{node.nome}' não foi declarada")

        elif isinstance(node, OpBin):
            self.verificar_expressao(node.opEsq)
            self.verificar_expressao(node.opDir)
