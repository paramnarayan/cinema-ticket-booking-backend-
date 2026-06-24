import sqlite3
import fastapi
from fastapi import Depends
from fastapi import HTTPException
import os
from pydantic import BaseModel  
from fastapi import status



app = fastapi.FastAPI(title="cinema REST API")



class BookingRequest(BaseModel):
    user_id: int
    showtime_id: int
    seat_id: int

def get_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'cinema.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()




@app.get("/movies")
def get_allmovies(db: sqlite3.Connection = Depends(get_connection)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    return {"movies": [dict(movie) for movie in movies]}



@app.get("/showtimes")
def get_showtimes(db: sqlite3.Connection = Depends(get_connection)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM showtimes")
    showtimes = cursor.fetchall()
    return {"showtimes": [dict(showtime) for showtime in showtimes]}



@app.post("/bookings",status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingRequest, db: sqlite3.Connection = Depends(get_connection)):
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO bookings (user_id, showtime_id, seat_id) VALUES (?, ?, ?)",
                   (booking.user_id, booking.showtime_id, booking.seat_id))
        db.commit()
        booking_id = cursor.lastrowid
        return {"message": "Booking created successfully", "booking_id": booking_id}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="seat is already taken ")
    



@app.get("/showtimes/{showtime_id}/seats")
def get_showtime_seats(showtime_id: int, db: sqlite3.Connection = Depends(get_connection)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM showtimes WHERE showtime_id = ?", (showtime_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    query="""SELECT * FROM seats 
        WHERE seat_id NOT IN (
            SELECT seat_id FROM bookings WHERE showtime_id = ?
        );
    """
    cursor.execute(query, (showtime_id,))
    available_seats = cursor.fetchall()
    return {"available_seats": [dict(seat) for seat in available_seats]}



@app.get("/users/{user_id/bookings}")
def get_user_bookings(user_id: int, db:sqlite3.Connection=Depends(get_connection)):
    cursor = db.cursor()
    query="""SELECT bookings.booking_id,movies.title,showtimes.start_time, bookings.seat_id FROM bookings
     JOIN showtimes on bookings.showtime_id=showtimes.showtime_id
     JOIN movies on showtimes.movie_id=movies.movie_id
     WHERE bookings.user_id = ?"""
    cursor.execute(query, (user_id,))
    user_bookings = cursor.fetchall()
    if not user_bookings:
        return {"message": "You have no active bookings."}
        
    return {"user_id": user_id, "tickets": [dict(ticket) for ticket in user_bookings]}


@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: sqlite3.Connection = Depends(get_connection)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM bookings WHERE booking_id = ?", (booking_id,))
    
    if not cursor.fetchone():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    
    
    cursor.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
    db.commit()
    return {"message":f"booking {booking_id} deleted successfully"}