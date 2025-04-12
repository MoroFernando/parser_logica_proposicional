class ParserLL1:
    def __init__(self, tokens):
        self.tokens = tokens + [("EOF", "$")]  # Adiciona marcador de fim
        self.pos = 0
        self.pilha = ["EOF", "FORMULA"]

        # Tabela preditiva: (não-terminal, lookahead) -> produção
        self.tabela = {
            ("FORMULA", "CONSTANTE"): ["CONSTANTE"],
            ("FORMULA", "PROPOSICAO"): ["PROPOSICAO"],
            ("FORMULA", "ABRE_PAREN"): ["ABRE_PAREN", "OPERADOR", "FORMULA", "FECHA_PAREN"],

            ("OPERADOR", "OPERADOR_UNARIO"): ["OPERADOR_UNARIO"],
            ("OPERADOR", "OPERADOR_BINARIO"): ["OPERADOR_BINARIO"]
        }

    def current_token(self):
        return self.tokens[self.pos][0] if self.pos < len(self.tokens) else "EOF"

    def match(self, esperado):
        atual_tipo, atual_valor = self.tokens[self.pos]
        if atual_tipo == esperado:
            self.pos += 1
        else:
            raise SyntaxError(f"Esperado '{esperado}', mas encontrado '{atual_tipo}'.")

    def parse(self):
        try:
            while self.pilha:
                topo = self.pilha.pop()
                lookahead = self.current_token()

                # Caso terminal
                if topo in ["CONSTANTE", "PROPOSICAO", "ABRE_PAREN", "FECHA_PAREN", "OPERADOR_UNARIO", "OPERADOR_BINARIO", "EOF"]:
                    self.match(topo)

                # Caso não-terminal
                else:
                    producao = self.tabela.get((topo, lookahead))
                    if not producao:
                        return (False, f"Erro sintático: '{topo}' não pode começar com '{lookahead}'.")
                    self.pilha.extend(reversed(producao))

            # Após esvaziar a pilha, esperamos que todo token tenha sido consumido
            if self.current_token() != "EOF":
                return (False, "Tokens restantes após fim da análise.")
            return (True, "Expressão válida")
        except SyntaxError as e:
            return (False, str(e))
