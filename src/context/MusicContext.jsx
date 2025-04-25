import React, { createContext, useContext, useState, useEffect, useRef } from 'react';

const MusicContext = createContext();

export function MusicProvider({ children }) {
  const [tracks, setTracks] = useState([]);
  const [currentTrackIndex, setCurrentTrackIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isRepeating, setIsRepeating] = useState(false);
  const [isShuffling, setIsShuffling] = useState(false);
  const [currentTime, setCurrentTime] = useState('00:00');
  const [duration, setDuration] = useState('00:00');
  const [progress, setProgress] = useState(0);
  const [showLibrary, setShowLibrary] = useState(false);
  const [likedTracks, setLikedTracks] = useState([]);
  const audioRef = useRef(new Audio());

  // Load track list once
  useEffect(() => {
    fetch('/db.json')
      .then(res => res.json())
      .then(data => setTracks(data))
      .catch(console.error);
  }, []);

  // Sync audio element on change
  useEffect(() => {
    if (!tracks.length) return;
    const audio = audioRef.current;
    audio.src = tracks[currentTrackIndex].file;

    const onTime = () => {
      if (!isNaN(audio.duration)) {
        setCurrentTime(formatTime(audio.currentTime));
        setProgress((audio.currentTime / audio.duration) * 100);
      }
    };
    const onMeta = () => {
      if (!isNaN(audio.duration)) {
        setDuration(formatTime(audio.duration));
      }
    };
    const onEnd = () => {
      if (isRepeating) {
        audio.currentTime = 0;
        audio.play();
      } else {
        nextTrack();
      }
    };

    audio.addEventListener('timeupdate', onTime);
    audio.addEventListener('loadedmetadata', onMeta);
    audio.addEventListener('ended', onEnd);

    isPlaying ? audio.play() : audio.pause();

    return () => {
      audio.removeEventListener('timeupdate', onTime);
      audio.removeEventListener('loadedmetadata', onMeta);
      audio.removeEventListener('ended', onEnd);
    };
  }, [tracks, currentTrackIndex, isPlaying, isRepeating]);

  const formatTime = secs => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60)
      .toString()
      .padStart(2, '0');
    return `${m}:${s}`;
  };

  const togglePlay = () => setIsPlaying(p => !p);

  const playTrack = idx => {
    setCurrentTrackIndex(idx);
    setIsPlaying(true);
  };

  const nextTrack = () => {
    if (isShuffling && tracks.length > 1) {
      let rand;
      do { rand = Math.floor(Math.random() * tracks.length); }
      while (rand === currentTrackIndex);
      setCurrentTrackIndex(rand);
    } else {
      setCurrentTrackIndex(i => (i === tracks.length - 1 ? 0 : i + 1));
    }
    setIsPlaying(true);
  };

  const prevTrack = () => {
    if (isShuffling && tracks.length > 1) {
      let rand;
      do { rand = Math.floor(Math.random() * tracks.length); }
      while (rand === currentTrackIndex);
      setCurrentTrackIndex(rand);
    } else {
      setCurrentTrackIndex(i => (i === 0 ? tracks.length - 1 : i - 1));
    }
    setIsPlaying(true);
  };

  const seekTo = pct => {
    const audio = audioRef.current;
    if (!isNaN(audio.duration)) {
      audio.currentTime = (audio.duration * pct) / 100;
    }
  };

  const replayTrack = () => {
    const audio = audioRef.current;
    audio.currentTime = 0;
    setIsRepeating(r => !r);
    if (!isPlaying) {
      audio.play();
      setIsPlaying(true);
    }
  };

  const toggleShuffle = () => setIsShuffling(s => !s);
  const toggleLibraryView = () => setShowLibrary(v => !v);

  // Like/unlike a single track
  const toggleLike = id =>
    setLikedTracks(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );

  const setVolume = pct => {
    audioRef.current.volume = pct / 100;
  };

  return (
    <MusicContext.Provider value={{
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
    }}>
      {children}
    </MusicContext.Provider>
  );
}

export const useMusic = () => useContext(MusicContext);
