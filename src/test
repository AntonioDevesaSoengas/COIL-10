import pytest
import pickle
from sklearn.linear_model import LinearRegression
import numpy as np

# Pruebas para la creación del modelo
def test_model_creation():
    # Datos de prueba
    X = np.array([[1], [2], [3]])
    y = np.array([2, 4, 6])
    
    # Crear modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Verificar coeficiente e intercepto
    assert model.coef_[0] == pytest.approx(2, rel=1e-2)
    assert model.intercept_ == pytest.approx(0, rel=1e-2)

def test_model_prediction():
    # Datos de prueba
    X = np.array([[1], [2], [3]])
    y = np.array([2, 4, 6])
    
    # Crear modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Verificar predicción
    predictions = model.predict(X)
    assert predictions[0] == pytest.approx(2, rel=1e-2)
    assert predictions[1] == pytest.approx(4, rel=1e-2)
    assert predictions[2] == pytest.approx(6, rel=1e-2)

# Pruebas para guardar y cargar el modelo
def test_model_saving_and_loading(tmp_path):
    # Datos de prueba
    X = [[1], [2], [3]]
    y = [2, 4, 6]
    
    # Crear modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Guardar modelo
    file_path = tmp_path / "model.pkl"
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)
    
    # Cargar modelo
    with open(file_path, 'rb') as f:
        loaded_model = pickle.load(f)
    
    # Verificar que el modelo cargado funcione correctamente
    assert loaded_model.predict([[4]])[0] == pytest.approx(8, rel=1e-2)
