## Integrantes
- TOBIAS FREIRE NUMERIANO - 20230012378
- EVERTON EMANUEL LLARENA DA SILVA - 20230012574

## Como rodar
`python3 tests.py`

## E/S
As entradas estão presentes no diretório `inputs`, são arquivos `.txt` com as expressões.

As saídas são mostradas no terminal, com o seguinte formato para cada token lido da entrada:
`<{tipo}, '{lexema}', {posicao}>`

Exemplo:
```bash
<ABRE_PARENTESE, '(', (0, 0)>
<NUMERO, '1', (0, 1)>
<ADICAO, '+', (0, 3)>
<NUMERO, '2', (0, 5)>
<FECHA_PARENTESE, ')', (0, 6)>
<END_OF_FILE, 'EOF', (0, 7)>
```

Se houver um erro léxico, a saída será:
`LexicalError: {mensagem}. Linha {linha} e coluna {coluna}`

Exemplo:
`LexicalError: Caractere inválido. Linha 0 e coluna 2`