import sqlite3

def list_all_documents():
    try:
        # Connect to database
        conn = sqlite3.connect('compliance_bot.db')
        cursor = conn.cursor()
        
        # Get all records from documents table
        cursor.execute("SELECT * FROM documents")
        records = cursor.fetchall()
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        if records:
            # Print column headers
            print(" | ".join(columns))
            # Calculate the length of the separator line
            separator_length = sum(len(col) for col in columns) + 3 * (len(columns) - 1)
            print("-" * separator_length)
            
            # Print records
            for record in records:
                print(" | ".join(str(value) for value in record))
        else:
            print("No records found in documents table")
            
    except sqlite3.OperationalError as e:
        print(f"Error accessing database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_all_documents()