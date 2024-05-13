import os
import time
import subprocess
import psycopg2

# Database connection parameters
db_params = {
    "dbname": "IP",
    "user": "yash",
    "password": "yash",
    "host": "localhost",
    "port": "5433"
}

# Function to connect to the database
def connect_to_database():
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

# Function to check for new folders, remove file_structure.json, update database, and run scripts
def check_and_update_database(database_path, initial_directories):
    # Get the list of directories in the Database folder
    current_directories = os.listdir(database_path)

    # Check for new folders
    new_directories = set(current_directories) - set(initial_directories)

    if new_directories:
        print("New folders detected:", new_directories)

        # Remove the file_structure.json file
        file_structure_path = os.path.join(database_path, "file_structure.json")
        if os.path.exists(file_structure_path):
            os.remove(file_structure_path)
            print("file_structure.json removed.")

        # Connect to the database
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()

                # Check if MAIN_FOLDER table exists, create if not
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS MAIN_FOLDER (
                        folder_id SERIAL PRIMARY KEY,
                        folder_name VARCHAR(255) NOT NULL,
                        abbreviation VARCHAR(10)
                    )
                """)

                # Check for new folders and insert into MAIN_FOLDER table
                for folder_name in new_directories:
                    cursor.execute("""
                        INSERT INTO MAIN_FOLDER (folder_name) VALUES (%s)
                    """, (folder_name,))

                # Remove duplicate files in the database
                cursor.execute("""
                    DELETE FROM FILE
                    WHERE file_id NOT IN (
                        SELECT MIN(file_id)
                        FROM FILE
                        GROUP BY file_name, file_type, file_path, folder_id
                    )
                """)

                connection.commit()
                cursor.close()
                connection.close()
                
                print("Database updated successfully.")

                # Run scripts after updating the database
                subprocess.run(["python3", "jsoncreator.py"])
                subprocess.run(["python3", "databaseinserter.py"])
                subprocess.run(["python3", "textfile_reader.py"])

            except psycopg2.Error as e:
                print("Error updating database:", e)
        else:
            print("Error: Unable to connect to the database.")

    return current_directories

# Path to the Database folder
database_path = "/Users/nvgenomics/Desktop/hostingdata/Database"

# Initial list of directories in the Database folder
initial_directories = os.listdir(database_path)

while True:
    initial_directories = check_and_update_database(database_path, initial_directories)

    # Sleep for a while before checking again
    time.sleep(10)  # Adjust the interval as needed
