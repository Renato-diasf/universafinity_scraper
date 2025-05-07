import React, { useEffect, useState } from 'react';
import Graph from 'graphology';
import Sigma from 'sigma';
import forceAtlas2 from 'graphology-layout-forceatlas2';

const GraphContainer = ({ searchTerm, setNodeList, minWeight }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sigmaInstance, setSigmaInstance] = useState(null);
  const [graph, setGraph] = useState(null);
  const [highlightedNode, setHighlightedNode] = useState(null);
  const [allEdges, setAllEdges] = useState([]);

  useEffect(() => {
    const container = document.getElementById('sigma-container');
    if (!container || container.offsetWidth === 0) return;

    const loadGraph = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch('http://192.168.0.73:5000/api/grafo');
        const data = await response.json();

        const newGraph = new Graph();

        // Adiciona os nós com posições aleatórias temporárias
        data.nodes.forEach(node => {
          newGraph.addNode(node.id, {
            label: node.label || node.id,
            x: Math.random() * 100,
            y: Math.random() * 100,
            size: 5,
            color: '#f97316'
          });
        });

        // Pega o nome de todos os nós, para passar para a SearchBar
        const nomes = data.nodes.map(n => n.label || n.id);
        setNodeList(nomes);

        // Adiciona as arestas
        setAllEdges(data.edges);

        data.edges.forEach(edge => {
          try {
            newGraph.addEdge(edge.source, edge.target, {
              size: edge.weight,
              color: edge.weight >= minWeight ? '#facc15' : 'transparent'
            });
          } catch (e) {
            console.warn(`Erro ao adicionar aresta ${edge.source}-${edge.target}`, e);
          }
        });

        if (newGraph.order === 0) {
          throw new Error('O grafo está vazio');
        }

        // Aplica o layout ForceAtlas2
        forceAtlas2.assign(newGraph, {
          iterations: 100,
          settings: {
            gravity: 0.1
          }
        });

        // Ajusta o tamanho com base no grau
        newGraph.forEachNode((node) => {
          const degree = newGraph.degree(node);
          newGraph.setNodeAttribute(node, 'size', Math.min(5 + degree, 20));
        });

        if (sigmaInstance) {
          sigmaInstance.kill(); // Mata o Sigma anterior se existir
        }
        container.innerHTML = '';

        

        // Instancia o Sigma com o grafo final
        const sigma = new Sigma(newGraph, container);
        setSigmaInstance(sigma);
        setGraph(newGraph);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    loadGraph();
  }, []);


  useEffect(() => {
    if (!graph) return;
  
    console.log('minWeight:', minWeight);
  
    // 1. Resetar todas as arestas
    graph.forEachEdge((edgeKey) => {
      graph.setEdgeAttribute(edgeKey, 'color', '#ccc');
    });
  
    // 2. Se houver um nó destacado, aplicar filtro de peso nas arestas conectadas a ele
    if (highlightedNode && graph.hasNode(highlightedNode)) {
      graph.forEachEdge(highlightedNode, (edgeKey, attributes) => {
        const weight = attributes.size;
        if (weight >= minWeight) {
          graph.setEdgeAttribute(edgeKey, 'color', '#24fc3e');
        }
      });
    }
  }, [minWeight, graph, highlightedNode]);

  useEffect(() => {
    let animationFrameId;
    let startTime;
    console.log('minWeight:', minWeight);
    if (searchTerm && graph && sigmaInstance) {
      const nodeExists = graph.hasNode(searchTerm);
  
      if (nodeExists) {
        // Resetar cor e tamanho do nó anterior (se houver)
        if (highlightedNode && graph.hasNode(highlightedNode)) {
          graph.forEachNode((node) => {
            graph.setNodeAttribute(node, 'color', '#f97316');
            graph.setNodeAttribute(node, 'size', Math.min(5 + graph.degree(node), 20));
          });
        }
  
        // Resetar cores de todas as arestas para o padrão 🧹
        graph.forEachEdge((edge) => {
          graph.setEdgeAttribute(edge, 'color', '#facc15');
        });
  
        // Destacar o novo nó
        graph.setNodeAttribute(searchTerm, 'color', '#EF4444');
        setHighlightedNode(searchTerm);
  
        // Realçar arestas conectadas ao nó buscado
        graph.forEachEdge(searchTerm, (edgeKey, attributes, source, target) => {
          graph.setEdgeAttribute(edgeKey, 'color', '#24fc3e');
        });

        // Realçar nós conectados ao nó buscado
        graph.forEachNeighbor(searchTerm, (neighbor) => {
          graph.setNodeAttribute(neighbor, 'color', '#facc15'); // amarelo vibrante
        });
  
        const baseSize = Math.min(5 + graph.degree(searchTerm), 20);
        const amplitude = 0.4; // A faixa será de 0.9x a 1.1x
        const speed = 2;

        const animate = (time) => {
          if (!startTime) startTime = time;
          const elapsed = (time - startTime) / 1000;

          const scaleFactor = 0.9 + ((Math.sin(elapsed * speed) + 1) / 2) * amplitude;
          const newSize = baseSize * scaleFactor;

          graph.setNodeAttribute(searchTerm, 'size', newSize);
          animationFrameId = requestAnimationFrame(animate);
        };

        animationFrameId = requestAnimationFrame(animate);
      } else {
        alert('Nó não encontrado no grafo!');
      }
    }
  
    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [searchTerm, graph, sigmaInstance]);

  return (
    <div className="absolute inset-0 z-0">
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-80 z-10">
          <div className="text-lg font-semibold">Carregando grafo...</div>
        </div>
      )}

      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-80 z-10">
          <div className="text-lg font-semibold text-red-600 p-4 bg-white rounded shadow">
            Erro ao carregar o grafo: {error}
          </div>
        </div>
      )}

      <div
        id="sigma-container"
        className="w-full h-full"
      />
    </div>
  );
};

export default GraphContainer;
