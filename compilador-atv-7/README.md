# Compilador EC1 (Expressões Constantes 1) - Atividade 7

Este é um compilador simples para a linguagem EC1, construído em Python. Ele traduz expressões aritméticas com operandos constantes diretamente para a linguagem assembly x86-64, utilizando um esquema de geração de código baseado em pilha.

## Alunos

- TOBIAS FREIRE NUMERIANO - 20230012378
- EVERTON EMANUEL LLARENA DA SILVA - 20230012574

## Dependências

Para rodar e testar este compilador, você precisará de:
*   **Python 3.x**
*   **GNU Assembler (gas)** e **Linker (ld)**: Ferramentas nativas em ambientes Linux para montagem e ligação do código x86-64.
*   O arquivo **`runtime.s`** (fornecido na especificação) deve estar no mesmo diretório em que o executável for gerado (já coloquei dentro da pasta para enviar a atividade completa).

## Como rodar o compilador normalmente

1. Crie um arquivo contendo um programa na linguagem EC1. Exemplo (`entrada.ci`):
   ```text
   (33 + (912 * 11))
   ```
2. Execute o compilador passando a entrada e a saída como argumentos: `python3 main.py <entrada.ci> <saida.s>` (ex.: `python3 main.py inputs/entrada.ci outputs/saida.s`)
3. Monte e ligue o arquivo assembly gerado para criar o executável:
    - Montar: `as --64 -o {arquivo}.o {arquivo}.s` (ex.: `as --64 -o outputs/saida.o outputs/saida.s`)
    - Linkar: `ld -o {arquivo} {arquivo}.o` (ex.: `ld -o outputs/saida outputs/saida.o`)
4. Execute o programa gerado: `./{arquivo}` (ex.: `./outputs/saida`)
5. A saída esperada no terminal para o exemplo acima é 10065.

## Como rodar os testes automatizados
O projeto inclui um script que testa automaticamente diversas expressões válidas e inválidas, verificando se a saída do assembly compilado ou as mensagens de erro batem com o esperado.
Para rodar os testes, basta executar:
`python3 testes.py`