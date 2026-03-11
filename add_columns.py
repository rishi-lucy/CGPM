"""
Script to add new columns to the existing database
Run this once to update the database schema
"""
import sqlite3
import os

# Path to the database
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'cgmp.db')

def add_columns():
    """Add missing columns to the complaint table"""
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check and add each column if it doesn't exist
    columns_to_add = [
        ('division', 'VARCHAR(100)'),
        ('subdivision', 'VARCHAR(200)'),
        ('other_division', 'VARCHAR(200)'),
        ('other_subdivision', 'VARCHAR(200)'),
        ('admin_image_path', 'VARCHAR(300)'),
        ('official_image_path', 'VARCHAR(300)')
    ]
    
    for column_name, column_type in columns_to_add:
        try:
            # Check if column exists
            cursor.execute(f"PRAGMA table_info(complaint)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if column_name not in columns:
                cursor.execute(f"ALTER TABLE complaint ADD COLUMN {column_name} {column_type}")
                print(f"✓ Added column: {column_name}")
            else:
                print(f"- Column already exists: {column_name}")
        except Exception as e:
            print(f"Error adding column {column_name}: {e}")
    
    conn.commit()
    conn.close()
    print("\n✅ Database updated successfully!")

if __name__ == '__main__':
    add_columns()

