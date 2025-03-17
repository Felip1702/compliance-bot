import sqlite3
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

DATABASE_PATH = "compliance_bot.db"  # Replace with your actual database path

def clean_document_records(user_id: str, document_ids_to_keep: list[str]):
    """
    Cleans up document-related records in the database for a specific user.

    This function deletes records from the `documents` table where the `user_id`
    matches the provided `user_id` AND where the `document_id` is NOT in the
    `document_ids_to_keep` list.  It's designed to allow you to keep certain
    document records while removing others.  It also cleans up messages related to those documents.

    Args:
        user_id: The user ID for whom to clean document records.
        document_ids_to_keep: A list of document IDs to *preserve*.  All
            other documents associated with the `user_id` will be deleted.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Build the SQL query.  We use a parameterized query to prevent SQL injection.
        # The '?' placeholders will be replaced by the values in the `params` tuple.
        # The `IN` clause is constructed dynamically based on the `document_ids_to_keep` list.
        placeholders = ', '.join('?' * len(document_ids_to_keep))
        sql_delete_documents = f"""
            DELETE FROM documents
            WHERE user_id = ?
            AND document_id NOT IN ({placeholders})
        """

        # Include the user_id and the document_ids_to_keep in the parameters for the query
        params = [user_id] + document_ids_to_keep

        # Execute the delete documents
        cursor.execute(sql_delete_documents, params)
        deleted_documents_count = cursor.rowcount
        logging.info(f"Deleted {deleted_documents_count} documents from the 'documents' table for user {user_id}.")

        # Delete messages associated with the deleted documents in the 'messages' table
        # Get the document_ids of the deleted documents by documents_id, because messages does not have user_id
        document_ids_to_delete_query = f"""
            SELECT document_id FROM documents
            WHERE user_id = ?
            AND document_id NOT IN ({placeholders})
        """
        cursor.execute(document_ids_to_delete_query, params)
        document_ids_to_delete = [row[0] for row in cursor.fetchall()]
        deleted_documents_ids = ', '.join('?' * len(document_ids_to_delete))

        # Delete all chats related to those Documents Ids
        sql_delete_chats = f"""
            DELETE FROM chats
            WHERE chat_id IN (
                SELECT chat_id FROM messages
                WHERE message_id IN ({deleted_documents_ids})
            )
        """
        cursor.execute(sql_delete_chats, document_ids_to_delete)
        deleted_chats_count = cursor.rowcount
        logging.info(f"Deleted {deleted_chats_count} chats related to deleted documents for user {user_id}.")

        # Delete messages associated with the deleted documents
        sql_delete_messages = f"""
            DELETE FROM messages
            WHERE chat_id IN (
                SELECT chat_id FROM messages
                WHERE message_id IN ({deleted_documents_ids})
            )
        """
        cursor.execute(sql_delete_messages, document_ids_to_delete)
        deleted_messages_count = cursor.rowcount
        logging.info(f"Deleted {deleted_messages_count} messages related to deleted documents for user {user_id}.")

        conn.commit()
        logging.info("Document cleanup completed successfully.")

    except sqlite3.Error as e:
        logging.error(f"Error cleaning document records: {e}")
        raise  # Re-raise the exception to signal failure
    finally:
        if conn:
            conn.close()

# Example usage:
if __name__ == '__main__':
    user_id_to_clean = "f2a80f37-95b9-4598-8b0c-b17ea7c386ee" # Replace with the actual user ID.
    document_ids_to_keep = ["f6439bd6-e2e6-4e59-b303-5800e64cc513"]  # Replace with document IDs you want to keep.  Empty list [] deletes all

    try:
        clean_document_records(user_id_to_clean, document_ids_to_keep)
        print("Document cleanup completed.")
    except Exception as e:
        print(f"Document cleanup failed: {e}")