import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from import_files import *

def regresion_lineal(data,columnas_entrada,columna_salida):

    #encode the 'ocean_proximity' column to add it into the model
    non_numeric_columns = data.select_dtypes(exclude=['number']).columns

    for column in non_numeric_columns:
        encoder = LabelEncoder()
        # Convertir los valores no numéricos a numéricos
        data[column] = encoder.fit_transform(data[column].astype(str))  # Convertimos a str en caso de valores mixtos
        # Aseguramos el tipo de dato float64
        data[column] = data[column].astype('float64')

    #divide dataframes into x(independent variable) and y(dependent variable) parameters
    x = data[columnas_entrada]
    y = data[columna_salida].values.ravel()

    #divide variables into test and train
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

    #train the model
    model = LinearRegression()
    model.fit(x_train,y_train)

    #get predictions
    predictions = model.predict(x_test)

    #get the Mean Squared Error(MSE) and Determination Coefficient(r^2)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    # Build the formula
    intercept = model.intercept_
    coeficientes = model.coef_
    formula = f"{columna_salida} = {intercept:.2f}"
    for i, coef in enumerate(coeficientes):
        formula += f" + ({coef:.2f}) * {columnas_entrada[i]}"

    return formula, mse, r2, x_test, y_test, predictions, model

def mostrar_grafica_regresion(y_test, predictions):
    # Generate the plot for regression
    plt.figure()
    plt.scatter(y_test, predictions, color="blue", label="Predictions")
    plt.plot(y_test, y_test, color="red", label="Ideal Fit")
    plt.xlabel("True Values")
    plt.ylabel("Predictions")
    plt.title("Regression Results")
    plt.legend()
    
    # Return the figure object
    return plt.gcf()

