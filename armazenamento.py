import os
import csv
from pathlib import Path
from datetime import datetime
"""
Este módulo realiza operações de manipulação de arquivos CSV e gerenciamento de dados. 

As bibliotecas importadas são:

- `os`: Fornece funcionalidades para interagir com o sistema operacional, como manipulação de arquivos e diretórios.
- `csv`: Usada para ler e escrever arquivos no formato CSV (Comma-Separated Values).
- `pathlib.Path`: Fornece classes para trabalhar com caminhos de arquivos e diretórios de forma mais orientada a objetos e independente de sistema operacional.
- `datetime`: Oferece classes para manipulação de datas e horários, permitindo formatação, comparação e cálculo de datas.

Essas bibliotecas são utilizadas para realizar operações de leitura, escrita, backup, exclusão e edição de dados no sistema.
"""

class Banco:
    """
    Classe responsável por gerenciar o armazenamento e manipulação de dados em arquivos CSV.

    Esta classe lida com operações de leitura e escrita em arquivos CSV, permitindo o cadastro,
    atualização, exclusão e consulta de registros. Ela também oferece a funcionalidade de backup
    e restauração de dados.

    Atributos:
        arquivo (str): O caminho do arquivo CSV onde os dados serão armazenados.
        colunas (list): Lista de nomes das colunas do arquivo CSV.
        arquivo_backup (str): Caminho do arquivo de backup para restauração de dados.

    Métodos:
        ler(): Lê os dados do arquivo CSV e os retorna como uma lista de listas.
        escrever(dados): Escreve novos dados no arquivo CSV.
        editar(dados): Edita um registro existente no arquivo CSV.
        excluir(id): Exclui um registro com o identificador fornecido.
        backup(): Cria um backup do arquivo de dados.
        restaurar_backup(): Restaura o arquivo de dados a partir do backup.
    """
    def __init__(self, arquivo, arquivo_backup= 'backup.csv', cabecalho=[None]):
        """
        Inicializa o banco de dados, criando o arquivo CSV e o diretório de dados, se necessário.

        Este método cria o diretório `dados` (caso não exista) e inicializa o arquivo CSV de dados
        com um cabeçalho fornecido. Caso o arquivo não exista, ele será criado com o cabeçalho
        especificado, e uma coluna adicional "ID" será inserida como a primeira coluna.

        Parâmetros:
            arquivo (str): Nome do arquivo CSV onde os dados serão armazenados.
            cabecalho (list of str): Lista contendo os nomes das colunas a serem usadas no arquivo CSV.
            arquivo_backup (str): Nome do arquivo de backup onde os dados serão salvos em caso de falha.

        Retorna:
            None
        """
        diretorio = Path('dados')
        diretorio.mkdir(parents=True, exist_ok=True)

        self.cabecalho = cabecalho
        self.arquivo_nome = arquivo
        self.arquivo_completo = diretorio / arquivo
        self.arquivo_backup = diretorio / arquivo_backup

    
    def __criar_arquivo__(self):
        if self.cabecalho == [None]:
            return 'cabecalho esta None'
        if not os.path.exists(self.arquivo_completo):
            with open(self.arquivo_completo, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for i, termo in enumerate(self.cabecalho):
                    if i == 0: cabecalho2 = ['ID']
                    cabecalho2.append(termo)
                writer.writerow(cabecalho2)

    def __data_hora_atual__(self):
        """Retorna a data e a hora atual no formato 'DD/MM/AAAAHH:MM:SS'."""
        return datetime.now().strftime("%d/%m/%Y_%H:%M:%S")

    def __proximo_id__(self, dados=None):
        """
        Obtém o próximo ID disponível no banco de dados.

        Args:
            dados (list, optional): Dados já carregados para evitar leitura duplicada.

        Returns:
            int: Próximo ID disponível.
        """
        if dados is None:
            dados = self.ler()
        if len(dados) <= 1:
            return 1
        ids = [int(linha[0]) for linha in dados[1:] if linha[0].isdigit()]
        return max(ids) + 1 if ids else 1
    
    def backup(self, arquivo_alterado, dados):
        """
        Cria um backup do arquivo de dados.

        Este método gera uma cópia do arquivo de dados atual em um arquivo de backup especificado.
        Caso ocorra algum erro ou a necessidade de recuperação, o backup pode ser restaurado.

        Retorna:
            str: Mensagem indicando o sucesso ou falha da operação de backup.
        """
        with open(self.arquivo_backup, 'a', newline='', encoding='utf-8') as backup:
            writer = csv.writer(backup)
            writer.writerow([self.__data_hora_atual__(), arquivo_alterado, dados])

    def escrever(self, valores, sobrescrever= False):
        """
        Escreve novos dados no arquivo CSV.

        Este método adiciona uma nova linha ao arquivo CSV com os dados fornecidos. Se o arquivo
        estiver vazio, a primeira linha escrita será o cabeçalho, e em seguida os dados serão
        armazenados nas linhas subsequentes.

        Parâmetros:
            valores (list): Lista contendo os dados a serem escritos no arquivo.
            sobescrever (bool): Se True o conteúdo anterior é apagado.

        Retorna:
            str: Mensagem indicando o sucesso ou falha da operação de escrita.
        """
        self.__criar_arquivo__()
        dados = self.ler()
        valores = [self.__proximo_id__(dados)] + valores
        
        if sobrescrever:
            titulo = self.ler()[0]
            with open(self.arquivo_completo, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(titulo)
                writer.writerow(valores)
        else:
            with open(self.arquivo_completo, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(valores)
                
        return 'Dados salvos com sucesso '

    def ler(self):
        """
        Lê os dados do arquivo CSV e retorna uma lista de listas.

        A primeira linha do arquivo é tratada como o cabeçalho, e as linhas subsequentes representam
        os dados registrados no arquivo. Cada linha será convertida em uma lista de valores.

        Retorna:
            list[list[str]]: Lista de listas contendo os dados do arquivo CSV, incluindo o cabeçalho.
            False: Se o arquivo não existir.
        """
        try:
            with open(self.arquivo_completo, mode='r', newline='', encoding='utf-8') as file:
                return list(csv.reader(file))
        except FileNotFoundError: return False

    def buscar(self, termo, coluna=0):
        """
        Busca registros que contenham um determinado termo em uma coluna específica.

        Este método percorre o arquivo CSV e procura por registros que contenham o termo
        fornecido em uma coluna específica. O termo é comparado com o valor da célula da coluna
        indicada, e se houver correspondência, o registro completo é adicionado aos resultados.

        Parâmetros:
            termo (str): Termo a ser pesquisado. O método buscará este termo na coluna especificada.
            coluna (int): Índice da coluna onde será feita a busca. O valor padrão é 0, que corresponde
                        à primeira coluna.

        Retorna:
            list[list[str]]: Lista de registros (linhas do CSV) que contêm o termo na coluna especificada.
                            Caso não haja correspondências, retorna uma lista vazia.
        """
        try:
            resultados = []
            with open(self.arquivo_completo, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for linha in reader:
                    if len(linha) > coluna and str(linha[coluna]) == str(termo):
                        resultados.append(linha)
            return resultados
        except FileNotFoundError: return 0

    def excluir(self, ID):
        """
        Exclui um registro com o identificador fornecido.

        Este método busca um registro no arquivo CSV pelo seu identificador (presumivelmente a
        primeira coluna) e o remove. A operação de exclusão é realizada diretamente no arquivo.

        Parâmetros:
            id (str): Identificador do registro a ser excluído.

        Retorna:
            str: Mensagem indicando o sucesso ou falha da operação de exclusão.
        """
        dados = self.ler()
        novas_linhas = [linha for linha in dados if linha[0] != str(ID)]
        linhas_excluidas = [linha for linha in dados if linha[0] == str(ID)]

        if not linhas_excluidas:
            return "Erro: ID não encontrado."

        self.backup(self.arquivo_nome, str(linhas_excluidas))

        with open(self.arquivo_completo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(novas_linhas)

        return f'{len(linhas_excluidas)} registro(s) excluído(s) com sucesso'

    def editar(self, novos_dados):
        """
        Edita um registro existente no arquivo CSV.

        Este método localiza um registro no arquivo CSV e atualiza suas informações com os novos
        dados fornecidos. A edição é realizada com base no identificador (geralmente a primeira
        coluna de cada linha), e as alterações são refletidas no arquivo.

        Parâmetros:
            dados (list): Lista contendo os dados atualizados do registro.

        Retorna:
            str: Mensagem indicando o sucesso ou falha da operação de edição.
        """
        dados = self.ler()
        encontrado = False
        for i, linha in enumerate(dados):
            if linha[0] == str(novos_dados[0]):
                self.backup(self.arquivo_nome, str(linha) + ' -> ' + str(novos_dados))
                dados[i] = novos_dados
                encontrado = True
        
        if not encontrado:
            return "Erro: ID não encontrado. Nenhum dado foi editado."

        with open(self.arquivo_completo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(dados)

        return "Dados editados com sucesso "

    def contagem(self):
        """
        Conta o número de registros armazenados no banco de dados.

        Returns:
            int: Quantidade de registros (excluindo o cabeçalho, se houver).
            int: 0 se o arquivo não existe.
        """
        try:
            with open(self.arquivo_completo, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                return sum(1 for _ in list(reader)) - 1
        except FileNotFoundError: return 0

if __name__ == '__main__':
    banco = Banco('estoqueInsumos.csv', ['Nome do Insumo', 'Quantidade', 'Unidade', 'Valor Unitário', 'Data'], 'Bakup.csv')
    n = banco.contagem()
    print(n)
