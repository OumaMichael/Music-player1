import React from 'react';
import { useMusic } from '../context/MusicContext';
import './Player.css';

export default function Player() {
  const {
    tracks,
    currentTrackIndex,
    isPlaying,
    isRepeating,
    isShuffling,
    currentTime,
    duration,
    progress,
    showLibrary,
    likedTracks,
    togglePlay,
    playTrack,
    nextTrack,
    prevTrack,
    seekTo,
    replayTrack,
    toggleShuffle,
    toggleLibraryView,
    toggleLike,
    setVolume,
  } = useMusic();

  const current = tracks[currentTrackIndex] || {};
  const isCurrentTrackLiked = current.id
    ? likedTracks.includes(current.id)
    : false;

  return (
    <div className="player-container">
      <div className="playing-info">
        PLAYING {currentTrackIndex + 1} OF {tracks.length}
      </div>

      <div className="album-cover">
        <img
          src={current.cover || '/images/default-cover.jpg'}
          alt={current.title}
        />
      </div>

      <div className="track-info">
        <h2>{current.title || 'Loading...'}</h2>
        <p>{current.artist || 'Artist'}</p>
      </div>

      <div className="control-buttons">
        {/* Shuffle */}
        <button
          className={`control-btn shuffle ${isShuffling ? 'active' : ''}`}
          onClick={toggleShuffle}
          title="Shuffle"
        >
          <i className="fa fa-random"></i>
        </button>

        {/* Previous */}
        <button
          className="control-btn"
          onClick={prevTrack}
          title="Previous"
        >
          <i className="fa fa-step-backward"></i>
        </button>

        {/* Play / Pause */}
        <button
          className="control-btn play"
          onClick={togglePlay}
          title="Play/Pause"
        >
          <i className={`fa ${isPlaying ? 'fa-pause' : 'fa-play'}`}></i>
        </button>

        {/* Next */}
        <button
          className="control-btn"
          onClick={nextTrack}
          title="Next"
        >
          <i className="fa fa-step-forward"></i>
        </button>

        {/* Repeat-one */}
        <button
          className={`control-btn repeat ${isRepeating ? 'active' : ''}`}
          onClick={replayTrack}
          title="Repeat Current Track"
        >
          <i className="fa fa-redo"></i>
        </button>

        {/* Library toggle */}
        <button
          className="control-btn library"
          onClick={toggleLibraryView}
          title="Library"
        >
          <i className="fa fa-list"></i>
        </button>

        {/* Like current track only */}
        <button
          className={`control-btn like-btn ${
            isCurrentTrackLiked ? 'liked' : ''
          }`}
          onClick={() => toggleLike(current.id)}
          title="Like"
        >
          <i className="fa fa-heart"></i>
        </button>
      </div>

      {/* Progress */}
      <div className="progress-container">
        <span className="time current">{currentTime}</span>
        <input
          type="range"
          min="0"
          max="100"
          value={progress}
          className="progress-bar"
          onChange={e => seekTo(e.target.value)}
        />
        <span className="time duration">{duration}</span>
      </div>

      {/* Volume */}
      <div className="volume-container">
        <i className="fa fa-volume-down"></i>
        <input
          type="range"
          min="0"
          max="100"
          defaultValue="80"
          className="volume-bar"
          onChange={e => setVolume(e.target.value)}
        />
        <i className="fa fa-volume-up"></i>
      </div>

      {/* Mini-library */}
      {showLibrary && (
        <div className="mini-library">
          <h3>Library</h3>
          <ul>
            {tracks.map((track, idx) => {
              const isActive = idx === currentTrackIndex;
              const isLiked = likedTracks.includes(track.id);
              return (
                <li
                  key={track.id}
                  className={isActive ? 'active' : ''}
                  onClick={() => playTrack(idx)}
                >
                  <img src={track.cover} alt={track.title} />
                  <div>
                    <span className="title">{track.title}</span>
                    <span className="artist">{track.artist}</span>
                  </div>

                  {/* show pause on the active track */}
                  <button
                    className="play-btn"
                    onClick={e => {
                      e.stopPropagation();
                      isActive ? togglePlay() : playTrack(idx);
                    }}
                  >
                    <i
                      className={`fa ${
                        isActive && isPlaying ? 'fa-pause' : 'fa-play'
                      }`}
                    ></i>
                  </button>

                  {/* per-item like */}
                  <button
                    className={`like-btn ${isLiked ? 'liked' : ''}`}
                    onClick={e => {
                      e.stopPropagation();
                      toggleLike(track.id);
                    }}
                  >
                    <i className="fa fa-heart"></i>
                  </button>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
}
