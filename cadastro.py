import re
from datetime import datetime
from front import Front
from armazenamento import Banco

class Cadastro:
    def __init__(self, argumento=None):
        self.front = Front()
        self.arq_backup = 'bakup.csv'
    
    def __tela_de_perguntas__(self, titulo='Titulo', perguntas=[['Perg1', 'txt']], lista_id=[1,2], comparar_txt=['txt']):
        """
        Verifica se foi informado o titulo imprime, se não, pula o titulo.
        Para cada pergunta in \'perguntas\':
            Verifica o tipo (txt, integer, data ou preco).
            Faz a validação da entrada com base no tipo dentro de um loop.
            Adiçiona a resposta em uma lista.
        Retorna a lista com as respostas das perguntas.

        Args:
            titulo (str, optional): O cabeçalho do \'menu\'. Defaults to 'Titulo'.
            perguntas (list of list of str, optional): Cada sublista contém a pergunta e o tipo(txt). Defaults to [['Perg1', 'txt']].

        Returns:
            list: Uma lista com com as respostas das perguntas.
        """
        TXT = 'txt'
        TXT_UNIC = 'txt_unic'
        INTEIRO = 'inteiro'
        ID = 'id'
        DATA = 'data'
        PRECO = 'preco'

        VOLTAR = 'voltar'
        
        if titulo != False: print('\n', titulo)

        print('Para cancelar digite \'Esc\'')
        ESC = ['ESC', 'ESc', 'EsC', 'Esc', 'eSC', 'eSc', 'esC', 'esc']

        respostas = []
        for perg in perguntas:
            perg[0] = perg[0] + ': '
            if perg[1] == TXT:
                resposta = input(perg[0])
                if resposta in ESC: return VOLTAR
                respostas.append(resposta)

            elif perg[1] == TXT_UNIC:
                while True:
                    resposta = input(perg[0])
                    if resposta in ESC: return VOLTAR
                    if not resposta in comparar_txt:
                        respostas.append(resposta)
                        break
                    print('O texto digitado já existe no banco, escolha outro texto!!!')

            elif perg[1] == INTEIRO:
                while True:
                    resposta = input(perg[0]).strip()
                    if resposta in ESC: return VOLTAR
                    if resposta.isdigit():
                        respostas.append(int(resposta))
                        break
                    print('Digite um número válido!!!')
            
            elif perg[1] == ID:
                while True:
                    resposta = input(perg[0]).strip()
                    if resposta in ESC: return VOLTAR
                    try: resposta = int(resposta)
                    except ValueError:
                        print('Digite um número!!!')
                        continue
                    if not resposta in lista_id:
                        print('ID não encontrado!!!')
                        continue
                    respostas.append(resposta)
                    break

            elif perg[1] == DATA:
                while True:
                    try:
                        resposta = input(perg[0]).strip()
                        if resposta in ESC: return VOLTAR
                        
                        # Verifica se a resposta segue o formato DD/MM/AA
                        if not re.match(r'^\d{2}/\d{2}/\d{2}$', resposta):
                            raise ValueError
                        
                        # Converte a string para um objeto de data para validar se é uma data real
                        datetime.strptime(resposta, "%d/%m/%y")
                        
                        # Adiciona a data formatada à lista
                        respostas.append(resposta)
                        break  # Sai do loop se a data for válida
                    
                    except ValueError:
                        print("Digite uma data válida no formato DD/MM/AA!")

            elif perg[1] == PRECO:
                while True:
                    try:
                        resposta = input(perg[0]).strip()
                        if resposta in ESC: return VOLTAR

                        # Substitui a vírgula por ponto, se houver
                        resposta = resposta.replace(",", ".")

                        # Converte para float
                        respostas.append(float(resposta))
                        break  # Sai do loop se o número for válido
                    
                    except ValueError:
                        print('Digite um número válido!!!')

            elif isinstance(perg[1], dict):  # Se a pergunta for um dicionário
                banco = Banco(perg[1]["arquivo"])
                dados = banco.ler()
                if dados == 0:
                    input('Nenhuma categoria cadastrada, cadastre uma antes ')
                    return 'voltar'
                
                self.front.__exibir_menu__('Categorias', dados[1:], False, False)

                while True:
                    resposta = input(perg[0]).strip()
                    if resposta in ESC: return VOLTAR
                    if resposta in [linha[0] for linha in dados[1:]]:  # Verifica se a resposta está na lista de opções
                        respostas.append(resposta)
                        break
                    print("Escolha uma opção válida da lista!!!")

            perg[0] = perg[0][:-2]
        return respostas

    def start(self, argumento):
        colunas_banco = list(argumento['colunas'].keys())
        saldo_atual = [[None]]
        comparar_txt = False
        animais_vendidos = Banco(argumento['arquivo'], self.arq_backup, colunas_banco)
        animais_vendidos_matrix = animais_vendidos.ler()    # matrix com os animais vendidos salvos

        self.front.__limpar_tela__()
        if "dados_salvos" in list(argumento.keys()):
            print('\t', argumento["dados_salvos"]["titulo"])    # imprime o titulo
            animais_comprados = Banco(argumento["dados_salvos"]["arquivo"], self.arq_backup)
            animais_comprados_matrix = animais_comprados.ler()  # matrix com os animais comprados
            if not animais_comprados_matrix:  # verifica se não tem animais cadastrados
                return input('Nenhum cadastro ainda, cadastre um antes ')

            for i, nome_coluna in enumerate(argumento["dados_salvos"]["colunas"]):
                animais_comprados_matrix[0][i] = nome_coluna    # troca o cabeçalho para melhor visualização

            if animais_vendidos_matrix: # verifica se tem animais vendidos
                input(argumento["dados_salvos"].get("calcular_estoque", False))
                # verifica se é para calcular o estoque
                if argumento["dados_salvos"].get("calcular_estoque", False):
                    animais_vendidos_ids = [linha[1] for linha in animais_vendidos_matrix[1:]]
                    input(animais_vendidos_ids)
                    for i, linha in enumerate(animais_comprados_matrix[1:], 1):
                        # verifica se a coluna ID dos animais comprados NÃO esta em animais vendidos
                        if not linha[0] in animais_vendidos_ids:
                            # lista com os ids dos animais que estão no lote
                            saldo_atual.append(int(linha[0]))

                else:
                    for linha in animais_comprados_matrix[1:]: saldo_atual.append(int(linha[0]))
                    
                del animais_comprados
            else:
                saldo_atual[0] = argumento["dados_salvos"]["colunas"]   # cabeçalho
                for linha in animais_comprados_matrix[1:]:
                    saldo_atual.append(linha)

        else: 
            comparar_txt = True

        dados_tabelado = self.front.__formatar_matriz__(saldo_atual)
        for linha in dados_tabelado: print(linha)

        perguntas_com_tipo = [argumento['colunas'][coluna] for coluna in colunas_banco]

        if animais_vendidos_matrix:
            if comparar_txt: comparar_txt = [linha[1] for i, linha in enumerate(animais_vendidos.ler()) if i != 0]
        if isinstance(comparar_txt, bool): comparar_txt = ['txt']
        
        while True:
            dados = self.__tela_de_perguntas__(argumento['titulo'], perguntas_com_tipo, [int(idx[0]) for idx in saldo_atual[1:]], comparar_txt)
            if dados == 'voltar': return

            salvar = False
            while True:
                escolha = input('Digite \'S\' para salvar, \'E\' para editar ou \'C\' para cancelar ')
                if escolha == 'E' or escolha == 'e': break
                if escolha == 'S' or escolha == 's':
                    salvar = True
                    break
                if escolha == 'C' or escolha == 'c': return
            if salvar: break
        input(animais_vendidos.escrever(dados))
