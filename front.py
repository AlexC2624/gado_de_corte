import os

class Front:
    def __init__(self): pass

    def __limpar_tela__(self):
        """
        Limpa a tela do terminal para melhorar a visualização do menu.

        Este método utiliza o comando apropriado para o sistema operacional 
        em uso (Windows ou Unix-based) e limpa a tela do terminal, 
        proporcionando uma interface mais limpa e organizada para o usuário.

        O comando utilizado para limpar a tela é:
            - 'cls' para sistemas Windows.
            - 'clear' para sistemas Unix-based (Linux, macOS).

        Retorna:
            None
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def __formatar_matriz__(self, matriz):
        """  
        Formata e alinha os elementos de uma matriz de strings em colunas organizadas.  

        Cada coluna é ajustada com base no maior elemento presente nela, garantindo um alinhamento uniforme.  
        O resultado é uma lista de strings, onde cada string representa uma linha da matriz formatada.  

        Parâmetros:  
            matriz (list[list[str]]): Matriz de strings a ser formatada.  

        Retorna:  
            list[str]: Lista de strings representando a matriz formatada com colunas alinhadas.  
        """
        
        # Determinar o tamanho máximo de cada coluna
        tamanho = [max(len(str(linha[i])) for linha in matriz) for i in range(len(matriz[0]))]
        
        # Formatar cada linha alinhando os elementos corretamente
        resultado = [' | '.join(str(elem).ljust(tamanho[i]) for i, elem in enumerate(linha)) for linha in matriz]

        return resultado

    def __exibir_menu__(self, titulo=None, menu=None, adicionar_id=True, limpar_tela=True):
        """  
        Exibe o menu de opções no terminal.  

        O menu é exibido de forma limpa e organizada, permitindo ao usuário visualizar as opções disponíveis.

        Parâmetros:  
            titulo (str): Título do menu exibido na tela.
            menu (list): Lista contendo as opções do menu.
            modo (int): Define o estilo de exibição do menu.

        Retorna:  
            int: O número de opções disponíveis no menu ou submenu.
        """

        if limpar_tela: self.__limpar_tela__()  # Limpa a tela antes de exibir o menu
        if titulo: print(f"----- {titulo} -----")
        if adicionar_id:
            limite = 0
            for i, opcao in enumerate(menu, 1):
                print(f"{i} - {opcao}")
                limite = i
            return limite
        else:
            for i, opcao in menu: print(f"{i} - {opcao}")

    def __obter_escolha_usuario__(self, limite= 1):
        """  
        Obtém e valida a escolha do usuário a partir das opções exibidas.  

        O usuário deve inserir um número correspondente a uma opção válida no menu.  
        Caso um valor inválido seja inserido, uma nova tentativa será solicitada.  
        O método valida se a escolha está dentro do intervalo de opções disponíveis, 
        e se for válida, retorna o índice da opção escolhida (ajustado para o índice de lista, começando do zero).

        Parâmetros:  
            limite (int, opcional): Número máximo de opções válidas. Padrão é 1.  

        Retorna:  
            int: Índice da opção escolhida pelo usuário (ajustado para começar do zero).  
        """
        while True:
            try:
                escolha = int(input(f"Escolha uma opção (1-{limite}): ").strip())
                if 1 <= escolha <= limite:
                    return escolha - 1  # Subtrai 1 para ajustar o índice
            except ValueError: pass

    def tela_de_menu(self, titulo='titulo', menu=['cadastro', 'cadastro 2']):
        """  
        Controla a interação com o usuário, exibindo um menu de opções e aguardando uma escolha.  

        O método exibe um menu de opções no terminal, permitindo que o usuário navegue entre diferentes
        opções. Ele chama o método responsável por mostrar o menu e obter a escolha do usuário, e, dependendo
        da escolha, executa a função correspondente ou retorna à tela anterior.

        Parâmetros:  
            titulo (str, opcional): Título do menu exibido na tela. O padrão é 'titulo'.  
            menu (list, opcional): Lista contendo as opções do menu. O padrão é uma lista com dois itens de exemplo.  
            modo (int, opcional): Controla o formato do menu exibido. Quando igual a 1, exibe as opções de forma simples; 
                                quando igual a 2, exibe um submenu com mais informações. O padrão é 1.  

        Retorna:  
            str ou int: Retorna 'voltar' se o usuário escolher voltar ao menu anterior, ou o índice da opção escolhida 
                        caso contrário.  
        """
        while True:
            menu.append('Sair' if 'Gestão' in titulo else 'Voltar')
            limite = self.__exibir_menu__(titulo, menu)
            escolha = self.__obter_escolha_usuario__(limite)
            menu.pop()
            if escolha == len(menu):
                return 'voltar'
            
            return escolha

    def sair(self):
        """  
        Finaliza o sistema e exibe uma mensagem de saída.  

        A função exibe a mensagem "Saindo..." no terminal e encerra a execução do programa.  

        Retorna:  
            None  
        """
        print('\nSaindo...')
        exit()

if __name__ == '__main__':
    front = Front()
    while True:
        resultado = front.tela_de_menu()
        if resultado == 'voltar': front.sair()
        resultado = front.novo_cadastro()
