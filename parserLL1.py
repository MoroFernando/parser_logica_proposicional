class ParserLL1:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
        self.erro = ""
    
    def advance(self):
        """Avança para o próximo token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def eat(self, token_type):
        """Consome o token atual se for do tipo esperado"""
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            expected = token_type
            found = self.current_token[0] if self.current_token else "fim da entrada"
            self.erro = f"Erro de sintaxe: esperado '{expected}', encontrado '{found}'"
            raise SyntaxError(self.erro)
    
    def parse(self):
        """Inicia o parsing da expressão"""
        try:
            self.formula()
            if self.current_token is not None:
                raise SyntaxError(f"Erro: tokens remanescentes após a fórmula completa: {self.current_token}")
            return (True, "Parsing concluído com sucesso")
        except SyntaxError as e:
            return (False, str(e))
    
    def formula(self):
        """FORMULA = CONSTANTE | PROPOSICAO | FORMULAUNARIA | FORMULABINARIA"""
        if not self.current_token:
            raise SyntaxError("Erro: fórmula incompleta")
        
        token_type = self.current_token[0]
        
        if token_type == 'CONSTANTE':
            self.eat('CONSTANTE')
        elif token_type == 'PROPOSICAO':
            self.eat('PROPOSICAO')
        elif token_type == 'ABRE_PAREN':
            # Pode ser FORMULAUNARIA ou FORMULABINARIA
            self.eat('ABRE_PAREN')
            
            if self.current_token and self.current_token[0] == 'OPERADOR_UNARIO':
                self.formula_unaria()
            elif self.current_token and self.current_token[0] == 'OPERADOR_BINARIO':
                self.formula_binaria()
            else:
                raise SyntaxError("Erro: esperado operador unário ou binário após '('")
            
            self.eat('FECHA_PAREN')
        else:
            raise SyntaxError(f"Erro: token inesperado '{token_type}' no início da fórmula")
    
    def formula_unaria(self):
        """FORMULAUNARIA = ABREPAREN OPERADORUNARIO FORMULA FECHAPAREN"""
        self.eat('OPERADOR_UNARIO')
        self.formula()
    
    def formula_binaria(self):
        """FORMULABINARIA = ABREPAREN OPERADORBINARIO FORMULA FORMULA FECHAPAREN"""
        self.eat('OPERADOR_BINARIO')
        self.formula()  # Primeira fórmula
        self.formula()  # Segunda fórmula