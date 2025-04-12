from lexer import Lexer

def processar_arquivo(nome_arquivo):
    """Lê e processa um arquivo com expressões lógicas"""
    try:
        with open(nome_arquivo, 'r') as arquivo:
            # Lê a primeira linha (número de expressões)
            primeira_linha = arquivo.readline().strip()
            try:
                num_expressoes = int(primeira_linha)
            except ValueError:
                print(f"Erro: A primeira linha deve conter um número inteiro. Valor encontrado: '{primeira_linha}'")
                return
            
            print(f"Arquivo contém {num_expressoes} expressões para analisar\n")
            
            # Processa cada expressão
            lexer = Lexer()
            for i, linha in enumerate(arquivo, 1):
                if i > num_expressoes:
                    print(f"\nAviso: O arquivo contém mais expressões que o informado ({num_expressoes})")
                    break
                
                expressao = linha.strip()
                print(f"\nExpressão {i}: {expressao}")
                sucesso, mensagem, tokens = lexer.analisar(expressao)
                
                if sucesso:
                    print("Status: VÁLIDA")
                    print("Tokens encontrados:")
                    for token in tokens:
                        print(f"  {token[0]}: {token[1]}")
                else:
                    print("Status: INVÁLIDA")
                    print(f"Erro: {mensagem}")
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Erro inesperado ao processar o arquivo: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python analisador_logico.py <arquivo_de_entrada>")
        print("Exemplo: python analisador_logico.py expressoes.txt")
        sys.exit(1)
    
    nome_arquivo = sys.argv[1]
    processar_arquivo(nome_arquivo)