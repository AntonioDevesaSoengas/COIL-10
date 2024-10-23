import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from import_files import *

#import and read data from the computer
data = import_data(r"C:\Users\ivanr\Desktop\Universidad\2º Curso\1º Cuatri\Ingenieria Software\housing.csv")

#turn data into a pandas dataframe
df = pd.DataFrame(data)

#divide dataframes into x(independent variable) and y(dependent variable) parameters
x = df[['housing_median_age','total_rooms','population','median_income']]
y = df['median_house_value']

#divide variables into test and train
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

#train the model
model = LinearRegression()
model.fit(x_train,y_train)

