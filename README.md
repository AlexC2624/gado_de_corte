# Gestão Pecuária — Sistema de Controle

Sistema CLI em Python para gerenciamento de fazendas de gado de corte. Permite controlar insumos, animais, custos e despesas, além de gerar análises sobre estoque, custo de produção e desempenho dos animais.

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Módulos](#módulos)
- [Armazenamento de Dados](#armazenamento-de-dados)
- [Sincronização com Google Drive](#sincronização-com-google-drive)
- [Contribuindo](#contribuindo)

---

## Funcionalidades

### Cadastros
| Funcionalidade        | Descrição                                                     |
|-----------------------|---------------------------------------------------------------|
| Novo Insumo           | Registra insumos com nome, unidade de medida e fornecedor    |
| Compra de Insumo      | Registra compras vinculadas a um insumo existente             |
| Consumo de Insumo     | Registra a quantidade consumida de um insumo                  |
| Compra de Animal      | Registra animais comprados com peso, preço/kg e fornecedor    |
| Venda de Animal       | Registra a venda de animais com peso, preço/kg e comprador    |
| Categorias Financeiras| Cria categorias para classificar custos e despesas            |
| Custo/Despesa Adicional| Registra despesas avulsas vinculadas a uma categoria         |

### Análises
| Análise                | Descrição                                                              |
|------------------------|------------------------------------------------------------------------|
| Estoque de Insumos     | Calcula o saldo de cada insumo (compras − consumos)                   |
| Custo de Produção      | Soma insumos consumidos, compra de animais e despesas adicionais       |
| Desempenho dos Animais | Compara compra × venda: ganho de peso, dias no sistema, GMD e lucro   |

---

## Estrutura do Projeto

```
gado_de_corte/
├── main.py               # Ponto de entrada e configuração central do sistema
├── front.py              # Interface CLI: menus, validação de input, formatação
├── cadastro.py           # Fluxos de cadastro com validação de tipos
├── armazenamento.py      # Operações em arquivos CSV (ler, escrever, editar, excluir)
├── analise.py            # Relatórios e análises de negócio
├── sincronizar_dados.py  # Sincronização de dados com Google Drive via rclone
├── dados/                # Diretório gerado automaticamente com os arquivos CSV
│   ├── insumo_dados.csv
│   ├── insumo_comprado.csv
│   ├── insumo_consumo.csv
│   ├── insumo_estoque.csv
│   ├── animal_comprado.csv
│   ├── animal_vendido.csv
│   ├── categoria_financeiro.csv
│   └── custos_despesas.csv
└── README.md
```

> O diretório `dados/` é criado automaticamente na primeira execução e está listado no `.gitignore`.

---

## Pré-requisitos

- Python 3.8 ou superior
- Biblioteca `requests` (para verificação de conectividade na sincronização)
- [rclone](https://rclone.org/) configurado com um remote chamado `meudrive` (opcional, apenas para sincronização com Google Drive)

---

## Instalação

1. Clone o repositório:

```bash
git clone git@github.com:AlexC2624/gado_de_corte.git
cd gado_de_corte
```

2. (Opcional) Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install requests
```

---

## Como Usar

Execute o sistema a partir do diretório `gado_de_corte/`:

```bash
python3 main.py
```

### Navegação nos menus

- Digite o **número** da opção desejada e pressione `Enter`
- Para voltar ao menu anterior, selecione a opção **Voltar**
- Para cancelar um cadastro em andamento, digite `Esc` em qualquer campo
- Para encerrar o sistema, selecione **Sair** no menu principal

### Fluxo de uso recomendado

```
1. Cadastros → Novo Insumo          (cadastre os insumos disponíveis)
2. Cadastros → Categorias           (crie categorias financeiras)
3. Cadastros → Compra de Insumo     (registre as compras)
4. Cadastros → Compra de Animal     (registre os animais)
5. Cadastros → Consumo de Insumo    (registre o uso dos insumos)
6. Cadastros → Custo/Despesa        (registre despesas avulsas)
7. Cadastros → Venda de Animal      (ao vender um animal)
8. Análizes  → Estoque / Custo / Desempenho
```

### Formatos de entrada

| Tipo   | Formato esperado | Exemplo     |
|--------|-----------------|-------------|
| Data   | `DD/MM/AA`       | `05/06/25`  |
| Preço  | Decimal com `.` ou `,` | `12.50` ou `12,50` |
| Inteiro| Apenas dígitos   | `350`       |
| ID     | Número de ID exibido na tabela | `3` |

---

## Módulos

### `main.py`
Define toda a estrutura de menus e submenus via o dicionário `sistema_var`. Cada opção aponta para uma classe, uma função e um conjunto de argumentos — o que torna a adição de novas telas simples e sem alterar a lógica de navegação.

### `front.py` — classe `Front`
Responsável pela interface com o usuário:
- `tela_de_menu(titulo, menu)` — exibe um menu numerado e retorna a escolha
- `__formatar_matriz__(matriz)` — alinha colunas de uma lista de listas para exibição tabular
- `__exibir_menu__(titulo, menu)` — renderiza o menu no terminal
- `__obter_escolha_usuario__(limite)` — valida e retorna a escolha numérica do usuário

### `cadastro.py` — classe `Cadastro`
Gerencia formulários de entrada de dados:
- `start(argumento)` — executa o fluxo completo de cadastro a partir da configuração passada por `main.py`
- `__tela_de_perguntas__(titulo, perguntas, lista_id, comparar_txt)` — itera pelas perguntas validando cada tipo (`txt`, `txt_unic`, `inteiro`, `id`, `data`, `preco`, ou dicionário para listas de opções)

### `armazenamento.py` — classe `Banco`
Abstrai operações sobre arquivos CSV:
- `ler()` — retorna todos os registros como lista de listas; `False` se o arquivo não existir
- `escrever(valores)` — insere nova linha com ID auto-incrementado
- `editar(novos_dados)` — atualiza um registro existente pelo ID
- `excluir(ID)` — remove um registro pelo ID, salvando backup antes
- `buscar(termo, coluna)` — filtra registros por valor em uma coluna
- `contagem()` — retorna o número de registros

### `analise.py` — classe `Analise`
Processa os dados CSV e gera relatórios:
- `estoque_insumo(argumento)` — saldo = Σ compras − Σ consumos por insumo
- `custo_producao(argumento)` — soma custos de insumos consumidos, animais e despesas
- `desempenho_animais(argumento)` — para cada animal vendido: ganho de peso, dias no sistema, GMD (kg/dia) e lucro

### `sincronizar_dados.py` — classe `Sincronizar`
Gerencia a sincronização da pasta `dados/` com o Google Drive via `rclone`:
- `verificar_conn()` — testa conectividade com a internet
- `push()` — envia alterações locais para o Drive
- `pull()` — baixa alterações do Drive para o local
- `teve_mudanca()` — detecta se há diferenças entre local e remoto
- `start()` — executa o fluxo completo de sincronização

---

## Armazenamento de Dados

Todos os dados são armazenados em arquivos CSV dentro do diretório `dados/`, criado automaticamente. Cada arquivo possui uma coluna `ID` auto-incrementada como primeira coluna.

| Arquivo                   | Conteúdo                                      |
|---------------------------|-----------------------------------------------|
| `insumo_dados.csv`        | Cadastro de insumos (nome, unidade, fornecedor) |
| `insumo_comprado.csv`     | Compras de insumos (ID insumo, data, qtd, valor) |
| `insumo_consumo.csv`      | Consumos de insumos (ID insumo, data, qtd, obs) |
| `insumo_estoque.csv`      | Estoque calculado (gerado por análise)         |
| `animal_comprado.csv`     | Compras de animais (data, nome, peso, preço, fornecedor) |
| `animal_vendido.csv`      | Vendas de animais (ID animal, data, peso, preço, comprador) |
| `categoria_financeiro.csv`| Categorias financeiras (nome)                 |
| `custos_despesas.csv`     | Despesas (categoria, data, descrição, valor)  |

Um arquivo `bakup.csv` é gerado automaticamente no diretório `dados/` registrando cada operação de exclusão ou edição com timestamp.

---

## Sincronização com Google Drive

A sincronização utiliza o [rclone](https://rclone.org/). Para configurá-lo:

1. Instale o rclone seguindo a [documentação oficial](https://rclone.org/install/)
2. Configure um remote chamado `meudrive` apontando para o Google Drive:

```bash
rclone config
```

3. A sincronização ocorre automaticamente ao executar `sincronizar_dados.py` diretamente:

```bash
python3 sincronizar_dados.py
```

Sem o rclone configurado, o sistema funciona normalmente de forma offline.

---

## Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua feature: `git checkout -b feature/minha-feature`
3. Faça commit das alterações: `git commit -m "Adiciona minha feature"`
4. Envie para o repositório remoto: `git push origin feature/minha-feature`
5. Abra um Pull Request
