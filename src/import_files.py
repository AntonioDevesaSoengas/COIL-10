import pandas as pd
import os
import sqlite3

def read_csv(file_path):
    return pd.read_csv(file_path)

def read_excel_file(file_path):
    return pd.read_excel(file_path)

def read_sqlite(db_path, query="SELECT * FROM california_housing_dataset"):
    with sqlite3.connect(db_path) as connection:
        return pd.read_sql_query(query, connection)

def import_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    # Selección automática de tipo de archivo
    file_ext = os.path.splitext(file_path)[-1].lower()
    try:
        if file_ext == ".csv":
            return read_csv(file_path)
        elif file_ext in [".xlsx", ".xls"]:
            return read_excel_file(file_path)
        elif file_ext in [".sqlite", ".db"]:
            return read_sqlite(file_path)
        else:
            raise ValueError(f"The file format '{file_ext}' is not supported.")
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        raise ValueError(f"Error reading the file: {e}")
