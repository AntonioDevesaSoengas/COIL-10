import statsmodels.formula.api as smf
import statsmodels.api as sm
import pandas as pd
from import_files import *

# Carga los datos del modelo 
data = import_data(r"C:\Users\Alejandro\Downloads\housing.csv")

# Visualiza las primeras filas de Data para verificar que los datos se hayan cargado correctamente
print(data.head())

'''
Convertir la columna 'ocean_proximity' en variables dummy mediante one-hot encoding.
Para evitar multicolinealidad, se elimina la primera categoría utilizando drop_first=True.
'''
data_encoded = pd.get_dummies(data, columns=['ocean_proximity'], drop_first=True)

# Verificar tipos de datos antes de cualquier conversión adicional
print("\nTipos de datos antes de la conversión:")
print(data_encoded.dtypes)

# Identificar y convertir columnas booleanas a float si existen
bool_cols = [col for col in data_encoded.columns if data_encoded[col].dtype == 'bool']
if bool_cols:
    print("\nColumnas booleanas identificadas:")
    print(bool_cols)
    data_encoded[bool_cols] = data_encoded[bool_cols].astype('float64')
else:
    print("\nNo se identificaron columnas booleanas.")

# Verificar tipos de datos después de la conversión
print("\nTipos de datos después de la conversión:")
print(data_encoded.dtypes)

# Verificar valores nulos en las columnas
print("\nConteo de valores nulos por columna:")
print(data_encoded.isnull().sum())

# Rellenar los valores nulos con la media de cada columna
data_encoded.fillna(data_encoded.mean(), inplace=True)

# Verificar nuevamente valores nulos después del manejo
print("\nConteo de valores nulos después de manejar los NaN:")
print(data_encoded.isnull().sum())

# Seleccionamos las variables independientes (X) y la variable dependiente (y)
x = data_encoded[['housing_median_age', 'total_rooms', 'population', 'median_income', 'longitude', 'latitude', 'total_bedrooms', 'households'] + 
                 [col for col in data_encoded.columns if 'ocean_proximity' in col]]
y = data_encoded['median_house_value']

# Añadimos el intercepto valor que toma la variable dependiente, cuando todas las independientes son cero
x = sm.add_constant(x)

# Verificar que no haya valores nulos en X e y
print("\nVerificación de NaN en X:")
print(x.isnull().sum())
print("\nVerificación de NaN en y:")
print(y.isnull().sum())

# Crear el modelo de regresión
model = sm.OLS(y, x)

# Ajustar el modelo
result = model.fit()

print("\nResumen del modelo de regresión OLS:")
print(result.summary())