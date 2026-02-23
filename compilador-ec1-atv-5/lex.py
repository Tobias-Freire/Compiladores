from models.Token import Token, PONTUACOES, OPERADORES
from errors import LexicalError

from typing import IO, List, Tuple

class LexAnalyzer:
    """
    Classe responsável pela análise léxica de expressões.
    Lê o arquivo de entrada linha por linha e gera uma lista de tokens.
    """
    def __init__(self):
        """
        Inicializa o LexAnalyzer.
        """
        self.tokens: List[Token] = []
        self.errors: List[LexicalError] = []

    def analyze(self, source_code: IO) -> Tuple[List[Token], List[LexicalError]]:
        """
        Retorna a lista de tokens e a lista de erros encontrados.

        Returns:
            Tuple[List[Token], List[LexicalError]]: A lista de tokens e a lista de erros encontrados.
        """
        return self.get_tokens(source_code), self.errors

    def get_tokens(self, source_code: IO) -> List[Token]:
        """
        Analisa o arquivo de entrada linha por linha e gera uma lista de tokens.

        Returns:
            List[Token]: A lista de tokens encontrados no arquivo de entrada.
        """
        line_index = 0
        column_index = 0

        for line_index, line in enumerate(source_code):
            column_index = 0
            while column_index < len(line):
                char = line[column_index]

                if char.isdigit():
                    column_index = self._process_number(line, line_index, column_index)
                    continue
                
                elif char in PONTUACOES:
                    self._add_token(PONTUACOES[char]["tipo"], PONTUACOES[char]["lexema"], line_index, column_index)
                
                elif char in OPERADORES:
                    self._add_token(OPERADORES[char]["tipo"], OPERADORES[char]["lexema"], line_index, column_index)
                
                elif char == " " or char == "\n":
                    pass
                
                else:
                    self.errors.append(LexicalError(posicao=(line_index, column_index)))
                
                column_index += 1

        self.tokens.append(Token(PONTUACOES["EOF"]["tipo"], PONTUACOES["EOF"]["lexema"], (line_index, column_index)))
        return self.tokens

    def _process_number(self, line: str, line_index: int, start_index: int) -> int:
        """
        Extrai um token de número da linha começando em start_index.

        Args:
            line (str): A linha atual do código.
            line_index (int): O número da linha atual.
            start_index (int): O índice da coluna inicial do número.

        Returns:
            int: O novo índice da coluna após processar o número.
        """
        number = ""
        current_index = start_index
        while current_index < len(line) and line[current_index].isdigit():
            number += line[current_index]
            current_index += 1
        
        self.tokens.append(Token("NUMERO", number, (line_index, start_index)))
        return current_index

    def _add_token(self, token_type: str, lexeme: str, line_index: int, column_index: int):
        """
        Adiciona um token à lista de tokens.
        """
        self.tokens.append(Token(token_type, lexeme, (line_index, column_index)))