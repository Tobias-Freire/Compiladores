class Exp: pass

class Const(Exp):
    def __init__(self, valor):
        self.valor = int(valor)

class OpBin(Exp):
    def __init__(self, operador, opEsq, opDir):
        self.operador = operador
        self.opEsq = opEsq
        self.opDir = opDir

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.proximo_token()

    def comer(self, tipo):
        if self.token_atual.tipo == tipo:
            self.token_atual = self.lexer.proximo_token()
        else:
            raise Exception(f"Erro sintático: esperado {tipo}, recebido {self.token_atual.tipo}")

    def analisaExp(self):
        tok = self.token_atual
        if tok.tipo == 'LITERAL_INTEIRO':
            self.comer('LITERAL_INTEIRO')
            return Const(tok.lexema)
        
        elif tok.tipo == 'ABRE_PARENTESE':
            self.comer('ABRE_PARENTESE')
            opEsq = self.analisaExp()
            
            if self.token_atual.tipo == 'OPERADOR':
                operador = self.token_atual.lexema
                self.comer('OPERADOR')
            else:
                raise Exception("Erro sintático: esperado um operador")
                
            opDir = self.analisaExp()
            self.comer('FECHA_PARENTESE')
            
            return OpBin(operador, opEsq, opDir)
            
        else:
            raise Exception(f"Erro sintático: token inesperado {tok}")

    def parse(self):
        ast = self.analisaExp()
        if self.token_atual.tipo != 'EOF':
            raise Exception("Erro sintático: conteúdo extra no final do arquivo")
        return ast