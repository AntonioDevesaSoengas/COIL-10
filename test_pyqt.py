import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
import sqlite3

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

    def open_file_dialog(self):
        # Abrir el explorador de archivos con filtro
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo", "",
                                                   "Archivos CSV (*.csv);;Archivos Excel (*.xlsx *.xls);;Bases de datos SQLite (*.sqlite *.db)", options=options)
        if file_path:  # Asegurarse de que el archivo haya sido seleccionado
            self.file_label.setText(f'Archivo cargado: {file_path}')
            try:
                # Cargar y visualizar el dataset
                self.load_data(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {str(e)}")

    def load_data(self, file_path):
        # Detectar tipo de archivo y cargar datos
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(file_path)
        elif file_path.endswith(('.sqlite', '.db')):
            # Conectar y cargar la primera tabla desde la base de datos SQLite
            conn = sqlite3.connect(file_path)
            query = "SELECT name FROM sqlite_master WHERE type='table' LIMIT 1;"
            table_name = pd.read_sql_query(query, conn)['name'][0]  # Obtener la primera tabla
            data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)  # Cargar los datos de la primera tabla
            conn.close()
        else:
            raise ValueError("Formato de archivo no soportado.")

        # Mostrar los datos en la tabla
        self.display_data_in_table(data)

    def display_data_in_table(self, data):
        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(data.columns))
        self.data_table.setHorizontalHeaderLabels(data.columns)

        for i, row in data.iterrows():
            for j, value in enumerate(row):
                self.data_table.setItem(i, j, QTableWidgetItem(str(value)))

        # Ajustar tamaño de columnas
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DataViewer()
    viewer.show()
    sys.exit(app.exec_())
