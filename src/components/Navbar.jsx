import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

export default function Navbar() {
  const location = useLocation();
  
  return (
    <nav className="nav">
      <div className="logo">
        <Link to="/">🎵 Melodify</Link>
      </div>
      <div className="links">
        <Link to="/">Home</Link>
        <Link to="/player">Player</Link>
        <Link to="/library">Tracklist</Link>
      </div>
    </nav>
  );
}