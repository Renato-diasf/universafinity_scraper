# FIXXXXXXXXXXXXXIT

# Não está funcionando no presente momento, o HTML recebido é diferente do visualizado na página
# Por enquanto estamos pegando o abstract do proprio Scholar.
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

        # cabeçalho para "enganar" detectores de bot na requisição
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
        response = requests.get(url_externo, headers=headers, timeout=10)

        #if response.status_code == 200:
        # linha abaixo deve ser comentada em condições normais, está sempre TRUE (1 = 1) para teste
        if 1 == 1:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # exibe o HTML completo da página
            print("\n=== HTML da página ===\n")
            print(soup.prettify())
            print("\n======================\n")

            # procura por um campo que contenha "Abstract" no texto
            abstract_tag = soup.find(text=lambda text: text and "abstract:" in text.lower())
            if abstract_tag:
                # tenta capturar o conteúdo próximo ao texto "Abstract"
                next_div = abstract_tag.find_next("div")
                if next_div:
                    return next_div.text.strip()
            else:
                print("Texto 'abstract:' não encontrado na página.")

        return "N/A"
    except Exception as e:
        print(f"Erro ao acessar a página externa: {e}")
        return "N/A"



