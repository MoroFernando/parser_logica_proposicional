from lexer import Lexer
from parserLL1 import ParserLL1

def processar_arquivo(nome_arquivo, debug=False):
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
            
            # Processa cada expressão
            lexer = Lexer()
            for i, linha in enumerate(arquivo, 1):
                if i > num_expressoes:
                    print(f"\nAviso: O arquivo contém mais expressões que o informado ({num_expressoes})")
                    break
                
                expressao = linha.strip()
                if debug:
                    print(f"\nExpressão {i} >>> {expressao}")
                sucesso, mensagem, tokens = lexer.analisar(expressao)

                if sucesso:
                    if debug:
                        print("   Tokens encontrados:")
                        for token in tokens:
                            print(f"     {token[0]}: {token[1]}")
                    parser = ParserLL1(tokens)
                    resultado, mensagem = parser.parse()
                    if resultado:
                        if debug:
                            print(f"\033[92m[VÁLIDA]\033[0m")
                        else:
                            print(f"válida")
                    else:
                        if debug:
                            print(f"\033[91m[INVÁLIDA]: {mensagem}\033[0m")
                        else:
                            print(f"inválida")
                else:
                    if debug:
                        print(f"\033[91m[INVÁLIDA]: {mensagem}\033[0m")
                    else:
                        print(f"inválida")
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Erro inesperado ao processar o arquivo: {str(e)}")

if __name__ == "__main__":
  import sys
  
  if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Uso: python analisador_logico.py <arquivo_de_entrada> [--debug]")
    print("Exemplo: python analisador_logico.py expressoes.txt --debug")
    sys.exit(1)
  
  nome_arquivo = sys.argv[1]
  debug = "--debug" in sys.argv
  processar_arquivo(nome_arquivo, debug=debug)