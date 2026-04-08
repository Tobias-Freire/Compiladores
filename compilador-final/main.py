import sys
import os
from Lexer import Lexer
from Syntactic import Parser
from Semantic import AnalisadorSemantico
from Generator import Generator

MODELO_ASSEMBLY = """\
  .section .bss
{variaveis_bss}

  .section .text
  .globl _start

_start:
{codigo_main}

  call imprime_num
  call sair

{codigo_funs}
  .include "runtime.s"
"""

def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py <arquivo.fun> <arquivo_saida.s>")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    arquivo_saida_nome = sys.argv[2]

    with open(arquivo_entrada, 'r') as f:
        codigo_fonte = f.read()

    # 1. Análise Léxica
    lexer = Lexer(codigo_fonte)

    # 2. Análise Sintática
    parser = Parser(lexer)
    ast = parser.parse()

    # 3. Análise Semântica
    semantico = AnalisadorSemantico()
    semantico.verificar(ast)

    # 4. Geração de Código
    gerador = Generator()
    gerador.gera_programa(ast)

    codigo_bss  = gerador.get_codigo_bss()
    codigo_main = gerador.get_codigo_main()
    codigo_funs = gerador.get_codigo_funs()

    saida = MODELO_ASSEMBLY.format(
        variaveis_bss=codigo_bss,
        codigo_main=codigo_main,
        codigo_funs=codigo_funs,
    )

    diretorio_saida = os.path.dirname(arquivo_saida_nome)
    if diretorio_saida:
        os.makedirs(diretorio_saida, exist_ok=True)

    with open(arquivo_saida_nome, 'w') as f:
        f.write(saida)

    print(f"Sucesso: Arquivo '{arquivo_saida_nome}' gerado.")

if __name__ == '__main__':
    main()
