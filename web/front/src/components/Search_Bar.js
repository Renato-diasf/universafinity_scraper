// src/SearchBar.js
import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearch(searchTerm.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full flex justify-center my-6 px-4">
      <div className="flex w-full max-w-2xl items-center bg-white border border-gray-300 rounded-xl shadow-md px-4 py-2 focus-within:ring-2 focus-within:ring-blue-400 transition">
        <input
          type="text"
          placeholder="Busque um docente pelo nome aqui!"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full text-black outline-none text-base placeholder-gray-500"
        />
        <button
          type="submit"
          className="ml-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-1 rounded-md transition"
        >
          Buscar
        </button>
      </div>
    </form>
  );
};

export default SearchBar;
