import sqlite3, csv
from pathlib import Path

schema = Path("database_schema\schema.sql")

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")
conn.executescript(schema.read_text()) # Creates table from file
conn.close()



