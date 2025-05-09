from flask import Flask, jsonify
import networkx as nx
from networkx.readwrite import json_graph
from scraper import obter_dados_professor
from grafo_coautoria import gerar_grafo_coautoria
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Cache para armazenar o grafo (só gera uma vez)
grafo_cache = None

def processar_grafo():
    global grafo_cache
    if grafo_cache is None:
        print("Gerando grafo de coautoria...")  # Para debug
        ids_professores = ["G-__GDUAAAAJ", "QZFWzugAAAAJ"]
        dados_professores = obter_dados_professor(ids_professores)
        variacoes_nomes = {
            "Alan Valejo": {"ADB Valejo", "A Valejo"},
            "Jo Ueyama": {"J Ueyama"}, 
            "Alfredo Colenci Neto": {"C Neto"},
        }
        grafo_cache = gerar_grafo_coautoria(dados_professores, variacoes_nomes)
    return grafo_cache

@app.route('/api/grafo', methods=['GET'])
def get_grafo():
    grafo = processar_grafo()
    data = json_graph.node_link_data(grafo)

    formatted_data = {
        "nodes": [{"id": node["id"], "label": node.get("label", str(node["id"]))} for node in data["nodes"]],
        "edges": [{"source": edge["source"], "target": edge["target"], "weight": edge.get("peso", 1)} for edge in data["links"]]
    }
    return jsonify(formatted_data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

