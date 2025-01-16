from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# MySQL connection setup
def get_mysql_connection():
    return connect(
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# Initialize the database
def initialize_database():
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()

        # Create the Articles table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            page_content TEXT NOT NULL,
            source VARCHAR(255) NOT NULL
        );
        """)

        # Create `Memory` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Memory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(255) NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully.")
    except Error as e:
        print(f"Error initializing database: {e}")


# Add a new article to the database
def add_article(page_content, source):
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()
        sql_query = """
        INSERT INTO Articles (page_content, source)
        VALUES (%s, %s);
        """
        cursor.execute(sql_query, (page_content, source))
        connection.commit()
        cursor.close()
        connection.close()
        print("Article added successfully.")
    except Error as e:
        print(f"Error adding article: {e}")


# Fetch articles that match the query
def fetch_articles(query):
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)
        sql_query = """
        SELECT id, page_content, source
        FROM Articles
        WHERE page_content LIKE %s;
        """
        cursor.execute(sql_query, (f"%{query}%",))
        articles = cursor.fetchall()
        cursor.close()
        connection.close()
        return articles
    except Error as e:
        print(f"Error fetching articles: {e}")
        return []


# Fetch all articles from the database
def fetch_all_articles():
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)
        sql_query = "SELECT * FROM Articles"
        cursor.execute(sql_query)
        articles = cursor.fetchall()
        cursor.close()
        connection.close()
        return articles
    except Error as e:
        print(f"Error fetching all articles: {e}")
        return []


# Store Memory in MySQL
def store_memory(session_id, query, response):
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO Memory (session_id, query, response)
            VALUES (%s, %s, %s)
            """,
            (session_id, query, response),
        )
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error storing Memory: {e}")


# Retrieve Memory from MySQL
def retrieve_memory(session_id):
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT query, response FROM Memory
            WHERE session_id = %s
            ORDER BY created_at ASC
            """,
            (session_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Error as e:
        print(f"Error retrieving Memory: {e}")
        return []


# Retrieve all available session IDs
def get_all_sessions():
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT session_id FROM Memory")
        sessions = cursor.fetchall()
        cursor.close()
        connection.close()
        return [session[0] for session in sessions]
    except Error as e:
        print(f"Error retrieving sessions: {e}")
        return []
