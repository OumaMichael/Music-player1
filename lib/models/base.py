import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Get the directory where this file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up two levels to get to the project root, then into lib/db
db_path = os.path.join(current_dir, '..', 'db', 'music_streaming.db')
db_path = os.path.abspath(db_path)

# Ensure the db directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Create database engine
engine = create_engine(f'sqlite:///{db_path}')

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Create base class for models
Base = declarative_base()

def get_session():
    return Session()