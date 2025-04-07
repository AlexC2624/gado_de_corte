from front import Front
from armazenamento import Banco
from datetime import datetime

class Analise:
    def __init__(self, argumento=None):
        self.arquivos = argumento['arquivos']
        self.front = Front()

    def estoque_insumo(self, argumento):
        insumo_dados = Banco(argumento["insumo_dados"])
        insumo_compra = Banco(argumento["insumo_comprado"])
        insumo_consumo = Banco(argumento["insumo_consumo"])

        # Ler os dados
        dados = insumo_dados.ler()
        compras = insumo_compra.ler()
        consumos = insumo_consumo.ler()

        if not False in [dados, compras, consumos]:
            # Ignorar as primeiras linhas de cabeçalhos
            dados, compras, consumos = dados[1:], compras[1:], consumos[1:] # Remove o titulo
            compras = compras[1:]
            consumos = consumos[1:]
            
            # Criar um dicionário para armazenar o estoque de cada insumo
            estoque = {}

            # Processar as compras
            for compra in compras:
                insumo_id = compra[1]  # ID do insumo
                quantidade = float(compra[3])  # Quantidade comprada
                
                # Inicializar estoque se ainda não existir
                if insumo_id not in estoque:
                    estoque[insumo_id] = 0
                
                # Somar a quantidade comprada ao estoque
                estoque[insumo_id] += quantidade

            # Processar os consumos
            for consumo in consumos:
                insumo_id = consumo[1]  # ID do insumo
                quantidade = float(consumo[3])  # Quantidade consumida
                
                # Subtrair a quantidade consumida do estoque
                if insumo_id in estoque:
                    estoque[insumo_id] -= quantidade

            # Exibir os resultados
            print(f"Estoque de insumos:")
            for insumo in dados:
                insumo_id = insumo[0]  # ID do insumo
                nome = insumo[1]  # Nome do insumo
                
                if insumo_id in estoque:
                    print(f"{nome}: {estoque[insumo_id]} {insumo[2]}")
                else:
                    print(f"{nome}: 0 {insumo[2]}")
        else: print('Cadastre mais dados sobre os insumos dados, compra, consumo!!!')
        input('ENTER para voltar ')

    def custo_producao(self, argumento):
        # Ler os bancos de dados
        insumo_compra = Banco(argumento["insumo_comprado"])
        insumo_consumo = Banco(argumento["insumo_consumo"])
        animal_comprado = Banco(argumento["animal_comprado"])
        custos_despesas = Banco(argumento["custos_despesas"])
        cat_financeiro = Banco(argumento["categoria_financeiro"])
        
        # Carregar os dados
        dados_compra = insumo_compra.ler()
        dados_consumo = insumo_consumo.ler()
        dados_animais = animal_comprado.ler()
        dados_despesas = custos_despesas.ler()
        dados_categorias = cat_financeiro.ler()

        if not False in [dados_compra, dados_consumo, dados_animais, dados_despesas, dados_categorias]: # Remove o titulo
            dados_compra, dados_consumo, dados_animais = dados_compra[1:], dados_consumo[1:], dados_animais[1:] # Remove o titulo
            dados_despesas, dados_categorias = dados_despesas[1:], dados_categorias[1:]

            # Dicionário para mapear categorias de despesas
            categorias = {cat[0]: cat[1] for cat in dados_categorias}  # ID -> Nome da categoria

            # Cálculo do custo de insumos consumidos
            custo_insumos = 0
            for consumo in dados_consumo:
                insumo_id = consumo[1]  # ID do insumo
                quantidade_consumida = float(consumo[3])  # Quantidade consumida
                
                # Buscar o valor unitário do insumo comprado
                for compra in dados_compra:
                    if compra[1] == insumo_id:
                        valor_unitario = float(compra[4])  # Valor unitário
                        break
                
                # Calcular o custo dos insumos consumidos
                custo_insumos += quantidade_consumida * valor_unitario

            # Cálculo do custo de animais comprados
            custo_animais = sum(float(animal[3]) * float(animal[4]) for animal in dados_animais)

            # Cálculo de outras despesas
            custo_despesas = sum(float(despesa[4]) for despesa in dados_despesas)

            # Cálculo total do custo de produção
            custo_total = custo_insumos + custo_animais + custo_despesas

            # Exibir os resultados
            print(f"Custo total de produção: R${custo_total:.2f}")
            print(f"- Custo com insumos: R${custo_insumos:.2f}")
            print(f"- Custo com animais: R${custo_animais:.2f}")
            print(f"- Outras despesas: R${custo_despesas:.2f}")

            # Exibir detalhes das despesas por categoria
            print("\nDetalhes das despesas:")
            for despesa in dados_despesas:
                categoria_id = despesa[1]
                descricao = despesa[3]
                valor = float(despesa[4])
                categoria_nome = categorias.get(categoria_id, "Desconhecido")
                print(f"  - {categoria_nome}: {descricao} - R${valor:.2f}")
        
        else: print('Cadastre mais dados sobre insumos, animais e financeiro!!!')
        input('ENTER para voltar ')

    def desempenho_animais(self, argumento):
        # Ler os dados dos arquivos
        animal_compra = Banco(argumento["animal_comprado"])
        animal_venda = Banco(argumento["animal_vendido"])
        
        # Carregar as listas de dados, ignorando os cabeçalhos
        dados_compra = animal_compra.ler()
        dados_venda = animal_venda.ler()
        
        if not False in [dados_compra, dados_venda]:
            dados_compra, dados_venda = dados_compra[1:], dados_venda[1:]   # Remove o titulo

            # Converter datas para o formato adequado
            def converter_data(data):
                return datetime.strptime(data, "%d/%m/%y")

            # Criar dicionário para armazenar os dados de compra
            compra_dict = {compra[0]: compra for compra in dados_compra}

            # Cabeçalhos da tabela
            matriz_desempenho = [
                ["ID", "Nome", "Ganho de Peso (kg)", "Dias no Sistema", "GMD (kg/dia)", "Lucro (R$)"]
            ]

            for venda in dados_venda:
                animal_id = venda[1]  # ID do animal vendido
                peso_final = float(venda[3])  # Peso na venda
                preco_venda = float(venda[4])  # Preço unitário na venda
                data_venda = converter_data(venda[2])  # Converter data de venda

                if animal_id in compra_dict:
                    compra = compra_dict[animal_id]
                    peso_inicial = float(compra[3])  # Peso na compra
                    preco_compra = float(compra[4])  # Preço unitário na compra
                    data_compra = converter_data(compra[1])  # Converter data de compra
                    
                    # Calcular desempenho
                    ganho_peso = peso_final - peso_inicial
                    dias = (data_venda - data_compra).days
                    gmd = ganho_peso / dias if dias > 0 else 0  # Evita divisão por zero
                    custo_total = peso_inicial * preco_compra
                    receita_total = peso_final * preco_venda
                    lucro = receita_total - custo_total
                    
                    # Adicionar os dados à matriz
                    matriz_desempenho.append([
                        animal_id,
                        compra[2],  # Nome do animal
                        f"{ganho_peso:.2f}",
                        str(dias),
                        f"{gmd:.2f}",
                        f"R$ {lucro:.2f}"
                    ])
            print('\tDesempenho dos animais\n')
            # Chamar a função de formatação para exibir a tabela formatada
            for linha in self.front.__formatar_matriz__(matriz_desempenho):
                print(linha)

        else: print('Cadastre mais dados sobre a compra e venda de animas!!!')
        input('ENTER para voltar ')
