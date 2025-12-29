from abc import ABC, abstractmethod

class Exp(ABC):
    @abstractmethod
    def avaliar(self) -> int:
        pass

    @abstractmethod
    def imprimir(self) -> str:
        pass


class Const(Exp):
    def __init__(self, valor: int):
        self.valor = valor

    def avaliar(self) -> int:
        return self.valor

    def imprimir(self) -> str:
        return str(self.valor)


class OpBin(Exp):
    def __init__(self, operador: str, op_esq: Exp, op_dir: Exp):
        self.operador = operador
        self.op_esq = op_esq
        self.op_dir = op_dir

    def avaliar(self) -> int:
        esquerda = self.op_esq.avaliar()
        direita = self.op_dir.avaliar()

        if self.operador == "ADICAO":
            return esquerda + direita
        elif self.operador == "SUBTRACAO":
            return esquerda - direita
        elif self.operador == "MULTIPLICACAO":
            return esquerda * direita
        elif self.operador == "DIVISAO":
            return esquerda // direita  # divisão inteira
        else:
            raise Exception("Operador inválido")

    def imprimir(self) -> str:
        op_map = {
            "ADICAO": "+",
            "SUBTRACAO": "-",
            "MULTIPLICACAO": "*",
            "DIVISAO": "/",
        }
        return f"({self.op_esq.imprimir()} {op_map[self.operador]} {self.op_dir.imprimir()})"

class ASTNode:
    def avaliar(self):
        raise NotImplementedError

    def pretty(self, prefix="", is_left=True):
        raise NotImplementedError


    def imprimir(self):
        raise NotImplementedError

class Const(ASTNode):
    def __init__(self, valor):
        self.valor = valor

    def avaliar(self):
        return self.valor
    
    def pretty(self, prefix="", is_left=True):
        return prefix + ("├── " if is_left else "└── ") + str(self.valor)


    def imprimir(self):
        return str(self.valor)

class OpBin(ASTNode):
    def __init__(self, operador, esq, dir):
        self.operador = operador
        self.esq = esq
        self.dir = dir

    def avaliar(self):
        if self.operador == "ADICAO":
            return self.esq.avaliar() + self.dir.avaliar()
        elif self.operador == "SUBTRACAO":
            return self.esq.avaliar() - self.dir.avaliar()
        elif self.operador == "MULTIPLICACAO":
            return self.esq.avaliar() * self.dir.avaliar()
        elif self.operador == "DIVISAO":
            return self.esq.avaliar() // self.dir.avaliar()
        
    def pretty(self, prefix="", is_left=True):
        simbolo = {
            "ADICAO": "+",
            "SUBTRACAO": "-",
            "MULTIPLICACAO": "*",
            "DIVISAO": "/"
        }[self.operador]

        result = prefix + ("├── " if is_left else "└── ") + simbolo + "\n"

        child_prefix = prefix + ("│   " if is_left else "    ")

        result += self.esq.pretty(child_prefix, True) + "\n"
        result += self.dir.pretty(child_prefix, False)

        return result


    def imprimir(self):
        op = {
            "ADICAO": "+",
            "SUBTRACAO": "-",
            "MULTIPLICACAO": "*",
            "DIVISAO": "/"
        }[self.operador]

        return f"({self.esq.imprimir()} {op} {self.dir.imprimir()})"
