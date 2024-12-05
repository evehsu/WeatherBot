import pytest
import os
import sqlite3

@pytest.fixture
def test_db(tmp_path):
    """Create a temporary test database"""
    test_db_path = str(tmp_path / "test_weather_subscribers.db")
    
    # Set the environment variable for the test database
    os.environ['DATABASE_NAME'] = test_db_path
    
    # Create fresh test database
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscribers (
        user_email TEXT PRIMARY KEY,
        user_destination TEXT,
        sunny_threshold TEXT,
        time_window TEXT,
        num_allowed_destination INTEGER DEFAULT 3
    )
    ''')
    conn.commit()
    conn.close()
    
    yield test_db_path
    
    # Cleanup
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Reset environment variable
    if 'DATABASE_NAME' in os.environ:
        del os.environ['DATABASE_NAME']
