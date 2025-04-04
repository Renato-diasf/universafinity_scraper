// src/Navbar.js
import React, {useState} from 'react';



const Navbar = ({ onSearch }) => {

  const [searchTerm, setSearchTerm] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearch(searchTerm.trim());
    }
  };

  return(
    <nav className="bg-[#7575a3] py-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center px-6">
        <span className="text-xl font-bold">Universafinity</span>
        <form onSubmit={handleSubmit} className="flex items-center gap-2">
            <input
              type="text"
              placeholder="Buscar nome no grafo..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="px-3 py-1 rounded-md focus:outline-none focus:ring w-64 text-black"
            />
            <button
              type="submit"
              className="bg-[#5a5a87] text-white px-4 py-1 rounded-md hover:bg-[#47476a] transition"
            >
              Buscar
            </button>
        </form>
      </div>
    </nav>
  );
};

export default Navbar;
