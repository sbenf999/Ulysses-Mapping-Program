import sqlite3
import os

class Handler:
    def create_database():
        current_directory = os.getcwd()
        folder_name = "Markers"
        folder_path = os.path.join(current_directory, folder_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        conn = sqlite3.connect('Markers/locationsM.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS locations
                     (id INTEGER PRIMARY KEY, longitude REAL, latitude REAL, name TEXT)''')
        conn.commit()
        conn.close()

    def add_location(longitude, latitude, name):
        conn = sqlite3.connect('Markers/locationsM.db')
        c = conn.cursor()
        c.execute("INSERT INTO locations (longitude, latitude, name) VALUES (?, ?, ?)", (longitude, latitude, name))
        conn.commit()
        conn.close()

    def load_locations():
        conn = sqlite3.connect('Markers/locationsM.db')
        c = conn.cursor()
        c.execute("SELECT longitude, latitude, name FROM locations")
        for row in c.fetchall():
            yield row
        conn.close()
        

