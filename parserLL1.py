class ParserLL1:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.erro = ""

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def match(self, expected_type):
        token = self.current_token()
        if token and token[0] == expected_type:
            self.pos += 1
            return True
        return False

    def parse(self):
        if self.FORMULA():
            if self.pos == len(self.tokens):
                return True, "Expressão válida."
            else:
                return False, f"Tokens extras após o fim da fórmula: {self.tokens[self.pos]}"
        else:
            return False, f"Erro sintático: {self.erro or 'estrutura inválida.'}"

    def FORMULA(self):
        token = self.current_token()
        if not token:
            self.erro = "Esperado uma fórmula, mas a entrada está vazia ou incompleta."
            return False

        token_type = token[0]

        if token_type == 'CONSTANTE':
            self.pos += 1
            return True
        elif token_type == 'PROPOSICAO':
            self.pos += 1
            return True
        elif token_type == 'ABRE_PAREN':
            if self.pos + 1 >= len(self.tokens):
                self.erro = "Esperado operador após '('."
                return False

            lookahead = self.tokens[self.pos + 1][0]

            if lookahead == 'OPERADOR_UNARIO':
                return self.FORMULAUNARIA()
            elif lookahead == 'OPERADOR_BINARIO':
                return self.FORMULABINARIA()
            else:
                self.erro = f"Operador esperado após '(', encontrado: {self.tokens[self.pos + 1]}"
                return False
        else:
            self.erro = f"Token inesperado: {token}"
            return False

    def FORMULAUNARIA(self):
        if not self.match('ABRE_PAREN'):
            self.erro = "Esperado '(' no início de fórmula unária."
            return False
        if not self.match('OPERADOR_UNARIO'):
            self.erro = "Esperado operador unário após '('."
            return False
        if not self.FORMULA():
            return False
        if not self.match('FECHA_PAREN'):
            self.erro = "Esperado ')' ao final de fórmula unária."
            return False
        return True

    def FORMULABINARIA(self):
        if not self.match('ABRE_PAREN'):
            self.erro = "Esperado '(' no início de fórmula binária."
            return False
        if not self.match('OPERADOR_BINARIO'):
            self.erro = "Esperado operador binário após '('."
            return False
        if not self.FORMULA():
            return False
        if not self.FORMULA():
            return False
        if not self.match('FECHA_PAREN'):
            self.erro = "Esperado ')' ao final de fórmula binária."
            return False
        return True
