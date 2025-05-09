// src/Navbar.js
import React, { useState } from 'react';
import HamburgerMenu from './Hamburguer_Menu';
import { Menu } from 'lucide-react';



const Navbar = () => {

  const [menuOpen, setMenuOpen] = useState(false);

  return(
    <nav className="bg-[#D1D5DB] py-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center px-6">
        <span className="text-xl font-bold text-[#1E3A8A]">Universafinity</span>
        <button
          className="text-[#1E3A8A] focus:outline-none"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <Menu size={28} />
        </button>
      </div>
      {menuOpen && <HamburgerMenu onClose={() => setMenuOpen(false)} />}
    </nav>
  );
};

export default Navbar;
