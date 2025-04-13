# 🧠 Validador de Expressões Lógicas Proposicionais

Este projeto consiste em um programa desenvolvido em Python que valida expressões de lógica proposicional escritas em LaTeX. A validação é realizada por meio de analisadores léxicos e sintáticos, construídos utilizando autômatos finitos e parsers LL(1).

## ⚙️ Funcionamento

O programa lê um arquivo de texto contendo expressões lógicas e verifica se elas estão corretas de acordo com as regras da gramática definida. Ele realiza duas etapas principais:

1. **Análise Léxica**: Identifica os tokens da expressão, como constantes, proposições, operadores e parênteses.

2. **Análise Sintática**: Verifica se a sequência de tokens segue as regras da gramática.

## 📜 Gramática Utilizada

A gramática utilizada para validar as expressões é definida pelas seguintes regras de produção:

| Regra              | Produção                                                                 |
|--------------------|--------------------------------------------------------------------------|
| FORMULA            | CONSTANTE \| PROPOSICAO \| FORMULAUNARIA \| FORMULABINARIA              |
| CONSTANTE          | `true` \| `false`                                                       |
| PROPOSICAO         | `[0-9][0-9a-z]*`                                                        |
| FORMULAUNARIA      | `ABREPAREN OPERADORUNARIO FORMULA FECHAPAREN`                           |
| FORMULABINARIA     | `ABREPAREN OPERATORBINARIO FORMULA FORMULA FECHAPAREN`                  |
| ABREPAREN          | `(`                                                                    |
| FECHAPAREN         | `)`                                                                    |
| OPERATORUNARIO     | `\neg`                                                                 |
| OPERATORBINARIO    | `\wedge` \| `\vee` \| `\rightarrow` \| `\leftrightarrow`               |

## 📂 Formato do Arquivo de Entrada

O arquivo de entrada deve seguir o seguinte formato:

1. A **primeira linha** contém um número inteiro que informa a quantidade de expressões lógicas no arquivo.
2. As **linhas seguintes** contêm as expressões lógicas que devem ser validadas.

Exemplo de arquivo de entrada (`expressoes.txt`):

`4 (\neg 2p) (\vee true false) true true (\neg)`

### Arquivos de Exemplo

Já foram disponibilizados **3 arquivos de exemplo** no repositório para facilitar os testes:  
- `expressoes.txt`  
- `expressoes_02.txt`  
- `expressoes_03.txt`

## 🚀 Como Executar

### Requisitos

Certifique-se de que você possui o Python 3 instalado.

### Rodando o Projeto Localmente

1. Clone o repositório para sua máquina local:
```bash
git clone https://github.com/MoroFernando/parser_logica_proposicional.git
```

Para executar o programa, utilize o seguinte comando no terminal:

```bash
python main.py <ARQUIVO_DE_ENTRADA>
```

Se desejar uma saída mais detalhada no console, execute o programa com a flag --debug:

```bash
python main.py <ARQUIVO_DE_ENTRADA> --debug
```

O programa exibirá se cada expressão é válida ou inválida, de acordo com as regras da gramática.