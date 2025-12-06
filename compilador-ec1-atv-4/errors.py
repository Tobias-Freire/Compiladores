class LexicalError:
    def __init__(self, posicao: tuple[int, int], mensagem: str = "Caractere inválido"):
        self.mensagem = mensagem
        self.posicao = posicao

    def show(self):
        print(f"LexicalError: {self.mensagem}. Linha {self.posicao[0]} e coluna {self.posicao[1]}")