import React from 'react';
import './LandingPage.css';

export default function LandingPage({ onStart, onBrowse }) {
  return (
    <div className="landing-container">
      <div className="content">
        <h1>
          Your Music,<br />
          Your Way
        </h1>
        <p>
          Experience music like never before with our intuitive
          and beautiful music player. Stream your favorite
          tracks anytime, anywhere.
        </p>
        <div className="buttons">
          <button className="primary" onClick={onStart}>
            Start Listening
          </button>
          <button className="secondary" onClick={onBrowse}>
            Browse Tracks
          </button>
        </div>
      </div>
      
      <div className="features-section">
        <h2>Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon shuffle">
              <i className="fas fa-random"></i>
            </div>
            <h3>Smart Shuffle</h3>
            <p>Intelligently shuffle your music based on your listening habits.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon library">
              <i className="fas fa-list"></i>
            </div>
            <h3>Organized Library</h3>
            <p>Keep your music organized with our intuitive library management.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon favorites">
              <i className="fas fa-heart"></i>
            </div>
            <h3>Favorites</h3>
            <p>Mark your favorite tracks and create personalized playlists.</p>
          </div>
        </div>
      </div>
      
      <div className="player-preview">
        <div className="play-button">
          <i className="fas fa-play"></i>
        </div>
      </div>
    </div>
  );
}