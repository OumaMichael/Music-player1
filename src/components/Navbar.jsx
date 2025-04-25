// src/components/Navbar.js
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

export default function Navbar() {
  const loc = useLocation();
  return (
    <nav className="nav">
      <div className="logo"><Link to="/">🎵 Melodify</Link></div>
      <div className="links">
        {loc.pathname !== '/'       && <Link to="/">Home</Link>}
        {loc.pathname !== '/player' && <Link to="/player">Player</Link>}
        {loc.pathname !== '/library'&& <Link to="/library">Tracklist</Link>}
      </div>
    </nav>
  );
}
