# Concert Management System

## Overview

This project manages a concert database with three main tables: `bands`, `venues`, and `concerts`. 

## Schema

1. **bands**: Stores information about bands.
   - `name` (TEXT, Primary Key)
   - `hometown` (TEXT)

2. **venues**: Stores information about venues.
   - `title` (TEXT, Primary Key)
   - `city` (TEXT)

3. **concerts**: Stores information about concerts.
   - `band_name` (TEXT, Foreign Key referencing `bands.name`)
   - `venue_title` (TEXT, Foreign Key referencing `venues.title`)
   - `date` (TEXT)
   - Primary Key: (`band_name`, `venue_title`, `date`)

## Setup

1. **Create Database and Tables**

   Use the provided SQL commands to create the `bands`, `venues`, and `concerts` tables.

2. **Python Script**

   The `concert_management.py` script includes methods for managing and querying the concert database using raw SQL queries.


## Dependencies

- Python 3.x
- sqlite3 (included with Python standard library)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
