import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QSpacerItem, QLabel, QTableView, QRadioButton,
    QListWidget, QAbstractItemView, QPushButton,
    QFileDialog, QHeaderView, QStackedWidget,QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from import_files import import_data
from data_preprocessing import *
from table import Table
from buttons import Button
from helpers import LabelHelper
from welcome_window import WelcomeWindow
from layouts import Layout
from data_preprocessing import *


class PreProcessing(QWidget):
    def __init__(self):
        super().__init__()
        self.df = None
        self.label = LabelHelper()
        self.layout = Layout()
        self.button = Button()

        self.nan_layout = QVBoxLayout()
        # Button for detecting non-existent values
        self.detect_button = self.button.add_QPushButton(text="🔍 Detectar", font_type="Arial", font_size=10, width=None,
                                                         height=None)
        self.detect_button.clicked.connect(self.handle_detect_missing_values)

        # Tabla para mostrar los datos preprocesados
        self.table_view = QTableView()
        self.table_view.setFont(QFont("Arial", 10))
        self.table_view.setVisible(False)

        # Drop-down menu for pre-processing options
        items = ["🗑️ Eliminar Filas con Valores Inexistentes", "📊 Rellenar con la Media", "📊 Rellenar con la Mediana",
                 "✏️ Rellenar con un Valor Constante"]
        self.preprocessing_options = self.button.add_QComboBox(
            items, None, None, True)

        # Confirmation button to apply pre-processing
        self.apply_button = self.button.add_QPushButton(text="🟢 Aplicar Preprocesado", font_type="Arial Black", font_size=8,
                                                        width=None, height=None)
        self.apply_button.clicked.connect(self.confirm_preprocessing)
        widgets = [self.detect_button,self.preprocessing_options,self.apply_button, self.table_view]
        self.layout.add_Widget(self.nan_layout,widgets)
        self.setLayout(self.nan_layout)


        # Preprocessing function to detect Non-existent Values
    def handle_detect_missing_values(self):
        if self.df is not None:
            message = detect_missing_values(self.df)
            QMessageBox.information(
                self, "Detección de Valores Inexistentes", message)
            

    def set_dataframe(self, dataframe):
        """Método para recibir el DataFrame desde la clase principal."""
        if dataframe is not None:
            self.df = dataframe.copy()  # Copiar para evitar modificaciones no deseadas
            self.display_data_in_table()
            QMessageBox.information(
                self,
                "Datos Cargados",
                "Los datos se han cargado correctamente y están listos para preprocesar."
            )
        else:
            QMessageBox.warning(
                self,
                "Advertencia",
                "El DataFrame recibido es None."
            )

    # Apply the selected pre-processing option in the ComboBox
    def confirm_preprocessing(self):
        option = self.preprocessing_options.currentText()
        if not option:
            QMessageBox.warning(
                self, "Advertencia", "Debes seleccionar una opción de preprocesado antes de confirmar.")
            return

        try:
            if option == "🗑️ Eliminar Filas con Valores Inexistentes":
                remove_missing_values(self)
            elif option == "📊 Rellenar con la Media":
                fill_with_mean(self)
            elif option == "📊 Rellenar con la Mediana":
                fill_with_median(self)
            elif option == "✏️ Rellenar con un Valor Constante":
                fill_with_constant(self)

            # Redisplay the table after preprocessing
            # Make sure the table is updated with the new content

            QMessageBox.information(
                self, "Éxito", "Preprocesado aplicado con éxito.")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error al aplicar el preprocesado: {str(e)}")
            
    def display_data_in_table(self):
        if self.df is not None:
            self.data_table = Table(self.df)
            self.table_view.setModel(self.data_table)
            self.table_view.setVisible(True)
            self.table_view.resizeColumnsToContents()
            self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            if self.width() > 1000:
                self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)