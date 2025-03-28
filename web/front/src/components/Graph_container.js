// src/GraphContainer.js
import React, { useEffect, useState } from 'react';
import Graph from 'graphology';
import Sigma from 'sigma';
import  forceAtlas2  from 'graphology-layout-forceatlas2';

const GraphContainer = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let sigmaInstance = null;
    
    const loadGraph = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch('http://192.168.0.73:5000/api/grafo');
        const data = await response.json();

        // Criar nova instância do grafo
        const graph = new Graph();

        // Adicionar nós
        data.nodes.forEach(node => {
          graph.addNode(node.id, {
            label: node.label || node.id,
            x: Math.random() * 10,
            y: Math.random() * 10,
            size: 5,
            color: '#ec5148'
          });
        });

        // Adicionar arestas
        data.edges.forEach(edge => {
          try {
            graph.addEdge(edge.source, edge.target, {
              size: edge.weight || 1,
              color: '#ccc'
            });
          } catch (e) {
            console.warn(`Failed to add edge ${edge.source}-${edge.target}:`, e);
          }
        });

        // Verificar se o grafo é válido
        if (graph.order === 0) {
          throw new Error('O grafo está vazio (sem nós)');
        }

        // Aplicar layout
        forceAtlas2.assign(graph, {
          iterations: 100,
          settings: {
            gravity: 0.1
          }
        });

        // Ajustar tamanho dos nós baseado no grau
        graph.forEachNode(node => {
          const degree = graph.degree(node);
          graph.setNodeAttribute(node, 'size', Math.min(5 + degree, 20));
        });

        // Renderizar com Sigma
        const container = document.getElementById('sigma-container');
        if (container) {
          container.innerHTML = ''; // Limpar container
          sigmaInstance = new Sigma(graph, container, {
            renderEdgeLabels: false,
            defaultNodeColor: '#ec5148',
            defaultEdgeColor: '#ccc'
          });
        }

        setLoading(false);
      } catch (err) {
        console.error('Erro ao carregar o grafo:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    loadGraph();

    return () => {
      if (sigmaInstance) {
        sigmaInstance.kill();
      }
    };
  }, []);

  return (
    <div className="relative w-full max-w-3xl h-[600px] mx-auto">
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
        className="w-full h-full border border-gray-300 rounded-lg shadow-md bg-white"
      />
    </div>
  );
};

export default GraphContainer;