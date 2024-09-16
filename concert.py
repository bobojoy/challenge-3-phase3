import sqlite3

def get_connection():
    return sqlite3.connect('concerts.db')

# Method to get the Band instance for a Concert
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

# Method to get all concerts for a Venue
def get_concerts_for_venue(venue_title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM concerts
        WHERE venue_title = ?
    """, (venue_title,))
    results = cursor.fetchall()
    conn.close()
    return results

# Method to get all bands who performed at a Venue
def get_bands_for_venue(venue_title):
    conn = get_connection()
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

# Method to get all concerts a Band has played
def get_concerts_for_band(band_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM concerts
        WHERE band_name = ?
    """, (band_name,))
    results = cursor.fetchall()
    conn.close()
    return results

# Method to get all venues a Band has performed at
def get_venues_for_band(band_name):
    conn = get_connection()
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

# Method to add a concert for a Band
def add_concert(band_name, venue_title, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO concerts (band_name, venue_title, date)
        VALUES (?, ?, ?)
    """, (band_name, venue_title, date))
    conn.commit()
    conn.close()

# Method to get all introductions for a Band
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

# Method to get the Band with the most performances
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
    result = cursor.fetchone()
    conn.close()
    return result

# Method to find a concert at a venue on a specific date
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

# Method to find the most frequent band at a venue
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
