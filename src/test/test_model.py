# Standard Libraries
import os
import sys
import pickle
import pytest

# Third-Party Libraries
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import sqlite3
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication, QWidget

# Ajustar sys.path para apuntar al directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

# Local Libraries
from data_preparation.import_files import import_data
from model_management.model_saver import ModelSaver
from model_management.model_loader import ModelLoader


# ------------------- Test for Model Creation -------------------
def test_model_creation():
    """
    Tests the creation of a linear regression model and verifies its coefficients and intercept.
    """
    X = np.array([[1], [2], [3]])
    y = np.array([2, 4, 6])

    model = LinearRegression()
    model.fit(X, y)

    assert model.coef_[0] == pytest.approx(2, rel=1e-2)
    assert model.intercept_ == pytest.approx(0, rel=1e-2)


# ------------------- Test for Model Prediction -------------------
def test_model_prediction():
    """
    Tests the prediction functionality of the linear regression model to ensure accuracy.
    """
    X = np.array([[1], [2], [3]])
    y = np.array([2, 4, 6])

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)
    assert predictions[0] == pytest.approx(2, rel=1e-2)
    assert predictions[1] == pytest.approx(4, rel=1e-2)
    assert predictions[2] == pytest.approx(6, rel=1e-2)


# ------------------- Test for Model Saving -------------------
def test_model_saving(tmp_path):
    X = [[1], [2], [3]]
    y = [2, 4, 6]

    model = LinearRegression()
    model.fit(X, y)

    file_path = tmp_path / "model.joblib"

    model_saver = ModelSaver(
        model=model,
        formula="y = 2x",
        r_squared=1.0,
        mse=0.0,
        input_columns=["x"],
        output_column="y",
        description="Test model"
    )

    with patch('PyQt5.QtWidgets.QFileDialog.getSaveFileName', return_value=(str(file_path), '')), \
         patch('PyQt5.QtWidgets.QMessageBox.information'), \
         patch('PyQt5.QtWidgets.QMessageBox.critical'):
        model_saver.save_model_dialog()

    assert file_path.exists()


# ------------------- Test for Model Loading -------------------
# ------------------- Test for Model Loading -------------------
def test_model_loading(tmp_path):
    """
    Tests the loading functionality of the linear regression model using joblib.
    """
    # Crear una instancia de QApplication
    app = QApplication(sys.argv)

    # Test data
    X = [[1], [2], [3]]
    y = [2, 4, 6]

    # Create and save a model
    model = LinearRegression()
    model.fit(X, y)
    file_path = tmp_path / "model.joblib"

    # Guardar el modelo como un diccionario
    model_data = {
        'model': model,
        'input_columns': ['x'],
        'output_column': 'y'
    }

    with open(file_path, 'wb') as f:
        pickle.dump(model_data, f)

    # Crear un QWidget como viewer
    viewer = QWidget()
    model_loader = ModelLoader(viewer=viewer)

    # Load model
    loaded_model = model_loader.load_model(file_path, test_mode=True)

    # Verify the loaded model prediction
    assert loaded_model.predict([[4]])[0] == pytest.approx(8, rel=1e-2)

    # Cerrar la aplicación después del test
    app.quit()



# ------------------- Test for Importing CSV File -------------------
def test_import_csv_file(tmp_path):
    csv_content = "col1,col2\n1,2\n3,4\n5,6"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    df = import_data(str(csv_file))

    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]
    assert df.iloc[0]["col1"] == 1
    assert df.iloc[0]["col2"] == 2


# ------------------- Test for Importing Excel File -------------------
def test_import_excel_file(tmp_path):
    excel_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"col1": [1, 3, 5], "col2": [2, 4, 6]})
    df.to_excel(excel_file, index=False)

    imported_df = import_data(str(excel_file))

    assert not imported_df.empty
    assert list(imported_df.columns) == ["col1", "col2"]
    assert imported_df.iloc[0]["col1"] == 1
    assert imported_df.iloc[0]["col2"] == 2


# ------------------- Test for Importing SQLite Database -------------------
def test_import_sqlite_file(tmp_path):
    db_file = tmp_path / "test.db"
    connection = sqlite3.connect(db_file)
    df = pd.DataFrame({"col1": [1, 3, 5], "col2": [2, 4, 6]})
    df.to_sql("test_table", connection, index=False)
    connection.close()

    imported_df = import_data(str(db_file))

    assert not imported_df.empty
    assert list(imported_df.columns) == ["col1", "col2"]
    assert imported_df.iloc[0]["col1"] == 1
    assert imported_df.iloc[0]["col2"] == 2


# ------------------- Test for Importing Invalid File -------------------
def test_import_invalid_file(tmp_path):
    invalid_file = tmp_path / "invalid_file.txt"
    invalid_file.write_text("This is not a valid dataset.")

    with pytest.raises(ValueError):
        import_data(str(invalid_file))
