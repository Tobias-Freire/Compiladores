import os
import subprocess

TESTES_SUCESSO = [
    # Programas sem variáveis (apenas expressão final)
    ("= 42", "42"),
    ("= 7 + 5", "12"),
    ("= 7 + 5 * 3", "22"),
    ("= (7 + 5) * 3", "36"),
    ("= 10 - 8 - 2", "0"),

    # Programas com uma variável
    ("x = 10;\n= x", "10"),
    ("x = 7 + 5;\n= x", "12"),
    ("x = 7 * 8;\n= x + 1", "57"),

    # Programas com múltiplas variáveis
    ("x = 10;\ny = 20;\n= x + y", "30"),
    ("x = 7 * 8;\ny = x + 1;\n= y", "57"),
    (
        "l = 30;\nc = 40;\n= l + l + c + c",
        "140"
    ),
    (
        "x = (7 + 4) * 12;\ny = x * 3 + 11;\n= (x * y) + (x * 11) + (y * 13)",
        "60467"
    ),

    # Variável usada na própria expressão de outra variável
    ("a = 5;\nb = a * 2;\nc = a + b;\n= c", "15"),

    # Programa do exemplo do professor (perímetro)
    ("l = 30;\nc = 40;\n= l + l + c + c", "140"),

    # Programa com expressão mais complexa
    (
        "x = 11 * 7;\ny = x * 3 + 5;\n= x * y",
        str(11 * 7 * (11 * 7 * 3 + 5))
    ),
]

# =====================================================
# Testes de erro semântico: variável não declarada
# =====================================================
TESTES_ERRO_SEMANTICO = [
    # Variável usada sem declaração na expressão final
    ("= x", "Erro semântico"),
    ("= x + 5", "Erro semântico"),

    # Variável usada na declaração antes de ser declarada
    ("x = 7 + y;\ny = 10;\n= x", "Erro semântico"),

    # Variável nunca declarada usada na expressão final
    ("x = 10;\ny = 20;\n= x + y + z", "Erro semântico"),
]

# =====================================================
# Testes de erro léxico e sintático
# =====================================================
TESTES_ERRO_LEXICO_SINTATICO = [
    # Erro léxico: número seguido de letras
    ("= 237axy", "Erro léxico"),

    # Erro léxico: caractere inválido
    ("= 5 @ 3", "Erro léxico"),

    # Erro sintático: parêntese não fechado
    ("= (42", "Erro sintático"),

    # Erro sintático: operador sem operando
    ("= 33 + * 2", "Erro sintático"),

    # Erro sintático: parênteses vazios
    ("= ()", "Erro sintático"),

    # Erro sintático: falta expressão final (só declaração)
    ("x = 10;", "Erro sintático"),
]


def rodar_comando(comando):
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    return resultado


def limpar_arquivos_temporarios():
    arquivos = ['temp.ev', 'temp.s', 'temp.o', 'temp_exe']
    for f in arquivos:
        if os.path.exists(f):
            os.remove(f)


def testar_sucesso():
    print("--- Rodando Testes de Sucesso ---")
    passou_todos = True

    for i, (codigo, esperado) in enumerate(TESTES_SUCESSO):
        with open('temp.ev', 'w') as f:
            f.write(codigo)

        # 1. Compilar
        res_comp = rodar_comando("python3 main.py temp.ev temp.s")

        if res_comp.returncode != 0:
            print(f"Teste {i+1} Falhou na compilação: {repr(codigo)}")
            print(f"  Erro: {res_comp.stderr.strip()}")
            passou_todos = False
            continue

        # 2. Montar e linkar
        res_as = rodar_comando("as --64 -o temp.o temp.s")
        res_ld = rodar_comando("ld -o temp_exe temp.o")

        if res_as.returncode != 0 or res_ld.returncode != 0:
            print(f"Teste {i+1} Falhou na montagem/ligação: {repr(codigo)}")
            if res_as.returncode != 0:
                print(f"  Erro as: {res_as.stderr.strip()}")
            if res_ld.returncode != 0:
                print(f"  Erro ld: {res_ld.stderr.strip()}")
            passou_todos = False
            continue

        # 3. Executar e verificar
        res_exe = rodar_comando("./temp_exe")
        saida_limpa = res_exe.stdout.strip()

        if saida_limpa == esperado:
            print(f"Teste {i+1} Passou: {repr(codigo)[:50]} == {esperado}")
        else:
            print(f"Teste {i+1} Falhou: {repr(codigo)[:50]}. Esperado '{esperado}', obteve '{saida_limpa}'")
            passou_todos = False

    return passou_todos


def testar_erros_semanticos():
    print("\n--- Rodando Testes de Erros Semânticos ---")
    passou_todos = True

    for i, (codigo, erro_esperado) in enumerate(TESTES_ERRO_SEMANTICO):
        with open('temp.ev', 'w') as f:
            f.write(codigo)

        res_comp = rodar_comando("python3 main.py temp.ev temp.s")

        if res_comp.returncode != 0 and erro_esperado.lower() in res_comp.stderr.lower():
            print(f"Teste Semântico {i+1} Passou: Capturou '{erro_esperado}' para {repr(codigo)[:50]}")
        else:
            print(f"Teste Semântico {i+1} Falhou: Esperava '{erro_esperado}' para {repr(codigo)[:50]}")
            print(f"  Saída: {res_comp.stderr.strip()}")
            passou_todos = False

    return passou_todos


def testar_erros_lexico_sintatico():
    print("\n--- Rodando Testes de Erros Léxicos/Sintáticos ---")
    passou_todos = True

    for i, (codigo, erro_esperado) in enumerate(TESTES_ERRO_LEXICO_SINTATICO):
        with open('temp.ev', 'w') as f:
            f.write(codigo)

        res_comp = rodar_comando("python3 main.py temp.ev temp.s")

        if res_comp.returncode != 0 and erro_esperado.lower() in res_comp.stderr.lower():
            print(f"Teste Léxico/Sintático {i+1} Passou: Capturou '{erro_esperado}' para {repr(codigo)[:50]}")
        else:
            print(f"Teste Léxico/Sintático {i+1} Falhou: Esperava '{erro_esperado}' para {repr(codigo)[:50]}")
            print(f"  Saída: {res_comp.stderr.strip()}")
            passou_todos = False

    return passou_todos


if __name__ == '__main__':
    if not os.path.exists("runtime.s"):
        print("Aviso: O arquivo 'runtime.s' não foi encontrado no diretório. Os testes de execução falharão.")

    try:
        sucesso = testar_sucesso()
        semantico = testar_erros_semanticos()
        lexico_sintatico = testar_erros_lexico_sintatico()

        if sucesso and semantico and lexico_sintatico:
            print("\nTODOS OS TESTES PASSARAM!")
        else:
            print("\nALGUNS TESTES FALHARAM. Verifique o log acima.")
    finally:
        limpar_arquivos_temporarios()
