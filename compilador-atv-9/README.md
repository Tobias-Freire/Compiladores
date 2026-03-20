# Compilador EV (Expressões com Variáveis) - Atividade 9

Este é um compilador para a linguagem **EV** (Expressões com Variáveis), construído em Python. Ele traduz programas com declarações de variáveis e expressões aritméticas para assembly x86-64.

Baseado no compilador EC2 (atividade 8), este projeto adiciona suporte a **variáveis**, **análise semântica** com tabela de símbolos, e **geração de código** com seção `.bss`.

## Alunos

- TOBIAS FREIRE NUMERIANO - 20230012378
- EVERTON EMANUEL LLARENA DA SILVA - 20230012574

## A Linguagem EV

A linguagem EV permite declarar variáveis e usá-las em expressões. Um programa é composto por zero ou mais declarações de variáveis, seguidas de uma expressão final (resultado), cujo valor é impresso na saída.

### Gramática

```
<programa>     ::= <decl>* <result>
<decl>         ::= <ident> '=' <exp> ';'
<result>       ::= '=' <exp>
<exp>          ::= <exp_m> (('+' | '-') <exp_m>)*
<exp_m>        ::= <prim> (('*' | '/') <prim>)*
<prim>         ::= <num> | <ident> | '(' <exp> ')'
<num>          ::= <digito><digito>*
<ident>        ::= <letra><letra_digito>*
```

### Exemplo de programa

```
x = (7 + 4) * 12;
y = x * 3 + 11;
= (x * y) + (x * 11) + (y * 13)
```

Resultado esperado: `60467`

### Regras

- Cada declaração termina com `;`
- A expressão final começa com `=`
- Variáveis só podem ser usadas após terem sido declaradas
- Uso de variável não declarada gera erro semântico

## Dependências

- **Python 3.x**
- **GNU Assembler (as)** e **Linker (ld)**: ferramentas nativas em ambientes Linux para montagem e ligação do código x86-64
- O arquivo **`runtime.s`** deve estar no mesmo diretório em que o executável for gerado

## Como usar o compilador

### 1. Criar um arquivo fonte com extensão `.ev`

Exemplo (`programa.ev`):
```
l = 30;
c = 40;
= l + l + c + c
```

### 2. Compilar

```bash
python3 main.py programa.ev saida.s
```

### 3. Montar e linkar

```bash
as --64 -o saida.o saida.s
ld -o saida_exe saida.o
```

### 4. Executar

```bash
./saida_exe
```

## Estrutura do Projeto

| Arquivo          | Descrição |
|------------------|-----------|
| `Token.py`       | Classe Token usada pelo analisador léxico |
| `Lexer.py`       | Analisador léxico — reconhece tokens (números, identificadores, operadores, `=`, `;`) |
| `Syntactic.py`   | Analisador sintático e definições da AST (Programa, Decl, Var, Const, OpBin) |
| `Semantic.py`    | Análise semântica — verificação de variáveis com tabela de símbolos |
| `Generator.py`   | Gerador de código assembly x86-64 (seções .bss e .text) |
| `main.py`        | Programa principal — fluxo completo de compilação |
| `runtime.s`      | Funções de suporte assembly (impressão e saída) |
| `testes.py`      | Suite de testes automatizados |

## Como executar os testes

```bash
cd compilador-atv-9
python3 testes.py
```

Os testes cobrem:
- **Testes de sucesso**: programas EV com e sem variáveis que devem compilar e produzir o resultado correto
- **Testes de erro semântico**: uso de variável não declarada
- **Testes de erro léxico/sintático**: caracteres inválidos, parênteses incorretos, etc.
