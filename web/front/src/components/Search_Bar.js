import React, { useState, useEffect } from 'react';

const SearchBar = ({ onSearch, nodeList = [] }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    if (searchTerm.trim()) {
      const matches = nodeList
        .filter((name) =>
          name.toLowerCase().includes(searchTerm.toLowerCase())
        )
        .slice(0, 5); // mostrar no máximo 5 sugestões

      setSuggestions(matches);
    } else {
      setSuggestions([]);
    }
  }, [searchTerm, nodeList]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearch(searchTerm.trim());
    }
  };

  const handleSuggestionClick = (name) => {
    setSearchTerm(name);
    setSuggestions([]);
    onSearch(name);
  };

  return (
    <div className="relative w-full flex justify-center my-6 px-4">
      <form
        onSubmit={handleSubmit}
        className="flex w-full max-w-2xl items-center bg-white border border-gray-300 rounded-xl shadow-md px-4 py-2 focus-within:ring-2 focus-within:ring-blue-400 transition"
      >
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
      </form>

      {suggestions.length > 0 && (
        <ul className="absolute top-full mt-1 w-full max-w-2xl bg-white border border-gray-300 rounded-lg shadow-md z-10 overflow-hidden">
          {suggestions.map((name, idx) => (
            <li
              key={idx}
              onClick={() => handleSuggestionClick(name)}
              className="px-4 py-2 hover:bg-blue-100 cursor-pointer text-black"
            >
              {name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchBar;
