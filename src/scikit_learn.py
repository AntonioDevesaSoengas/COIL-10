import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from import_files import *

def regresion_lineal(data,columnas_entrada,columna_salida):
    #encode the 'ocean_proximity' column to add it into the model
    data_encoded = pd.get_dummies(data, columns=['ocean_proximity'], drop_first=True)

    #divide dataframes into x(independent variable) and y(dependent variable) parameters
    x = columnas_entrada
    y = columna_salida

    #imput median in the Nan values 
    imputer = SimpleImputer(strategy='median')
    x_imputed = imputer.fit_transform(x)

    #divide variables into test and train
    x_train, x_test, y_train, y_test = train_test_split(x_imputed,y, test_size=0.2, random_state=42)

    #train the model
    model = LinearRegression()
    model.fit(x_train,y_train)

    #get predictions
    predictions = model.predict(x_test)

    #get the Mean Squared Error(MSE) and Determination Coefficient(r^2)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
