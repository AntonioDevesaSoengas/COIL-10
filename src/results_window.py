from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QGroupBox, QMessageBox, QLabel, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from scikit_learn import linear_regression, plot_regression_graph
from model_saver import ModelSaver

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

        # Cuadro de texto para la descripción del modelo
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Escriba aquí su descripción...")

        # Grupo para la gráfica
        graph_group = QGroupBox("Gráfica de Regresión")
        self.graph_layout = QVBoxLayout()
        graph_group.setLayout(self.graph_layout)

        # Grupo para la fórmula y métricas
        formula_group = QGroupBox("Fórmula del Modelo y Métricas")
        formula_layout = QVBoxLayout()
        self.formula_label = QLabel()
        self.formula_label.setFont(QFont("Arial", 9))
        formula_layout.addWidget(self.formula_label)
        formula_group.setLayout(formula_layout)

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
        # Ejecutar regresión y obtener resultados
        formula, mse, r2, x_test, y_test, predictions = linear_regression(
            self.data, self.columnas_entrada, self.columna_salida
        )

        self.formula = formula
        self.mse = mse
        self.r_squared = r2

        # Mostrar fórmula y métricas
        self.formula_label.setText(f"{formula}\nMSE: {mse:.2f}\nR^2: {r2:.2f}")

        # Generar y mostrar la gráfica
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
