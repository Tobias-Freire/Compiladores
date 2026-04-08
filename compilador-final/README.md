# Compilador Fun - Projeto Final

Este é um compilador para a linguagem **Fun**, construído em Python. Ele traduz programas com **funções, escopo local e controle de fluxo** para assembly x86-64.

Baseado na atividade 11, este projeto cumpre a especificação do **Projeto Final**, adicionando suporte a 4 extensões simples:

- **Novos operadores de comparação:** `<=`, `>=`, `!=`
- **Novo operador aritmético (módulo):** `%`
- **Operadores compostos de atribuição:** `+=`, `-=`, `*=`, `/=`
- **Comandos de `return` arbitrários:** Permitir o uso de `return <exp>;` em qualquer parte do código (por exemplo, dentro de um `if` para finalização antecipada da função).

Todas as features originais (suporte a funções recursivas, variáveis locais, etc) continuam suportadas.

---

## Alunos

- TOBIAS FREIRE NUMERIANO - 20230012378
- EVERTON EMANUEL LLARENA DA SILVA - 20230012574

---

## A Linguagem Fun

A linguagem Fun (evolução da Cmd/EV) agora suporta sub-programas[cite: 8, 14]. Um programa possui:

1. Sequência de declarações (variáveis globais e funções)[cite: 30].
2. Um bloco principal demarcado pela palavra-chave `main`[cite: 32].
3. O corpo das funções e do main contendo declarações de variáveis locais, comandos e uma expressão `return` final[cite: 26, 35].

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

- **Escopo:** Parâmetros e variáveis locais escondem variáveis globais de mesmo nome.
- **Chamadas:** O número de argumentos passados na chamada deve ser igual ao número de parâmetros declarados na função.
- Cada comando termina com `;` (exceto blocos de if/while).
- O programa e todas as funções devem conter um `return`.
- **Erros possíveis:**
  - Erro léxico: símbolo ou caractere inválido.
  - Erro sintático: estrutura gramatical incorreta ou falta de main.
  - Erro semântico: Variável ou função não declarada no escopo atual, ou número incorreto de parâmetros na chamada[cite: 112].

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
    ```fun
    fun dobro(x) {
        return x + x;
    }

    main {
        return dobro(21);
    }
    ```

- Compilar

    ```bash
    python3 main.py programa.fun saida.s
    ```

- Montar e linkar

    ```bash
    as --64 -o saida.o saida.s && ld -o programa saida.o
    ```

- Executar

    ```bash
    ./programa
    ```

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
- Modulo de inteiros (`%`).
- Comparadores lógicos complexos (`<=`, `>=`, `!=`).
- Atribuições compostas alterando variáveis.
- Validação de retorno imediato (early return).

---

## Conclusão

Este projeto implementa um compilador plenamente funcional com:

- Análise léxica avançada
- Parsing preditivo com precedência
- Construção de AST robusta
- Análise semântica baseada em contexto (Tabelas de Símbolos isoladas)
- Geração de código assembly x86-64 com manipulação manual da pilha para Frames de Chamada

Representando o amadurecimento do compilador, que agora suporta a quebra da complexidade através de sub-programas reutilizáveis.