from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QGroupBox, QMessageBox, QLabel, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QGroupBox, QMessageBox, QLineEdit
)
import pandas as pd
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from scikit_learn import linear_regression, plot_regression_graph
from model_saver import ModelSaver
from helpers import LabelHelper, ButtonHelper


class ResultWindow(QWidget):
    """
    Una clase QWidget para mostrar los resultados de un análisis de regresión lineal.
    
    Atributos:
        data (pd.DataFrame): Dataset utilizado para el análisis de regresión.
        columnas_entrada (list): Lista de nombres de columnas de entrada.
        columna_salida (str): Nombre de la columna de salida.
        model: Modelo de regresión generado.
        formula (str): Fórmula de regresión generada.
        mse (float): Error cuadrático medio del modelo.
        r_squared (float): Coeficiente de determinación del modelo.
        graph (matplotlib.figure.Figure): Gráfica del modelo.
    """
    def __init__(self, data, columnas_entrada, columna_salida):
        super().__init__()
        
        self.data = data
        self.columnas_entrada = columnas_entrada
        self.columna_salida = columna_salida
        self.model = None  # Modelo de regresión
        self.formula = None
        self.mse = None
        self.r_squared = None
        self.graph = None  # Almacena la gráfica generada
        self.initUI()

    def initUI(self):
        """
        Configura la interfaz de usuario para la ventana de resultados.
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

        # Grupo para la gráfica
        graph_group = QGroupBox("Gráfica de Regresión")
        self.graph_layout = QVBoxLayout()
        graph_group.setLayout(self.graph_layout)

        # Grupo para la fórmula y métricas
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
        self.predicted_value_output.setStyleSheet("padding: 5px; font-size: 12px; color: gray; font-weight: bold;")
        
        # Add prediction's button
        self.predict_button = self.button.add_QPushButton("📊 Prediction",
        "Arial Black",12,262,None,True,
        background_color="blue",color="white",padding="10px")
        self.button.set_QPushButton_hoverStyle(self.predict_button,"darkblue","lightgrey")
        self.predict_button.clicked.connect(self.handle_prediction)
        
        # Botón para guardar el modelo
        self.save_button = QPushButton("💾 Guardar Modelo")
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

        # Añadir componentes al diseño principal
        vertical_layout.addWidget(self.text_box)
        vertical_layout.addWidget(graph_group)
        vertical_layout.addWidget(formula_group)
        vertical_layout.addWidget(self.prediction_input)
        vertical_layout.addWidget(self.predict_button)
        vertical_layout.addWidget(self.predicted_value_output)
        vertical_layout.addWidget(self.save_button)

        self.setLayout(vertical_layout)
        self.setWindowTitle("Resultados")
        self.setMinimumSize(800, 600)

        self.display_results()

    def display_results(self):
        """
        Ejecuta la regresión lineal, muestra la fórmula y las métricas,
        y genera una gráfica de regresión si es aplicable.
        """
        # Run regression and get results.
        formula, mse, r2, x_test, y_test, predictions, model = linear_regression(
            self.data, self.columnas_entrada, self.columna_salida
        )
        
        # Save model to make predictions
        self.model = model
        
        self.formula = formula
        self.mse = mse
        self.r_squared = r2

        # Mostrar fórmula y métricas
        self.formula_label.setText(f"{formula}\nMSE: {mse:.2f}\nR^2: {r2:.2f}")
        
        # Generate and display the graph.
        if len(self.columnas_entrada) == 1:
            self.graph = plot_regression_graph(y_test, predictions)
            self.canvas = FigureCanvas(self.graph)
            self.graph_layout.addWidget(self.canvas)
        else:
            # Notificar al usuario que no se puede mostrar la gráfica
            QMessageBox.warning(
                self,
                "Advertencia",
                "No se puede generar la gráfica porque hay múltiples variables de entrada."
            )

    def save_model(self):
        """
        Maneja el evento de clic del botón "Guardar Modelo".
        """
        description = self.text_box.toPlainText()
        
        # Crear e invocar ModelSaver
        model_saver = ModelSaver(
            model=self.model,
            formula=self.formula,
            r_squared=self.r_squared,
            mse=self.mse,
            input_columns=self.columnas_entrada,
            output_column=self.columna_salida,
            description=description,
            graph=self.graph  # Pasar la gráfica generada
        )
        model_saver.save_model_dialog()

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
