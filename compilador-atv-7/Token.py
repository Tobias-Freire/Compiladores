class Token:
    def __init__(self, tipo, lexema):
        self.tipo = tipo
        self.lexema = lexema

    def __repr__(self):
        return f"<{self.tipo}, '{self.lexema}'>"