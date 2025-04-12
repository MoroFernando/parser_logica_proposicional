class Lexer:
    def __init__(self):
        self.estado_atual = 0
        self.tokens = []
        self.lexema = ""
        self.erro = ""
        
        # Estados
        self.ESTADO_INICIAL = 0
        self.ESTADO_LENDO_PROPOSICAO = 1
        self.ESTADO_LENDO_OPERADOR_UNARIO = 2
        self.ESTADO_LENDO_OPERADOR_BINARIO = 3
        self.ESTADO_LENDO_CONSTANTE = 4
        self.ESTADO_ERRO = -1
        
        # Tipos de tokens
        self.TOKEN_CONSTANTE = 'CONSTANTE'
        self.TOKEN_PROPOSICAO = 'PROPOSICAO'
        self.TOKEN_OPERADOR_UNARIO = 'OPERADOR_UNARIO'
        self.TOKEN_OPERADOR_BINARIO = 'OPERADOR_BINARIO'
        self.TOKEN_ABRE_PAREN = 'ABRE_PAREN'
        self.TOKEN_FECHA_PAREN = 'FECHA_PAREN'
    
    def reset(self):
        """Reinicia o analisador para processar uma nova entrada"""
        self.estado_atual = self.ESTADO_INICIAL
        self.tokens = []
        self.lexema = ""
        self.erro = ""
    
    def adicionar_token(self, tipo, valor=None):
        """Adiciona um token à lista de tokens"""
        if valor is None:
            valor = self.lexema
        self.tokens.append((tipo, valor))
        self.lexema = ""
    
    def transicao_estado(self, char):
        """Máquina de estados para análise léxica"""
        if self.estado_atual == self.ESTADO_INICIAL:
            if char == '(':
                self.adicionar_token(self.TOKEN_ABRE_PAREN, '(')
            elif char == ')':
                self.adicionar_token(self.TOKEN_FECHA_PAREN, ')')
            elif char == '\\':
                self.lexema += char
                self.estado_atual = self.ESTADO_LENDO_OPERADOR_UNARIO
            elif char.isdigit():
                self.lexema += char
                self.estado_atual = self.ESTADO_LENDO_PROPOSICAO
            elif char in ['t', 'f']:
                self.lexema += char
                self.estado_atual = self.ESTADO_LENDO_CONSTANTE
            elif char == ' ':
                pass  # Ignora espaços em branco
            else:
                self.estado_atual = self.ESTADO_ERRO
                self.erro = f"Caractere inválido no início: '{char}'"
        
        elif self.estado_atual == self.ESTADO_LENDO_PROPOSICAO:
            if char.isdigit() or char.isalpha():
                self.lexema += char
            elif char in [' ', ')']:
                self.adicionar_token(self.TOKEN_PROPOSICAO)
                self.estado_atual = self.ESTADO_INICIAL
                # Reprocessa o caractere atual
                if char == ')':
                    self.transicao_estado(char)
            else:
                self.estado_atual = self.ESTADO_ERRO
                self.erro = f"Caractere inválido em proposição: '{char}'"
        
        elif self.estado_atual == self.ESTADO_LENDO_OPERADOR_UNARIO:
            self.lexema += char
            if self.lexema == '\\neg':
                self.adicionar_token(self.TOKEN_OPERADOR_UNARIO)
                self.estado_atual = self.ESTADO_INICIAL
            elif len(self.lexema) > 4:  # '\\neg' tem 4 caracteres
                self.estado_atual = self.ESTADO_ERRO
                self.erro = f"Operador unário inválido: '{self.lexema}'"
        
        elif self.estado_atual == self.ESTADO_LENDO_OPERADOR_BINARIO:
            self.lexema += char
            if self.lexema in ['\\wedge', '\\vee', '\\rightarrow', '\\leftrightarrow']:
                self.adicionar_token(self.TOKEN_OPERADOR_BINARIO)
                self.estado_atual = self.ESTADO_INICIAL
            elif len(self.lexema) > len('\\leftrightarrow'):
                self.estado_atual = self.ESTADO_ERRO
                self.erro = f"Operador binário inválido: '{self.lexema}'"
        
        elif self.estado_atual == self.ESTADO_LENDO_CONSTANTE:
            self.lexema += char
            if self.lexema == 'true':
                self.adicionar_token(self.TOKEN_CONSTANTE, 'true')
                self.estado_atual = self.ESTADO_INICIAL
            elif self.lexema == 'false':
                self.adicionar_token(self.TOKEN_CONSTANTE, 'false')
                self.estado_atual = self.ESTADO_INICIAL
            elif len(self.lexema) > 5:  # 'false' tem 5 caracteres
                self.estado_atual = self.ESTADO_ERRO
                self.erro = f"Constante inválida: '{self.lexema}'"
    
    def analisar(self, expressao):
        """Analisa uma expressão de lógica proposicional"""
        self.reset()
        i = 0
        n = len(expressao)
        
        while i < n and self.estado_atual != self.ESTADO_ERRO:
            char = expressao[i]
            self.transicao_estado(char)
            i += 1
        
        # Processa o último lexema, se houver
        if self.lexema and self.estado_atual != self.ESTADO_ERRO:
            if self.estado_atual == self.ESTADO_LENDO_PROPOSICAO:
                self.adicionar_token(self.TOKEN_PROPOSICAO)
            elif self.estado_atual == self.ESTADO_LENDO_CONSTANTE:
                if self.lexema in ['true', 'false']:
                    self.adicionar_token(self.TOKEN_CONSTANTE)
                else:
                    self.estado_atual = self.ESTADO_ERRO
                    self.erro = f"Constante inválida: '{self.lexema}'"
            elif self.estado_atual == self.ESTADO_LENDO_OPERADOR_UNARIO:
                if self.lexema == '\\neg':
                    self.adicionar_token(self.TOKEN_OPERADOR_UNARIO)
                else:
                    self.estado_atual = self.ESTADO_ERRO
                    self.erro = f"Operador unário inválido: '{self.lexema}'"
            elif self.estado_atual == self.ESTADO_LENDO_OPERADOR_BINARIO:
                if self.lexema in ['\\wedge', '\\vee', '\\rightarrow', '\\leftrightarrow']:
                    self.adicionar_token(self.TOKEN_OPERADOR_BINARIO)
                else:
                    self.estado_atual = self.ESTADO_ERRO
                    self.erro = f"Operador binário inválido: '{self.lexema}'"
        
        if self.estado_atual == self.ESTADO_ERRO:
            return (False, self.erro, [])
        else:
            return (True, "Análise léxica concluída com sucesso", self.tokens)
