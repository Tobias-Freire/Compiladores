# Compilador Fun (Funções e Escopo) - Atividade 11

Este é um compilador para a linguagem **Fun**, construído em Python. [cite_start]Ele traduz programas com **funções, escopo local e controle de fluxo** para assembly x86-64[cite: 14, 154].

Baseado na atividade 10, este projeto adiciona suporte a:

- [cite_start]Declaração e chamada de funções (palavra-chave `fun`) [cite: 14, 15]
- [cite_start]Passagem de múltiplos parâmetros [cite: 15]
- [cite_start]Variáveis locais com escopo restrito (palavra-chave `var`) [cite: 26, 27]
- [cite_start]Resolução de escopo (variáveis locais têm prioridade sobre globais) [cite: 28]
- [cite_start]Suporte a funções recursivas (recursão direta) [cite: 129]
- [cite_start]Bloco de execução principal obrigatório (`main`) [cite: 32]
- [cite_start]Convenção de chamada utilizando a pilha do sistema (Stack Frames com `RBP` e `RSP`)[cite: 182, 235, 242].

---

## Alunos

- TOBIAS FREIRE NUMERIANO - 20230012378
- EVERTON EMANUEL LLARENA DA SILVA - 20230012574

---

## A Linguagem Fun

[cite_start]A linguagem Fun (evolução da Cmd/EV) agora suporta sub-programas[cite: 8, 14]. Um programa possui:

1. [cite_start]Sequência de declarações (variáveis globais e funções)[cite: 30].
2. [cite_start]Um bloco principal demarcado pela palavra-chave `main`[cite: 32].
3. [cite_start]O corpo das funções e do main contendo declarações de variáveis locais, comandos e uma expressão `return` final[cite: 26, 35].

---

## Gramática (simplificada)

<programa> ::= <decl>* 'main' '{' <cmd>* 'return' <exp>';' [cite_start]'}' [cite: 35]
<decl> ::= <vardecl> | [cite_start]<fundecl> [cite: 36]
<fundecl> ::= 'fun' <ident> '(' <arglist>? ')' '{' <vardecl>* <cmd>* 'return' <exp> ';' [cite_start]'}' [cite: 37, 39]
<arglist> ::= <ident> | [cite_start]<ident>','<arglist> [cite: 40]
[cite_start]<vardecl> ::= 'var' <ident> '=' <exp> ';' [cite: 41]

<cmd> ::= <if> | <while> | [cite_start]<atrib> [cite: 43, 44]
[cite_start]<atrib> ::= <ident> '=' <exp> ';' [cite: 49, 50]
[cite_start]<if> ::= 'if' <exp> '{' <cmd>* '}' 'else' '{' <cmd>* '}' [cite: 45, 46]
[cite_start]<while> ::= 'while' <exp> '{' <cmd>* '}' [cite: 47, 48]

[cite_start]<exp> ::= <exp_a> (('<' | '>' | '==') <exp_a>)* [cite: 51, 52, 53]
<exp_a> ::= <exp_m> (('+' | '-') <exp_m>)* [cite: 54, 55]
[cite_start]<exp_m> ::= <prim> (('*' | '/') <prim>)* [cite: 56, 57, 58]
<prim> ::= <num> | <ident> | '(' <exp> ')' | [cite_start]<fun> [cite: 59, 60]
[cite_start]<fun> ::= <ident> '(' <params>? ')' [cite: 61, 62]
<params> ::= <exp> | [cite_start]<exp> ',' <params> [cite: 64]

---

## Exemplo de programa

    var base = 10;

    fun quadrado(x) {
        return x * x;
    }

    fun soma_quadrados(a, b) {
        var qa = 0;
        var qb = 0;
        qa = quadrado(a);
        qb = quadrado(b);
        return qa + qb;
    }

    main {
        return soma_quadrados(3, 4);
    }

    Resultado Esperado -> 25

---

## Regras

- [cite_start]**Escopo:** Parâmetros e variáveis locais escondem variáveis globais de mesmo nome[cite: 28].
- [cite_start]**Chamadas:** O número de argumentos passados na chamada deve ser igual ao número de parâmetros declarados na função[cite: 112].
- Cada comando termina com `;` (exceto blocos de if/while).
- [cite_start]O programa e todas as funções devem conter um `return`[cite: 26, 35].
- **Erros possíveis:**
  - Erro léxico: símbolo ou caractere inválido.
  - Erro sintático: estrutura gramatical incorreta ou falta de main.
  - [cite_start]Erro semântico: Variável ou função não declarada no escopo atual, ou número incorreto de parâmetros na chamada[cite: 112].

---

## Dependências

- Python 3.x
- GNU Assembler (as) e Linker (ld)
- Sistema Linux ou WSL
- Arquivo `runtime.s` no diretório raiz do projeto

---

## Como usar o compilador

- Criar um arquivo `.fun`

    Exemplo (`programa.fun`):
        fun dobro(x) {
            return x + x;
        }

        main {
            return dobro(21);
        }

- Compilar

    python3 main.py programa.fun saida.s

- Montar e linkar

    as --64 -o saida.o saida.s
    ld -o programa saida.o

- Executar

    ./programa

---

## Estrutura do Projeto

Arquivo         | Descrição
--------------- | ---------
`Token.py`      | Definição de tokens (agora com `fun`, `var`, `main`, `,`)
`Lexer.py`      | Analisador léxico atualizado para novas palavras-chave
`Syntactic.py`  | Parser + AST com regras para declaração e chamada de funções
`Semantic.py`   | Verificação de escopo (tabelas locais/globais) e checagem de parâmetros
`Generator.py`  | Geração de assembly com registros de ativação (`RBP`/`RSP`)
`main.py`       | Pipeline completo estruturando seções `.bss` e `.text`
`runtime.s`     | Rotinas auxiliares (impressão de inteiros e encerramento)
`testes.py`     | Script de automação para testar os arquivos `.fun`

---

## Como executar os testes

Basta rodar o script de automação, que se encarregará de compilar, linkar, executar e verificar a saída de todos os arquivos de teste:

    python3 testes.py

### Tipos de Testes Inclusos (pasta `/testes`)
- Funções básicas e passagem de argumentos múltiplos.
- Sombreamento de variáveis (escopo local vs global).
- Recursividade direta (ex: Fibonacci).

---

## Conclusão

Este projeto implementa um compilador plenamente funcional com:

- Análise léxica avançada
- Parsing preditivo com precedência
- Construção de AST robusta
- Análise semântica baseada em contexto (Tabelas de Símbolos isoladas)
- Geração de código assembly x86-64 com manipulação manual da pilha para Frames de Chamada

Representando o amadurecimento do compilador, que agora suporta a quebra da complexidade através de sub-programas reutilizáveis.