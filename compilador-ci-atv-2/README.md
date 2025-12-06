## Integrantes
- TOBIAS FREIRE NUMERIANO - 20230012378
- EVERTON EMANUEL LLARENA DA SILVA - 20230012574

## Rodando essa atividade
- `python3 ci_compiler.py <entrada.ci> <saida.s>` 
- `as --64 -o <saida.o> <saida.s>`
- `ld -o <saida> <saida.o>`
- `./<saida>`

Exemplo:
```bash
python3 ci_compiler.py p1.ci saida.s
as --64 -o saida.o saida.s
ld -o saida saida.o
./saida
```