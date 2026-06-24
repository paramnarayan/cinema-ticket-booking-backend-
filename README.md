# Backend REST API for Cinema Booking System 
This project was aimed at understanding the working of various ticket booking platforms.
# What I Learned Building This Project
Transitioning this project from a simple Python script to a fully decoupled REST API taught me several core backend engineering principles:

* **Relational Database Design:** I learned how to structure data across multiple tables (`Users`, `Movies`, `Showtimes`, `Seats`) and connect them using Primary and Foreign keys to maintain data integrity.
* **Handling Concurrency (Race Conditions):** I solved the classic "double-booking" problem by enforcing `UNIQUE` constraints at the database level and using Python `try/except` blocks to gracefully catch `IntegrityErrors` and return clean HTTP 400 responses.
* **Advanced SQL Queries:** I wrote complex queries utilizing `JOIN` statements to aggregate data across multiple tables, and used sub-queries to dynamically filter out physical seats that already existed in the `bookings` table.
* **API Architecture & Data Validation:** I learned how to build a 3-tier architecture using **FastAPI**. I used **Pydantic** models to strictly validate incoming JSON payloads, ensuring the server only processes correctly formatted requests.


# Features

* **RESTful Architecture:** Clean separation of data, logic, and routing.
* **Concurrency Handling:** Utilizes SQL `UNIQUE` constraints and Python `try/except` blocks to handle race conditions and prevent double-booking of physical seats.
* **Dynamic Seat Filtering:** Sub-queries automatically cross-reference physical theater seats against active bookings to return only available seats.

# Project Structure

├── main.py               # The FastAPI application and core routing logic
├── setup_full_db.py      # Database initialization and seeding script
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignored files (database, cache)
└── README.md             # Project documentation



# Available Endpoints
**GET	/movies**	Returns a list of all available movies.
**GET	/showtimes**	Returns all scheduled showtimes.
**GET	/showtimes/{id}/seats**	Returns a list of available seats for a specific showtime.
**POST	/bookings**	Books a ticket (Requires JSON body: user_id, showtime_id, seat_id).
**GET	/users/{id}/bookings**	Returns all active tickets for a specific user.
**DELETE	/bookings/{id}**	Cancels a specific booking and frees up the seat.
