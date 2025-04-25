from front import Front
from cadastro import Cadastro
from analise import Analise

def partida():
    # Variáveis do sistema
    TXT = 'txt'
    TXT_UNIC = 'txt_unic'
    INTEIRO = 'inteiro'
    ID = 'id'
    DATA = 'data'
    PRECO = 'preco'

    CSV = {
        "insumo_dados": "insumo_dados.csv",
        "insumo_comprado": "insumo_comprado.csv",
        "insumo_consumo": "insumo_consumo.csv",
        "animal_comprado": "animal_comprado.csv",
        "animal_vendido": "animal_vendido.csv",
        "categoria_financeiro": "categoria_financeiro.csv",
        "custos_despesas": "custos_despesas.csv"
    }

    sistema_var = { # Variável base do sistema
        "sistema": "Gestão Pecuária - Sistema de Controle", # Título menu home.
        "menu": {   # Menu Home.
            "Cadastros": {   # Opção do menu home.
                "classe": Cadastro,     # Classe a ser instanciaca para o submenu.
                "argumento": None,
                "submenu": {            # Submenu.
                    "Novo Insumo": {  # Opção Submenu.
                        "funcao": "start",    # Função que será chamada junto com a classe
                        "argumento": {  # Conteúdo que será passado para a função acima
                            "titulo": "Cadastro de Insumo",
                            "arquivo": CSV["insumo_dados"],  # Nome do arquivo para armazenar os dados.
                            "colunas": {
                                "nome": ["Nome do Insumo", TXT_UNIC],   # Nome da pergunta, tipo de verificação.
                                "unidade": ["Unidade de medida", TXT],
                                "fornecedor": ["Fornecedor", TXT]
                            }
                        }
                    },
                    "Compra de Insumo": {
                        "funcao": "start",
                        "argumento": {
                            "dados_salvos": {   # Imprime os dados salvos por causa do ID que deve ser um existente
                                "titulo": "Insumos Cadastrados",
                                "arquivo": CSV["insumo_dados"],
                                "colunas": ["ID", "Nome", "Unid.", "Fornecedor"]
                            },
                            "titulo": "Cadastro de Compra de Insumo",
                            "arquivo": CSV["insumo_comprado"],
                            "colunas": {
                                "insumo_id": ["ID do insumo", ID],
                                "data": ["Data da compra", DATA],
                                "quantidade": ["Quantidade adquirida", INTEIRO],
                                "valor_unitario": ["Valor unitário", PRECO]
                            }
                        }
                    },
                    "Consumo de Insumo": {
                        "funcao": "start",
                        "argumento": {
                            "dados_salvos": {
                                "titulo": "Insumos Cadastrados",
                                "arquivo": CSV["insumo_dados"],
                                "colunas": ["ID", "Nome", "Unid.", "Fornecedor"]
                            },
                            "titulo": "Cadastro de Consumo de Insumo",
                            "arquivo": CSV["insumo_consumo"],
                            "colunas": {
                                "insumo": ["ID do Insumo", ID],
                                "data": ["Data que foi alterado", DATA],
                                "quantidade": ["Quantidade a ser fornecida", INTEIRO],
                                "obs": ["Obeservação", TXT]
                            }
                        }
                    },
                    "Compra de Animal": {
                        "funcao": "start",
                        "argumento": {
                            "titulo": "Cadastro de Compra de Aimais",
                            "arquivo": CSV["animal_comprado"],
                            "colunas": {
                                "data": ["Data da comprado", DATA],
                                "nome": ["Nome do animal", TXT_UNIC],
                                "peso": ["Peso (kg)", INTEIRO],
                                "preco_unitario": ["Preço por kg", PRECO],
                                "fornecedor": ["Fornecedor", TXT]
                            }
                        }
                    },
                    "Venda de Animal": {
                        "funcao": "start",
                        "argumento": {
                            "dados_salvos": {
                                "titulo": "Animais Ativos",
                                "arquivo": CSV["animal_comprado"],
                                "colunas": ["ID", "Data", "Nome", "Peso", 'Preco(R$/Kg)', 'Fornecedor'],
                                "calcular_estoque": True,
                            },
                            "titulo": "Cadastro de Venda de Animais",
                            "arquivo": CSV["animal_vendido"],
                            "colunas": {
                                "id": ["ID do animal", ID],
                                "data": ["Data da venda", DATA],
                                "peso": ["Peso (kg)", INTEIRO],
                                "preco_unitario": ["Preço por kg", PRECO],
                                "comprador": ["Comprador", TXT]
                            }
                        }
                    },
                    "Categorias": {
                        "funcao": "start",
                        "argumento": {
                            "titulo": "Cadastro de Categorias para Custos/Despesas",
                            "arquivo": CSV["categoria_financeiro"],
                            "colunas": {"nome": ["Nome", TXT_UNIC]}
                        },
                    },
                    "Custo/Despesa Adicional": {
                        "funcao": "start",
                        "argumento": {
                            "titulo": "Cadastro de Custos/Despesas",
                            "arquivo": CSV["custos_despesas"],
                            "colunas": {
                                "categoria": ["Categoria", {"arquivo": CSV["categoria_financeiro"]}],  # Lista de opções
                                "data": ["Data do pagamento", DATA],
                                "descricao": ["Descrição", TXT],
                                "valor": ["Valor (R$)", PRECO]
                            }
                        }
                    }   # Opção Submenu
                }   # Sub menu
            },  # Opção Menu Home
            "Análizes": {   # Opção do menu home.
                "classe": Analise,      # Classe a ser instanciaca para o submenu.
                "argumento": {
                    "arquivos": CSV,
                },
                "submenu": {            # Submenu.
                    "Estoque Insumos": {    # Opção Submenu.
                        "funcao": "estoque_insumo",  # Função que será chamada junto com a classe
                        "argumento": {      # Conteúdo que será passado para a função acima
                            "insumo_dados": CSV["insumo_dados"],
                            "insumo_comprado": CSV["insumo_comprado"],
                            "insumo_consumo": CSV["insumo_consumo"]
                        }
                    },
                    "Custo de Produção": {
                        "funcao": "custo_producao",
                        "argumento": {
                            "insumo_comprado": CSV["insumo_comprado"],
                            "insumo_consumo": CSV["insumo_consumo"],
                            "animal_comprado": CSV["animal_comprado"],
                            "custos_despesas": CSV["custos_despesas"],
                            "categoria_financeiro": CSV["categoria_financeiro"]
                        }
                    },
                    "Desempenho dos Animais": {
                        "funcao": "desempenho_animais",
                        "argumento": {
                            "animal_comprado": CSV["animal_comprado"],
                            "animal_vendido": CSV["animal_vendido"]
                        }
                    }   # Opção Submenu
                }   # Submenu
            }   # Opção Menu Home
        }   # Menu Home
    }   # Sistema_var

    front = Front()
    while True:
        opcoes_menu_home = list(sistema_var["menu"].keys())

        # Imprime Menu Home
        escolha = front.tela_de_menu(sistema_var["sistema"], opcoes_menu_home)
        if escolha == 'voltar': front.sair()

        while True:
            opcoes_submenu = list(sistema_var["menu"][opcoes_menu_home[escolha]]["submenu"].keys())
            # Imprime Submenu
            escolha2 = front.tela_de_menu(opcoes_menu_home[escolha], opcoes_submenu)
            if escolha2 == 'voltar': break
            
            # Instancia a classe e chama a função correspondente
            classe = sistema_var["menu"][opcoes_menu_home[escolha]]["classe"](sistema_var["menu"][opcoes_menu_home[escolha]]["argumento"])
            funcao = sistema_var["menu"][opcoes_menu_home[escolha]]["submenu"][opcoes_submenu[escolha2]]["funcao"]
            argumento = sistema_var["menu"][opcoes_menu_home[escolha]]["submenu"][opcoes_submenu[escolha2]]["argumento"]

            front.__limpar_tela__()
            getattr(classe, funcao)(argumento)

            del classe

def start():
    try:
        partida()
    except KeyboardInterrupt: print('\n\n\tSistema interompido!!!\n')

if __name__ == '__main__': start()