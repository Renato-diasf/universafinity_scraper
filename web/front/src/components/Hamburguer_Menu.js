import React from 'react';
import { Link } from 'react-router-dom';

const HamburgerMenu = ({ onClose }) => {
  return (
    <div className="absolute top-16 right-6 bg-white shadow-lg rounded-md w-52 z-50">
      <ul className="flex flex-col">
        <li>
          <Link
            to="/"
            className="block px-4 py-2 text-gray-800 hover:bg-gray-200"
            onClick={onClose}
          >
            Página Inicial
          </Link>
        </li>
        <li>
          <Link
            to="/grafo2"
            className="block px-4 py-2 text-gray-800 hover:bg-gray-200"
            onClick={onClose}
          >
            Grafo 2
          </Link>
        </li>
        <li>
          <Link
            to="/grafo3"
            className="block px-4 py-2 text-gray-800 hover:bg-gray-200"
            onClick={onClose}
          >
            Grafo 3
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default HamburgerMenu;
