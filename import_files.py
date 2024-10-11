from tkinter import filedialog, Tk
import pandas as pd
import os
import sqlite3

def choose_file():
    root = Tk()
    root.withdraw()
    file = filedialog.askopenfilename(
    filetypes = [("csv files", "*.csv"),
                 ("Excel files", "*.xlsx;*.xls"),
                 ("SQlite databases", "*.sqlite;*.db")]
    )
    return file

def read_csv(file_path):
    # Try reading the CSV file
    try:
        df = pd.read_csv(file_path)
        print("CSV file loaded successfully.")
        print(df.head())  # This will print the first 5 rows once
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
    """
    Reads an Excel file and displays the first few rows if read successfully.
    If there is an error, it displays an error message.

    :param file_path: Path to the Excel file.
    :param rows: Number of rows to display (default is 5).
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return
    
    try:
        # Try reading the Excel file
        df = pd.read_excel(file_path)
        
        # Display the first rows of the file
        print(f"Successfully read the file {file_path}. Displaying the first {rows} rows:")
        print(df.head(rows))
    
    except Exception as e:
        # In case of an error, display the error message
        print(f"Error reading the file {file_path}: {str(e)}")

# Example of usage
file_path = 'path/to/your/file.xlsx'
read_excel_file(file_path)

def read_sqlite(db_path, query = "SELECT * FROM nombre_tabla"):
    try:
        connection = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, connection)
        print("SQLite file succesfully loaded.")
        print(df.head())
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
              
read_sqlite(r"C:\Users\Pc\Downloads\housing.db", "SELECT * FROM california_housing_dataset")


def import_data():
    file_path = choose_file()

    if not file_path:
        print("No file was selected.")
        return

    if file_path.endswith(".csv"):
        read_csv(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        read_excel_file(file_path)
    elif file_path.endswith(".sqlite") or file_path.endswith(".db"):
        read_sqlite(file_path, "SELECT * FROM nombre_tabla")
    else:
        print(f"Error: The file '{file_path}' is not a supported format.")

import_data()