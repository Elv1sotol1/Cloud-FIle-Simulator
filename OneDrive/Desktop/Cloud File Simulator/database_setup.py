import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path='cloud_storage.db'):
        """
        Initialize the database connection and create table if not exists
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.create_table()

    def get_connection(self):
        """
        Establish and return a database connection
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        return sqlite3.connect(self.db_path)

    def create_table(self):
        """
        Create the files table if it doesn't exist
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS files (
                    filename TEXT PRIMARY KEY,
                    upload_time TEXT,
                    additional_info TEXT
                )
            ''')
            conn.commit()

    def insert_file(self, filename, upload_time, additional_info=''):
        """
        Insert a new file record into the database
        
        Args:
            filename (str): Name of the file
            upload_time (str): Timestamp of file upload
            additional_info (str, optional): Additional file information
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO files 
                    (filename, upload_time, additional_info) 
                    VALUES (?, ?, ?)
                ''', (filename, upload_time, additional_info))
                conn.commit()
            except sqlite3.Error as e:
                print(f"An error occurred while inserting file: {e}")

    def get_all_files(self):
        """
        Retrieve all file records from the database
        
        Returns:
            list: List of tuples containing file records
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT filename, upload_time FROM files')
            return dict(cursor.fetchall())

    def update_filename(self, old_filename, new_filename):
        """
        Update the filename of an existing record
        
        Args:
            old_filename (str): Current filename
            new_filename (str): New filename to replace the old one
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    UPDATE files 
                    SET filename = ? 
                    WHERE filename = ?
                ''', (new_filename, old_filename))
                conn.commit()
            except sqlite3.Error as e:
                print(f"An error occurred while updating filename: {e}")

    def delete_file(self, filename):
        """
        Delete a file record from the database
        
        Args:
            filename (str): Name of the file to delete
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM files WHERE filename = ?', (filename,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"An error occurred while deleting file: {e}")

# Example usage in main application
def initialize_database():
    """
    Create a global database manager instance
    
    Returns:
        DatabaseManager: Instance of the database manager
    """
    return DatabaseManager()