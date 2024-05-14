# Idea Insprire-backend
This project consists of several components aimed at managing and searching through a database of files, leveraging Flask for the web interface, psycopg2 for database interactions, and fuzzy matching for search functionality. The project also includes a script for structuring file information into JSON format.
the database is updated via python script which adds the data into the database and the database is automatically updated when run.py is runnung in the background

## The project includes the following key files and scripts:
1. flaskapp.py:
  1. Handles HTTP requests and provides endpoints for searching the database.
  2. Uses fuzzy matching to find relevant records based on search inputs.
  3. Configures CORS to allow cross-origin requests.
  4. Connects to a PostgreSQL database to retrieve and search through file records.
2. Databaseinserter.py
  1. Defines the structure of the database, creating tables for folders (MAIN_FOLDER) and files (FILE).
  2. Reads from a JSON file (file_structure.json) to populate the database with initial data.
  3. Generates abbreviations for folder names and inserts them into the database.1.
3. jsoncreator.py
  1. Traverses a specified directory to collect file information.
  2. Converts this information into a nested dictionary structure.
  3. Writes the structured data to a JSON file (file_structure.json).
4. advancesearchapi.py
   1. Contains the logic for performing fuzzy searches on the database summaries.

## How to initiate the backend?
start by initiating the database 
    ``` python3 databaseinserter.py ``` 
