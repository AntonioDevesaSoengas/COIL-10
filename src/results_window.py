# Standard libraries.
import sys

# Third-party libraries.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QGroupBox, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Local libraries.
from scikit_learn import linear_regression, plot_regression_graph
from helpers import LabelHelper


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
            alignment=Qt.AlignLeft
        )
        formula_layout.addWidget(self.formula_label)
        formula_group.setLayout(formula_layout)

        # Add widgets to the main layout.
        vertical_layout.addWidget(self.result_label)
        vertical_layout.addWidget(self.text_box)
        vertical_layout.addWidget(graph_group)
        vertical_layout.addWidget(formula_group)

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
        formula, mse, r2, x_test, y_test, predictions = linear_regression(
            self.data, self.columnas_entrada, self.columna_salida
        )

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
