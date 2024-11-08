import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont   
from PyQt5.QtCore import Qt
from scikit_learn import regresion_lineal,mostrar_grafica_regresion


class ResultWindow(QWidget):
    def __init__(self,data,columnas_entrada,columna_salida):
        super().__init__()
        self.data = data
        self.columnas_entrada = columnas_entrada
        self.columna_salida = columna_salida
        self.initUI()

    def initUI(self):

        vertical_layout = QVBoxLayout()

        # Text
        self.result_label = QLabel("Descripción de mi modelo:")
        self.result_label.setFont(QFont("Arial",9))
        # Descripcion del ususario
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Escriba aquí su descripción...")

        # Graphic
        graph_group = QGroupBox("Gráfica de Regresión")
        self.graph_layout = QVBoxLayout()
        graph_group.setLayout(self.graph_layout)
        
        # Formula 
        formula_group = QGroupBox("Fórmula del Modelo y Métricas")
        formula_layout = QVBoxLayout()
        
        self.formula_label = QLabel()
        self.formula_label.setFont(QFont("Arial", 9))
        formula_layout.addWidget(self.formula_label)
        formula_group.setLayout(formula_layout)

        vertical_layout.addWidget(self.result_label)
        vertical_layout.addWidget(self.text_box)
        vertical_layout.addWidget(graph_group)
        vertical_layout.addWidget(formula_group)        

        self.setLayout(vertical_layout)
        self.setWindowTitle("Results")
        self.setMinimumSize(800,600)

        self.display_results()

    
    def display_results(self):
        # Run regression and get results
        formula, mse, r2, x_test, y_test, predictions = regresion_lineal(self.data, self.columnas_entrada, self.columna_salida)

        # Display formula and metrics
        self.formula_label.setText(f"{formula}\nMSE: {mse:.2f}\nR^2: {r2:.2f}")

        # Generate and display the graph
        if len(self.columnas_entrada) == 1:
            fig = mostrar_grafica_regresion(y_test, predictions)
            self.canvas = FigureCanvas(fig)
            self.graph_layout.addWidget(self.canvas)
        else:
            # Notify user that graph cannot be displayed
            QMessageBox.warning(self, "Warning", "Cannot generate the graph because there are multiple input features.")
