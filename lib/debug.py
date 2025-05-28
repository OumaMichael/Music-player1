#!/usr/bin/env python3

import os
import sys
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

# Determine the correct path setup based on where the script is run from
script_dir = os.path.dirname(os.path.abspath(__file__))
script_name = os.path.basename(__file__)

# If we're in the lib directory, add parent to path
if os.path.basename(script_dir) == 'lib':
    # Running from lib directory
    project_root = os.path.dirname(script_dir)
    sys.path.insert(0, project_root)
    lib_dir = script_dir
else:
    # Running from project root
    project_root = script_dir
    sys.path.insert(0, project_root)
    lib_dir = os.path.join(project_root, 'lib')

print(f"Script location: {script_dir}")
print(f"Project root: {project_root}")
print(f"Lib directory: {lib_dir}")

def find_database():
    """Find the database file in various possible locations"""
    
    # Possible database locations
    possible_paths = [
        # From project root
        os.path.join(project_root, 'lib', 'db', 'music_streaming.db'),
        # From lib directory
        os.path.join(lib_dir, 'db', 'music_streaming.db'),
        # Alternative paths
        os.path.join(script_dir, 'db', 'music_streaming.db'),
        os.path.join(script_dir, 'music_streaming.db'),
    ]
    
    print("Searching for database in the following locations:")
    
    for path in possible_paths:
        print(f"  Checking: {path}")
        if os.path.exists(path):
            print(f"   Found database at: {path}")
            return path
        else:
            print(f"   Not found")
    
    return None

# Find the database
DB_PATH = find_database()
if DB_PATH:
    DB_DIR = os.path.dirname(DB_PATH)
    DATABASE_URL = f"sqlite:///{DB_PATH}"
else:
    # Default fallback
    DB_DIR = os.path.join(lib_dir, 'db')
    DB_PATH = os.path.join(DB_DIR, 'music_streaming.db')
    DATABASE_URL = f"sqlite:///{DB_PATH}"

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n--- {title} ---")

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_paths_and_find_database():
    """Check all possible paths and find the database"""
    print_header("PATH ANALYSIS AND DATABASE SEARCH")
    
    print(f"Script location: {__file__}")
    print(f"Script directory: {script_dir}")
    print(f"Project root: {project_root}")
    print(f"Lib directory: {lib_dir}")
    print(f"Python path: {sys.path[:3]}...")  # Show first 3 entries
    
    print("\nDirectory structure:")
    
    # Show project root contents
    print(f"\nContents of project root ({project_root}):")
    try:
        for item in os.listdir(project_root):
            item_path = os.path.join(project_root, item)
            if os.path.isdir(item_path):
                print(f"   {item}/")
            else:
                print(f"   {item}")
    except Exception as e:
        print(f"   Cannot list directory: {e}")
    
    # Show lib directory contents
    print(f"\nContents of lib directory ({lib_dir}):")
    try:
        for item in os.listdir(lib_dir):
            item_path = os.path.join(lib_dir, item)
            if os.path.isdir(item_path):
                print(f"   {item}/")
                # If it's db directory, show its contents
                if item == 'db':
                    db_path = os.path.join(lib_dir, 'db')
                    print(f"    Contents of db/:")
                    try:
                        for db_item in os.listdir(db_path):
                            print(f"       {db_item}")
                    except Exception as e:
                        print(f"       Cannot list db directory: {e}")
            else:
                print(f"   {item}")
    except Exception as e:
        print(f"   Cannot list lib directory: {e}")
    
    # Search for database files
    print("\nSearching for database files...")
    
    def search_for_db(directory, max_depth=3, current_depth=0):
        """Recursively search for database files"""
        if current_depth > max_depth:
            return []
        
        found_dbs = []
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path) and item.endswith('.db'):
                    found_dbs.append(item_path)
                elif os.path.isdir(item_path):
                    found_dbs.extend(search_for_db(item_path, max_depth, current_depth + 1))
        except PermissionError:
            pass
        except Exception:
            pass
        
        return found_dbs
    
    # Search from project root
    db_files = search_for_db(project_root)
    
    if db_files:
        print("Found database files:")
        for db_file in db_files:
            print(f"   {db_file}")
            # Check if it's our music streaming database
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
                if cursor.fetchone():
                    print(f"    🎵 This appears to be a music streaming database!")
                    global DB_PATH, DATABASE_URL
                    DB_PATH = db_file
                    DATABASE_URL = f"sqlite:///{DB_PATH}"
                conn.close()
            except Exception:
                pass
    else:
        print(" No database files found")
    
    print(f"\nUsing database path: {DB_PATH}")
    print(f"Database exists: {os.path.exists(DB_PATH) if DB_PATH else False}")
    
    return DB_PATH is not None and os.path.exists(DB_PATH)

def check_database_exists():
    """Check if the database file exists"""
    print_header("DATABASE FILE CHECK")
    
    if not DB_PATH:
        print(" Database path not determined")
        return False
    
    print(f"Database directory: {DB_DIR}")
    print(f"Database path: {DB_PATH}")
    print(f"Database exists: {os.path.exists(DB_PATH)}")
    
    if os.path.exists(DB_PATH):
        file_size = os.path.getsize(DB_PATH)
        print(f"Database size: {file_size} bytes")
        
        # Check file permissions
        print(f"Readable: {os.access(DB_PATH, os.R_OK)}")
        print(f"Writable: {os.access(DB_PATH, os.W_OK)}")
        
        # Get file modification time
        mod_time = os.path.getmtime(DB_PATH)
        mod_datetime = datetime.fromtimestamp(mod_time)
        print(f"Last modified: {mod_datetime}")
    else:
        print(" Database file does not exist!")
        print("Please run 'python setup.py' first to create the database.")
        return False
    
    return True

def check_database_connection():
    """Test database connection"""
    print_header("DATABASE CONNECTION TEST")
    
    if not os.path.exists(DB_PATH):
        print(f" Database file not found: {DB_PATH}")
        print("Please run 'python setup.py' first to create the database.")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]
        print(f" SQLite version: {version}")
        
        # Check if we can create a temporary table
        cursor.execute("CREATE TEMPORARY TABLE test_table (id INTEGER)")
        cursor.execute("DROP TABLE test_table")
        print(" Database is writable")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f" Database connection failed: {str(e)}")
        return False

def check_table_structure():
    """Check database table structure"""
    print_header("DATABASE SCHEMA CHECK")
    
    if not os.path.exists(DB_PATH):
        print(f" Database file not found: {DB_PATH}")
        print("Please run 'python setup.py' first to create the database.")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check each table structure
        expected_tables = ['users', 'artists', 'albums', 'genres', 'songs', 'playlists', 'playlist_songs']
        
        for table_name in expected_tables:
            print_section(f"Table: {table_name}")
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if not cursor.fetchone():
                print(f" Table '{table_name}' does not exist!")
                continue
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("Columns:")
            for col in columns:
                col_id, name, data_type, not_null, default_val, pk = col
                pk_str = " (PRIMARY KEY)" if pk else ""
                not_null_str = " NOT NULL" if not_null else ""
                default_str = f" DEFAULT {default_val}" if default_val else ""
                print(f"  {name}: {data_type}{not_null_str}{default_str}{pk_str}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Row count: {count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f" Schema check failed: {str(e)}")
        return False

def check_data_integrity():
    """Check data integrity and relationships"""
    print_header("DATA INTEGRITY CHECK")
    
    if not os.path.exists(DB_PATH):
        print(f" Database file not found: {DB_PATH}")
        print("Please run 'python setup.py' first to create the database.")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check users table
        print_section("Users")
        cursor.execute("SELECT id, username, email, is_admin FROM users")
        users = cursor.fetchall()
        
        for user in users:
            user_id, username, email, is_admin = user
            admin_str = " (ADMIN)" if is_admin else ""
            print(f"  ID: {user_id}, Username: {username}, Email: {email}{admin_str}")
        
        # Check artists and their songs
        print_section("Artists and Songs")
        cursor.execute("""
        SELECT a.id, a.name, COUNT(s.id) as song_count
        FROM artists a
        LEFT JOIN songs s ON a.id = s.artist_id
        GROUP BY a.id, a.name
        ORDER BY a.name
        """)
        artists = cursor.fetchall()
        
        for artist in artists:
            artist_id, name, song_count = artist
            print(f"  {name}: {song_count} songs")
        
        # Check albums and their songs
        print_section("Albums and Songs")
        cursor.execute("""
        SELECT al.title, ar.name, COUNT(s.id) as song_count
        FROM albums al
        JOIN artists ar ON al.artist_id = ar.id
        LEFT JOIN songs s ON al.id = s.album_id
        GROUP BY al.id, al.title, ar.name
        ORDER BY ar.name, al.title
        """)
        albums = cursor.fetchall()
        
        for album in albums:
            album_title, artist_name, song_count = album
            print(f"  {artist_name} - {album_title}: {song_count} songs")
        
        # Check genres and their songs
        print_section("Genres and Songs")
        cursor.execute("""
        SELECT g.name, COUNT(s.id) as song_count
        FROM genres g
        LEFT JOIN songs s ON g.id = s.genre_id
        GROUP BY g.id, g.name
        ORDER BY g.name
        """)
        genres = cursor.fetchall()
        
        for genre in genres:
            genre_name, song_count = genre
            print(f"  {genre_name}: {song_count} songs")
        
        # Check playlists
        print_section("Playlists")
        cursor.execute("""
        SELECT p.name, u.username, COUNT(ps.song_id) as song_count
        FROM playlists p
        JOIN users u ON p.user_id = u.id
        LEFT JOIN playlist_songs ps ON p.id = ps.playlist_id
        GROUP BY p.id, p.name, u.username
        ORDER BY u.username, p.name
        """)
        playlists = cursor.fetchall()
        
        for playlist in playlists:
            playlist_name, username, song_count = playlist
            print(f"  {username}'s '{playlist_name}': {song_count} songs")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f" Data integrity check failed: {str(e)}")
        return False

def test_authentication():
    """Test user authentication"""
    print_header("AUTHENTICATION TEST")
    
    if not os.path.exists(DB_PATH):
        print(f" Database file not found: {DB_PATH}")
        print("Please run 'python setup.py' first to create the database.")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Test users
        test_users = [
            ("admin", "admin123"),
            ("user", "password123"),
            ("Winnie", "MARINE")
        ]
        
        for username, password in test_users:
            print_section(f"Testing user: {username}")
            
            # Hash the password
            hashed_password = hash_password(password)
            print(f"Password hash: {hashed_password}")
            
            # Check if user exists and password matches
            cursor.execute("""
            SELECT id, username, email, is_admin, password_hash
            FROM users 
            WHERE username = ?
            """, (username,))
            
            user = cursor.fetchone()
            if user:
                user_id, db_username, email, is_admin, db_password_hash = user
                print(f" User found: ID={user_id}, Email={email}, Admin={is_admin}")
                
                if db_password_hash == hashed_password:
                    print(" Password matches")
                else:
                    print(" Password does not match")
                    print(f"Expected: {hashed_password}")
                    print(f"Got:      {db_password_hash}")
            else:
                print(f" User '{username}' not found")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f" Authentication test failed: {str(e)}")
        return False

def test_sqlalchemy_import():
    """Test SQLAlchemy imports and models"""
    print_header("SQLALCHEMY IMPORT TEST")
    
    try:
        # Test basic imports
        print("Testing imports...")
        print(f"Python path: {sys.path[:2]}")
        
        # Try different import strategies
        try:
            from lib.models.base import Base
            print(" Base imported successfully (lib.models.base)")
        except ImportError:
            try:
                from models.base import Base
                print(" Base imported successfully (models.base)")
            except ImportError:
                # Try adding lib to path if not already there
                if lib_dir not in sys.path:
                    sys.path.insert(0, lib_dir)
                from models.base import Base
                print(" Base imported successfully (models.base with lib path)")
        
        try:
            from lib.models.models import User, Artist, Album, Genre, Song, Playlist, PlaylistSong
            print(" Models imported successfully (lib.models.models)")
        except ImportError:
            try:
                from models.models import User, Artist, Album, Genre, Song, Playlist, PlaylistSong
                print(" Models imported successfully (models.models)")
            except ImportError:
                if lib_dir not in sys.path:
                    sys.path.insert(0, lib_dir)
                from models.models import User, Artist, Album, Genre, Song, Playlist, PlaylistSong
                print(" Models imported successfully (models.models with lib path)")
        
        try:
            from lib.helpers import get_db_session, register_user, login_user
            print(" Helper functions imported successfully (lib.helpers)")
        except ImportError:
            try:
                from helpers import get_db_session, register_user, login_user
                print(" Helper functions imported successfully (helpers)")
            except ImportError:
                if lib_dir not in sys.path:
                    sys.path.insert(0, lib_dir)
                from helpers import get_db_session, register_user, login_user
                print(" Helper functions imported successfully (helpers with lib path)")
        
        # Test database session creation
        print("\nTesting database session...")
        session = get_db_session()
        print(" Database session created")
        
        # Test a simple query
        users = session.query(User).all()
        print(f" Found {len(users)} users via SQLAlchemy")
        
        session.close()
        print(" Session closed successfully")
        
        return True
        
    except Exception as e:
        print(f" SQLAlchemy test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_helper_functions():
    """Test helper functions"""
    print_header("HELPER FUNCTIONS TEST")
    
    try:
        # Try different import strategies
        try:
            from lib.helpers import (
                register_user, login_user, get_all_songs, get_all_artists,
                search_songs, get_user_playlists, create_playlist
            )
            print(" Imported from lib.helpers")
        except ImportError:
            try:
                from helpers import (
                    register_user, login_user, get_all_songs, get_all_artists,
                    search_songs, get_user_playlists, create_playlist
                )
                print(" Imported from helpers")
            except ImportError:
                if lib_dir not in sys.path:
                    sys.path.insert(0, lib_dir)
                from helpers import (
                    register_user, login_user, get_all_songs, get_all_artists,
                    search_songs, get_user_playlists, create_playlist
                )
                print(" Imported from helpers with lib path")
        
        # Test login
        print_section("Testing login function")
        success, result = login_user("Winnie", "MARINE")
        if success:
            print(" Login successful")
            print(f"User data: {result}")
        else:
            print(f" Login failed: {result}")
        
        # Test get all songs
        print_section("Testing get_all_songs")
        songs = get_all_songs()
        print(f" Found {len(songs)} songs")
        if songs:
            print("Sample song:")
            print(f"  {songs[0]}")
        
        # Test get all artists
        print_section("Testing get_all_artists")
        artists = get_all_artists()
        print(f" Found {len(artists)} artists")
        if artists:
            print("Sample artist:")
            print(f"  {artists[0]}")
        
        # Test search
        print_section("Testing search_songs")
        search_results = search_songs("Satan")
        print(f" Search for 'Satan' returned {len(search_results)} results")
        
        return True
        
    except Exception as e:
        print(f" Helper functions test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def show_detailed_song_info():
    """Show detailed information about all songs"""
    print_header("DETAILED SONG INFORMATION")
    
    if not os.path.exists(DB_PATH):
        print(f" Database file not found: {DB_PATH}")
        print("Please run 'python setup.py' first to create the database.")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT 
            s.id,
            s.title,
            ar.name as artist_name,
            al.title as album_title,
            g.name as genre_name,
            s.duration,
            s.file_path
        FROM songs s
        JOIN artists ar ON s.artist_id = ar.id
        JOIN albums al ON s.album_id = al.id
        LEFT JOIN genres g ON s.genre_id = g.id
        ORDER BY ar.name, al.title, s.title
        """)
        
        songs = cursor.fetchall()
        
        for song in songs:
            song_id, title, artist, album, genre, duration, file_path = song
            duration_str = f"{duration}s" if duration else "Unknown"
            genre_str = genre if genre else "No genre"
            
            print(f"\nSong ID: {song_id}")
            print(f"Title: {title}")
            print(f"Artist: {artist}")
            print(f"Album: {album}")
            print(f"Genre: {genre_str}")
            print(f"Duration: {duration_str}")
            print(f"File Path: {file_path}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f" Detailed song info failed: {str(e)}")
        return False

def execute_custom_query():
    """Execute a custom SQL query"""
    print_header("CUSTOM SQL QUERY")
    
    if not os.path.exists(DB_PATH):
        print(f" Database file not found: {DB_PATH}")
        print("Please run 'python setup.py' first to create the database.")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("Enter your SQL query (or 'exit' to return):")
        query = input("SQL> ").strip()
        
        if query.lower() == 'exit':
            return
        
        cursor.execute(query)
        
        if query.lower().startswith('select'):
            results = cursor.fetchall()
            print(f"\nResults ({len(results)} rows):")
            for row in results:
                print(row)
        else:
            conn.commit()
            print(" Query executed successfully")
        
        conn.close()
        
    except Exception as e:
        print(f" Query failed: {str(e)}")

def run_all_tests():
    """Run all debug tests"""
    print_header("MUSIC STREAMING CLI - DEBUG REPORT")
    print(f"Generated at: {datetime.now()}")
    
    tests = [
        ("Path Analysis", check_paths_and_find_database),
        ("Database File Check", check_database_exists),
        ("Database Connection", check_database_connection),
        ("Table Structure", check_table_structure),
        ("Data Integrity", check_data_integrity),
        ("Authentication", test_authentication),
        ("SQLAlchemy Import", test_sqlalchemy_import),
        ("Helper Functions", test_helper_functions),
        ("Song Information", show_detailed_song_info)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n {test_name} crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = " PASS" if result else " FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print(" All tests passed! Your database is working correctly.")
    else:
        print("  Some tests failed. Check the details above.")

def interactive_debug():
    """Interactive debug menu"""
    while True:
        print_header("INTERACTIVE DEBUG MENU")
        print("1. Run all tests")
        print("2. Check database file")
        print("3. Check table structure")
        print("4. Test authentication")
        print("5. Test helper functions")
        print("6. Show song details")
        print("7. Execute custom SQL query")
        print("8. Check paths and find database")
        print("0. Exit")
        
        choice = input("\n🔧 Select option: ").strip()
        
        if choice == "0":
            print(" Goodbye!")
            break
        elif choice == "1":
            run_all_tests()
        elif choice == "2":
            check_database_exists()
        elif choice == "3":
            check_table_structure()
        elif choice == "4":
            test_authentication()
        elif choice == "5":
            test_helper_functions()
        elif choice == "6":
            show_detailed_song_info()
        elif choice == "7":
            execute_custom_query()
        elif choice == "8":
            check_paths_and_find_database()
        else:
            print(" Invalid option")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # Run all tests automatically
        run_all_tests()
    else:
        # Interactive mode
        interactive_debug()