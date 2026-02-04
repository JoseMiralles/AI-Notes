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


def execute_query(query: str, db_path: str):
    """
    Executes a SQL query against the specified SQLite database and returns the results.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    return results


def fill_sql_template(query: str) -> str:
    """
    Replaces dynamic placeholders in the SQL query with example values from the CSV.
    Placeholders are expected to be in the format <field_name>.
    """
    csv_path = './data/template_fields.csv'
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Template fields file not found at: {csv_path}")

    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            placeholder = f"<{row['field_name']}>"
            query = query.replace(placeholder, row['example_value'])
    
    return query
