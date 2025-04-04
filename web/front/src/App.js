// src/App.js
import React, { useState } from 'react';
import Navbar from './components/Navbar';
import GraphContainer from './components/Graph_container';

const App = () => {
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="bg-[#47476b] text-white">
      <Navbar onSearch={(term) => setSearchTerm(term)} />
      <div className="container mx-auto text-center py-12 px-4">
        <h1 className="text-5xl font-extrabold mb-4">Universafinity</h1>
        <p className="text-lg text-gray-300 max-w-2xl mx-auto mb-8">
          Um ambiente interativo para visualizar conexões acadêmicas e explorar redes de coautoria.
        </p>
        <GraphContainer searchTerm={searchTerm} />
      </div>
    </div>
  );
};
export default App;
