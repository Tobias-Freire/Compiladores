import os
import subprocess

# Testes de sucesso: (Código fonte EC1, Saída esperada no terminal)
TESTES_SUCESSO = [
    ("42", "42"),
    ("(7 + 11)", "18"),
    ("(11 - 7)", "4"),
    ("(6 * 7)", "42"),
    ("(9 / 3)", "3"),
    ("(3 + (4 + (11 + 7)))", "25"),
    ("(33 + (912 * 11))", "10065"),
    ("((427 / 7) + (11 * (231 + 5)))", "2657"),
    ("7 + 5 * 3", "22"),
    ("10 - 8 - 2", "0"),
    ("7 * 3 + 2", "23"),
    ("(7 + 5) * 3", "36")
]

# Testes de erro: (Código fonte EC1, Fragmento de erro esperado)
TESTES_ERRO = [
    ("abc", "Erro léxico"),
    ("(33 + * 2)", "Erro sintático"),
    ("(42", "Erro sintático"),
    ("()", "Erro sintático")
]

def rodar_comando(comando):
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    return resultado

def limpar_arquivos_temporarios():
    arquivos = ['temp.ci', 'temp.s', 'temp.o', 'temp_exe']
    for f in arquivos:
        if os.path.exists(f):
            os.remove(f)

def testar_sucesso():
    print("--- Rodando Testes de Sucesso ---")
    passou_todos = True

    for i, (codigo, esperado) in enumerate(TESTES_SUCESSO):
        # 1. Cria o arquivo de entrada
        with open('temp.ci', 'w') as f:
            f.write(codigo)
        
        # 2. Roda o compilador passando os 2 argumentos (entrada e saída)
        res_comp = rodar_comando("python3 main.py temp.ci temp.s")
        
        if res_comp.returncode != 0:
            print(f"Teste {i+1} Falhou na compilação: {codigo}")
            passou_todos = False
            continue
            
        # 3. Monta e Linka
        res_as = rodar_comando("as --64 -o temp.o temp.s")
        res_ld = rodar_comando("ld -o temp_exe temp.o")
        
        if res_as.returncode != 0 or res_ld.returncode != 0:
            print(f"Teste {i+1} Falhou na montagem/ligação: {codigo}")
            passou_todos = False
            continue

        # 4. Executa e verifica a saída
        res_exe = rodar_comando("./temp_exe")
        saida_limpa = res_exe.stdout.strip()
        
        if saida_limpa == esperado:
            print(f"Teste {i+1} Passou: {codigo} == {esperado}")
        else:
            print(f"Teste {i+1} Falhou: {codigo}. Esperado '{esperado}', obteve '{saida_limpa}'")
            passou_todos = False

    return passou_todos

def testar_erros():
    print("\n--- Rodando Testes de Erros Léxicos/Sintáticos ---")
    passou_todos = True

    for i, (codigo, erro_esperado) in enumerate(TESTES_ERRO):
        with open('temp.ci', 'w') as f:
            f.write(codigo)
            
        # Ao rodar o compilador com erro, também passamos o arquivo de saída
        # Esperamos que ele falhe e retorne a mensagem de erro no STDERR
        res_comp = rodar_comando("python3 main.py temp.ci temp.s")
        
        if res_comp.returncode != 0 and erro_esperado.lower() in res_comp.stderr.lower():
            print(f"Teste de Erro {i+1} Passou: Capturou '{erro_esperado}' corretamente para '{codigo}'")
        else:
            print(f"Teste de Erro {i+1} Falhou. Esperava capturar '{erro_esperado}'")
            print(f"  Saída obtida: {res_comp.stderr.strip()}")
            passou_todos = False

    return passou_todos

if __name__ == '__main__':
    if not os.path.exists("runtime.s"):
        print("Aviso: O arquivo 'runtime.s' não foi encontrado no diretório. Os testes de execução falharão.")
        
    try:
        sucesso = testar_sucesso()
        erros = testar_erros()
        
        if sucesso and erros:
            print("\nTODOS OS TESTES PASSARAM!")
        else:
            print("\nALGUNS TESTES FALHARAM. Verifique o log acima.")
    finally:
        limpar_arquivos_temporarios()