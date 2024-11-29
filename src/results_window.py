# Standard libraries.
import sys

# Third-party libraries.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QGroupBox, QMessageBox, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Local libraries.
from scikit_learn import linear_regression, plot_regression_graph
from helpers import LabelHelper, ButtonHelper

class ResultWindow(QWidget):
    """
    A QWidget-based class to display the results of a linear regression analysis.

    Attributes:
        data (pd.DataFrame): The dataset used for regression analysis.
        columnas_entrada (list): List of input feature column names.
        columna_salida (str): Output feature column name.
        result_label (QLabel): Label to describe the results.
        text_box (QTextEdit): Text area for user to input descriptions.
        formula_label (QLabel): Label to display the regression formula and metrics.
        canvas (FigureCanvas): Canvas to display the regression graph.
    """

    def __init__(self, data, columnas_entrada, columna_salida):
        """
        Initialize the ResultWindow with the dataset and selected features.

        Args:
            data (pd.DataFrame): The dataset to be used for regression.
            columnas_entrada (list): The input features for regression.
            columna_salida (str): The target output feature.
        """
        super().__init__()
        
        self.data = data
        self.columnas_entrada = columnas_entrada
        self.columna_salida = columna_salida
        self.initUI()

    def initUI(self):
        """
        Set up the user interface for the ResultWindow.
        """
        vertical_layout = QVBoxLayout()
        self.button = ButtonHelper()

        # Text.
        self.result_label = LabelHelper.create_label(
            parent=self,
            text="Descripción de mi modelo:",
            font=("Arial", 9),
            alignment=Qt.AlignLeft
        )

        # Description text box.
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Escriba aquí su descripción...")

        # Graph group.
        graph_group = QGroupBox("Gráfica de Regresión")
        self.graph_layout = QVBoxLayout()
        graph_group.setLayout(self.graph_layout)

        # Formula group.
        formula_group = QGroupBox("Fórmula del Modelo y Métricas")
        formula_layout = QVBoxLayout()
        self.formula_label = LabelHelper.create_label(
            parent=self,
            font=("Arial", 9),
            alignment=Qt.AlignLeft,
            visible=True
        )
        formula_layout.addWidget(self.formula_label)
        formula_group.setLayout(formula_layout)

        # Box for the value to be entered by user
        self.prediction_input = QLineEdit()
        self.prediction_input.setPlaceholderText("Introduzca un valor numérico")
        self.prediction_input.setFixedHeight(30)  # Reducimos el tamaño
        self.prediction_input.setStyleSheet("padding: 5px; font-size: 12px;")
        
        # Box for the predicted value
        self.predicted_value_output = QLineEdit()
        self.predicted_value_output.setPlaceholderText("El resultado aparecerá aquí")
        self.predicted_value_output.setFixedHeight(30)  # Ajustar tamaño
        self.predicted_value_output.setReadOnly(True)  # Hacer que sea solo lectura
        self.predicted_value_output.setStyleSheet("padding: 5px; font-size: 12px; color: green; font-weight: bold;")
        
        # Add prediction's button
        self.predict_button = self.button.add_QPushButton("📊 Prediction",
        "Arial Black",12,262,None,True,
        background_color="blue",color="white",padding="10px")
        self.button.set_QPushButton_hoverStyle(self.predict_button,"darkblue","lightgrey")
        self.predict_button.clicked.connect(self.handle_prediction)
        
        # Add widgets to the main layout.
        vertical_layout.addWidget(self.result_label)
        vertical_layout.addWidget(self.text_box)
        vertical_layout.addWidget(graph_group)
        vertical_layout.addWidget(formula_group)
        vertical_layout.addWidget(self.prediction_input)
        vertical_layout.addWidget(self.predict_button)
        vertical_layout.addWidget(self.predicted_value_output)

        self.setLayout(vertical_layout)
        self.setWindowTitle("Results")
        self.setMinimumSize(800, 600)

        # Display results after UI setup.
        self.display_results()

    def display_results(self):
        """
        Perform linear regression, display the formula and metrics,
        and generate a regression graph if applicable.
        """
        # Run regression and get results.
        formula, mse, r2, x_test, y_test, predictions, model = linear_regression(
            self.data, self.columnas_entrada, self.columna_salida
        )
        
        # Save model to make predictions
        self.model = model
        
        # Display formula and metrics.
        self.formula_label.setText(f"{formula}\nMSE: {mse:.2f}\nR^2: {r2:.2f}")
        
        # Generate and display the graph.
        if len(self.columnas_entrada) == 1:
            fig = plot_regression_graph(y_test, predictions)
            self.canvas = FigureCanvas(fig)
            self.graph_layout.addWidget(self.canvas)
        else:
            # Notify user that graph cannot be displayed.
            QMessageBox.warning(
                self,
                "Warning",
                "Cannot generate the graph because there are multiple input features."
            )

    def handle_prediction(self):
        """
        Maneja la predicción al hacer clic en el botón de predicción.
        """
        try:
            # Recuperar los valores ingresados por el usuario desde QLineEdit
            input_text = self.prediction_input.text()  # Obtiene el texto del QLineEdit
            input_values = input_text.split(",")  # Divide los valores separados por comas

            # Validar que el número de valores coincida con las columnas de entrada
            if len(input_values) != len(self.columnas_entrada):  # self.columnas_entrada tiene 3 columnas, por ejemplo
                self.predicted_value_output.setText(
                    f"Error: Debe ingresar exactamente {len(self.columnas_entrada)} valores separados por comas."
                )
                return

            # Validar que todos los valores sean numéricos
            try:
                input_values = [float(value.strip()) for value in input_values]
            except ValueError:
                self.predicted_value_output.setText("Error: Por favor, ingrese solo valores numéricos.")
                return

            # Verificar que el modelo existe
            if not hasattr(self, "model") or self.model is None:
                self.predicted_value_output.setText("Error: El modelo no está disponible.")
                return

            # Realizar la predicción
            predicted_value = self.model.predict([input_values])[0]

            # Mostrar el resultado en el QLineEdit de salida
            self.predicted_value_output.setText(f"{predicted_value:.2f}")

        except Exception as e:
            # Mostrar cualquier otro error en el QLineEdit de salida
            self.predicted_value_output.setText(f"Error: {str(e)}")