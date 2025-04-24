import React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import Player from './components/Player';
import Library from './components/Library';
import Navbar from './components/Navbar';
import './App.css';

export default function App() {
  const navigate = useNavigate();
  
  return (
    <>
      <Navbar />
      <Routes>
        {/* Landing Page */}
        <Route path="/" element={
          <LandingPage 
            onStart={() => navigate('/player')}
            onBrowse={() => navigate('/library')}
          />
        } />
        
        {/* Player View */}
        <Route path="/player" element={<Player />} />
        
        {/* Library View */}
        <Route path="/library" element={<Library />} />
      </Routes>
    </>
  );
}
