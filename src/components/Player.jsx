import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import './Player.css';

export default function Player() {
  const [tracks, setTracks] = useState([]);
  const [currentTrack, setCurrentTrack] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState('00:00');
  const [duration, setDuration] = useState('00:00');
  const [progress, setProgress] = useState(0);
  const [showLibrary, setShowLibrary] = useState(false);
  const audioRef = useRef(new Audio());

  // Fetch data from dj.json in public folder
  useEffect(() => {
    fetch("/db.json")
      .then(response => response.json())
      .then(data => {
        setTracks(data);
      })
      .catch(error => {
        console.error('Error fetching tracks:', error);
      });
  }, []);

  useEffect(() => {
    if (tracks.length === 0) return;
    
    const audio = audioRef.current;
    audio.src = tracks[currentTrack]?.file;
    
    if (isPlaying) {
      audio.play();
    }
    
    const updateTime = () => {
      if (audio.duration) {
        setCurrentTime(formatTime(audio.currentTime));
        setProgress((audio.currentTime / audio.duration) * 100);
      }
    };
    
    const loadMetadata = () => {
      setDuration(formatTime(audio.duration));
    };
    
    const handleEnded = () => {
      if (currentTrack < tracks.length - 1) {
        setCurrentTrack(currentTrack + 1);
      } else {
        setCurrentTrack(0);
      }
    };
    
    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('loadedmetadata', loadMetadata);
    audio.addEventListener('ended', handleEnded);
    
    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('loadedmetadata', loadMetadata);
      audio.removeEventListener('ended', handleEnded);
    };
  }, [currentTrack, tracks, isPlaying]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60).toString().padStart(2, '0');
    return `${mins}:${secs}`;
  };

  const togglePlay = () => {
    const audio = audioRef.current;
    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handlePrevious = () => {
    setCurrentTrack((prev) => (prev === 0 ? tracks.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setCurrentTrack((prev) => (prev === tracks.length - 1 ? 0 : prev + 1));
  };

  const handleSeek = (e) => {
    const audio = audioRef.current;
    const seekTime = (audio.duration * e.target.value) / 100;
    audio.currentTime = seekTime;
  };

  const toggleLibrary = () => {
    setShowLibrary(!showLibrary);
  };

  const playTrack = (index) => {
    setCurrentTrack(index);
    setIsPlaying(true);
  };

  return (
    <div className="player-container">
      <div className="playing-info">
        PLAYING {currentTrack + 1} OF {tracks.length}
      </div>
      
      <div className="album-cover">
        <img 
          src={tracks[currentTrack]?.cover || '/images/default-cover.jpg'} 
          alt={tracks[currentTrack]?.title || 'Album cover'} 
        />
      </div>
      
      <div className="track-info">
        <h2>{tracks[currentTrack]?.title || 'Loading...'}</h2>
        <p>{tracks[currentTrack]?.artist || 'Artist'}</p>
      </div>
      
      <div className="control-buttons">
        <button className="control-btn shuffle">
          <i className="fa fa-random"></i>
        </button>
        <button className="control-btn" onClick={handlePrevious}>
          <i className="fa fa-step-backward"></i>
        </button>
        <button className="control-btn play" onClick={togglePlay}>
          <i className={`fa ${isPlaying ? 'fa-pause' : 'fa-play'}`}></i>
        </button>
        <button className="control-btn" onClick={handleNext}>
          <i className="fa fa-step-forward"></i>
        </button>
        <button className="control-btn repeat">
          <i className="fa fa-repeat"></i>
        </button>
        <button className="control-btn" onClick={toggleLibrary}>
          <i className="fa fa-list"></i>
        </button>
      </div>
      
      <div className="progress-container">
        <span className="time current">{currentTime}</span>
        <input
          type="range"
          min="0"
          max="100"
          value={progress}
          className="progress-bar"
          onChange={handleSeek}
        />
        <span className="time duration">{duration}</span>
      </div>
      
      <div className="volume-container">
        <i className="fa fa-volume-down"></i>
        <input
          type="range"
          min="0"
          max="100"
          defaultValue="80"
          className="volume-bar"
          onChange={(e) => {
            audioRef.current.volume = e.target.value / 100;
          }}
        />
        <i className="fa fa-volume-up"></i>
      </div>
      
      {showLibrary && (
        <div className="mini-library">
          <h3>Library</h3>
          <ul>
            {tracks.map((track, index) => (
              <li 
                key={track.id} 
                className={currentTrack === index ? 'active' : ''}
                onClick={() => playTrack(index)}
              >
                <img src={track.cover} alt={track.title} />
                <div>
                  <span className="title">{track.title}</span>
                  <span className="artist">{track.artist}</span>
                </div>
                <button className="play-btn">
                  <i className="fa fa-play"></i>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}