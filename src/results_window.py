import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from scikit_learn import regresion_lineal, mostrar_grafica_regresion


class ResultWindow(QWidget):
    def __init__(self, data, columnas_entrada, columna_salida):
        super().__init__()
        self.data = data
        self.columnas_entrada = columnas_entrada
        self.columna_salida = columna_salida
        self.model = None  # Modelo de regresión
        self.initUI()

    def initUI(self):
        vertical_layout = QVBoxLayout()

        # Texto descriptivo
        self.result_label = QLabel("Descripción de mi modelo:")
        self.result_label.setFont(QFont("Arial", 9))
        # Descripción del usuario
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Escriba aquí su descripción...")

        # Gráfica
        graph_group = QGroupBox("Gráfica de Regresión")
        self.graph_layout = QVBoxLayout()
        graph_group.setLayout(self.graph_layout)

        # Fórmula y métricas
        formula_group = QGroupBox("Fórmula del Modelo y Métricas")
        formula_layout = QVBoxLayout()
        self.formula_label = QLabel()
        self.formula_label.setFont(QFont("Arial", 9))
        formula_layout.addWidget(self.formula_label)
        formula_group.setLayout(formula_layout)

        # Entrada y predicción
        prediction_group = QGroupBox("Realizar Predicción")
        prediction_layout = QVBoxLayout()

        self.prediction_input = QLineEdit(self)
        self.prediction_input.setPlaceholderText("Introduce un valor para predecir")
        prediction_layout.addWidget(self.prediction_input)

        self.predict_button = QPushButton("📊 Predecir", self)
        self.predict_button.setFont(QFont("Arial Black", 10))
        self.predict_button.clicked.connect(self.perform_prediction)
        prediction_layout.addWidget(self.predict_button)

        self.prediction_result_label = QLabel("Resultado: ", self)
        self.prediction_result_label.setFont(QFont("Arial Black", 12))
        self.prediction_result_label.setVisible(False)
        prediction_layout.addWidget(self.prediction_result_label)

        prediction_group.setLayout(prediction_layout)

        # Añadir componentes al diseño principal
        vertical_layout.addWidget(self.result_label)
        vertical_layout.addWidget(self.text_box)
        vertical_layout.addWidget(graph_group)
        vertical_layout.addWidget(formula_group)
        vertical_layout.addWidget(prediction_group)

        self.setLayout(vertical_layout)
        self.setWindowTitle("Results")
        self.setMinimumSize(800, 600)

        self.display_results()

    def display_results(self):
        # Ejecutar regresión y obtener resultados
        formula, mse, r2, x_test, y_test, predictions, model = regresion_lineal(
            self.data, self.columnas_entrada, self.columna_salida
        )

        self.model = model
        self.mse = mse
        self.r_squared = r2

        # Mostrar fórmula y métricas
        self.formula_label.setText(f"{formula}\nMSE: {mse:.2f}\nR^2: {r2:.2f}")

        # Generar y mostrar la gráfica
        if len(self.columnas_entrada) == 1:
            fig = mostrar_grafica_regresion(y_test, predictions)
            self.canvas = FigureCanvas(fig)
            self.graph_layout.addWidget(self.canvas)
        else:
            # Notificar al usuario que no se puede mostrar la gráfica
            QMessageBox.warning(self, "Warning", "Cannot generate the graph because there are multiple input features.")

    def perform_prediction(self):
        """
        Realiza una predicción utilizando el modelo generado.
        """
        try:
            input_value = float(self.prediction_input.text())  # Convertir entrada a flotante
            prediction = self.model.predict([[input_value]])[0]  # Realizar la predicción
            self.prediction_result_label.setText(f"Resultado: {prediction:.2f}")
            self.prediction_result_label.setVisible(True)  # Mostrar el resultado
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "Por favor, introduce un valor numérico válido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error durante la predicción: {str(e)}")

