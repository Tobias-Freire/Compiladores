"""
Testes automatizados para o analisador sintático da linguagem EC1.

Cobertura de testes:
1. Expressões válidas simples
2. Expressões aninhadas
3. Construção correta da árvore sintática
4. Avaliação (interpretação) das expressões
5. Detecção de erros sintáticos

Executar com: python3 -m unittest test_parser -v
"""

import unittest
from io import StringIO

from lex import LexAnalyzer
from parser import Parser, SyntaxError


class ParserTestBase(unittest.TestCase):
    """Classe base com utilitário para análise completa."""

    def parse(self, code: str):
        lex = LexAnalyzer()
        tokens, errors = lex.analyze(StringIO(code))
        self.assertEqual(len(errors), 0, "Erro léxico inesperado")
        parser = Parser(tokens)
        return parser.parse()  


class TestValidExpressions(ParserTestBase):
    """Testes para expressões sintaticamente válidas."""

    def test_single_number(self):
        tree = self.parse("42")
        self.assertEqual(tree.avaliar(), 42)
        self.assertEqual(tree.imprimir(), "42")

    def test_simple_addition(self):
        tree = self.parse("(1 + 2)")
        self.assertEqual(tree.avaliar(), 3)
        self.assertEqual(tree.imprimir(), "(1 + 2)")

    def test_simple_subtraction(self):
        tree = self.parse("(10 - 4)")
        self.assertEqual(tree.avaliar(), 6)

    def test_simple_multiplication(self):
        tree = self.parse("(6 * 7)")
        self.assertEqual(tree.avaliar(), 42)

    def test_simple_division(self):
        tree = self.parse("(20 / 5)")
        self.assertEqual(tree.avaliar(), 4)

    def test_nested_expression(self):
        tree = self.parse("(33 + (912 * 11))")
        self.assertEqual(tree.avaliar(), 33 + 912 * 11)
        self.assertEqual(tree.imprimir(), "(33 + (912 * 11))")

    def test_deeply_nested_expression(self):
        tree = self.parse("((1 + 2) * (3 + 4))")
        self.assertEqual(tree.avaliar(), 21)

    def test_multiple_levels(self):
        tree = self.parse("((2 * (3 + 4)) - 5)")
        self.assertEqual(tree.avaliar(), 9)


class TestSyntaxErrors(unittest.TestCase):
    """Testes para erros sintáticos."""

    def parse_with_error(self, code: str):
        lex = LexAnalyzer()
        tokens, errors = lex.analyze(StringIO(code))
        self.assertEqual(len(errors), 0, "Erro léxico inesperado")
        parser = Parser(tokens)
        parser.parse()   # ← agora usa parse()

    def test_missing_closing_parenthesis(self):
        with self.assertRaises(SyntaxError):
            self.parse_with_error("(1 + 2")

    def test_missing_opening_parenthesis(self):
        with self.assertRaises(SyntaxError):
            self.parse_with_error("1 + 2)")

    def test_empty_parentheses(self):
        with self.assertRaises(SyntaxError):
            self.parse_with_error("()")

    def test_operator_without_operands(self):
        with self.assertRaises(SyntaxError):
            self.parse_with_error("(+ 1 2)")

    def test_extra_tokens_after_expression(self):
        with self.assertRaises(SyntaxError):
            self.parse_with_error("1 2")


if __name__ == "__main__":
    unittest.main()
