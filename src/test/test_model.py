# Standard Libraries
import pickle

# Third-Party Libraries
import pytest
import numpy as np
from sklearn.linear_model import LinearRegression


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


# Test for saving the model
def test_model_saving(tmp_path):
    """
    Tests the saving functionality of the linear regression model using pickle.

    Args:
        tmp_path (Path): A temporary directory provided by pytest for file operations.
    """
    # Test data
    X = [[1], [2], [3]]
    y = [2, 4, 6]

    # Create model
    model = LinearRegression()
    model.fit(X, y)

    # Save model
    file_path = tmp_path / "model.pkl"
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)

    # Verify that the file was created
    assert file_path.exists()

    # Test for loading the model
def test_model_loading(tmp_path):
    """
    Tests the loading functionality of the linear regression model using pickle.

    Args:
        tmp_path (Path): A temporary directory provided by pytest for file operations.
    """
    # Create and save a model to a file
    X = [[1], [2], [3]]
    y = [2, 4, 6]
    model = LinearRegression()
    model.fit(X, y)

    file_path = tmp_path / "model.pkl"
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)

    # Load model
    with open(file_path, 'rb') as f:
        loaded_model = pickle.load(f)

    # Verify that the loaded model works correctly
    assert loaded_model.predict([[4]])[0] == pytest.approx(8, rel=1e-2)
