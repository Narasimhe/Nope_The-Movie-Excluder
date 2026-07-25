import sqlite3

# Connect to your database
with sqlite3.connect("data/movie_excluder.db") as conn:
    # Fetch the schema for all tables
    cursor = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL")
    
    print("\n--- DATABASE SCHEMA ---\n")
    for row in cursor:
        print(row[0])
        print("\n-----------------------\n")