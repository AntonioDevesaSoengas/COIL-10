import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from import_files import *

#import and read data from the computer
data = import_data(r"C:\Users\ivanr\Desktop\Universidad\2º Curso\1º Cuatri\Ingenieria Software\housing.csv")

#encode the 'ocean_proximity' column to add it into the model
data_encoded = pd.get_dummies(data, columns=['ocean_proximity'], drop_first=True)

#divide dataframes into x(independent variable) and y(dependent variable) parameters
x = data_encoded[['housing_median_age','total_rooms','population','median_income','longitude','latitude','total_bedrooms','households'] + [col for col in data_encoded.columns if 'ocean_proximity' in col]]
y = data_encoded['median_house_value']

#imput median in the Nan values 
imputer = SimpleImputer(strategy='median')
x_imputed = imputer.fit_transform(x)

#divide variables into test and train
x_train, x_test, y_train, y_test = train_test_split(x_imputed,y, test_size=0.2, random_state=42)

#train the model
model = LinearRegression()
model.fit(x_train,y_train)

#print summary
print(data_encoded.describe())

#get predictions
predictions = model.predict(x_test)
print(f"Predictions: {predictions}")

#get the Mean Squared Error(MSE) and Determination Coefficient(r^2)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"Mean squared error (MSE): {mse}")
print(f"Determination coefficient (r^2): {r2}")