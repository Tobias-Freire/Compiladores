import sys
import os
from Lexer import Lexer
from Syntactic import Parser
from Generator import Generator

# ==========================================
# Rotina Principal e Modelo Assembly
# ==========================================
MODELO_ASSEMBLY = """#
# modelo de saida para o compilador
#

  .section .text
  .globl _start

_start:
{codigo_gerado}

  call imprime_num
  call sair

  .include "runtime.s"
"""

def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py <arquivo.ci> <arquivo_saida.s>")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    arquivo_saida_nome = sys.argv[2]
    
    with open(arquivo_entrada, 'r') as f:
        codigo_fonte = f.read()

    # Fluxo de compilação
    lexer = Lexer(codigo_fonte)
    parser = Parser(lexer)
    ast = parser.parse()
    
    gerador = Generator()
    gerador.gera(ast)
    
    codigo_assembly_exp = gerador.get_codigo()
    arquivo_saida_conteudo = MODELO_ASSEMBLY.replace("{codigo_gerado}", codigo_assembly_exp)

    # Salva o resultado diretamente no arquivo
    diretorio_saida = os.path.dirname(arquivo_saida_nome)
    if diretorio_saida:
        os.makedirs(diretorio_saida, exist_ok=True)

    with open(arquivo_saida_nome, 'w') as f:
        f.write(arquivo_saida_conteudo)
    
    print(f"Sucesso: Arquivo '{arquivo_saida_nome}' gerado.")

if __name__ == '__main__':
    main()