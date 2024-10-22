import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog, QComboBox

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
        layout.addWidget(self.back_button)

        # Etiqueta para mostrar la ruta del archivo cargado
        self.file_label = QLabel('Ruta del archivo cargado:')
        layout.addWidget(self.file_label)

        # Tabla para mostrar los datos
        self.data_table = QTableWidget()
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        layout.addWidget(self.data_table)

        # Selectores de columnas
        self.feature_selector = QComboBox(self)
        self.feature_selector.setEnabled(False)  # Inicia desactivado hasta que cargues datos
        self.feature_selector.setToolTip("Selecciona las columnas de entrada (features)")
        layout.addWidget(QLabel("Columnas de Entrada (Features)"))
        layout.addWidget(self.feature_selector)

        self.target_selector = QComboBox(self)
        self.target_selector.setEnabled(False)  # Inicia desactivado hasta que cargues datos
        self.target_selector.setToolTip("Selecciona la columna de salida (target)")
        layout.addWidget(QLabel("Columna de Salida (Target)"))
        layout.addWidget(self.target_selector)

        # Botón de confirmación
        self.confirm_button = QPushButton('Confirmar selección', self)
        self.confirm_button.setEnabled(False)  # Se activa solo cuando hay datos cargados
        self.confirm_button.clicked.connect(self.confirm_selection)
        layout.addWidget(self.confirm_button)

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

    def load_data(self, file_path):
        try:
            # Llamamos a import_data y obtenemos el DataFrame
            data = import_data(file_path)

            if data is not None:
                self.display_data_in_table(data)
                self.populate_selectors(data)

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

    def populate_selectors(self, data):
        # Habilitar los selectores y el botón de confirmación
        self.feature_selector.setEnabled(True)
        self.target_selector.setEnabled(True)
        self.confirm_button.setEnabled(True)

        # Limpiar los selectores actuales
        self.feature_selector.clear()
        self.target_selector.clear()

        # Agregar las columnas disponibles
        self.feature_selector.addItems(data.columns)
        self.target_selector.addItems(data.columns)

    def confirm_selection(self):
        # Obtener las selecciones
        selected_features = self.feature_selector.currentText()
        selected_target = self.target_selector.currentText()

        if not selected_features or not selected_target:
            QMessageBox.warning(self, "Selección incompleta", "Debes seleccionar al menos una columna de entrada y una de salida.")
            return

        # Mostrar mensaje de éxito
        QMessageBox.information(self, "Selección confirmada", f"Has seleccionado las columnas de entrada: {selected_features} y la columna de salida: {selected_target}.")

    def clear_table_and_choose_file(self):
        # Limpiar la tabla y seleccionar un nuevo archivo
        self.data_table.clear()
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        self.feature_selector.clear()
        self.target_selector.clear()
        self.file_label.setText('Ruta del archivo cargado:')
        self.feature_selector.setEnabled(False)
        self.target_selector.setEnabled(False)
        self.confirm_button.setEnabled(False)
        self.open_file_dialog()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DataViewer()
    viewer.show()
    sys.exit(app.exec_())



