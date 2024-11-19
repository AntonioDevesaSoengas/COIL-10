# Third-party library imports.
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder


def linear_regression(data, input_columns, output_columns):
    """
    Perform linear regression on the given dataset.

    Args:
        data (pd.DataFrame): The dataset containing the data to model.
        input_columns (list): Column names used as independent variables.
        output_column (str): The column name used as the dependent variable.

    Returns:
        tuple: Contains the regression formula, Mean Squared Error (MSE),
               R-squared value, test data (X and Y), and predictions.
    """
    # Encode the non-numeric columns to add them into the model.
    non_numeric_columns = data.select_dtypes(exclude=["number"]).columns

    for column in non_numeric_columns:
        encoder = LabelEncoder()
        # Convert non-numeric values to numeric.
        # Convert to str in case of mixed values.
        data[column] = encoder.fit_transform(data[column].astype(str))
        # Ensure the data type is float64.
        data[column] = data[column].astype("float64")

    # Divide data into x (independent variables) and y (dependent variable).
    x = data[input_columns]
    y = data[output_columns].values.ravel()

    # Split variables into test and train sets.
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42)

    # Train the model.
    model = LinearRegression()
    model.fit(x_train, y_train)

    # Get predictions.
    predictions = model.predict(x_test)

    # Calculate Mean Squared Error (MSE) and R-squared (r^2).
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    # Build the regression formula.
    intercept = model.intercept_
    coefficients = model.coef_
    formula = f"{output_columns} = {intercept:.2f}"
    for i, coef in enumerate(coefficients):
        formula += f" + ({coef:.2f}) * {input_columns[i]}"

    return formula, mse, r2, x_test, y_test, predictions


def plot_regression_graph(y_test, predictions):
    """
    Generate a regression plot showing the true values and predictions.

    Args:
        y_test (array-like): True values of the dependent variable.
        predictions (array-like): Predicted values of the dependent variable.

    Returns:
        matplotlib.figure.Figure: The figure object containing the plot.
    """
    # Generate the plot for regression.
    plt.figure()
    plt.scatter(y_test, predictions, color="blue", label="Predictions")
    plt.plot(y_test, y_test, color="red", label="Ideal Fit")
    plt.xlabel("True Values")
    plt.ylabel("Predictions")
    plt.title("Regression Results")
    plt.legend()

    # Return the figure object.
    return plt.gcf()