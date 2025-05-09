// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import GraphContainer from './components/Graph_container';
import SearchBar from './components/Search_Bar';
import Grafo2 from './pages/Grafo2';
import Grafo3 from './pages/Grafo3';
import WeightFilter from './components/Weight_Filter';

const HomePage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [nodeList, setNodeList] = useState([]);
  const [minWeight, setMinWeight] = useState(1);

  return (
    <div className="relative bg-[#1E3A8A] text-white min-h-screen z-10">
    {/* Graph no fundo */}
    <div className="absolute inset-0 -z-10">
      <GraphContainer searchTerm={searchTerm} setNodeList={setNodeList} minWeight={minWeight} />
    </div>

    {/* Conteúdo sobreposto */}
    <div className="container mx-auto text-center py-12 px-4 relative z-10">
      <div className="bg-[#D1D5DB]/70 backdrop-blur-md rounded-2xl p-6 max-w-3xl mx-auto">
          <h1 className="text-5xl font-extrabold mb-4 text-[#1E3A8A]">Universafinity</h1>
          <p className="text-lg max-w-2xl mx-auto mb-8 text-[#1E3A8A]">
            Um ambiente interativo para visualizar conexões acadêmicas e explorar redes de coautoria.
          </p>
          <SearchBar onSearch={setSearchTerm} nodeList={nodeList} />
          <WeightFilter minWeight={minWeight} setMinWeight={setMinWeight} />
        </div>
      </div>
  </div>
  );
};

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/grafo2" element={<Grafo2 />} />
        <Route path="/grafo3" element={<Grafo3 />} />
      </Routes>
    </Router>
  );
};


export default App;
