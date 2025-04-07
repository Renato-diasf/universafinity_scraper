// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import GraphContainer from './components/Graph_container';
import SearchBar from './components/Search_Bar';
import Grafo2 from './pages/Grafo2';
import Grafo3 from './pages/Grafo3';

const HomePage = () => {
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="bg-[#1E3A8A] text-white">
      <div className="container mx-auto text-center py-12 px-4">
        <h1 className="text-5xl font-extrabold mb-4">Universafinity</h1>
        <p className="text-lg text-gray-300 max-w-2xl mx-auto mb-8">
          Um ambiente interativo para visualizar conexões acadêmicas e explorar redes de coautoria.
        </p>
        <SearchBar onSearch={setSearchTerm} />
        <GraphContainer searchTerm={searchTerm} />
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
