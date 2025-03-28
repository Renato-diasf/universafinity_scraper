// src/App.js
import React from 'react';
import Navbar from './components/Navbar';
import GraphContainer from './components/Graph_container';

const App = () => (
  <div className="bg-[#47476b] text-white">
    <Navbar />
    <div className="container mx-auto text-center py-12 px-4">
      <h1 className="text-5xl font-extrabold mb-4">Universafinity</h1>
      <p className="text-lg text-gray-300 max-w-2xl mx-auto mb-8">
        Um ambiente interativo para visualizar conexões acadêmicas e explorar redes de coautoria.
      </p>
      <GraphContainer />
    </div>
  </div>
);

export default App;
