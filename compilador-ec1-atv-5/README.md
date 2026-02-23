# Atividade 05 – Analisador Sintático (Parser)

Disciplina: Compiladores  
Curso: Ciência da Computação  
Linguagem: Python 3  

---

## Gramática da Linguagem EC1

A gramática adotada é definida da seguinte forma:

<programa> ::= <expressao>
<expressao> ::= <literal-inteiro> | '(' <expressao> <operador> <expressao> ')'
<operador> ::= '+' | '-' | '*' | '/'
<literal-inteiro> ::= <digito>+
<digito> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

## Funcionalidades de cada arquivo/pasta

compilador-eci-atv-5/
|
|---lex.py --> Analisador léxico
|---parser.py --> Analisador sintático (parser)
|---errors.py --> Definição de erros léxicos
|---ast_ec1.py --> Nós da árvore sintática (AST)
|
|---models/
|    |---Token.py
|
|---tests/
|    |---test_lexer.py # Testes do analisador léxico
|    |---test_parser.py # Testes do analisador sintático
|
|---README.md

## Como executar o analisador

O programa realiza:

    1. Análise léxica da expressão de entrada

    2. Análise sintática utilizando parser descendente recursivo

    3. Construção da árvore sintática abstrata (AST)

    4. Interpretação da árvore por varredura recursiva

Para testar expressões quaisquer:

    Na raiz do projeto, executar:

        python3 main.py "<expressao>" 

    Exemplo:

        python3 main.py "(33 + (912 * 11))"
    
    Saída esperada:
        
        Árvore sintática:
        (33 + (912 * 11))

        Valor da expressão:
        10065

        Árvore sintática (estrutura):
        └── +
            ├── 33
            └── *
                ├── 912
                └── 11

Execução dos testes automatizados:

    Os testes automatizados verificam:

        1. O funcionamento do analisador léxico

        2. O reconhecimento correto de expressões válidas

        3. A detecção de erros sintáticos

        4. A construção correta da árvore sintática

        5. A interpretação correta das expressões

    Na raiz do projeto, execute:

        python3 -m unittest discover -s tests -v 
    
    Sáida esperada:
        .
        .
        .
        ------------------------------------------------------------------
        Ran 50 tests in X.XXXs

        OK

    Esse comando executa automaticamente todos os arquivos de teste localizados no diretório tests/.

## Observações:

    -> Erros léxicos são detectados durante a análise léxica e reportados antes da análise sintática.

    -> Erros sintáticos são detectados pelo parser e interrompem a interpretação da expressão.

    -> O método parse() garante que toda a entrada corresponda a uma única expressão válida, sinalizando erro caso existam tokens extras.