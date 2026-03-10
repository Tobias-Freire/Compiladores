# Compilador EC2 (Expressões Constantes 2 - Precedência) - Atividade 8

Este é um compilador simples para a linguagem EC2, construído em Python. Ele traduz expressões aritméticas com operandos constantes diretamente para a linguagem assembly x86-64, utilizando um esquema de geração de código baseado em pilha.

Diferente da versão anterior (EC1), esta versão permite escrever expressões sem a necessidade de parênteses obrigatórios, seguindo corretamente as regras tradicionais de **precedência** e **associatividade** dos operadores aritméticos.

## Alunos

- TOBIAS FREIRE NUMERIANO - 20230012378
- EVERTON EMANUEL LLARENA DA SILVA - 20230012574

## Dependências

Para rodar e testar este compilador, você precisará de:

* **Python 3.x**
* **GNU Assembler (gas)** e **Linker (ld)**: Ferramentas nativas em ambientes Linux para montagem e ligação do código x86-64.
* O arquivo **`runtime.s`** (fornecido na especificação) deve estar no mesmo diretório em que o executável for gerado.

## Funcionalidades

O compilador suporta:

- Constantes inteiras
- Operadores aritméticos:
  - `+` soma
  - `-` subtração
  - `*` multiplicação
  - `/` divisão
- Parênteses opcionais para controle de precedência
- Precedência correta dos operadores (`*` e `/` antes de `+` e `-`)
- Associatividade à esquerda para operadores de mesma precedência

Exemplo de expressões válidas:
