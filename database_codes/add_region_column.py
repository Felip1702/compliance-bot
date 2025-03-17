import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

DATABASE_PATH = "compliance_bot.db"  # Replace with your actual database path

def add_region_column():
    """Adds the 'region' column to the 'documents' table if it doesn't exist."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Check if the 'region' column already exists.
        cursor.execute("PRAGMA table_info(documents);")
        columns = [col[1] for col in cursor.fetchall()] # Extract column names

        if "region" not in columns:
            # Add the 'region' column with a default value of NULL.
            cursor.execute("ALTER TABLE documents ADD COLUMN region TEXT DEFAULT NULL;")
            conn.commit()
            logging.info("Added 'region' column to the 'documents' table.")
        else:
            logging.info("The 'region' column already exists in the 'documents' table.")

    except sqlite3.Error as e:
        logging.error(f"Error adding 'region' column: {e}")
        raise  # Re-raise to signal failure

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    try:
        add_region_column()
        print("Database migration completed.")
    except Exception as e:
        print(f"Database migration failed: {e}")