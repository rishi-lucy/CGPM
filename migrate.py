"""
Database Migration Script
Adds official_image_path column to complaints table
"""

import sqlite3
import os

def migrate():
    db_path = os.path.join('instance', 'cgmp.db')
    
    if not os.path.exists(db_path):
        print("Database doesn't exist. It will be created automatically.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("PRAGMA table_info(complaint)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'official_image_path' not in columns:
        cursor.execute("ALTER TABLE complaint ADD COLUMN official_image_path VARCHAR(300)")
        conn.commit()
        print("Successfully added 'official_image_path' column to complaints table.")
    else:
        print("Column 'official_image_path' already exists.")
    
    conn.close()

if __name__ == '__main__':
    migrate()

