"""
Testes automatizados para o analisador léxico da linguagem EC1.

Cobertura de testes:
1. Expressões com diferentes tipos de espaços em branco (espaços, tabs, newlines)
2. Tokens numéricos
3. Operadores (+, -, *, /)
4. Pontuações (parênteses)
5. Detecção de erros léxicos (caracteres inválidos)

Executar com: python3 -m unittest test_lexer -v
"""

import unittest
from io import StringIO
from lex import LexAnalyzer


def format_tokens(tokens):
    """Formata tokens para comparação de output."""
    return [f"<{t.tipo}, '{t.lexema}', {t.posicao}>" for t in tokens]


def format_errors(errors):
    """Formata erros para comparação."""
    return [f"LexicalError: {e.mensagem}. Linha {e.posicao[0]} e coluna {e.posicao[1]}" for e in errors]


class TestWhitespaceHandling(unittest.TestCase):
    """Testes para diferentes tipos de espaços em branco."""

    def test_single_space_between_tokens(self):
        """Testa espaço simples entre tokens."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1 + 2"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].tipo, "NUMERO")
        self.assertEqual(tokens[0].lexema, "1")
        self.assertEqual(tokens[1].tipo, "ADICAO")
        self.assertEqual(tokens[2].tipo, "NUMERO")
        self.assertEqual(tokens[2].lexema, "2")

    def test_multiple_spaces_between_tokens(self):
        """Testa múltiplos espaços entre tokens."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1    +    2"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].lexema, "1")
        self.assertEqual(tokens[1].tipo, "ADICAO")
        self.assertEqual(tokens[2].lexema, "2")

    def test_no_spaces_between_tokens(self):
        """Testa tokens sem espaços entre eles."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1+2"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].lexema, "1")
        self.assertEqual(tokens[1].tipo, "ADICAO")
        self.assertEqual(tokens[2].lexema, "2")

    def test_newlines_between_expressions(self):
        """Testa quebras de linha entre expressões."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1+2\n3+4"))
        
        self.assertEqual(len(errors), 0)
        token_lexemas = [t.lexema for t in tokens[:-1]]  # Exclui EOF
        self.assertEqual(token_lexemas, ["1", "+", "2", "3", "+", "4"])

    def test_leading_spaces(self):
        """Testa espaços no início da expressão."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("   1 + 2"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].lexema, "1")
        self.assertEqual(tokens[0].posicao, (0, 3))

    def test_trailing_spaces(self):
        """Testa espaços no final da expressão."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1 + 2   "))
        
        self.assertEqual(len(errors), 0)
        token_lexemas = [t.lexema for t in tokens[:-1]]
        self.assertEqual(token_lexemas, ["1", "+", "2"])

    def test_mixed_whitespace_positions(self):
        """Testa espaços em diversas posições."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("  ( 1 + 2 )  "))
        
        self.assertEqual(len(errors), 0)
        token_tipos = [t.tipo for t in tokens[:-1]]
        self.assertEqual(token_tipos, ["ABRE_PARENTESE", "NUMERO", "ADICAO", "NUMERO", "FECHA_PARENTESE"])


class TestNumberTokens(unittest.TestCase):
    """Testes para tokens numéricos."""

    def test_single_digit_number(self):
        """Testa número de um único dígito."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("5"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].tipo, "NUMERO")
        self.assertEqual(tokens[0].lexema, "5")

    def test_multi_digit_number(self):
        """Testa número com múltiplos dígitos."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("12345"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].tipo, "NUMERO")
        self.assertEqual(tokens[0].lexema, "12345")

    def test_number_starting_with_zero(self):
        """Testa número começando com zero."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("007"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].lexema, "007")

    def test_multiple_numbers(self):
        """Testa múltiplos números separados."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("10 20 30"))
        
        self.assertEqual(len(errors), 0)
        numeros = [t.lexema for t in tokens if t.tipo == "NUMERO"]
        self.assertEqual(numeros, ["10", "20", "30"])


class TestOperators(unittest.TestCase):
    """Testes para operadores."""

    def test_addition_operator(self):
        """Testa operador de adição."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("+"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].tipo, "ADICAO")
        self.assertEqual(tokens[0].lexema, "+")

    def test_subtraction_operator(self):
        """Testa operador de subtração."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("-"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].tipo, "SUBTRACAO")
        self.assertEqual(tokens[0].lexema, "-")

    def test_multiplication_operator(self):
        """Testa operador de multiplicação."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("*"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].tipo, "MULTIPLICACAO")
        self.assertEqual(tokens[0].lexema, "*")

    def test_division_operator(self):
        """Testa operador de divisão."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("/"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].tipo, "DIVISAO")
        self.assertEqual(tokens[0].lexema, "/")

    def test_all_operators_in_sequence(self):
        """Testa todos os operadores em sequência."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("+ - * /"))
        
        self.assertEqual(len(errors), 0)
        tipos = [t.tipo for t in tokens[:-1]]
        self.assertEqual(tipos, ["ADICAO", "SUBTRACAO", "MULTIPLICACAO", "DIVISAO"])


class TestPunctuation(unittest.TestCase):
    """Testes para pontuações."""

    def test_open_parenthesis(self):
        """Testa parêntese de abertura."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("("))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].tipo, "ABRE_PARENTESE")
        self.assertEqual(tokens[0].lexema, "(")

    def test_close_parenthesis(self):
        """Testa parêntese de fechamento."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO(")"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].tipo, "FECHA_PARENTESE")
        self.assertEqual(tokens[0].lexema, ")")

    def test_matched_parentheses(self):
        """Testa parênteses balanceados."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("(1 + 2)"))
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(tokens[0].tipo, "ABRE_PARENTESE")
        self.assertEqual(tokens[-2].tipo, "FECHA_PARENTESE")

    def test_nested_parentheses(self):
        """Testa parênteses aninhados."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("((1 + 2) * 3)"))
        
        self.assertEqual(len(errors), 0)
        parenteses = [t for t in tokens if t.tipo in ["ABRE_PARENTESE", "FECHA_PARENTESE"]]
        self.assertEqual(len(parenteses), 4)


class TestLexicalErrors(unittest.TestCase):
    """Testes para detecção de erros léxicos."""

    def test_invalid_character_letter(self):
        """Testa detecção de caractere inválido (letra)."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1 + a"))
        
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].posicao, (0, 4))

    def test_invalid_character_equals(self):
        """Testa detecção de caractere inválido (=)."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("3 = 3"))
        
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].posicao, (0, 2))

    def test_multiple_invalid_characters(self):
        """Testa múltiplos caracteres inválidos."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("a + b"))
        
        self.assertEqual(len(errors), 2)

    def test_invalid_at_start(self):
        """Testa caractere inválido no início."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("@1 + 2"))
        
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].posicao, (0, 0))

    def test_invalid_at_end(self):
        """Testa caractere inválido no final."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1 + 2#"))
        
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].posicao, (0, 5))

    def test_special_characters(self):
        """Testa vários caracteres especiais inválidos."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("$%^&"))
        
        self.assertEqual(len(errors), 4)

    def test_valid_tokens_with_errors(self):
        """Testa que tokens válidos são reconhecidos mesmo com erros."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1 + x + 2"))
        
        self.assertEqual(len(errors), 1)  # Apenas 'x' é inválido
        numeros = [t.lexema for t in tokens if t.tipo == "NUMERO"]
        self.assertEqual(numeros, ["1", "2"])


class TestComplexExpressions(unittest.TestCase):
    """Testes para expressões complexas."""

    def test_simple_addition(self):
        """Testa expressão de adição simples."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("(1 + 2)"))
        
        self.assertEqual(len(errors), 0)
        tipos = [t.tipo for t in tokens[:-1]]
        self.assertEqual(tipos, ["ABRE_PARENTESE", "NUMERO", "ADICAO", "NUMERO", "FECHA_PARENTESE"])

    def test_multiple_operations(self):
        """Testa expressão com múltiplas operações."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("(1 + 2) * (3 - 4)"))
        
        self.assertEqual(len(errors), 0)
        operadores = [t.tipo for t in tokens if t.tipo in ["ADICAO", "SUBTRACAO", "MULTIPLICACAO", "DIVISAO"]]
        self.assertEqual(operadores, ["ADICAO", "MULTIPLICACAO", "SUBTRACAO"])

    def test_deeply_nested(self):
        """Testa expressão profundamente aninhada."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("(((1)))"))
        
        self.assertEqual(len(errors), 0)
        abre = len([t for t in tokens if t.tipo == "ABRE_PARENTESE"])
        fecha = len([t for t in tokens if t.tipo == "FECHA_PARENTESE"])
        self.assertEqual(abre, 3)
        self.assertEqual(fecha, 3)


class TestTokenPositions(unittest.TestCase):
    """Testes para posições dos tokens."""

    def test_first_token_position(self):
        """Testa posição do primeiro token."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("123"))
        
        self.assertEqual(tokens[0].posicao, (0, 0))

    def test_token_positions_in_line(self):
        """Testa posições dos tokens na linha."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1 + 2"))
        
        self.assertEqual(tokens[0].posicao, (0, 0))  # "1"
        self.assertEqual(tokens[1].posicao, (0, 2))  # "+"
        self.assertEqual(tokens[2].posicao, (0, 4))  # "2"

    def test_token_positions_multiline(self):
        """Testa posições dos tokens em múltiplas linhas."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1\n2\n3"))
        
        self.assertEqual(tokens[0].posicao[0], 0)  # Linha 0
        self.assertEqual(tokens[1].posicao[0], 1)  # Linha 1
        self.assertEqual(tokens[2].posicao[0], 2)  # Linha 2


class TestEOFToken(unittest.TestCase):
    """Testes para o token EOF."""

    def test_eof_is_last_token(self):
        """Testa que EOF é o último token."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1 + 2"))
        
        self.assertEqual(tokens[-1].tipo, "END_OF_FILE")
        self.assertEqual(tokens[-1].lexema, "EOF")

    def test_eof_on_empty_input(self):
        """Testa EOF em entrada vazia."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO(""))
        
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].tipo, "END_OF_FILE")


class TestOutputFormat(unittest.TestCase):
    """Testes para formato de saída (similar ao tests.py original)."""

    def test_output_format(self):
        """Testa o formato de saída dos tokens."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("(1 + 2)"))
        
        output = format_tokens(tokens)
        
        self.assertEqual(output[0], "<ABRE_PARENTESE, '(', (0, 0)>")
        self.assertEqual(output[-1], f"<END_OF_FILE, 'EOF', {tokens[-1].posicao}>")

    def test_error_format(self):
        """Testa o formato de saída dos erros."""
        analyzer = LexAnalyzer()
        tokens, errors = analyzer.analyze(StringIO("1 + x"))
        
        output = format_errors(errors)
        
        self.assertIn("LexicalError", output[0])
        self.assertIn("Linha 0", output[0])
        self.assertIn("coluna 4", output[0])


if __name__ == "__main__":
    unittest.main()