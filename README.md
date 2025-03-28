<h1 align="center"> 🚀 Universafinity 🖥 </h1>

<p align="center">
  <img src="https://github.com/Maracujacake/universafinity_scraper/blob/main/readme_img%20(2).png" width="500" alt="Universafinity">
</p>

## 📌 Sobre o Projeto

**Universafinity** é uma ferramenta desenvolvida para a **UFSCar** com o objetivo de conectar docentes por meio de suas colaborações em trabalhos científicos. A plataforma utiliza um modelo baseado em **grafos** para representar as conexões entre professores e seus respectivos coautores.

## 📜 Funcionalidades

- 🔎 **Busca por docentes**: Encontre professores a partir de nomes ou áreas de pesquisa.
- 🔗 **Mapeamento de conexões**: Visualização das colaborações através de um grafo interativo.
- 📊 **Análise de coautoria**: Identifica relações fortes entre pesquisadores com base na frequência de publicações conjuntas.
- 📁 **Exportação de dados**: Possibilidade de exportar a rede de colaborações para análises externas.

## 🚀 Tecnologias Utilizadas

- **Python** 🐍 (Web Scraping, Processamento de Dados)
- **NetworkX** 🔗 (Construção de Grafos)
- **Flask** 🌐 (API Backend)
- **React.js** ⚛️ (Interface Web - Opcional)
- **MySQL** 🗄️ (Armazenamento de dados)

## 📦 Instalação e Uso

### 1️⃣ Clone o Repositório
```bash
 git clone https://github.com/Maracujacake/universafinity_scraper.git
 cd universafinity_scraper
```

### 2️⃣ Instale as Dependências
```bash
 pip install -r requirements.txt
```

### 3️⃣ Execute a Ferramenta
```bash
 python main.py
```

## 📊 Como Funciona

1. O script faz web scraping no **Google Scholar** e coleta informações sobre publicações e coautores.
2. Os dados são processados e estruturados em um **grafo**, onde cada nó representa um docente e as arestas indicam colaborações.
3. O usuário pode interagir com a interface web (se disponível) ou utilizar a API para acessar as informações.

## 📜 Licença

Este projeto é licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 💡 Contribuição

Sinta-se à vontade para abrir **issues** e enviar **pull requests**. Qualquer sugestão para aprimoramento é bem-vinda! 😊
