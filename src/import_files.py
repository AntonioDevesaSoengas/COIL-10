import pandas as pd
import os
import sqlite3

def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except pd.errors.ParserError:
        print("Error: The CSV file is corrupted or in an invalid format.")
    except FileNotFoundError:
        print("Error: The file was not found at the specified path.")
    except Exception as e:
        print(f"Error reading the CSV file: {e}")

def read_excel_file(file_path, rows=5):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return
    
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error reading the file {file_path}: {str(e)}")

def read_sqlite(db_path, query):
    try:
        connection = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, connection)
        return df
    except sqlite3.DatabaseError as e:
        print(f"Error reading SQLite database: {e}")
    except FileNotFoundError:
        print("Error: Database file wasn't found in the specified path.")
    except Exception as e:
        print(f"Error reading database: {e}")
    finally: 
        if connection:
            connection.close()

def import_data(file_path):
    if not file_path:
        print("No file was selected.")
        return None
    elif file_path.endswith(".csv"):
        return read_csv(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        return read_excel_file(file_path)
    elif file_path.endswith(".sqlite") or file_path.endswith(".db"):
        return read_sqlite(file_path, "SELECT * FROM california_housing_dataset")
    else:
        print(f"Error: The file '{file_path}' is not a supported format.")
        return None
