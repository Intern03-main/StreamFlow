import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if any)
load_dotenv()

# DB Credentials
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Create connection to MySQL
def create_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            print("[INFO] Connected to MySQL database.")
            return connection
    except Error as e:
        print(f"[ERROR] Error connecting to MySQL: {e}")
        return None

# Create table if not exists
def create_table():
    """Create the streamflow_data table if it does not exist."""
    connection = create_connection()
    if connection is None:
        print("[ERROR] Failed to create database connection.")
        return

    create_table_query = """
    CREATE TABLE IF NOT EXISTS streamflow_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        station_id VARCHAR(255),
        date DATE,
        discharge FLOAT
    )
    """

    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print("[INFO] Table 'streamflow_data' is ready.")
    except Error as e:
        print(f"[ERROR] Failed to create table: {e}")
    finally:
        cursor.close()
        connection.close()

# Insert data into the table
def insert_data(data):
    """Inserts scraped data into the MySQL database, updating if the record already exists."""
    connection = create_connection()
    if not connection:
        return

    try:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO streamflow_data (station_id, date, discharge)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            discharge = VALUES(discharge)
        """

        cursor.executemany(insert_query, data)
        connection.commit()
        print(f"[SUCCESS] Inserted/Updated {cursor.rowcount} rows into the database.")
    except mysql.connector.Error as e:
        print(f"[ERROR] Failed to insert/update data: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()