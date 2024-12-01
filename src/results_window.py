# Third-party libraries.
import pandas as pd
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QGroupBox,
    QMessageBox,
    QPushButton,
    QLineEdit
)
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas
)

# Local libraries.
from scikit_learn import linear_regression, plot_regression_graph
from model_saver import ModelSaver
from helpers import LabelHelper, ButtonHelper


class ResultWindow(QWidget):
    """
    A QWidget class to display the results of a linear regression analysis.

    Attributes:
        data (pd.DataFrame): Dataset used for regression analysis.
        input_columns (list): List of input column names.
        output_column (str): Name of the output column.
        model: Generated regression model.
        formula (str): Generated regression formula.
        mse (float): Mean Squared Error of the model.
        r_squared (float): Coefficient of determination of the model.
        graph (matplotlib.figure.Figure): Graph of the model.
    """

    def __init__(self, data, input_columns, output_column):
        """
        Initialize the ResultWindow with data, input, and output columns.

        Args:
            data (pd.DataFrame): Dataset used for regression analysis.
            input_columns (list): List of input column names.
            output_column (str): Name of the output column.
        """
        super().__init__()

        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.model = None  # Regression model
        self.formula = None
        self.mse = None
        self.r_squared = None
        self.graph = None  # Stores the generated graph
        self.initUI()

    def initUI(self):
        """
        Configures the user interface for the results window.
        """
        vertical_layout = QVBoxLayout()
        self.button = ButtonHelper()

        # Text.
        self.result_label = LabelHelper.create_label(
            parent=self,
            text="Model Description:",
            font=("Arial", 9),
            alignment=Qt.AlignLeft
        )

        # Description text box.
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Write your description here...")

        # Group for the graph.
        graph_group = QGroupBox("Regression Graph")
        self.graph_layout = QVBoxLayout()
        graph_group.setLayout(self.graph_layout)

        # Group for the formula and metrics.
        formula_group = QGroupBox("Model Formula and Metrics")
        formula_layout = QVBoxLayout()
        self.formula_label = LabelHelper.create_label(
            parent=self,
            font=("Arial", 9),
            alignment=Qt.AlignLeft,
            visible=True
        )
        formula_layout.addWidget(self.formula_label)
        formula_group.setLayout(formula_layout)

        # Input box for user entry.
        self.prediction_input = QLineEdit()
        self.prediction_input.setPlaceholderText("Enter a numeric value")
        self.prediction_input.setFixedHeight(30)
        self.prediction_input.setStyleSheet("padding: 5px; font-size: 12px;")

        # Output box for predicted value.
        self.predicted_value_output = QLineEdit()
        self.predicted_value_output.setPlaceholderText(
            "The result will appear here")
        self.predicted_value_output.setFixedHeight(30)
        self.predicted_value_output.setReadOnly(True)
        self.predicted_value_output.setStyleSheet(
            "padding: 5px; font-size: 12px; color: gray; font-weight: bold;"
        )

        # Add prediction button.
        self.predict_button = self.button.add_QPushButton(
            "📊 Prediction",
            "Arial Black",
            12,
            262,
            None,
            True,
            background_color="blue",
            color="white",
            padding="10px"
        )
        self.button.set_QPushButton_hoverStyle(
            self.predict_button, "darkblue", "lightgrey"
        )
        self.predict_button.clicked.connect(self.handle_prediction)

        # Save model button.
        self.save_button = QPushButton("💾 Save Model")
        self.save_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #007BFF;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
                color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #003f7f;
            }
        """)
        self.save_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.save_button.clicked.connect(self.save_model)

        # Add components to the main layout.
        vertical_layout.addWidget(self.text_box)
        vertical_layout.addWidget(graph_group)
        vertical_layout.addWidget(formula_group)
        vertical_layout.addWidget(self.prediction_input)
        vertical_layout.addWidget(self.predict_button)
        vertical_layout.addWidget(self.predicted_value_output)
        vertical_layout.addWidget(self.save_button)

        self.setLayout(vertical_layout)
        self.setWindowTitle("Results")
        self.setMinimumSize(800, 600)

        self.display_results()

    def display_results(self):
        """
        Executes linear regression, displays the formula and metrics,
        and generates a regression graph if applicable.
        """
        # Run regression and get results.
        (
            formula,
            mse,
            r2,
            x_test,
            y_test,
            predictions,
            model
        ) = linear_regression(
            self.data,
            self.input_columns,
            self.output_column
        )

        # Save model to make predictions
        self.model = model

        self.formula = formula
        self.mse = mse
        self.r_squared = r2

        # Display formula and metrics.
        self.formula_label.setText(f"{formula}\nMSE: {mse:.2f}\nR^2: {r2:.2f}")

        # Generate and display the graph.
        if len(self.input_columns) == 1:
            self.graph = plot_regression_graph(y_test, predictions)
            self.canvas = FigureCanvas(self.graph)
            self.graph_layout.addWidget(self.canvas)
        else:
            # Notify the user that the graph cannot be displayed.
            QMessageBox.warning(
                self,
                "Warning",
                "Cannot generate the graph because there are multiple inputs."
            )

    def save_model(self):
        """
        Handles the click event of the "Save Model" button.
        """
        description = self.text_box.toPlainText()

        # Create and invoke ModelSaver.
        model_saver = ModelSaver(
            model=self.model,
            formula=self.formula,
            r_squared=self.r_squared,
            mse=self.mse,
            input_columns=self.input_columns,
            output_column=self.output_column,
            description=description,
            graph=self.graph
        )
        model_saver.save_model_dialog()

    def handle_prediction(self):
        """
        Handles the prediction when the prediction button is clicked.
        """
        try:
            # Retrieve user-entered values from QLineEdit.
            input_text = self.prediction_input.text()
            input_values = input_text.split(",")

            # Validate that the number of values matches input columns.
            if len(input_values) != len(self.input_columns):
                self.predicted_value_output.setStyleSheet(
                    "color: red; font-weight: bold;"
                )
                error_message = (
                    f"Error: You must enter exactly {len(self.input_columns)} "
                    "values separated by commas."
                )
                self.predicted_value_output.setText(error_message)
                return

            # Validate that all values are numeric.
            try:
                input_values = [float(value.strip()) for value in input_values]
            except ValueError:
                self.predicted_value_output.setStyleSheet(
                    "color: red; font-weight: bold;"
                )
                self.predicted_value_output.setText(
                    "Error: Please enter only numeric values."
                )
                return

            # Create a DataFrame with input column names.
            input_df = pd.DataFrame([input_values], columns=self.input_columns)

            # Check if the model exists.
            if not hasattr(self, "model") or self.model is None:
                self.predicted_value_output.setStyleSheet(
                    "color: red; font-weight: bold;"
                )
                self.predicted_value_output.setText(
                    "Error: The model is not available."
                )
                return

            # Perform prediction.
            predicted_value = self.model.predict(input_df)[0]

            # Display the result in the output QLineEdit in green.
            self.predicted_value_output.setStyleSheet(
                "color: green; font-weight: bold;"
            )
            self.predicted_value_output.setText(f"{predicted_value:.2f}")

        except Exception as e:
            # Display any other errors in the output QLineEdit in red.
            self.predicted_value_output.setStyleSheet(
                "color: red; font-weight: bold;"
            )
            self.predicted_value_output.setText(f"Error: {str(e)}")
