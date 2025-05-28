from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from lib.models.models import User, Song, Artist, Album, Genre, Playlist, PlaylistSong
from lib.models.base import Base
import hashlib
import os

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'music_streaming.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Create and return a new database session"""
    return SessionLocal()

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    """Register a new user"""
    session = get_db_session()
    try:
        # Check if user already exists
        existing_user = session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            return False, "Username or email already exists"
        
        # Create new user
        hashed_password = hash_password(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        
        session.add(new_user)
        session.commit()
        
        # Return the user ID instead of the object
        user_id = new_user.id
        return True, user_id
        
    except Exception as e:
        session.rollback()
        return False, f"Registration failed: {str(e)}"
    finally:
        session.close()

def login_user(username, password):
    """Authenticate a user"""
    session = get_db_session()
    try:
        hashed_password = hash_password(password)
        user = session.query(User).filter(
            User.username == username,
            User.password_hash == hashed_password
        ).first()
        
        if user:
            # Return user data as a dictionary instead of the object
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin
            }
            return True, user_data
        else:
            return False, "Invalid username or password"
            
    except Exception as e:
        return False, f"Login failed: {str(e)}"
    finally:
        session.close()

def get_user_by_id(user_id):
    """Get user by ID"""
    session = get_db_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin
            }
            return user_data
        return None
    finally:
        session.close()

def search_songs(query):
    """Search for songs by title, artist, or album"""
    session = get_db_session()
    try:
        songs = session.query(Song).join(Artist).join(Album).filter(
            (Song.title.ilike(f'%{query}%')) |
            (Artist.name.ilike(f'%{query}%')) |
            (Album.title.ilike(f'%{query}%'))
        ).all()
        
        # Convert to dictionaries
        song_list = []
        for song in songs:
            song_data = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist.name,
                'album': song.album.title,
                'genre': song.genre.name if song.genre else 'Unknown',
                'duration': song.duration,
                'file_path': song.file_path
            }
            song_list.append(song_data)
        
        return song_list
    finally:
        session.close()

def get_all_songs():
    """Get all songs"""
    session = get_db_session()
    try:
        songs = session.query(Song).join(Artist).join(Album).all()
        
        song_list = []
        for song in songs:
            song_data = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist.name,
                'album': song.album.title,
                'genre': song.genre.name if song.genre else 'Unknown',
                'duration': song.duration,
                'file_path': song.file_path
            }
            song_list.append(song_data)
        
        return song_list
    finally:
        session.close()

def get_all_artists():
    """Get all artists"""
    session = get_db_session()
    try:
        artists = session.query(Artist).all()
        
        artist_list = []
        for artist in artists:
            artist_data = {
                'id': artist.id,
                'name': artist.name,
                'bio': artist.bio
            }
            artist_list.append(artist_data)
        
        return artist_list
    finally:
        session.close()

def get_artist_songs(artist_id):
    """Get all songs by an artist"""
    session = get_db_session()
    try:
        songs = session.query(Song).join(Artist).filter(Artist.id == artist_id).all()
        
        song_list = []
        for song in songs:
            song_data = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist.name,
                'album': song.album.title,
                'genre': song.genre.name if song.genre else 'Unknown',
                'duration': song.duration,
                'file_path': song.file_path
            }
            song_list.append(song_data)
        
        return song_list
    finally:
        session.close()

def get_user_playlists(user_id):
    """Get all playlists for a user"""
    session = get_db_session()
    try:
        playlists = session.query(Playlist).filter(Playlist.user_id == user_id).all()
        
        playlist_list = []
        for playlist in playlists:
            playlist_data = {
                'id': playlist.id,
                'name': playlist.name,
                'description': playlist.description,
                'created_at': playlist.created_at
            }
            playlist_list.append(playlist_data)
        
        return playlist_list
    finally:
        session.close()

def create_playlist(user_id, name, description=""):
    """Create a new playlist"""
    session = get_db_session()
    try:
        playlist = Playlist(
            name=name,
            description=description,
            user_id=user_id
        )
        
        session.add(playlist)
        session.commit()
        
        playlist_id = playlist.id
        return True, playlist_id
        
    except Exception as e:
        session.rollback()
        return False, f"Failed to create playlist: {str(e)}"
    finally:
        session.close()

def add_song_to_playlist(playlist_id, song_id):
    """Add a song to a playlist"""
    session = get_db_session()
    try:
        # Check if song is already in playlist
        existing = session.query(PlaylistSong).filter(
            PlaylistSong.playlist_id == playlist_id,
            PlaylistSong.song_id == song_id
        ).first()
        
        if existing:
            return False, "Song already in playlist"
        
        # Get the next position
        max_position = session.query(PlaylistSong).filter(
            PlaylistSong.playlist_id == playlist_id
        ).count()
        
        playlist_song = PlaylistSong(
            playlist_id=playlist_id,
            song_id=song_id,
            position=max_position + 1
        )
        
        session.add(playlist_song)
        session.commit()
        
        return True, "Song added to playlist"
        
    except Exception as e:
        session.rollback()
        return False, f"Failed to add song: {str(e)}"
    finally:
        session.close()

def get_playlist_songs(playlist_id):
    """Get all songs in a playlist"""
    session = get_db_session()
    try:
        playlist_songs = session.query(PlaylistSong).join(Song).join(Artist).join(Album).filter(
            PlaylistSong.playlist_id == playlist_id
        ).order_by(PlaylistSong.position).all()
        
        song_list = []
        for ps in playlist_songs:
            song = ps.song
            song_data = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist.name,
                'album': song.album.title,
                'genre': song.genre.name if song.genre else 'Unknown',
                'duration': song.duration,
                'file_path': song.file_path,
                'position': ps.position
            }
            song_list.append(song_data)
        
        return song_list
    finally:
        session.close()

def get_all_genres():
    """Get all genres"""
    session = get_db_session()
    try:
        genres = session.query(Genre).all()
        
        genre_list = []
        for genre in genres:
            genre_data = {
                'id': genre.id,
                'name': genre.name
            }
            genre_list.append(genre_data)
        
        return genre_list
    finally:
        session.close()

def get_songs_by_genre(genre_id):
    """Get all songs in a genre"""
    session = get_db_session()
    try:
        songs = session.query(Song).join(Artist).join(Album).filter(Song.genre_id == genre_id).all()
        
        song_list = []
        for song in songs:
            song_data = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist.name,
                'album': song.album.title,
                'genre': song.genre.name if song.genre else 'Unknown',
                'duration': song.duration,
                'file_path': song.file_path
            }
            song_list.append(song_data)
        
        return song_list
    finally:
        session.close()