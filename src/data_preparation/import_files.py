# Standard libraries.
import os
import sqlite3

# Third-party libraries.
import pandas as pd


# Reads a CSV file and returns a DataFrame.
def _read_csv(file_path):
    return pd.read_csv(file_path)


# Reads an Excel file and returns a DataFrame.
def _read_excel_file(file_path):
    return pd.read_excel(file_path)


# Connects to a SQLite database and executes a query to return
# the result as a DataFrame.
def _read_sqlite(db_path, query="SELECT * FROM test_table"):
    with sqlite3.connect(db_path) as connection:
        return pd.read_sql_query(query, connection)


def import_data(file_path):
    """
    Import data from a file based on its extension and return a DataFrame.

    Args:
        file_path (str): Path to the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is not supported or if there's an error
            reading the file.

    Returns:
        pd.DataFrame: DataFrame containing the imported data.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    file_ext = os.path.splitext(file_path)[-1].lower()

    try:
        if file_ext == ".csv":
            return _read_csv(file_path)
        elif file_ext in [".xlsx", ".xls"]:
            return _read_excel_file(file_path)
        elif file_ext in [".sqlite", ".db"]:
            return _read_sqlite(file_path)
        else:
            raise ValueError(f"The file format '{file_ext}' is not supported.")

    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        raise ValueError(f"Error reading the file: {e}")
