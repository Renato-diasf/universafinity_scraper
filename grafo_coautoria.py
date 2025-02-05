import matplotlib.pyplot as plt
import networkx as nx

def gerar_grafo_coautoria(dados_professores, variacoes_nomes):
    G = nx.Graph()
    
    # Criar um dicionário para mapear nomes alternativos para um único nome base
    nome_padronizado = {}
    for nome_principal, variacoes in variacoes_nomes.items():
        for variacao in variacoes:
            nome_padronizado[variacao] = nome_principal
        nome_padronizado[nome_principal] = nome_principal  # Garante que o nome principal também está mapeado
    
    # Criar nós para cada professor
    for professor in dados_professores:
        nome_canonico = nome_padronizado.get(professor, professor)
        G.add_node(nome_canonico)
    
    # Criar arestas baseadas nas coautorias
    for professor, info in dados_professores.items():
        nome_canonico = nome_padronizado.get(professor, professor)
        coautores_contagem = {}
        
        for trabalho in info["trabalhos"]:
            for coautor in trabalho["coautores"]:
                coautor_canonico = nome_padronizado.get(coautor, coautor)
                if coautor_canonico != nome_canonico:  # Evitar auto-conexões
                    coautores_contagem[coautor_canonico] = coautores_contagem.get(coautor_canonico, 0) + 1
        
        # Adicionar arestas ao grafo com pesos
        for coautor, peso in coautores_contagem.items():
            if G.has_edge(nome_canonico, coautor):
                G[nome_canonico][coautor]["peso"] += peso
            else:
                G.add_edge(nome_canonico, coautor, peso=peso)
    
    return G
