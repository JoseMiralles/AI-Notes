import csv
import sqlite3
import os

def load_template_fields() -> str:
    """
    Reads ./data/template_fields.csv and returns the contents as a string.
    """
    try:
        with open('./data/template_fields.csv', mode='r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "Error: ./data/template_fields.csv not found."



def load_chinook_schema(db_path: str) -> str:
    """
    Connects to the SQLite database and extracts the full DDL (Data Definition Language).
    Returns a single string containing all CREATE TABLE statements.
    """
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query the master table to get the SQL used to create the tables
    # Filter out 'sqlite_sequence' which is an internal housekeeping table
    cursor.execute("""
        SELECT sql 
        FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """)
    
    tables = cursor.fetchall()
    conn.close()
    
    # Unwrap the tuples and join them with newlines
    # logic: row[0] contains the actual "CREATE TABLE..." string
    full_schema = "\n\n".join([row[0] for row in tables if row[0] is not None])
    
    return full_schema
