import os
import sys
from lib.helpers import (
    register_user, login_user, get_user_by_id, search_songs, get_all_songs,
    get_all_artists, get_artist_songs, get_user_playlists, create_playlist,
    add_song_to_playlist, get_playlist_songs, get_all_genres, get_songs_by_genre
)

class MusicStreamingCLI:
    def __init__(self):
        self.current_user = None
        self.running = True

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print the application header"""
        print("=" * 60)
        print("                  🎵 MUSIC STREAMING CLI 🎵")
        print("           Your Personal Music Collection Manager")
        print("=" * 60)
        print()

    def print_menu(self, title, options):
        """Print a menu with options"""
        print(f"=== {title} ===")
        for key, value in options.items():
            print(f"{key}. {value}")

    def get_input(self, prompt):
        """Get user input with a prompt"""
        return input(f"🎵 {prompt}: ").strip()

    def pause(self):
        """Pause and wait for user input"""
        input("\n⏸️  Press Enter to continue...")

    def show_main_menu(self):
        """Show the main menu"""
        self.clear_screen()
        self.print_header()
        
        if self.current_user:
            options = {
                "1": "🎵 Browse Music",
                "2": "🔍 Search Songs",
                "3": "👥 Browse Artists",
                "4": "🎭 Browse Genres",
                "5": "📋 My Playlists",
                "6": "➕ Create Playlist",
                "7": "👤 Profile",
                "8": "🚪 Logout",
                "0": "🚪 Exit"
            }
        else:
            options = {
                "1": "👤 Register",
                "2": "🔐 Login",
                "3": "🎵 Browse Music (Guest Mode)",
                "0": "🚪 Exit"
            }
        
        self.print_menu("MAIN MENU", options)
        return self.get_input("Select option")

    def register(self):
        """Handle user registration"""
        self.clear_screen()
        self.print_menu("USER REGISTRATION", {})
        
        username = self.get_input("Enter username")
        email = self.get_input("Enter email")
        password = self.get_input("Enter password")
        
        success, result = register_user(username, email, password)
        
        if success:
            print(f"User {username} registered successfully!")
            # Auto-login after registration
            login_success, user_data = login_user(username, password)
            if login_success:
                self.current_user = user_data
                print(f"Welcome, {user_data['username']}!")
            else:
                print("Registration successful, but auto-login failed. Please login manually.")
        else:
            print(f"❌ Registration failed: {result}")
        
        self.pause()

    def login(self):
        """Handle user login"""
        self.clear_screen()
        self.print_menu("USER LOGIN", {})
        
        username = self.get_input("Enter username")
        password = self.get_input("Enter password")
        
        success, result = login_user(username, password)
        
        if success:
            self.current_user = result
            print(f"✅ Welcome back, {result['username']}!")
        else:
            print(f"❌ Login failed: {result}")
        
        self.pause()

    def logout(self):
        """Handle user logout"""
        if self.current_user:
            username = self.current_user['username']
            self.current_user = None
            print(f"👋 Goodbye, {username}!")
        self.pause()

    def show_profile(self):
        """Show user profile"""
        if not self.current_user:
            print("❌ Please login first")
            self.pause()
            return
        
        self.clear_screen()
        print("=== USER PROFILE ===")
        print(f"👤 Username: {self.current_user['username']}")
        print(f"📧 Email: {self.current_user['email']}")
        print(f"🔑 Admin: {'Yes' if self.current_user['is_admin'] else 'No'}")
        print(f"🆔 User ID: {self.current_user['id']}")
        self.pause()

    def browse_music(self):
        """Browse all music"""
        self.clear_screen()
        print("=== 🎵 MUSIC LIBRARY ===")
        
        songs = get_all_songs()
        
        if not songs:
            print("No songs found in the library.")
            self.pause()
            return
        
        print(f"Found {len(songs)} songs:\n")
        
        for i, song in enumerate(songs, 1):
            duration_str = f"{song['duration']}s" if song['duration'] else "Unknown"
            print(f"{i:2d}. 🎵 {song['title']}")
            print(f"    👤 Artist: {song['artist']}")
            print(f"    💿 Album: {song['album']}")
            print(f"    🎭 Genre: {song['genre']}")
            print(f"    ⏱️  Duration: {duration_str}")
            print()
        
        if self.current_user:
            choice = self.get_input("Enter song number to add to playlist (or press Enter to continue)")
            if choice.isdigit():
                song_index = int(choice) - 1
                if 0 <= song_index < len(songs):
                    self.add_to_playlist_menu(songs[song_index]['id'])
        
        self.pause()

    def search_music(self):
        """Search for music"""
        if not self.current_user:
            print("❌ Please login to search music")
            self.pause()
            return
        
        self.clear_screen()
        print("=== 🔍 SEARCH MUSIC ===")
        
        query = self.get_input("Enter search term (song, artist, or album)")
        
        if not query:
            print("❌ Please enter a search term")
            self.pause()
            return
        
        songs = search_songs(query)
        
        if not songs:
            print(f"No songs found matching '{query}'")
            self.pause()
            return
        
        print(f"\nFound {len(songs)} songs matching '{query}':\n")
        
        for i, song in enumerate(songs, 1):
            duration_str = f"{song['duration']}s" if song['duration'] else "Unknown"
            print(f"{i:2d}. 🎵 {song['title']}")
            print(f"    👤 Artist: {song['artist']}")
            print(f"    💿 Album: {song['album']}")
            print(f"    🎭 Genre: {song['genre']}")
            print(f"    ⏱️  Duration: {duration_str}")
            print()
        
        choice = self.get_input("Enter song number to add to playlist (or press Enter to continue)")
        if choice.isdigit():
            song_index = int(choice) - 1
            if 0 <= song_index < len(songs):
                self.add_to_playlist_menu(songs[song_index]['id'])
        
        self.pause()

    def browse_artists(self):
        """Browse all artists"""
        self.clear_screen()
        print("=== 👥 ARTISTS ===")
        
        artists = get_all_artists()
        
        if not artists:
            print("No artists found.")
            self.pause()
            return
        
        print(f"Found {len(artists)} artists:\n")
        
        for i, artist in enumerate(artists, 1):
            print(f"{i:2d}. 👤 {artist['name']}")
            if artist['bio']:
                print(f"    📝 {artist['bio']}")
            print()
        
        choice = self.get_input("Enter artist number to view songs (or press Enter to continue)")
        if choice.isdigit():
            artist_index = int(choice) - 1
            if 0 <= artist_index < len(artists):
                self.show_artist_songs(artists[artist_index]['id'], artists[artist_index]['name'])
        
        self.pause()

    def show_artist_songs(self, artist_id, artist_name):
        """Show songs by a specific artist"""
        self.clear_screen()
        print(f"=== 🎵 SONGS BY {artist_name.upper()} ===")
        
        songs = get_artist_songs(artist_id)
        
        if not songs:
            print(f"No songs found for {artist_name}")
            return
        
        print(f"Found {len(songs)} songs:\n")
        
        for i, song in enumerate(songs, 1):
            duration_str = f"{song['duration']}s" if song['duration'] else "Unknown"
            print(f"{i:2d}. 🎵 {song['title']}")
            print(f"    💿 Album: {song['album']}")
            print(f"    🎭 Genre: {song['genre']}")
            print(f"    ⏱️  Duration: {duration_str}")
            print()

    def browse_genres(self):
        """Browse all genres"""
        self.clear_screen()
        print("=== 🎭 GENRES ===")
        
        genres = get_all_genres()
        
        if not genres:
            print("No genres found.")
            self.pause()
            return
        
        print(f"Found {len(genres)} genres:\n")
        
        for i, genre in enumerate(genres, 1):
            print(f"{i:2d}. 🎭 {genre['name']}")
        
        choice = self.get_input("Enter genre number to view songs (or press Enter to continue)")
        if choice.isdigit():
            genre_index = int(choice) - 1
            if 0 <= genre_index < len(genres):
                self.show_genre_songs(genres[genre_index]['id'], genres[genre_index]['name'])
        
        self.pause()

    def show_genre_songs(self, genre_id, genre_name):
        """Show songs in a specific genre"""
        self.clear_screen()
        print(f"=== 🎵 {genre_name.upper()} SONGS ===")
        
        songs = get_songs_by_genre(genre_id)
        
        if not songs:
            print(f"No songs found in {genre_name} genre")
            self.pause()
            return
        
        print(f"Found {len(songs)} songs:\n")
        
        for i, song in enumerate(songs, 1):
            duration_str = f"{song['duration']}s" if song['duration'] else "Unknown"
            print(f"{i:2d}. 🎵 {song['title']}")
            print(f"    👤 Artist: {song['artist']}")
            print(f"    💿 Album: {song['album']}")
            print(f"    ⏱️  Duration: {duration_str}")
            print()
        
        self.pause()

    def show_playlists(self):
        """Show user playlists"""
        if not self.current_user:
            print("❌ Please login to view playlists")
            self.pause()
            return
        
        self.clear_screen()
        print("=== 📋 MY PLAYLISTS ===")
        
        playlists = get_user_playlists(self.current_user['id'])
        
        if not playlists:
            print("You don't have any playlists yet.")
            print("Create your first playlist from the main menu!")
            self.pause()
            return
        
        print(f"You have {len(playlists)} playlists:\n")
        
        for i, playlist in enumerate(playlists, 1):
            print(f"{i:2d}. 📋 {playlist['name']}")
            if playlist['description']:
                print(f"    📝 {playlist['description']}")
            print(f"    📅 Created: {playlist['created_at']}")
            print()
        
        choice = self.get_input("Enter playlist number to view songs (or press Enter to continue)")
        if choice.isdigit():
            playlist_index = int(choice) - 1
            if 0 <= playlist_index < len(playlists):
                self.show_playlist_songs(playlists[playlist_index]['id'], playlists[playlist_index]['name'])
        
        self.pause()

    def show_playlist_songs(self, playlist_id, playlist_name):
        """Show songs in a playlist"""
        self.clear_screen()
        print(f"=== 📋 {playlist_name.upper()} ===")
        
        songs = get_playlist_songs(playlist_id)
        
        if not songs:
            print("This playlist is empty.")
            return
        
        print(f"Playlist contains {len(songs)} songs:\n")
        
        for song in songs:
            duration_str = f"{song['duration']}s" if song['duration'] else "Unknown"
            print(f"{song['position']:2d}. 🎵 {song['title']}")
            print(f"    👤 Artist: {song['artist']}")
            print(f"    💿 Album: {song['album']}")
            print(f"    🎭 Genre: {song['genre']}")
            print(f"    ⏱️  Duration: {duration_str}")
            print()

    def create_new_playlist(self):
        """Create a new playlist"""
        if not self.current_user:
            print("❌ Please login to create playlists")
            self.pause()
            return
        
        self.clear_screen()
        print("=== ➕ CREATE PLAYLIST ===")
        
        name = self.get_input("Enter playlist name")
        if not name:
            print("❌ Playlist name cannot be empty")
            self.pause()
            return
        
        description = self.get_input("Enter playlist description (optional)")
        
        success, result = create_playlist(self.current_user['id'], name, description)
        
        if success:
            print(f"✅ Playlist '{name}' created successfully!")
        else:
            print(f"❌ Failed to create playlist: {result}")
        
        self.pause()

    def add_to_playlist_menu(self, song_id):
        """Show menu to add song to playlist"""
        playlists = get_user_playlists(self.current_user['id'])
        
        if not playlists:
            print("\n❌ You don't have any playlists yet.")
            create = self.get_input("Would you like to create a playlist first? (y/n)")
            if create.lower() == 'y':
                self.create_new_playlist()
            return
        
        print("\n=== ADD TO PLAYLIST ===")
        print("Your playlists:")
        
        for i, playlist in enumerate(playlists, 1):
            print(f"{i}. {playlist['name']}")
        
        choice = self.get_input("Enter playlist number")
        if choice.isdigit():
            playlist_index = int(choice) - 1
            if 0 <= playlist_index < len(playlists):
                playlist_id = playlists[playlist_index]['id']
                success, message = add_song_to_playlist(playlist_id, song_id)
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"❌ {message}")

    def run(self):
        """Main application loop"""
        while self.running:
            try:
                choice = self.show_main_menu()
                
                if choice == "0":
                    self.running = False
                    print("👋 Thank you for using Music Streaming CLI!")
                    break
                
                if not self.current_user:
                    # Guest/Not logged in menu
                    if choice == "1":
                        self.register()
                    elif choice == "2":
                        self.login()
                    elif choice == "3":
                        self.browse_music()
                    else:
                        print("❌ Invalid option")
                        self.pause()
                else:
                    # Logged in menu
                    if choice == "1":
                        self.browse_music()
                    elif choice == "2":
                        self.search_music()
                    elif choice == "3":
                        self.browse_artists()
                    elif choice == "4":
                        self.browse_genres()
                    elif choice == "5":
                        self.show_playlists()
                    elif choice == "6":
                        self.create_new_playlist()
                    elif choice == "7":
                        self.show_profile()
                    elif choice == "8":
                        self.logout()
                    else:
                        print("❌ Invalid option")
                        self.pause()
                        
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {str(e)}")
                self.pause()

def main():
    """Entry point for the CLI application"""
    app = MusicStreamingCLI()
    app.run()

if __name__ == "__main__":
    main()