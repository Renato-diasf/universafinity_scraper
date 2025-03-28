import time
from scholarly import scholarly
import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt

from grafo_coautoria import gerar_grafo_coautoria


def obter_dados_professor(ids_professores):
    """
    Obtém os trabalhos publicados, locais de publicação, coautores e palavras-chave
    acessando páginas detalhadas de cada publicação.
    
    Args:
        ids_professores (list): Lista de IDs de perfil no Google Scholar.
    
    Returns:
        dict: Dados obtidos de cada professor.
    """
    resultados = {}

    for user_id in ids_professores:
        # URL padrao do scholar
        url_perfil = f"https://scholar.google.com/citations?hl=pt-BR&user={user_id}"
        print(f"Processando perfil: {url_perfil}")

        try:
            # pega as informaçoes dos docentes
            perfil = scholarly.search_author_id(user_id)
            perfil_info = scholarly.fill(perfil)

            nome = perfil_info.get("name", "N/A")
            coautores = [coautor.get("name", "N/A") for coautor in perfil_info.get("coauthors", [])]
            publicacoes = perfil_info.get("publications", [])
            all_coautores = set(coautores)  # Inicializa com os coautores do perfil

            # VARIAVEL PARA DEBUGAR (IGNORAR)
            teste = 1

            trabalhos = []
            for pub in publicacoes:
                pub_info = scholarly.fill(pub)
                # define local e abstract como N/A para pegar posteriormente na pagina especifica do trab.
                trabalho_coautores = []
                trabalho = {
                    "titulo": pub_info.get("bib", {}).get("title", "N/A"),

                    "local": "N/A",  # Placeholder para local de publicação

                    "ano": pub_info.get("bib", {}).get("pub_year", "N/A"),

                    "palavras_chave": pub_info.get("bib", {}).get("keywords", []),

                    "abstract": "N/A",  # Placeholder para abstract

                    "link_externo": "N/A", #Placeholder para link externo do artigo

                    "coautores": "N/A" # coautores do trabalho em questão
                }

                # URL de cada publicacao 
                author_pub_id = pub_info.get("author_pub_id")
                print(author_pub_id)
                if author_pub_id and teste == 1:
                    scholar_url = f"https://scholar.google.com/citations?view_op=view_citation&hl=pt-BR&user={user_id}&citation_for_view={author_pub_id}"
                    try:
                        print(f"Acessando página do artigo no Google Scholar: {scholar_url}")

                        # cabeçalho para o google scholar nao detectar como bot e barrar o acesso
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                        }

                        response =  requests.get(scholar_url, headers=headers, timeout=10)
                        soup = BeautifulSoup(response.content, "html.parser")

                        #printa o html recebido
                        #print(soup.prettify())

                        if response.status_code == 200:
                            
                            # procura o local de publicação de acordo com a classe da div na pagina
                            campos = soup.find_all("div", class_="gsc_oci_field")
                            valores = soup.find_all("div", class_="gsc_oci_value")

                            #print de depuracao (todos os valores que da pra encontrar)
                            #print("Campos encontrados:", [campo.text for campo in campos])
                            #print("Valores encontrados:", [valor.text for valor in valores])

                            for campo, valor in zip(campos, valores):
                                campo_texto = campo.text.strip().lower()
                                valor_texto = valor.text.strip()
                                
                                # verificações dinâmicas para os diferentes tipos de publicações (tem varios valores possiveis)
                                if "publicado em" in campo_texto or "published in" in campo_texto:
                                    trabalho["local"] = valor_texto
                                elif "conferência" in campo_texto or "conference" in campo_texto:
                                    trabalho["local"] = valor_texto  
                                elif "journal" in campo_texto or "revista" in campo_texto:
                                    trabalho["local"] = valor_texto  
                                elif "book" in campo_texto or "livro" in campo_texto:
                                    trabalho["local"] = valor_texto
                                elif "publicações" in campo_texto:
                                    trabalho["local"] = valor_texto
                                elif "editora" in campo_texto or "publisher" in campo_texto:
                                    trabalho["local"] = valor_texto

                                # acha os coautores de cada trabalho
                                if "autores" in campo_texto:
                                    trabalho["coautores"] = [nome.strip() for nome in valor_texto.split(",")]


                                
                                trabalho_coautores = [nome.strip() for nome in valor_texto.split(",")]
                                all_coautores.update(trabalho["coautores"])


                                # caso ache o abstract
                                if "descrição" in campo_texto:
                                    trabalho["abstract"] = valor_texto

                                
                            # procura o link externo para o artigo
                            link_externo = soup.find("a", class_="gsc_oci_title_link")
                            if link_externo and link_externo.get("href"):
                                trabalho["link_externo"] = link_externo["href"]
                                #teste = teste
                            #teste += 1
                    except Exception as e:
                        print(f"Erro ao acessar a página do artigo no Google Scholar: {e}")

                trabalhos.append(trabalho)

            resultados[nome] = {
                "coautores": coautores,
                "all_coautores": list(all_coautores),
                "trabalhos": trabalhos,
            }

        except Exception as e:
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

        # Exibe a lista de coautores mas referente ao perfil do docente (aquela listinha que fica na direita)
        print("Coautores:")
        if info["coautores"]:
            for coautor in info["coautores"]:
                print(f"  - {coautor}")
        else:
            print("  Nenhum coautor listado.")

        # Exibe a lista unificada de coautores
        print("\nTodos os coautores (perfil + trabalhos):")
        if info["all_coautores"]:
            for coautor in info["all_coautores"]:
                print(f"  - {coautor}")
        else:
            print("  Nenhum coautor listado.")


        # Exibe trabalho por trabalho, junto com os coautores de cada trabalho
        print("\nTrabalhos publicados:")
        for i, trabalho in enumerate(info["trabalhos"], 1):
            print(f"  {i}. {trabalho['titulo']} ({trabalho['ano']})")
            print(f"     Local: {trabalho['local']}")
            if trabalho["palavras_chave"]:
                print(f"     Palavras-chave: {', '.join(trabalho['palavras_chave'])}")

            if(trabalho['abstract'] != 'N/A'):
                print("\n")
            print(f"     Abstract: {trabalho['abstract']}")
            if(trabalho['abstract'] != 'N/A'):
                print("\n")
            
            if(trabalho['coautores'] != 'N/A'):
                print("\n")
            print(f"     Co-Autores: {trabalho['coautores']}")
            if(trabalho['coautores'] != 'N/A'):
                print("\n")
            
            print(f"     Link_Externo: {trabalho['link_externo']}")
            print("=" * 25 + "\n")
        print("=" * 50 + "\n")




# IDs de exemplo
# Fred : "G-__GDUAAAAJ"
# Alan: "QZFWzugAAAAJ"
ids_professores = ["G-__GDUAAAAJ"]
dados_professores = obter_dados_professor(ids_professores)
exibir_dados_formatados(dados_professores)


variacoes_nomes = {
    "Alan Valejo": {"ADB Valejo", "A Valejo"},
    "Jo Ueyama": {"J Ueyama"}, 
    "Alfredo Colenci Neto" : {"C Neto"},
}


grafo = gerar_grafo_coautoria(dados_professores, variacoes_nomes)
