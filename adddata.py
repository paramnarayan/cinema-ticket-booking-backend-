import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'cinema.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Safely insert dummy showtimes and seats if they are missing
    cursor.executescript("""
        INSERT OR IGNORE INTO showtimes (showtime_id, movie_id, hall_number, start_time) VALUES 
        (1, 1, 1, '2023-11-01 18:00'),
        (2, 2, 2, '2023-11-01 20:30');

        INSERT OR IGNORE INTO seats (seat_id, hall_number, row_num, seat_num) VALUES 
        (1, 1, 1, 1), (2, 1, 1, 2), (3, 1, 1, 3), (4, 1, 2, 1), (5, 1, 2, 2);
    """)
    conn.commit()
    print("✅ Showtimes and Seats successfully added to the database!")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    conn.close()