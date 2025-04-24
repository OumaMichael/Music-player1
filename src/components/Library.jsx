import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Library.css';

export default function Library() {
  const [tracks, setTracks] = useState([]);
  const [selectedTrack, setSelectedTrack] = useState(null);
  const navigate = useNavigate();

  // Fetch data from dj.json in public folder
  useEffect(() => {
    fetch('/db.json')
      .then(response => response.json())
      .then(data => {
        setTracks(data);
      })
      .catch(error => {
        console.error('Error fetching tracks:', error);
      });
  }, []);

  const handleTrackSelect = (track) => {
    setSelectedTrack(track);
  };

  const playTrack = (trackId) => {
    navigate(`/player?track=${trackId}`);
  };

  const likeTrack = (e, trackId) => {
    e.stopPropagation();
    // Add like functionality
    console.log('Liked track:', trackId);
  };

  return (
    <div className="library-container">
      <h1>Music Library</h1>
      
      <div className="library-content">
        <div className="tracks-list">
          <h3>All Tracks</h3>
          
          <div className="tracks">
            {tracks.map((track) => (
              <div
                key={track.id}
                className={`track-item ${selectedTrack?.id === track.id ? 'selected' : ''}`}
                onClick={() => handleTrackSelect(track)}
              >
                <img src={track.cover} alt={track.title} />
                <div className="track-details">
                  <span className="track-title">{track.title}</span>
                  <span className="track-artist">{track.artist}</span>
                </div>
                <div className="track-actions">
                  <button className="play-btn" onClick={() => playTrack(track.id)}>
                    <i className="fa fa-play"></i>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {selectedTrack && (
          <div className="track-details-panel">
            <div className="track-header">
              <h3>Track Details</h3>
              <button className="close-btn" onClick={() => setSelectedTrack(null)}>
                <i className="fa fa-times"></i>
              </button>
            </div>
            
            <div className="track-info">
              <img
                src={selectedTrack.cover}
                alt={selectedTrack.title}
                className="detail-cover"
              />
              
              <h2 className="detail-title">{selectedTrack.title}</h2>
              <p className="detail-artist">{selectedTrack.artist}</p>
              
              <div className="detail-metadata">
                <div className="metadata-item">
                  <span className="label">Album:</span>
                  <span className="value">{selectedTrack.album}</span>
                </div>
                <div className="metadata-item">
                  <span className="label">Genre:</span>
                  <span className="value">{selectedTrack.genre}</span>
                </div>
                <div className="metadata-item">
                  <span className="label">Duration:</span>
                  <span className="value">{selectedTrack.duration}</span>
                </div>
              </div>
              
              <div className="detail-actions">
                <button className="action-btn primary" onClick={() => playTrack(selectedTrack.id)}>
                  <i className="fa fa-play"></i> Play
                </button>
                <button className="action-btn" onClick={(e) => likeTrack(e, selectedTrack.id)}>
                  <i className="fa fa-heart"></i> Like
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}