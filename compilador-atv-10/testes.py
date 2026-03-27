import os
import subprocess

TESTES_SUCESSO = [
    # Básico
    ("{\nreturn 42;\n}", "42"),
    ("{\nreturn 7 + 5;\n}", "12"),
    ("{\nreturn 7 + 5 * 3;\n}", "22"),
    ("{\nreturn (7 + 5) * 3;\n}", "36"),

    # Com variáveis
    ("x = 10;\n{\nreturn x;\n}", "10"),
    ("x = 7 + 5;\n{\nreturn x;\n}", "12"),

    # Atribuição dentro do bloco
    ("x = 10;\n{\nx = x + 1;\nreturn x;\n}", "11"),

    # IF
    (
        "a = 10;\nb = 5;\n{\nif a > b {\na = 1;\n} else {\na = 2;\n}\nreturn a;\n}",
        "1"
    ),
    (
        "a = 2;\nb = 5;\n{\nif a > b {\na = 1;\n} else {\na = 2;\n}\nreturn a;\n}",
        "2"
    ),

    # WHILE
    (
        "a = 3;\n{\nwhile a > 0 {\na = a - 1;\n}\nreturn a;\n}",
        "0"
    ),

    # Combinação
    (
        "a = 5;\n{\nwhile a > 0 {\na = a - 1;\n}\nif a == 0 {\na = 10;\n} else {\na = 20;\n}\nreturn a;\n}",
        "10"
    ),
]

# =====================================================
# Testes de erro semântico: variável não declarada
# =====================================================
TESTES_ERRO_SEMANTICO = [
    # Variável não declarada
    ("{\nreturn x;\n}", "Erro semântico"),

    # Uso antes da declaração
    ("x = y + 1;\ny = 10;\n{\nreturn x;\n}", "Erro semântico"),

    # Atribuição inválida
    ("x = 10;\n{\ny = 5;\nreturn y;\n}", "Erro semântico"),
]

# =====================================================
# Testes de erro léxico e sintático
# =====================================================
TESTES_ERRO_LEXICO_SINTATICO = [
    # Léxico
    ("{\nreturn 237axy;\n}", "Erro léxico"),
    ("{\nreturn 5 @ 3;\n}", "Erro léxico"),

    # Sintático
    ("{\nreturn (42;\n}", "Erro sintático"),
    ("{\nreturn 33 + * 2;\n}", "Erro sintático"),

    # Falta return
    ("{\nx = 10;\n}", "Erro sintático"),

    # Falta ponto e vírgula
    ("{\nreturn 10\n}", "Erro sintático"),
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
