import sys
import os
import hashlib
import json

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from lib.models.base import get_session
from lib.models.models import User, Artist, Album, Genre, Song, Playlist

def hash_password(password):
    """Simple password hashing using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def seed_data():
    """Seed the database with your music data"""
    session = get_session()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        session.query(Playlist).delete()
        session.query(Song).delete()
        session.query(Album).delete()
        session.query(Artist).delete()
        session.query(Genre).delete()
        session.query(User).delete()
        session.commit()
        
        # Create users
        print("Creating users...")
        user1 = User.create(session, "john_doe", "john@example.com", hash_password("password123"))
        user2 = User.create(session, "jane_smith", "jane@example.com", hash_password("password456"))
        user3 = User.create(session, "admin", "admin@example.com", hash_password("admin123"))
        user4 = User.create(session, "music_lover", "music@example.com", hash_password("music123"))
        
        # Your music data
        music_data = [
            {
                "id": 1,
                "file": "/Files/Survivor s Guilt   Dave.m4a",
                "cover": "/Files/Survivor.jfif",
                "title": "Survivor's Guilt",
                "artist": "Satan Dave",
                "album": "Satanic Sessions",
                "genre": "Hip Hop",
                "duration": "3:47"
            },
            {
                "id": 2,
                "file": "/Files/Laho.m4a",
                "cover": "/Files/enjoyment.jfif",
                "title": "Minister of Enjoyment",
                "artist": "Laho",
                "album": "Joyful Hymns",
                "genre": "Rumba",
                "duration": "4:02"
            },
            {
                "id": 3,
                "file": "/Files/BURUKLYN BOYZ, MR RIGHT - PIGA LEAN (Dir By AllDayAmar ) - BURUKLYN BOYZ.mp3",
                "cover": "/Files/Boyz.jpg",
                "title": "Piga Lean",
                "artist": "BURUKLYN BOYZ",
                "album": "Street Anthems",
                "genre": "Kenyan Hip Hop",
                "duration": "3:21"
            },
            {
                "id": 4,
                "file": "/Files/Lucky-Dube-One-Love.mp3",
                "cover": "/Files/lucky.jpg",
                "title": "One-Love",
                "artist": "Lucky Dube",
                "album": "National Splendour",
                "genre": "Reggae",
                "duration": "4:05"
            },
            {
                "id": 5,
                "file": "/Files/King Kaka Ft Scar Mkadinali & Sewersydaa - Soko.mp3",
                "cover": "/Files/soko.jfif",
                "title": "Soko",
                "artist": "Wakadinali",
                "album": "Marketplace Vibes",
                "genre": "Kenyan Hip Hop",
                "duration": "3:12"
            },
            {
                "id": 6,
                "file": "/Files/Marioo-Nairobi-Feat-Bien.mp3",
                "cover": "/Files/mario.jfif",
                "title": "Nairobi (feat. Bien)",
                "artist": "Marioo",
                "album": "City Lights",
                "genre": "Bongo Flava",
                "duration": "3:36"
            },
            {
                "id": 7,
                "file": "/Files/WAKADINALI-Mariwanna.mp3",
                "cover": "/Files/wakad.jfif",
                "title": "Mariwanna",
                "artist": "Wakadinali",
                "album": "Urban Tales",
                "genre": "Kenyan Hip Hop",
                "duration": "3:50"
            },
            {
                "id": 8,
                "file": "/Files/PRIDE.m4a",
                "cover": "/Files/kendrick.jpg",
                "title": "Pride",
                "artist": "Kendrick Lamar",
                "album": "DAMN.",
                "genre": "Hip Hop",
                "duration": "3:34"
            },
            {
                "id": 9,
                "file": "/Files/psycho.mp3",
                "cover": "./Files/Survivor.jfif",
                "title": "Psycho",
                "artist": "Satan Dave",
                "album": "Satanic Sessions",
                "genre": "Hip Hop",
                "duration": "3:47"
            },
            {
                "id": 10,
                "file": "/Files/19th Birthday.mp3",
                "cover": "/Files/Survivor.jfif",
                "title": "My 19th Birthday",
                "artist": "Satan Dave",
                "album": "Satanic Sessions",
                "genre": "Hip Hop",
                "duration": "3:47"
            },
            {
                "id": 11,
                "file": "./Files/Titanium.m4a",
                "cover": "/Files/Survivor.jfif",
                "title": "Titanium",
                "artist": "Satan Dave",
                "album": "Satanic Sessions",
                "genre": "Hip Hop",
                "duration": "3:47"
            },
            {
                "id": 12,
                "file": "/Files/How I met my ex.mp3",
                "cover": "/Files/Survivor.jfif",
                "title": "How I Met My Ex",
                "artist": "Satan Dave",
                "album": "Satanic Sessions",
                "genre": "Hip Hop",
                "duration": "3:47"
            },
            {
                "id": 13,
                "file": "/Files/Money Trees (feat. Jay Rock)   Kendrick Lamar.m4a",
                "cover": "./Files/money.jfif",
                "title": "Money Trees (feat. Jay Rock)",
                "artist": "Kendrick Lamar",
                "album": "good kid, m.A.A.d city",
                "genre": "Hip Hop",
                "duration": "5:25"
            },
            {
                "id": 14,
                "file": "/Files/Not Like Us   Kendrick Lamar.m4a",
                "cover": "./Files/notlike.jfif",
                "title": "Not Like Us",
                "artist": "Kendrick Lamar",
                "album": "good kid, m.A.A.d city",
                "genre": "Hip Hop",
                "duration": "3:45"
            }
        ]
        
        # Extract unique genres, artists, and albums from the data
        unique_genres = set()
        unique_artists = set()
        unique_albums = set()
        
        for song_data in music_data:
            unique_genres.add(song_data["genre"])
            unique_artists.add(song_data["artist"])
            unique_albums.add(song_data["album"])
        
        # Create genres
        print("Creating genres...")
        genre_map = {}
        for genre_name in unique_genres:
            genre = Genre.create(session, genre_name)
            genre_map[genre_name] = genre
            print(f"  - {genre_name}")
        
        # Create artists
        print("Creating artists...")
        artist_map = {}
        for artist_name in unique_artists:
            artist = Artist.create(session, artist_name)
            artist_map[artist_name] = artist
            print(f"  - {artist_name}")
        
        # Create albums
        print("Creating albums...")
        album_map = {}
        for album_name in unique_albums:
            # Use the first cover image found for this album
            cover_image = None
            for song_data in music_data:
                if song_data["album"] == album_name:
                    cover_image = song_data["cover"]
                    break
            
            album = Album.create(session, album_name, cover_image)
            album_map[album_name] = album
            print(f"  - {album_name}")
        
        # Create songs
        print("Creating songs...")
        created_songs = []
        for song_data in music_data:
            artist = artist_map[song_data["artist"]]
            album = album_map[song_data["album"]]
            genre = genre_map[song_data["genre"]]
            
            song = Song.create(
                session,
                title=song_data["title"],
                artist_id=artist.id,
                album_id=album.id,
                genre_id=genre.id,
                file_path=song_data["file"],
                cover_image=song_data["cover"],
                duration=song_data["duration"]
            )
            created_songs.append(song)
            print(f"  - {song_data['title']} by {song_data['artist']}")
        
        # Create some sample playlists
        print("Creating sample playlists...")
        
        # Hip Hop playlist - only Hip Hop genre songs
        hip_hop_songs = [s for s in created_songs if s.genre.name == "Hip Hop"]
        if hip_hop_songs:
            hip_hop_playlist = Playlist.create(session, user1.id, "Hip Hop Favorites")
            for i, song in enumerate(hip_hop_songs[:5], 1):  # Add first 5 Hip Hop songs
                hip_hop_playlist.add_song(session, song.id, i)
        
        # Kenyan Hip Hop playlist
        kenyan_songs = [s for s in created_songs if s.genre.name == "Kenyan Hip Hop"]
        if kenyan_songs:
            kenyan_playlist = Playlist.create(session, user2.id, "Kenyan Vibes")
            for i, song in enumerate(kenyan_songs, 1):
                kenyan_playlist.add_song(session, song.id, i)
        
        # Satan Dave playlist
        dave_songs = [s for s in created_songs if s.artist.name == "Satan Dave"]
        if dave_songs:
            dave_playlist = Playlist.create(session, user4.id, "Satan Dave Collection")
            for i, song in enumerate(dave_songs, 1):
                dave_playlist.add_song(session, song.id, i)
        
        # Kendrick Lamar playlist
        kendrick_songs = [s for s in created_songs if s.artist.name == "Kendrick Lamar"]
        if kendrick_songs:
            kendrick_playlist = Playlist.create(session, user1.id, "Kendrick Classics")
            for i, song in enumerate(kendrick_songs, 1):
                kendrick_playlist.add_song(session, song.id, i)
        
        # Mixed playlist - different songs from different genres
        if len(created_songs) >= 5:
            mixed_playlist = Playlist.create(session, user3.id, "Admin's Mix")
            # Select songs from different genres to avoid duplicates
            selected_songs = []
            used_songs = set()
            
            # Try to get one song from each genre
            for genre_name in unique_genres:
                genre_songs = [s for s in created_songs if s.genre.name == genre_name and s.id not in used_songs]
                if genre_songs:
                    selected_songs.append(genre_songs[0])
                    used_songs.add(genre_songs[0].id)
                    if len(selected_songs) >= 5:
                        break
            
            # If we need more songs, add from remaining
            if len(selected_songs) < 5:
                remaining_songs = [s for s in created_songs if s.id not in used_songs]
                for song in remaining_songs:
                    selected_songs.append(song)
                    if len(selected_songs) >= 5:
                        break
            
            for i, song in enumerate(selected_songs, 1):
                mixed_playlist.add_song(session, song.id, i)
        
        print("\nDatabase seeded successfully with your music collection!")
        print(f"Created {len(User.get_all(session))} users")
        print(f"Created {len(Artist.get_all(session))} artists")
        print(f"Created {len(Album.get_all(session))} albums")
        print(f"Created {len(Genre.get_all(session))} genres")
        print(f"Created {len(Song.get_all(session))} songs")
        print(f"Created {len(Playlist.get_all(session))} playlists")
        
        # Print summary by genre
        print("\n=== Music Collection Summary ===")
        for genre_name, genre in genre_map.items():
            song_count = len([s for s in created_songs if s.genre.name == genre_name])
            print(f"{genre_name}: {song_count} songs")
        
        # Print summary by artist
        print("\n=== Artists Summary ===")
        for artist_name, artist in artist_map.items():
            song_count = len([s for s in created_songs if s.artist.name == artist_name])
            print(f"{artist_name}: {song_count} songs")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()