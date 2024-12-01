# Third-party libraries.
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QWidget,
    QGroupBox,
    QLineEdit
)
from PyQt5.QtCore import Qt
import pandas as pd
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas
)

# Local libraries.
from helpers import ButtonHelper


class ModelWindow(QMainWindow):
    """
    A window to display model details, description, graph, and predictions.

    Attributes:
        model: The linear regression model.
        input_columns (list): List of input feature column names.
    """

    def __init__(self, model_data, input_columns):
        super().__init__()
        self.setWindowTitle("Model Details")
        self.setGeometry(100, 100, 800, 600)
        self.model = model_data.get('model', None)
        self.input_columns = input_columns

        # Main layout.
        layout = QVBoxLayout()
        self.button = ButtonHelper()

        # Description section.
        description_group = QGroupBox("Model Description")
        description_layout = QVBoxLayout()
        description_text = QTextEdit()
        description_text.setText(
            model_data.get('description', 'No description available.')
        )
        description_text.setReadOnly(True)
        description_layout.addWidget(description_text)
        description_group.setLayout(description_layout)
        layout.addWidget(description_group)

        # Graph section.
        graph_group = QGroupBox("Regression Graph")
        graph_layout = QVBoxLayout()

        # Check if graph data is available.
        if 'graph' in model_data and model_data['graph']:
            canvas = FigureCanvas(model_data['graph'])
            graph_layout.addWidget(canvas)
        else:
            graph_label = QLabel("Graph not available.")
            graph_label.setAlignment(Qt.AlignCenter)
            graph_layout.addWidget(graph_label)

        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)

        # Metrics section (Formula, MSE, R²).
        metrics_group = QGroupBox("Model Metrics")
        metrics_layout = QVBoxLayout()

        formula_label = QLabel(
            f"Formula: {model_data.get('formula', 'N/A')}"
        )
        formula_label.setAlignment(Qt.AlignLeft)
        metrics_layout.addWidget(formula_label)

        mse_label = QLabel(f"MSE: {model_data.get('mse', 'N/A')}")
        mse_label.setAlignment(Qt.AlignLeft)
        metrics_layout.addWidget(mse_label)

        r_squared_label = QLabel(f"R²: {model_data.get('r_squared', 'N/A')}")
        r_squared_label.setAlignment(Qt.AlignLeft)
        metrics_layout.addWidget(r_squared_label)

        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)

        # Input box for user entry.
        self.prediction_input = QLineEdit()
        self.prediction_input.setPlaceholderText("Enter a numeric value")
        self.prediction_input.setFixedHeight(30)  # Reduced size
        self.prediction_input.setStyleSheet(
            "padding: 5px; font-size: 12px;"
        )

        # Output box for predicted value.
        self.predicted_value_output = QLineEdit()
        self.predicted_value_output.setPlaceholderText(
            "The result will appear here"
        )
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

        layout.addWidget(self.prediction_input)
        layout.addWidget(self.predict_button)
        layout.addWidget(self.predicted_value_output)

        # Main container.
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_prediction(self):
        """
        Handle the prediction when the prediction button is clicked.

        This method retrieves user input, validates it, performs prediction
        using the model, and displays the result or error messages.
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
                self.predicted_value_output.setText(
                    f"Error: You must enter exactly {len(self.input_columns)} values separated by commas."
                )
                return

            # Validate that all values are numeric.
            try:
                input_values = [
                    float(value.strip()) for value in input_values
                ]
            except ValueError:
                self.predicted_value_output.setStyleSheet(
                    "color: red; font-weight: bold;"
                )  
                self.predicted_value_output.setText(
                    "Error: Please enter only numeric values."
                )
                return

            # Create a DataFrame with input column names.
            input_df = pd.DataFrame(
                [input_values], columns=self.input_columns
            )

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
