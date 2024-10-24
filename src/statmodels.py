import statsmodels.formula.api as smf
import statsmodels.api as sm
import pandas as pd
from import_files import *

# Load the model data
data = import_data(r"C:\Users\Alejandro\Downloads\housing.csv")

# Display the first few rows of the DataFrame to verify that the data has been loaded correctly
print(data.head())

'''
Convert the 'ocean_proximity' column into dummy variables using one-hot encoding.
To avoid multicollinearity, set drop_first=True to remove the first category and set it as the reference.
'''
data_encoded = pd.get_dummies(data, columns=['ocean_proximity'], drop_first=True)

# Verify data types before any additional conversion
print("\nData types before conversion:")
print(data_encoded.dtypes)

# Identify and convert boolean columns to float if they exist
bool_cols = [col for col in data_encoded.columns if data_encoded[col].dtype == 'bool']
if bool_cols:
    print("\nIdentified boolean columns:")
    print(bool_cols)
    data_encoded[bool_cols] = data_encoded[bool_cols].astype('float64')
else:
    print("\nNo boolean columns identified.")

# Verify data types after conversion
print("\nData types after conversion:")
print(data_encoded.dtypes)

# Check for null values in the columns
print("\nCount of null values per column:")
print(data_encoded.isnull().sum())

# Fill null values with the mean of each column
data_encoded.fillna(data_encoded.mean(), inplace=True)

# Check again for null values after handling
print("\nCount of null values after handling NaNs:")
print(data_encoded.isnull().sum())

# Select independent variables (X) and the dependent variable (y)
x = data_encoded[['housing_median_age', 'total_rooms', 'population', 'median_income', 'longitude', 'latitude', 'total_bedrooms', 'households'] + 
                 [col for col in data_encoded.columns if 'ocean_proximity' in col]]
y = data_encoded['median_house_value']

# Add the intercept, which is the value the dependent variable takes when all independents are zero
x = sm.add_constant(x)

# Verify that there are no null values in X and y
print("\nVerification of NaNs in X:")
print(x.isnull().sum())
print("\nVerification of NaNs in y:")
print(y.isnull().sum())

# Create the regression model
model = sm.OLS(y, x)

# Fit the model
result = model.fit()

# Generate predictions using the fitted model
predictions = result.predict(x)

# Show the first 5 predictions
print("\nModel Predictions (first 5):")
print(predictions.head())

# Show the summary
print("\nSummary of the OLS regression model:")
print(result.summary())

# Calculate MSE and R²
mse = result.mse_resid  # Residual Mean Squared Error
r_squared = result.rsquared  # R-squared

print(f"\nMean Squared Error (MSE): {mse}")
print(f"R-squared (R²): {r_squared}")
