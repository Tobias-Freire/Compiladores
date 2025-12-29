import sys
import re

ASSEMBLY_TEMPLATE = """\
.section .text
.globl _start

_start:
mov ${value}, %rax
call imprime_num
call sair

.include "runtime.s"
"""

def main():
	if len(sys.argv) != 3:
		print("Faltam argumentos para rodar o compilador")
		print("Uso: python3 ci_compiler.py <entrada.ci> <saida.s>")

	input = sys.argv[1]
	output = sys.argv[2]

	try:
		with open(input, "r") as f:
			content = f.read().strip()
	except Exception:
		print("Erro: Não foi possível ler o arquivo de entrada.")
		sys.exit()

	# regex para verificar se o conteudo do arquivo de fato eh um numero
	if not re.fullmatch(r"[0-9]+", content):
		print("Erro: O arquivo não contém uma constante inteira válida")
		sys.exit(1)

	assembly = ASSEMBLY_TEMPLATE.replace("{value}", content)

	try:
		with open(output, "w") as f:
			f.write(assembly)
	except Exception:
		print("Erro: Não foi possível escrever o arquivo de saída")
		sys.exit(1)

if __name__ == "__main__":
	main()
