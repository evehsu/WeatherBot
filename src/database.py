import sqlite3
from typing import List
from contextlib import contextmanager
import json
from subscribe_objects import Subscriber
import os

@contextmanager
def get_db_connection():
    database_name = os.getenv('DATABASE_NAME', 'weather_subscribers.db')
    conn = sqlite3.connect(database_name)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize the database with the subscribers table"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            user_email TEXT PRIMARY KEY,
            user_destination TEXT,  -- JSON string array
            sunny_threshold TEXT,   -- JSON integer array
            time_window TEXT,       -- JSON integer array
            num_allowed_destination INTEGER DEFAULT 3
        )
        ''')
        conn.commit()

def save_subscriber(subscriber: Subscriber):
    """Save or update a subscriber in the database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO subscribers 
        (user_email, user_destination, sunny_threshold, time_window, num_allowed_destination)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            subscriber.user_email,
            json.dumps(subscriber.user_destination),
            json.dumps(subscriber.sunny_threshold),
            json.dumps(subscriber.time_window),
            subscriber.num_allowed_destination
        ))
        conn.commit()

def get_all_subscribers(verbose = False) -> List[Subscriber]:
    """Retrieve all subscribers from the database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM subscribers')
        rows = cursor.fetchall()
        
        subscribers = []
        for row in rows:
            subscriber = Subscriber(
                user_email=row[0],
                user_destination=json.loads(row[1]),
                sunny_threshold=json.loads(row[2]),
                time_window=json.loads(row[3]),
                num_allowed_destination=row[4]
            )
            subscribers.append(subscriber)
        if verbose:
            print(subscribers)
        return subscribers

def get_subscriber_by_email(email: str) -> Subscriber | None:
    """Retrieve a specific subscriber by email"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM subscribers WHERE user_email = ?', (email,))
        row = cursor.fetchone()
        
        if row:
            return Subscriber(
                user_email=row[0],
                user_destination=json.loads(row[1]),
                sunny_threshold=json.loads(row[2]),
                time_window=json.loads(row[3]),
                num_allowed_destination=row[4]
            )
        return None 
