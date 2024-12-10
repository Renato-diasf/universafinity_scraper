from scholarly import scholarly

def obter_dados_professor(ids_professores):
    """
    Obtém os trabalhos publicados, coautores e palavras-chave dos perfis do Google Scholar
    
    Args:
        ids_professores (list): Lista de IDs de perfil no Google Scholar.
    
    Returns:
        dict: Dados obtidos de cada professor.
    """
    resultados = {}

    for user_id in ids_professores:
        # Busca pelo perfil usando o user_id
        url_perfil = f"https://scholar.google.com/citations?hl=pt-BR&user={user_id}"

        # Print genérico só pra eu ter certeza de que o negócio tá rodando
        print(f"Processando perfil: {url_perfil}")

        try:
            # Pesquisa o perfil pelo user_id
            perfil = scholarly.search_author_id(user_id)

            # Pega todas as informações possíveis do perfil: name, afiliation, interests e o que mais tiver explicado no link: (https://scholarly.readthedocs.io/en/latest/quickstart.html#about-the-publications)
            perfil_info = scholarly.fill(perfil)

            # Coleta dados principais
            nome = perfil_info.get("name", "N/A")
            coautores = [coautor.get("name", "N/A") for coautor in perfil_info.get("coauthors", [])]
            publicacoes = perfil_info.get("publications", [])
            
            # Lista de trabalhos com informações relevantes
            trabalhos = []
            for pub in publicacoes:
                pub_info = scholarly.fill(pub)
                trabalhos.append({
                    "titulo": pub_info.get("bib", {}).get("title", "N/A"),
                    # A linha abaixo está comentada para melhor visualização no console, se descomentar
                    # vai ficar uma resposta gigante, só avisando
                    #"autores": pub_info.get("bib", {}).get("author", "N/A"),
                    "ano": pub_info.get("bib", {}).get("pub_year", "N/A"),
                    "palavras_chave": pub_info.get("bib", {}).get("keywords", []),
                })

            # Adiciona os dados ao resultado
            resultados[nome] = {
                "coautores": coautores,
                "trabalhos": trabalhos,
            }

        except Exception as e:
            # Se o ID passado deu B.O
            print(f"Erro ao processar {user_id}: {e}")

    return resultados


def exibir_dados_formatados(dados):
    """
    Exibe os dados de maneira formatada e legível.
    
    Args:
        dados (dict): Dados processados dos professores.
    """
    for professor, info in dados.items():
        print("=" * 50)
        print(f"Professor: {professor}\n")
        print("Coautores:")
        if info["coautores"]:
            for coautor in info["coautores"]:
                print(f"  - {coautor}")
        else:
            print("  Nenhum coautor listado.")

        print("\nTrabalhos publicados:")
        for i, trabalho in enumerate(info["trabalhos"], 1):
            print(f"  {i}. {trabalho['titulo']} ({trabalho['ano']})")
            if trabalho["palavras_chave"]:
                print(f"     Palavras-chave: {', '.join(trabalho['palavras_chave'])}")
        print("=" * 50 + "\n")

# ID's dos docentes lá no scholar, padrão é user=XXXXXXXX no final da URL
# ids_professores = ["QZFWzugAAAAJ", "1P_SzY0AAAAJ"] -> Alan e Delano 😎
# ids_professores = ["1P_SzY0AAAAJ"] -> Delano 🥳
ids_professores = ["G-__GDUAAAAJ"] # -> Fredy 🧐
dados_professores = obter_dados_professor(ids_professores)

# printa os resultados
exibir_dados_formatados(dados_professores)
