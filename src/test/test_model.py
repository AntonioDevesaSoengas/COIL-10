# Standard Libraries
import os
import sys
import pickle
import pytest


# Third-Party Libraries
from sklearn.linear_model import LinearRegression
import pandas as pd
from pathlib import Path
import numpy as np
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Local Libraries
from data_preparation.import_files import import_data
from model_management.model_saver import ModelSaver
from model_management.model_loader import ModelLoader



# ------------------- Test for Model Creation -------------------
def test_model_creation():
    """
    Tests the creation of a linear regression model and verifies its coefficients and intercept.
    """
    # Test data
    X = np.array([[1], [2], [3]])
    y = np.array([2, 4, 6])

    # Create model
    model = LinearRegression()
    model.fit(X, y)

    # Verify coefficient and intercept
    assert model.coef_[0] == pytest.approx(2, rel=1e-2)
    assert model.intercept_ == pytest.approx(0, rel=1e-2)


# ------------------- Test for Model Prediction -------------------
def test_model_prediction():
    """
    Tests the prediction functionality of the linear regression model to ensure accuracy.
    """
    # Test data
    X = np.array([[1], [2], [3]])
    y = np.array([2, 4, 6])

    # Create model
    model = LinearRegression()
    model.fit(X, y)

    # Verify prediction
    predictions = model.predict(X)
    assert predictions[0] == pytest.approx(2, rel=1e-2)
    assert predictions[1] == pytest.approx(4, rel=1e-2)
    assert predictions[2] == pytest.approx(6, rel=1e-2)


# ------------------- Test for Model Saving -------------------
def test_model_saving(tmp_path):
    """
    Tests the saving functionality of the linear regression model using pickle.
    """
    # Test data
    X = [[1], [2], [3]]
    y = [2, 4, 6]

    # Create model
    model = LinearRegression()
    model.fit(X, y)

    # Save model using ModelSaver
    file_path = tmp_path / "model.pkl"
    model_saver = ModelSaver(
        model=model,
        formula="y = 2x",
        r_squared=1.0,
        mse=0.0,
        input_columns=["x"],
        output_column="y",
        description="Test model"
    )
    model_saver.save_model(file_path)

    # Verify that the file was created
    assert file_path.exists()


# ------------------- Test for Model Loading -------------------
def test_model_loading(tmp_path):
    """
    Tests the loading functionality of the linear regression model using pickle.
    """
    # Test data
    X = [[1], [2], [3]]
    y = [2, 4, 6]

    # Create and save a model
    model = LinearRegression()
    model.fit(X, y)
    file_path = tmp_path / "model.pkl"

    with open(file_path, 'wb') as f:
        pickle.dump(model, f)

    # Load model using ModelLoader
    model_loader = ModelLoader()
    loaded_model = model_loader.load_model(file_path)

    # Verify that the loaded model works correctly
    assert loaded_model.predict([[4]])[0] == pytest.approx(8, rel=1e-2)


# ------------------- Test for Importing CSV File -------------------
def test_import_csv_file(tmp_path):
    """
    Tests importing a CSV file using the import_data function.
    """
    # Create a sample CSV file
    csv_content = "col1,col2\n1,2\n3,4\n5,6"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    # Import data
    df = import_data(str(csv_file))

    # Verify the imported data
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]
    assert df.iloc[0]["col1"] == 1
    assert df.iloc[0]["col2"] == 2


# ------------------- Test for Importing Excel File -------------------
def test_import_excel_file(tmp_path):
    """
    Tests importing an Excel file using the import_data function.
    """
    # Create a sample Excel file
    excel_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"col1": [1, 3, 5], "col2": [2, 4, 6]})
    df.to_excel(excel_file, index=False)

    # Import data
    imported_df = import_data(str(excel_file))

    # Verify the imported data
    assert not imported_df.empty
    assert list(imported_df.columns) == ["col1", "col2"]
    assert imported_df.iloc[0]["col1"] == 1
    assert imported_df.iloc[0]["col2"] == 2


# ------------------- Test for Importing SQLite Database -------------------
def test_import_sqlite_file(tmp_path):
    """
    Tests importing data from a SQLite database using the import_data function.
    """
    # Create a sample SQLite database
    db_file = tmp_path / "test.db"
    connection = sqlite3.connect(db_file)
    df = pd.DataFrame({"col1": [1, 3, 5], "col2": [2, 4, 6]})
    df.to_sql("test_table", connection, index=False)
    connection.close()

    # Import data
    imported_df = import_data(str(db_file))

    # Verify the imported data
    assert not imported_df.empty
    assert list(imported_df.columns) == ["col1", "col2"]
    assert imported_df.iloc[0]["col1"] == 1
    assert imported_df.iloc[0]["col2"] == 2


# ------------------- Test for Importing Invalid File -------------------
def test_import_invalid_file():
    """
    Tests importing an invalid file format, expecting a ValueError.
    """
    with pytest.raises(ValueError):
        import_data("invalid_file.txt")
