import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QSpacerItem, QLabel, QTableView, QRadioButton,
    QListWidget, QAbstractItemView, QPushButton,
    QFileDialog, QHeaderView, QStackedWidget,QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from helpers import LabelHelper
from layouts import Layout
from buttons import Button
from table import Table
from import_files import import_data



class LoadData(QWidget):
    def __init__(self,on_data_loaded):
        super().__init__()

        self.on_data_loaded = on_data_loaded  # Callback para cuando los datos se cargan

        self.label = LabelHelper()
        self.layout = Layout()
        self.button = Button()
        self.last_file_path = None
        self.data_table = None
        self.df = None

        self.first_step_layout = QVBoxLayout()
        # Botón para cargar archivo
        self.load_button = self.button.add_QPushButton(text='📂 Cargar Dataset', font_type="Arial Black",
                                                    font_size=12, width=243, height=None,
                                                    background_color="green", color="white", padding="10px")
        self.button.set_QPushButton_hoverStyle(
            self.load_button, "darkgreen", "lightgrey"
        )
        self.load_button.clicked.connect(self.open_file_dialog)


        # Button to go back and choose another file
        self.back_button = self.button.add_QPushButton(text="🔄️ Elegir otro archivo", font_type="Arial Black", font_size=12,
                                                    width=262, height=None, visibility=False, background_color="orange",
                                                    color="white", padding="10px")
        self.button.set_QPushButton_hoverStyle(
            self.back_button, "darkorange", "lightgrey")
        self.back_button.clicked.connect(self.clear_table_and_choose_file)

        # Label to display the path of the uploaded file
        self.file_label = LabelHelper.create_label(self,
            text="📂 Ruta del archivo cargado:",
            font=("Arial", 10)
        )
        self.file_label.setVisible(False)


        # Table to display data
        self.table_view = QTableView()
        self.table_view.setFont(QFont("Arial", 10))
        self.table_view.setVisible(True)

        items = [self.load_button,self.back_button,self.file_label,self.table_view]
        self.layout.add_Widget(self.first_step_layout,items)
        self.setLayout(self.first_step_layout)
        
        


    def open_file_dialog(self):
        # Open File Explorer with PyQt5's QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo", "",
                                                   "Archivos CSV (*.csv);;Archivos Excel (*.xlsx *.xls);;Bases de datos SQLite (*.sqlite *.db)")
        if file_path:
            if self.last_file_path == file_path:
                # Show message and confirmation options if it's the same file
                result = QMessageBox.question(self, "Advertencia",
                                              "Estás seleccionando el mismo archivo que ya has cargado. ¿Deseas cargarlo de nuevo?",
                                              QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.No:
                    return
                elif result == QMessageBox.Yes:
                    # Reload the dataset directly without opening the browser
                    self.load_data(file_path)

            else:
                self.last_file_path = file_path
                self.file_label.setText(f'📂 Archivo cargado: {file_path}')
                self.load_data(file_path)

    def load_data(self, file_path):
        try:
            self.df = import_data(file_path)
            if self.df is not None and not self.df.empty:
                self.display_data_in_table()
                # Enable buttons if data is loaded correctly
                self.file_label.setText(f'📂 Archivo cargado: {file_path}')
                # Ejecutar el callback si está definido
                if self.on_data_loaded:
                    self.on_data_loaded(self.df)
            else:
                QMessageBox.warning(
                    self, "Advertencia", "El archivo está vacío o no se pudo cargar correctamente.")
        except pd.errors.EmptyDataError:
            QMessageBox.critical(
                self, "Error", "El archivo CSV está vacío. Por favor, selecciona otro archivo.")
        except pd.errors.ParserError:
            QMessageBox.critical(
                self, "Error", "El archivo CSV está corrupto o tiene un formato inválido.")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo cargar el archivo: {str(e)}")

    def display_data_in_table(self):
        self.data_table = Table(self.df)
        self.table_view.setModel(self.data_table)

        # Mostrar únicamente la tabla y elementos relevantes
        self.table_view.setVisible(True)

        # Show file path
        self.file_label.setVisible(True)
        self.load_button.setVisible(False)
        self.back_button.setVisible(True)

        # Adjust Table Size
        self.table_view.resizeColumnsToContents()
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        if self.width() > 1000:
            self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def clear_table_and_choose_file(self):
        # Clean up the table and select a new file
        file_path = self.open_file_dialog()
        if file_path and file_path != self.last_file_path:
            self.data_table.clear()
            self.load_data(file_path)

    def actualizar_datos(self):
        return self.df
    
                

