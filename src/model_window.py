from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QTextEdit, QWidget, QGroupBox, QLineEdit
from PyQt5.QtCore import Qt
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from helpers import ButtonHelper

class ModelWindow(QMainWindow):
    def __init__(self, model_data, columnas_entrada):
        super().__init__()
        self.setWindowTitle("Model Details")
        self.setGeometry(100, 100, 800, 600)  # Adjusted size for better visualization
        self.model = model_data.get('model', None)
        self.columnas_entrada = columnas_entrada
        
        # Main layout
        layout = QVBoxLayout()
        self.button = ButtonHelper()
        
        # Description section
        description_group = QGroupBox("Model Description")
        description_layout = QVBoxLayout()
        description_text = QTextEdit()
        description_text.setText(model_data.get('description', 'No description available.'))
        description_text.setReadOnly(True)
        description_layout.addWidget(description_text)
        description_group.setLayout(description_layout)
        layout.addWidget(description_group)

        # Graph section
        graph_group = QGroupBox("Regression Graph")
        graph_layout = QVBoxLayout()

        # Check if graph data is available
        if 'graph' in model_data and model_data['graph']:
            canvas = FigureCanvas(model_data['graph'])
            graph_layout.addWidget(canvas)
        else:
            graph_label = QLabel("Graph not available.")
            graph_label.setAlignment(Qt.AlignCenter)
            graph_layout.addWidget(graph_label)

        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)

        # Metrics section (Formula, MSE, R²)
        metrics_group = QGroupBox("Model Metrics")
        metrics_layout = QVBoxLayout()

        formula_label = QLabel(f"Formula: {model_data.get('formula', 'N/A')}")
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
        self.predicted_value_output.setStyleSheet("padding: 5px; font-size: 12px; color: gray; font-weight: bold;")
        
        # Add prediction's button
        self.predict_button = self.button.add_QPushButton("📊 Prediction",
        "Arial Black",12,262,None,True,
        background_color="blue",color="white",padding="10px")
        self.button.set_QPushButton_hoverStyle(self.predict_button,"darkblue","lightgrey")
        self.predict_button.clicked.connect(self.handle_prediction)
        
        layout.addWidget(self.prediction_input)
        layout.addWidget(self.predict_button)
        layout.addWidget(self.predicted_value_output)

        # Main container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
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
                self.predicted_value_output.setStyleSheet("color: red; font-weight: bold;")  # Mensajes en rojo
                self.predicted_value_output.setText(
                    f"Error: Debe ingresar exactamente {len(self.columnas_entrada)} valores separados por comas."
                )
                return

            # Validar que todos los valores sean numéricos
            try:
                input_values = [float(value.strip()) for value in input_values]
            except ValueError:
                self.predicted_value_output.setStyleSheet("color: red; font-weight: bold;")  # Mensajes en rojo
                self.predicted_value_output.setText("Error: Por favor, ingrese solo valores numéricos.")
                return

            # Crear un DataFrame con los nombres de las columnas de entrada
            input_df = pd.DataFrame([input_values], columns=self.columnas_entrada)

            # Verificar que el modelo existe
            if not hasattr(self, "model") or self.model is None:
                self.predicted_value_output.setStyleSheet("color: red; font-weight: bold;")  # Mensajes en rojo
                self.predicted_value_output.setText("Error: El modelo no está disponible.")
                return

            # Realizar la predicción
            predicted_value = self.model.predict(input_df)[0]

            # Mostrar el resultado en el QLineEdit de salida en verde
            self.predicted_value_output.setStyleSheet("color: green; font-weight: bold;")  # Mensajes en verde
            self.predicted_value_output.setText(f"{predicted_value:.2f}")

        except Exception as e:
            # Mostrar cualquier otro error en el QLineEdit de salida en rojo
            self.predicted_value_output.setStyleSheet("color: red; font-weight: bold;")
            self.predicted_value_output.setText(f"Error: {str(e)}")

