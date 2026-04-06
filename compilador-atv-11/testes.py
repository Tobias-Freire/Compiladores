import os
import subprocess

# Lista de tuplas: (caminho_do_arquivo, saida_esperada)
TESTES = [
    ("testes/t1_dobro.fun", "42"),
    ("testes/t2_abs.fun", "42"),
    ("testes/t3_fib.fun", "21"),
    ("testes/t4_composto.fun", "25"),
    ("testes/t5_semparams.fun", "42"),
]

def rodar_comando(comando):
    return subprocess.run(comando, shell=True, capture_output=True, text=True)

def main():
    print("--- Rodando Testes da Linguagem Fun ---")
    
    if not os.path.exists("runtime.s"):
        print("Aviso: O arquivo 'runtime.s' não foi encontrado. Os testes falharão.")
        return

    passou_todos = True

    for arquivo, esperado in TESTES:
        if not os.path.exists(arquivo):
            print(f"[ERRO] Arquivo não encontrado: {arquivo}")
            passou_todos = False
            continue

        # 1. Compilar (.fun -> .s)
        res_comp = rodar_comando(f"python3 main.py {arquivo} temp.s")
        if res_comp.returncode != 0:
            print(f"[{arquivo}] Falhou na compilação.\nErro: {res_comp.stderr.strip()}")
            passou_todos = False
            continue

        # 2. Montar e linkar (.s -> .o -> executável)
        res_as = rodar_comando("as --64 -o temp.o temp.s")
        res_ld = rodar_comando("ld -o temp_exe temp.o")
        if res_as.returncode != 0 or res_ld.returncode != 0:
            print(f"[{arquivo}] Falhou na montagem/ligação.")
            passou_todos = False
            continue

        # 3. Executar e verificar a saída
        res_exe = rodar_comando("./temp_exe")
        saida = res_exe.stdout.strip()

        if saida == esperado:
            print(f"[PASSOU] {arquivo} -> Saída: {saida}")
        else:
            print(f"[FALHOU] {arquivo} -> Esperado: {esperado}, Obtido: {saida}")
            passou_todos = False

    # 4. Limpar arquivos temporários gerados durante os testes
    for f in ['temp.s', 'temp.o', 'temp_exe']:
        if os.path.exists(f):
            os.remove(f)

    if passou_todos:
        print("\nTODOS OS TESTES PASSARAM! 🎉")
    else:
        print("\nALGUNS TESTES FALHARAM.")

if __name__ == '__main__':
    main()