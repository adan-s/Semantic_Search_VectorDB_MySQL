import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# Establish a connection to MySQL
conn = mysql.connector.connect(
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Create the Articles table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    page_content TEXT NOT NULL,
    source VARCHAR(255) NOT NULL
);
""")
conn.commit()

def add_article(page_content, source):
    """Add a new article to the database."""
    sql_query = """
    INSERT INTO Articles (page_content, source)
    VALUES (%s, %s);
    """
    cursor.execute(sql_query, (page_content, source))
    conn.commit()
    print("Article added successfully.")

def fetch_articles(query):
    """Fetch articles that match the query."""
    sql_query = """
    SELECT id, page_content, source
    FROM Articles
    WHERE page_content LIKE %s;
    """
    cursor.execute(sql_query, (f"%{query}%",))
    return cursor.fetchall()

def fetch_all_articles():
    """Fetch all articles from the database."""
    cursor = conn.cursor()
    query = "SELECT * FROM Articles"
    cursor.execute(query)
    articles = cursor.fetchall()
    cursor.close()
    return articles