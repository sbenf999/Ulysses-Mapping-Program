import sqlite3

class Handler:
    def create_database():
        conn = sqlite3.connect('locationsM.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS locations
                     (id INTEGER PRIMARY KEY, longitude REAL, latitude REAL, name TEXT)''')
        conn.commit()
        conn.close()

    # Function to add a record to the database
    def add_location(longitude, latitude, name):
        conn = sqlite3.connect('locationsM.db')
        c = conn.cursor()
        c.execute("INSERT INTO locations (longitude, latitude, name) VALUES (?, ?, ?)", (longitude, latitude, name))
        conn.commit()
        conn.close()

    # Function to load records from the database one by one
    def load_locations():
        conn = sqlite3.connect('locationsM.db')
        c = conn.cursor()
        c.execute("SELECT longitude, latitude, name FROM locations")
        for row in c.fetchall():
            yield row
        conn.close()
        

