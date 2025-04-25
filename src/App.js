/* src/App.jsx */
import React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { MusicProvider } from './context/MusicContext';
import LandingPage from './components/LandingPage';
import Player from './components/Player';
import Library from './components/Library';
import Navbar from './components/Navbar';
import './App.css';

export default function App() {
  const navigate = useNavigate();

  return (
    <MusicProvider>
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage onStart={() => navigate('/player')} onBrowse={() => navigate('/library')} />} />
        <Route path="/player" element={<Player />} />
        <Route path="/library" element={<Library />} />
      </Routes>
    </MusicProvider>
  );
}