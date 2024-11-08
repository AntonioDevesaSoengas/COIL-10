import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from import_files import import_data
from data_preprocessing import detect_missing_values, remove_missing_values, fill_with_mean, fill_with_median, fill_with_constant

class DataViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.df = None
        self.last_file_path = None
        self.columnas_entrada = []
        self.columna_salida = []

    def initUI(self):
        # Principal layout
        layout = QVBoxLayout()

        # Botón para cargar archivo
        self.load_button = QPushButton('📂 Cargar Dataset', self)
        self.load_button.setFont(QFont('Arial Black', 12))
        self.load_button.setFixedWidth(260)
        self.load_button.setStyleSheet("""
            QPushButton{
                background-color: green; color: white; padding: 10px;}
            QPushButton:hover{
                background-color: darkgreen; color: lightgrey;}
        """)
        self.load_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.load_button)

        # Button to go back and choose another file
        self.back_button = QPushButton('🔄 Elegir otro archivo', self)
        self.back_button.setFont(QFont('Arial Black', 12))
        self.back_button.setFixedWidth(260)
        self.back_button.setStyleSheet("""
            QPushButton{
                background-color: orange; color: white; padding: 10px;}
            QPushButton:hover{
                background-color: darkorange; color: lightgrey;}
        """)
        self.back_button.clicked.connect(self.clear_table_and_choose_file)
        self.back_button.setVisible(False)  # No visible hasta cargar los datasets
        layout.addWidget(self.back_button)

        # Table to display data
        self.data_table = QTableWidget()
        self.data_table.setFont(QFont('Arial', 10))
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        layout.addWidget(self.data_table)

        # Label to display the path of the uploaded file
        self.file_label = QLabel('📂 Ruta del archivo cargado:')
        self.file_label.setFont(QFont('Arial', 10))
        layout.addWidget(self.file_label)

        # Button for detecting non-existent values
        self.detect_button = QPushButton('🔍 Detectar', self)
        self.detect_button.clicked.connect(self.handle_detect_missing_values)
        self.detect_button.setEnabled(False)
        layout.addWidget(self.detect_button)

        # Drop-down menu for pre-processing options
        layout.addWidget(QLabel("Opciones de Manejo de Datos Inexistentes"))
        self.preprocessing_options = QComboBox(self)
        self.preprocessing_options.addItems([
            "🗑️ Eliminar Filas con Valores Inexistentes",
            "📊 Rellenar con la Media",
            "📊 Rellenar con la Mediana",
            "✏️ Rellenar con un Valor Constante"
        ])
        self.preprocessing_options.setEnabled(False)
        layout.addWidget(self.preprocessing_options)

        # Confirmation button to apply pre-processing
        self.apply_button = QPushButton('🟢 Aplicar Preprocesado', self)
        self.apply_button.setFont(QFont('Arial Black', 8))
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.confirm_preprocessing)
        layout.addWidget(self.apply_button)

        # Radio buttons to select the type of regression
        self.radio_simple = QRadioButton("Regresión Simple")
        self.radio_multiple = QRadioButton("Regresión Múltiple")
        self.radio_simple.setChecked(True)  # Por defecto, regresión simple
        self.radio_simple.toggled.connect(self.update_feature_selector)
        self.radio_multiple.toggled.connect(self.update_feature_selector)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_simple)
        radio_layout.addWidget(self.radio_multiple)
        layout.addLayout(radio_layout)

        # Column selector (features)
        self.feature_selector = QListWidget(self)
        self.feature_selector.setSelectionMode(QAbstractItemView.SingleSelection)  # Por defecto, solo una selección (regresión simple)
        self.feature_selector.setEnabled(False)  # Inicia desactivado hasta que cargues datos
        layout.addWidget(QLabel("Columnas de Entrada (Features)"))
        layout.addWidget(self.feature_selector)

        # Simple selector for the output column (target)
        self.target_selector = QListWidget(self)
        self.target_selector.setSelectionMode(QAbstractItemView.SingleSelection)  # Permitir selección unica para la salida
        self.target_selector.setEnabled(False)  # Inicia desactivado hasta que cargues datos
        layout.addWidget(QLabel("Columnas de Salida (Target)"))
        layout.addWidget(self.target_selector)

        # Confirmation button
        self.confirm_button = QPushButton('✅ Confirmar selección', self)
        self.confirm_button.setFont(QFont('Arial Black', 10))
        self.confirm_button.setStyleSheet("""
            QPushButton{
                background-color: lightgreen; color: darkgrey;}
            QPushButton:hover{
                background-color: green; color: white;}
        """)
        self.confirm_button.setEnabled(False)  # Se activa solo cuando hay datos cargados
        self.confirm_button.clicked.connect(self.confirm_selection)
        layout.addWidget(self.confirm_button)

    
        # Create Regression Model Button
        self.create_model_button = QPushButton('📈 Crear Modelo de Regresión', self)
        self.create_model_button.setFont(QFont('Arial Black', 10))
        self.create_model_button.setStyleSheet("""
            QPushButton{
                background-color: blue; color: white; padding: 10px;}
            QPushButton:hover{
                background-color: darkblue; color: lightgrey;}
        """)
        self.create_model_button.setEnabled(False)  # Enabled only when the selection is confirmed
        self.create_model_button.clicked.connect(self.show_results)
        layout.addWidget(self.create_model_button)

        # Configurar layout
        self.setLayout(layout)
        self.setWindowTitle('Visualizador de Datasets')
        self.resize(800, 600)  # Tamaño de la ventana ajustado

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
                    self.load_data(file_path)  # Reload the dataset directly without opening the browser
        
            else:
                self.last_file_path = file_path    
                self.file_label.setText(f'📂 Archivo cargado: {file_path}')
                self.back_button.setVisible(True) 
                self.load_data(file_path)

    def load_data(self, file_path):
        try:
            data = import_data(file_path)
            if data is not None and not data.empty:
                self.df = data
                self.display_data_in_table(data)
                # Enable buttons if data is loaded correctly
                self.detect_button.setEnabled(True)
                self.preprocessing_options.setEnabled(True)
                self.back_button.setVisible(True)
                self.file_label.setText(f'📂 Archivo cargado: {file_path}')
                self.populate_selectors(data) 
                self.apply_button.setEnabled(True)
            else:
                QMessageBox.warning(self, "Advertencia", "El archivo está vacío o no se pudo cargar correctamente.")
        except pd.errors.EmptyDataError:
            QMessageBox.critical(self, "Error", "El archivo CSV está vacío. Por favor, selecciona otro archivo.")
        except pd.errors.ParserError:
            QMessageBox.critical(self, "Error", "El archivo CSV está corrupto o tiene un formato inválido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {str(e)}")

    def display_data_in_table(self, data):
        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(data.columns))
        self.data_table.setHorizontalHeaderLabels(data.columns)

        for i, row in data.iterrows():
            for j, value in enumerate(row):
                self.data_table.setItem(i, j, QTableWidgetItem(str(value)))

        # Adjust Table Size
        self.data_table.resizeColumnsToContents()
        self.data_table.resizeRowsToContents()
        self.data_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.data_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Make sure the board takes up the entire width of the frame
        for j in range(len(data.columns)):
            self.data_table.setColumnWidth(j, self.data_table.width() // len(data.columns))  # Ajustar el ancho de cada columna

        # Disable Load Datasets button
        self.load_button.setVisible(False)

    def resizeEvent(self, event):
        # Adjust the size of the table when resizing the window
        self.data_table.setFixedWidth(self.width() - 40)  # Adjust with a margin
        super().resizeEvent(event)

    def populate_selectors(self, data):
        # Enable the Selectors and Confirmation Button
        self.feature_selector.setEnabled(True)
        self.target_selector.setEnabled(True)
        self.confirm_button.setEnabled(True)

        # Clean up your current selectors
        self.feature_selector.clear()
        self.target_selector.clear()

        # Add the available columns
        self.feature_selector.addItems(data.columns)
        self.target_selector.addItems(data.columns)

        # Update feature selection based on the selected regression type
        self.update_feature_selector()

    def update_feature_selector(self):
        if self.radio_simple.isChecked():
            # Simple Regression: Only One Selection Allowed
            self.feature_selector.setSelectionMode(QAbstractItemView.SingleSelection)
        else:
            # Multiple Regression: Multiple Choice Allowed
            self.feature_selector.setSelectionMode(QAbstractItemView.MultiSelection)

    def confirm_selection(self):
        # Get feature selections
        selected_features = [item.text() for item in self.feature_selector.selectedItems()]
        self.columnas_entrada = selected_features
        # Obtener la selección de target
        selected_target = [item.text() for item in self.target_selector.selectedItems()]
        self.columna_salida = selected_target
        if not selected_features or not selected_target:
            QMessageBox.warning(self, "Selección incompleta", "Debes seleccionar al menos una columna de entrada y una de salida.")
            return

        # Succes message of the selected columns
        QMessageBox.information(self, "Selección confirmada", f"Has seleccionado las columnas de entrada: {', '.join(selected_features)} y la columna de salida: {', '.join(selected_target)}.")
        self.create_model_button.setEnabled(True)

    def clear_table_and_choose_file(self):
        # Clean up the table and select a new file
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

    # Preprocessing function to detect Non-existent Values
    def handle_detect_missing_values(self):
        if self.df is not None:
            message = detect_missing_values(self.df)
            QMessageBox.information(self, "Detección de Valores Inexistentes", message)

    # Apply the selected pre-processing option in the ComboBox
    def confirm_preprocessing(self):  
        option = self.preprocessing_options.currentText()
        if not option:
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar una opción de preprocesado antes de confirmar.")
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
            self.display_data_in_table(self.df)  # Make sure the table is updated with the new content

            QMessageBox.information(self, "Éxito", "Preprocesado aplicado con éxito.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al aplicar el preprocesado: {str(e)}")

    def show_results(self):
        from results_window import ResultWindow
        try:
            self.result_window = ResultWindow(self.df, self.columnas_entrada, self.columna_salida)
            self.result_window.show()
        
            # Success Message
            QMessageBox.information(self, "Éxito", "El modelo de regresión se ha creado correctamente.")
        
        except Exception as e:
            # Error Message
            QMessageBox.critical(self, "Error", f"Ocurrió un error al crear el modelo: {str(e)}")
