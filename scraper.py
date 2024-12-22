import time
from scholarly import scholarly
import requests
from bs4 import BeautifulSoup

def obter_dados_professor(ids_professores):
    """
    Obtém os trabalhos publicados, coautores e palavras-chave dos perfis do Google Scholar,
    acessando páginas detalhadas de cada publicação e, quando possível, páginas externas.
    
    Args:
        ids_professores (list): Lista de IDs de perfil no Google Scholar.
    
    Returns:
        dict: Dados obtidos de cada professor.
    """
    resultados = {}

    for user_id in ids_professores:
        url_perfil = f"https://scholar.google.com/citations?hl=pt-BR&user={user_id}"
        print(f"Processando perfil: {url_perfil}")

        try:
            perfil = scholarly.search_author_id(user_id)
            perfil_info = scholarly.fill(perfil)

            nome = perfil_info.get("name", "N/A")
            coautores = [coautor.get("name", "N/A") for coautor in perfil_info.get("coauthors", [])]
            publicacoes = perfil_info.get("publications", [])
            
            trabalhos = []
            for pub in publicacoes:
                pub_info = scholarly.fill(pub)
                trabalho = {
                    "titulo": pub_info.get("bib", {}).get("title", "N/A"),
                    "local": "N/A",  # Placeholder para local de publicação
                    "ano": pub_info.get("bib", {}).get("pub_year", "N/A"),
                    "palavras_chave": pub_info.get("bib", {}).get("keywords", []),
                    "abstract": "N/A",  # Placeholder para abstract
                }

                # construir URL da página detalhada no Google Scholar (precisa do id da pub)
                author_pub_id = pub_info.get("author_pub_id")
                print(author_pub_id)
                if author_pub_id:
                    scholar_url = f"https://scholar.google.com/citations?view_op=view_citation&hl=pt-BR&user={user_id}&citation_for_view={author_pub_id}"
                    try:
                        print(f"Acessando página do artigo no Google Scholar: {scholar_url}")
                        # necessario pro google scholar nao barrar a gente
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                        }
                        response =  requests.get(scholar_url, headers=headers, timeout=10)
                        soup = BeautifulSoup(response.content, "html.parser")
                        #print(soup.prettify())
                        if response.status_code == 200:
                            
                            # Procura o local de publicação
                            campos = soup.find_all("div", class_="gsc_oci_field")
                            valores = soup.find_all("div", class_="gsc_oci_value")
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
                                elif "editora" in campo_texto or "publisher" in campo_texto:
                                    trabalho["local"] = valor_texto
                                elif "páginas" in campo_texto or "pages" in campo_texto:
                                    trabalho["local"] = valor_texto
                                elif "Book" in campo_texto or "livro" in campo_texto:
                                    trabalho["local"] = valor_texto
                                elif "publicações" in campo_texto:
                                    trabalho["local"] = valor_texto

                                if "autores" in campo_texto:
                                    trabalho["autores"] = valor_texto
                                
                            # Procura o link externo para o artigo
                            link_externo = soup.find("a", class_="gsc_oci_title_link")
                            if link_externo and link_externo.get("href"):
                                trabalho["abstract"] = obter_abstract_externo(link_externo["href"])
                    except Exception as e:
                        print(f"Erro ao acessar a página do artigo no Google Scholar: {e}")

                trabalhos.append(trabalho)

            resultados[nome] = {
                "coautores": coautores,
                "trabalhos": trabalhos,
            }

        except Exception as e:
            print(f"Erro ao processar {user_id}: {e}")

    return resultados

def obter_abstract_externo(url_externo):
    """
    Acessa uma página externa do artigo para tentar capturar o abstract.
    
    Args:
        url_externo (str): URL externa do artigo.
    
    Returns:
        str: Abstract encontrado na página, ou "N/A" se não encontrado.
    """
    try:
        print(f"Acessando página externa: {url_externo}")
        response = requests.get(url_externo, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Procura por um campo que contenha "Abstract" no texto
            abstract_tag = soup.find(text=lambda text: text and "abstract:" in text.lower())
            if abstract_tag:
                # Tenta capturar o conteúdo próximo ao texto "Abstract"
                parent = abstract_tag.find_parent()
                if parent:
                    return parent.text.strip()
        return "N/A"
    except Exception as e:
        print(f"Erro ao acessar a página externa: {e}")
        return "N/A"

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
            print(f"     Local: {trabalho['local']}")
            if trabalho["palavras_chave"]:
                print(f"     Palavras-chave: {', '.join(trabalho['palavras_chave'])}")
            print(f"     Abstract: {trabalho['abstract']}")
        print("=" * 50 + "\n")

# IDs de exemplo
ids_professores = ["G-__GDUAAAAJ"]
dados_professores = obter_dados_professor(ids_professores)
exibir_dados_formatados(dados_professores)
