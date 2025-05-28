#!/usr/bin/env python3

import os
import sys
import sqlite3
import hashlib
import time
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Database setup
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib', 'db')
DB_PATH = os.path.join(DB_DIR, 'music_streaming.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def setup_database():
    """Set up the database from scratch"""
    print("🎵 Setting up Music Streaming CLI Database...\n")
    
    # Ensure the database directory exists
    os.makedirs(DB_DIR, exist_ok=True)
    
    # Remove existing database if it exists
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("Removed existing database.")
        except PermissionError:
            print("❌ Could not remove existing database (file in use).")
            print("Please close any applications using the database and try again.")
            return False
    
    print("1. Initializing database...")
    
    # Create a new database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
    -- Users table
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(256) NOT NULL,
        is_admin BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Artists table
    CREATE TABLE artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        bio TEXT
    );
    
    -- Albums table
    CREATE TABLE albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        release_year INTEGER,
        artist_id INTEGER NOT NULL,
        FOREIGN KEY (artist_id) REFERENCES artists (id)
    );
    
    -- Genres table
    CREATE TABLE genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    
    -- Songs table
    CREATE TABLE songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        duration FLOAT,
        file_path VARCHAR(255),
        artist_id INTEGER NOT NULL,
        album_id INTEGER NOT NULL,
        genre_id INTEGER,
        FOREIGN KEY (artist_id) REFERENCES artists (id),
        FOREIGN KEY (album_id) REFERENCES albums (id),
        FOREIGN KEY (genre_id) REFERENCES genres (id)
    );
    
    -- Playlists table
    CREATE TABLE playlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    
    -- PlaylistSongs table
    CREATE TABLE playlist_songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        playlist_id INTEGER NOT NULL,
        song_id INTEGER NOT NULL,
        position INTEGER NOT NULL,
        FOREIGN KEY (playlist_id) REFERENCES playlists (id),
        FOREIGN KEY (song_id) REFERENCES songs (id)
    );
    ''')
    
    print("Database initialized successfully.")
    print(f"Database location: {DATABASE_URL}")
    
    print("\n2. Loading your music collection...")
    print("Clearing existing data...")
    
    # Create admin user
    admin_password = hash_password("admin123")
    cursor.execute('''
    INSERT INTO users (username, email, password_hash, is_admin)
    VALUES (?, ?, ?, ?)
    ''', ("admin", "admin@example.com", admin_password, 1))
    
    # Create regular user
    user_password = hash_password("password123")
    cursor.execute('''
    INSERT INTO users (username, email, password_hash, is_admin)
    VALUES (?, ?, ?, ?)
    ''', ("user", "user@example.com", user_password, 0))
    
    # Create test user with marine password
    marine_password = hash_password("MARINE")
    cursor.execute('''
    INSERT INTO users (username, email, password_hash, is_admin)
    VALUES (?, ?, ?, ?)
    ''', ("Winnie", "winnie@example.com", marine_password, 0))
    
    print("Creating users...")
    
    # Create genres
    print("Creating genres...")
    genres = ["Rumba", "Bongo Flava", "Reggae", "Kenyan Hip Hop", "Hip Hop"]
    for genre in genres:
        cursor.execute('INSERT INTO genres (name) VALUES (?)', (genre,))
    
    # Create artists
    print("Creating artists...")
    artists = [
        ("Wakadinali", "Kenyan hip hop group"),
        ("Kendrick Lamar", "American rapper and songwriter"),
        ("Satan Dave", "Fictional artist for testing"),
        ("BURUKLYN BOYZ", "Kenyan hip hop group"),
        ("Laho", "Fictional artist for testing"),
        ("Lucky Dube", "South African reggae musician"),
        ("Marioo", "Tanzanian bongo flava artist")
    ]
    for name, bio in artists:
        cursor.execute('INSERT INTO artists (name, bio) VALUES (?, ?)', (name, bio))
    
    # Create albums
    print("Creating albums...")
    albums = [
        ("National Splendour", 2021, 1),  # Wakadinali
        ("Satanic Sessions", 2022, 3),    # Satan Dave
        ("DAMN.", 2017, 2),               # Kendrick Lamar
        ("Street Anthems", 2020, 4),      # BURUKLYN BOYZ
        ("Joyful Hymns", 2019, 5),        # Laho
        ("Urban Tales", 2018, 1),         # Wakadinali
        ("Marketplace Vibes", 2015, 7),   # Marioo
        ("good kid, m.A.A.d city", 2012, 2),  # Kendrick Lamar
        ("City Lights", 2005, 6)          # Lucky Dube
    ]
    for title, year, artist_id in albums:
        cursor.execute('INSERT INTO albums (title, release_year, artist_id) VALUES (?, ?, ?)', 
                      (title, year, artist_id))
    
    # Create songs
    print("Creating songs...")
    songs = [
        ("Survivor's Guilt", 180, "/music/survivors_guilt.mp3", 3, 2, 5),  # Satan Dave, Satanic Sessions, Hip Hop
        ("Minister of Enjoyment", 210, "/music/minister_of_enjoyment.mp3", 5, 5, 1),  # Laho, Joyful Hymns, Rumba
        ("Piga Lean", 195, "/music/piga_lean.mp3", 4, 4, 4),  # BURUKLYN BOYZ, Street Anthems, Kenyan Hip Hop
        ("One-Love", 240, "/music/one_love.mp3", 6, 9, 3),  # Lucky Dube, City Lights, Reggae
        ("Soko", 185, "/music/soko.mp3", 1, 1, 4)  # Wakadinali, National Splendour, Kenyan Hip Hop
    ]
    for title, duration, file_path, artist_id, album_id, genre_id in songs:
        cursor.execute('''
        INSERT INTO songs (title, duration, file_path, artist_id, album_id, genre_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, duration, file_path, artist_id, album_id, genre_id))
    
    # Create sample playlists
    cursor.execute('''
    INSERT INTO playlists (name, description, user_id)
    VALUES (?, ?, ?)
    ''', ("My Favorites", "My favorite songs", 2))
    
    cursor.execute('''
    INSERT INTO playlists (name, description, user_id)
    VALUES (?, ?, ?)
    ''', ("Workout Mix", "Songs for working out", 2))
    
    # Add songs to playlists
    cursor.execute('''
    INSERT INTO playlist_songs (playlist_id, song_id, position)
    VALUES (?, ?, ?)
    ''', (1, 1, 1))
    
    cursor.execute('''
    INSERT INTO playlist_songs (playlist_id, song_id, position)
    VALUES (?, ?, ?)
    ''', (1, 3, 2))
    
    cursor.execute('''
    INSERT INTO playlist_songs (playlist_id, song_id, position)
    VALUES (?, ?, ?)
    ''', (2, 2, 1))
    
    cursor.execute('''
    INSERT INTO playlist_songs (playlist_id, song_id, position)
    VALUES (?, ?, ?)
    ''', (2, 4, 2))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("\nDatabase setup complete!")
    return True

if __name__ == "__main__":
    try:
        if setup_database():
            # Start the CLI application
            print("\n============================================================")
            print("                  🎵 MUSIC STREAMING CLI 🎵")
            print("           Your Personal Music Collection Manager")
            print("============================================================")
            
            # Import and run the CLI
            from lib.cli import main
            main()
        else:
            print("\n❌ Database setup failed. Please check the error messages above.")
    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        print("\nTrying to clean up and retry...")
        try:
            # Wait a moment in case of file locks
            time.sleep(1)
            if os.path.exists(DB_PATH):
                os.remove(DB_PATH)
            setup_database()
        except Exception as cleanup_error:
            print(f"❌ Setup failed even on retry: {str(cleanup_error)}")
            print("Please check your database configuration and try again.")