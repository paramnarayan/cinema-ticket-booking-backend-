import sqlite3
import os

def complete_db():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'cinema.db')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    
    create_users = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );'''

    create_movies = '''
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );'''

    create_showtime = """
        CREATE TABLE IF NOT EXISTS showtimes (
            showtime_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            hall_number INTEGER,
            start_time TEXT NOT NULL,
            FOREIGN KEY (movie_id) REFERENCES movies (movie_id) 
        );"""

    create_seats = """
        CREATE TABLE IF NOT EXISTS seats (
            seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hall_number INTEGER,
            row_num INTEGER,
            seat_num INTEGER
        );"""

    create_bookings = """
        CREATE TABLE IF NOT EXISTS bookings(
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            showtime_id INTEGER,
            seat_id INTEGER,
            booking_time INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (showtime_id) REFERENCES showtimes (showtime_id),
            FOREIGN KEY (seat_id) REFERENCES seats (seat_id),
            UNIQUE(showtime_id, seat_id)
        );"""

   
    c.execute(create_users)
    c.execute(create_movies)
    c.execute(create_showtime)
    c.execute(create_seats)
    c.execute(create_bookings)

    
    insert_data = '''
        INSERT OR IGNORE INTO users (user_id, name, username, password) 
        VALUES (1, 'Test User', 'testuser', 'password123');

        INSERT OR IGNORE INTO movies (title, genre, user_id)
        VALUES
          ('Inception', 'Sci-Fi', 1),
          ('The Matrix', 'Sci-Fi', 1),
          ('Interstellar', 'Sci-Fi', 1);
    '''
    c.executescript(insert_data)

    
    conn.commit()
    conn.close()
    
    print(f"Database created successfully at: {db_path}")


if __name__ == "__main__":
    complete_db()