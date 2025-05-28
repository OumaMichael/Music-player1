import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from lib.models.base import engine, Base
from lib.models.models import User, Artist, Album, Genre, Song, Playlist, PlaylistSong

def init_db():
    """Initialize the database by creating all tables"""
    try:
        # Create all tables
        Base.metadata.create_all(engine)
        print("Database initialized successfully.")
        print(f"Database location: {engine.url}")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    init_db()