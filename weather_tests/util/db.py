import sqlite3
import random

DB_FILE = "data/data.db"

def start_db():
    db = sqlite3.connect("data/data.db")  # Open if file exists, otherwise create
    c = db.cursor()  # Facilitate db operations
    return db, c


def end_db(db):
    db.commit()  # Save changes to database
    db.close() # Close database

def get_db():
    """Prints all rows in locations"""
    db, c = start_db()
    c.execute("SELECT * FROM locations")
    print(c.fetchall())
    end_db(db)


def create_table():
    """Makes 'posts' table in data.db"""
    db, c = start_db()
    try:
        c.execute(
            '''CREATE TABLE locations (
                ip TEXT NOT NULL,
                location TEXT NOT NULL
            )'''
        )
    except sqlite3.OperationalError:  # if table already exists
        pass
    end_db(db)


def add_location(ip, location):
    """Adds a location 'locations'"""
    db, c = start_db()
    params = (random.SystemRandom().getrandbits(16), location)
    print('add_location: {ip}\t{location}'.format(
        ip=random.SystemRandom().getrandbits(16),
        location=location
    ))
    c.execute("INSERT INTO locations VALUES (?,?)", params)
    end_db(db)
