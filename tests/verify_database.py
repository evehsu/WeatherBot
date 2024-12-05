# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent))  # Add parent directory to Python path

from database import get_db_connection, init_db
import argparse

def get_db_stats():
    """Get database statistics including column names, total records, and unique primary keys"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute('PRAGMA table_info(subscribers)')
        columns = [column[1] for column in cursor.fetchall()]
        
        # Get total number of records
        cursor.execute('SELECT COUNT(*) FROM subscribers')
        total_records = cursor.fetchone()[0]
        
        # Get count of distinct primary keys (user_email)
        cursor.execute('SELECT COUNT(DISTINCT user_email) FROM subscribers')
        unique_emails = cursor.fetchone()[0]
        
        return {
            'columns': columns,
            'total_records': total_records,
            'unique_primary_keys': unique_emails
        }

def get_records_by_user(user_email):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM subscribers WHERE user_email = ?', (user_email,))
        records = cursor.fetchall()
    
        return records
        

# Example usage:
if __name__ == '__main__':
    init_db()  # Ensure the database exists
    stats = get_db_stats()
    print(f"Column names: {stats['columns']}")
    print(f"Total records: {stats['total_records']}")
    print(f"Unique primary keys: {stats['unique_primary_keys']}")

    ## create an optional parameter for user email and run get_records_by_user
    parser = argparse.ArgumentParser(description='Database verification tool')
    parser.add_argument('--email', type=str, help='User email to look up specific records', required = False)
    args = parser.parse_args()

    if args.email:
        records = get_records_by_user(args.email)
        if records:
            print(f"\nRecords for {args.email}:")
            for record in records:
                print(record)
        else:
            print(f"\nNo records found for {args.email}")
