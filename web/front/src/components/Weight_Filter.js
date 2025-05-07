// src/components/WeightFilter.js
import React from 'react';

// Serve como um filtro para o peso mínimo da conexão entre o nó pesquisado e seus vizinhos
const WeightFilter = ({ minWeight, setMinWeight }) => (
  <div className="text-center text-white mt-4">
    <label htmlFor="weightRange" className="block mb-2 text-[#1E3A8A]">Peso de conexões entre docentes: {minWeight}</label>
    <input
      id="weightRange"
      type="range"
      min="1"
      max="10"
      value={minWeight}
      onChange={(e) => setMinWeight(Number(e.target.value))}
      className="w-full max-w-md"
    />
  </div>
);

export default WeightFilter;
