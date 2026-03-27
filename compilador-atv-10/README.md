# Compilador EV (Comandos e Controle de Fluxo) - Atividade 10

Este é um compilador para a linguagem **EV**, construído em Python. Ele traduz programas com **declarações, comandos e estruturas de controle** para assembly x86-64.

Baseado na atividade 9, este projeto adiciona suporte a:

- Blocos de comandos `{ ... }`
- Comando `return`
- Estruturas condicionais `if/else`
- Estruturas de repetição `while`
- Comparações (`>`, `<`, `==`, etc.)
- Geração de código para controle de fluxo (labels e saltos)

---

## Alunos

- TOBIAS FREIRE NUMERIANO - 20230012378
- EVERTON EMANUEL LLARENA DA SILVA - 20230012574

---

## A Linguagem EV

A linguagem EV agora suporta comandos estruturados. Um programa possui:

1. Declarações de variáveis
2. Um bloco principal com comandos
3. Um `return` final com o resultado

---

## Gramática (simplificada)

<programa> ::= <decl>* <bloco>
<decl> ::= <ident> '=' <exp> ';'

<bloco> ::= '{' <cmd>* '}'

<cmd> ::= <atrib>
| <if>
| <while>
| <return>

<atrib> ::= <ident> '=' <exp> ';'

<if> ::= 'if' <exp> <bloco> ('else' <bloco>)?

<while> ::= 'while' <exp> <bloco>

<return> ::= 'return' <exp> ';'

<exp> ::= <exp_rel>
<exp_rel> ::= <exp_arit> (('>' | '<' | '==') <exp_arit>)?
<exp_arit> ::= <exp_m> (('+' | '-') <exp_m>)*
<exp_m> ::= <prim> (('' | '/') <prim>)
<prim> ::= <num> | <ident> | '(' <exp> ')'

---

## Exemplo de programa

    ```c
    a = 10;
    b = 5;

    {
        if a > b {
            a = a + 1;
        } else {
            a = a - 1;
        }

        return a;
    }

    Resultado Esperado -> 11

---

## Regras

Variáveis devem ser declaradas antes do uso
Cada comando termina com ; (exceto blocos)
O programa deve conter um return
Expressões condicionais retornam 0 (falso) ou 1 (verdadeiro)
Erros possíveis:
Erro léxico: símbolo inválido
Erro sintático: estrutura inválida
Erro semântico: variável não declarada

---

## Dependências

Python 3.x
GNU Assembler (as) e Linker (ld)
Sistema Linux ou WSL
Arquivo runtime.s no diretório

---

## Como usar o compilador

- Criar um arquivo .ev

    Exemplo (programa.ev):
        a = 3;

        {
            while a > 0 {
                a = a - 1;
            }

            return a;
        }

- Compilar

    python3 main.py programa.ev saida.s

- Montar e linkar

    as --64 -o saida.o saida.s
    ld -o programa saida.o

- Executar

    ./programa

---

## Estrutura do Projeto

Arquivo	        Descrição

Token.py	    Definição de tokens
Lexer.py	    Analisador léxico
Syntactic.py	Parser + AST + comandos (if, while, return)
Semantic.py	    Verificação de variáveis
Generator.py	Geração de assembly com controle de fluxo
main.py	        Pipeline completo
runtime.s	    Rotinas auxiliares
testes.py	    Testes automatizados

---

## Como executar os testes

python3 testes.py

## Tipos de Testes

    Testes de sucesso: expressões, variáveis, if e while
    Erros semânticos: variável não declarada
    Erros léxicos/sintáticos: tokens inválidos e estrutura incorreta

---

## Conclusão

Este projeto implementa um compilador funcional com:

Análise léxica
Parsing com precedência
AST estruturada
Análise semântica
Geração de código assembly
Controle de fluxo real (if, while)

Representando uma evolução da linguagem EV para um modelo imperativo mais completo.