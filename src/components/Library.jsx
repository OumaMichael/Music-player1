/* src/components/Library.jsx */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMusic } from '../context/MusicContext';
import './Library.css';

export default function Library() {
  const {
    tracks,
    currentTrackIndex,
    isPlaying,
    playTrack,
    togglePlay,
    likedTracks,
    toggleLike
  } = useMusic();
  const [selectedTrack, setSelectedTrack] = useState(null);
  const navigate = useNavigate();

  const handleTrackSelect = track => setSelectedTrack(track);
  const handlePlayButton = idx => {
    if (idx === currentTrackIndex) {
      togglePlay();
    } else {
      playTrack(idx);
      navigate(`/player?track=${idx}`);
    }
  };
  const handleLike = (e, id) => { 
    e.stopPropagation(); 
    toggleLike(id); 
  };

  const selectedIndex = selectedTrack
    ? tracks.findIndex(t => t.id === selectedTrack.id)
    : -1;

  return (
    <div className="library-container">
      <h1>Music Library</h1>
      <div className="library-content">
        <div className="tracks-list">
          <h3>All Tracks</h3>
          <div className="tracks">
            {tracks.map((track, index) => {
              const isLiked = likedTracks.includes(track.id);
              const isActive = index === currentTrackIndex;
              const showPause = isActive && isPlaying;
              return (
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
                    <button
                      className="play-btn"
                      onClick={e => {
                        e.stopPropagation();
                        handlePlayButton(index);
                      }}
                    >
                      <i className={`fa ${showPause ? 'fa-pause' : 'fa-play'}`} />
                    </button>
                    <button
                      className={`like-btn ${isLiked ? 'liked' : ''}`}
                      onClick={e => handleLike(e, track.id)}
                    >
                      <i className="fa fa-heart" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {selectedTrack && selectedIndex !== -1 && (
          <div className="track-details-panel">
            <div className="track-header">
              <h3>Track Details</h3>
              <button className="close-btn" onClick={() => setSelectedTrack(null)}>
                <i className="fa fa-times" />
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
                  <span className="label">Album:</span>{' '}
                  <span className="value">{selectedTrack.album}</span>
                </div>
                <div className="metadata-item">
                  <span className="label">Genre:</span>{' '}
                  <span className="value">{selectedTrack.genre}</span>
                </div>
                <div className="metadata-item">
                  <span className="label">Duration:</span>{' '}
                  <span className="value">{selectedTrack.duration}</span>
                </div>
              </div>
              <div className="detail-actions">
                {/*
                  Show pause icon and togglePlay if this track is current,
                  otherwise play and navigate to it
                */}
                <button
                  className="action-btn primary"
                  onClick={() => {
                    if (selectedIndex === currentTrackIndex) {
                      togglePlay();
                    } else {
                      playTrack(selectedIndex);
                      navigate(`/player?track=${selectedIndex}`);
                    }
                  }}
                >
                  <i
                    className={`fa ${
                      selectedIndex === currentTrackIndex && isPlaying
                        ? 'fa-pause'
                        : 'fa-play'
                    }`}
                  />{' '}
                  {selectedIndex === currentTrackIndex && isPlaying ? 'Pause' : 'Play'}
                </button>
                <button
                  className={`action-btn like-btn ${
                    likedTracks.includes(selectedTrack.id) ? 'liked' : ''
                  }`}
                  onClick={e => handleLike(e, selectedTrack.id)}
                >
                  <i className="fa fa-heart" /> Like
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
