import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog
from import_files import import_data

class DataViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout()

        # Botón para cargar archivo
        self.load_button = QPushButton('Cargar Dataset', self)
        self.load_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.load_button)

        # Botón para ir hacia atrás y elegir otro archivo
        self.back_button = QPushButton('Elegir otro archivo', self)
        self.back_button.clicked.connect(self.clear_table_and_choose_file)
        self.back_button.setVisible(False)
        layout.addWidget(self.back_button)

        # Etiqueta para mostrar la ruta del archivo cargado
        self.file_label = QLabel('Ruta del archivo cargado:')
        layout.addWidget(self.file_label)

        # Tabla para mostrar los datos
        self.data_table = QTableWidget()
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        layout.addWidget(self.data_table)

        # Configurar layout
        self.setLayout(layout)
        self.setWindowTitle('Visualizador de Datasets')
        self.resize(800, 600)  # Tamaño de la ventana ajustado

    def open_file_dialog(self):
        # Abrir el explorador de archivos con QFileDialog de PyQt5
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo", "", 
                                                   "Archivos CSV (*.csv);;Archivos Excel (*.xlsx *.xls);;Bases de datos SQLite (*.sqlite *.db)")
        if file_path:
            self.file_label.setText(f'Archivo cargado: {file_path}')
            self.load_data(file_path)
            self.back_button.setVisible(True)  # Mostrar el botón una vez cargado el archivo

    def load_data(self, file_path):
        try:
            # Llamamos a import_data y obtenemos el DataFrame
            data = import_data(file_path)

            if data is not None:
                self.display_data_in_table(data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {str(e)}")

    def display_data_in_table(self, data):
        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(data.columns))
        self.data_table.setHorizontalHeaderLabels(data.columns)

        for i, row in data.iterrows():
            for j, value in enumerate(row):
                self.data_table.setItem(i, j, QTableWidgetItem(str(value)))
        # Ajustar tamaño de columnas
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def clear_table_and_choose_file(self):
        self.data_table.clear()
        self.file_label.setText('Ruta del archivo cargado:')
        self.open_file_dialog()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DataViewer()
    viewer.show()
    sys.exit(app.exec_())

