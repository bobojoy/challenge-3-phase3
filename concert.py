import sqlite3

#Connect to database
class ConcertDatabase:
    def __init__(self, db_name='concerts.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bands (
                name TEXT PRIMARY KEY,
                hometown TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS venues (
                title TEXT PRIMARY KEY,
                city TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS concerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                band_name TEXT,
                venue_title TEXT,
                date TEXT,
                FOREIGN KEY (band_name) REFERENCES bands(name),
                FOREIGN KEY (venue_title) REFERENCES venues(title)
            )
        """)
        self.conn.commit()

    def insert_data(self):
        bands = [
            ('The Beatles', 'Liverpool'),
            ('Led Zeppelin', 'London'),
            ('Queen', 'London')
        ]
        venues = [
            ('The O2', 'London'),
            ('The Lava Stone', 'Glasgow'),
            ('The Royal Albert Hall', 'London')
        ]
        concerts = [
            ('The Beatles', 'The O2', '2023-06-15'),
            ('Led Zeppelin', 'The Lava Stone', '2023-07-01'),
            ('Queen', 'The Royal Albert Hall', '2023-08-20')
        ]

        self.cursor.executemany("INSERT INTO bands (name, hometown) VALUES (?, ?)", bands)
        self.cursor.executemany("INSERT INTO venues (title, city) VALUES (?, ?)", venues)
        self.cursor.executemany("INSERT INTO concerts (band_name, venue_title, date) VALUES (?, ?, ?)", concerts)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()    
        
    
    
class Concert:
    def __init__(self, id, band_name, venue_title, date):
        self.id = id
        self.band_name = band_name
        self.venue_title = venue_title
        self.date = date

    def __repr__(self):
        return f"Concert(id={self.id}, band_name='{self.band_name}', venue_title='{self.venue_title}', date='{self.date}')"
   
    @staticmethod
    def get_connection():
        return sqlite3.connect('concerts.db')

# Method to get the Band instance for a Concert
    @staticmethod
    def get_band_for_concert(concert_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bands.name, bands.hometown
            FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            WHERE concerts.id = ?
        """, (concert_id,))
        result = cursor.fetchone()
        conn.close()
        return result

# Method to get the Venue instance for a Concert
    @staticmethod
    def get_venue_for_concert(concert_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT venues.title, venues.city
            FROM venues
            JOIN concerts ON venues.title = concerts.venue_title
            WHERE concerts.id = ?
        """, (concert_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    

# Method to get all introductions for a Band
    @staticmethod
    def get_all_introductions(band_name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT "Hello " || venues.city || "!!!!! We are " || bands.name || " and we're from " || bands.hometown
            FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            JOIN venues ON concerts.venue_title = venues.title
            WHERE bands.name = ?
        """, (band_name,))
        results = cursor.fetchall()
        conn.close()
        return [r[0] for r in results]
    
# Method to add a concert for a Band
    @staticmethod
    def add_concert(band_name, venue_title, date):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO concerts (band_name, venue_title, date)
            VALUES (?, ?, ?)
        """, (band_name, venue_title, date))
        conn.commit()
        conn.close()
    



# Method to find a concert at a venue on a specific date
    @staticmethod
    def find_concert_on_date(venue_title, date):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM concerts
            WHERE venue_title = ? AND date = ?
        """, (venue_title, date))
        result = cursor.fetchone()
        conn.close()
        return result   
    
class Band:
    def __init__(self, db: ConcertDatabase):
        self.db = db
    def get_band_for_concert(self, concert_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bands.name, bands.hometown
            FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            WHERE concerts.id = ?
        """, (concert_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_concerts_for_band(self, band_name):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM concerts
            WHERE band_name = ?
        """, (band_name,))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_venues_for_band(self, band_name):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT venues.title, venues.city
            FROM venues
            JOIN concerts ON venues.title = concerts.venue_title
            WHERE concerts.band_name = ?
        """, (band_name,))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_band_with_most_performances():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bands.name, COUNT(*) as performance_count
            FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            GROUP BY bands.name
            ORDER BY performance_count DESC
            LIMIT 1
        """)
        return self.db.cursor.fetchone()
            

# Method to get all concerts for a Venue
class Venue:
    def __init__(self, db:ConcertDatabase):
        self.db = db
    def __repr__(self):
        return f"Venue(title='{self.title}', city='{self.city}')"
    

    def get_venue_for_concert(self, concert_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT venues.title, venues.city
            FROM venues
            JOIN concerts ON venues.title = concerts.venue_title
            WHERE concerts.id = ?
        """, (concert_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_all_concerts_for_venue(self, venue_title):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM concerts
            WHERE venue_title = ?
        """, (venue_title,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_bands_for_venue(self, venue_title):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT bands.name, bands.hometown
            FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            WHERE concerts.venue_title = ?
        """, (venue_title,))
        results = cursor.fetchall()
        conn.close()
        return results
    

    def get_most_frequent_band_at_venue(venue_title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bands.name, COUNT(*) as performance_count
            FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            WHERE concerts.venue_title = ?
            GROUP BY bands.name
            ORDER BY performance_count DESC
             LIMIT 1
        """, (venue_title,))
        result = cursor.fetchone()
        conn.close()
        return result


# Initialize the database and insert sample data
db = ConcertDatabase()
db.create_tables()
db.insert_sample_data()

# Instances of the classes
band = Band(db)
venue = Venue(db)
concert = Concert(db)

# Example usage
concert.concert_introduction(1)
all_bands + band.band_with_most_performances()
print("Band with the most performances:", all_bands)

db.close_connection()