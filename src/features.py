import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from import_files import import_data
from data_preprocessing import detect_missing_values, remove_missing_values, fill_with_mean, fill_with_median, fill_with_constant
from model_saver import ModelSaver
from model_loader import ModelLoader

class DataViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.df = None
        self.last_file_path = None
        self.columnas_entrada = []
        self.columna_salida = []

        # Crear el layout principal y asignarlo al widget
        self.layout = QVBoxLayout()  
        self.setLayout(self.layout)


        # Configuración de la interfaz de usuario
        self.initUI()  # Llamamos a initUI una vez, donde se agregan los widgets al layout

    def initUI(self):
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
        self.layout.addWidget(self.load_button)

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
        self.layout.addWidget(self.back_button)

        # Table to display data
        self.data_table = QTableWidget()
        self.data_table.setFont(QFont('Arial', 10))
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        self.layout.addWidget(self.data_table)

        # Label to display the path of the uploaded file
        self.file_label = QLabel('📂 Ruta del archivo cargado:')
        self.file_label.setFont(QFont('Arial', 10))
        self.layout.addWidget(self.file_label)

        # Button for detecting non-existent values
        self.detect_button = QPushButton('🔍 Detectar', self)
        self.detect_button.clicked.connect(self.handle_detect_missing_values)
        self.detect_button.setEnabled(False)
        self.layout.addWidget(self.detect_button)

        # Drop-down menu for pre-processing options
        self.layout.addWidget(QLabel("Opciones de Manejo de Datos Inexistentes"))
        self.preprocessing_options = QComboBox(self)
        self.preprocessing_options.addItems([
            "🗑️ Eliminar Filas con Valores Inexistentes",
            "📊 Rellenar con la Media",
            "📊 Rellenar con la Mediana",
            "✏️ Rellenar con un Valor Constante"
        ])
        self.preprocessing_options.setEnabled(False)
        self.layout.addWidget(self.preprocessing_options)

        # Confirmation button to apply pre-processing
        self.apply_button = QPushButton('🟢 Aplicar Preprocesado', self)
        self.apply_button.setFont(QFont('Arial Black', 8))
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.confirm_preprocessing)
        self.layout.addWidget(self.apply_button)

        # Radio buttons to select the type of regression
        self.radio_simple = QRadioButton("Regresión Simple")
        self.radio_multiple = QRadioButton("Regresión Múltiple")
        self.radio_simple.setChecked(True)  # Por defecto, regresión simple
        self.radio_simple.toggled.connect(self.update_feature_selector)
        self.radio_multiple.toggled.connect(self.update_feature_selector)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_simple)
        radio_layout.addWidget(self.radio_multiple)
        self.layout.addLayout(radio_layout)

        # Column selector (features)
        self.feature_selector = QListWidget(self)
        self.feature_selector.setSelectionMode(QAbstractItemView.SingleSelection)  # Por defecto, solo una selección (regresión simple)
        self.feature_selector.setEnabled(False)  # Inicia desactivado hasta que cargues datos
        self.layout.addWidget(QLabel("Columnas de Entrada (Features)"))
        self.layout.addWidget(self.feature_selector)

        # Simple selector for the output column (target)
        self.target_selector = QListWidget(self)
        self.target_selector.setSelectionMode(QAbstractItemView.SingleSelection)  # Permitir selección unica para la salida
        self.target_selector.setEnabled(False)  # Inicia desactivado hasta que cargues datos
        self.layout.addWidget(QLabel("Columnas de Salida (Target)"))
        self.layout.addWidget(self.target_selector)

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
        self.layout.addWidget(self.confirm_button)

    
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
        self.layout.addWidget(self.create_model_button)

        # Define los labels para mostrar los datos del modelo cargado
        self.formula_label = QLabel("Fórmula: ")
        self.mse_label = QLabel("MSE: ")
        self.r_squared_label = QLabel("R²: ")
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)

        # Agrega estos widgets al layout, pero inicialmente están ocultos
        self.layout.addWidget(self.formula_label)
        self.layout.addWidget(self.mse_label)
        self.layout.addWidget(self.r_squared_label)
        self.layout.addWidget(self.description_text)
        
        # Oculta los detalles del modelo cargado inicialmente
        self.hide_model_details()

        # Botón para cargar modelo
        self.load_model_button = QPushButton("📂 Cargar Modelo", self)
        self.load_model_button.setFont(QFont("Arial Black", 10))
        self.load_model_button.setStyleSheet("""
            QPushButton {
                background-color: lightblue; color: black; padding: 10px;}
            QPushButton:hover {
                background-color: blue; color: white;}
        """)
        self.load_model_button.setEnabled(True)  # Desactivado hasta que sea necesario
        self.load_model_button.clicked.connect(self.open_model_loader)
        self.layout.addWidget(self.load_model_button)

        # Botón para guardar el modelo
        self.save_model_button = QPushButton("💾 Guardar Modelo", self)
        self.save_model_button.setFont(QFont("Arial Black", 10))
        self.save_model_button.setStyleSheet("""
            QPushButton {
                background-color: lightblue; color: black; padding: 10px;}
            QPushButton:hover {
                background-color: darkblue; color: white;}
        """)
        self.save_model_button.setEnabled(False)
        self.save_model_button.clicked.connect(self.open_model_saver)
        self.layout.addWidget(self.save_model_button)

        # Configurar layout
        self.setLayout(self.layout)
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

    
    def open_model_loader(self):
        try:
            # Llama directamente al método de ModelLoader para cargar el modelo
            model_loader = ModelLoader(self)  # Crea el objeto de ModelLoader
            model_loader.load_model_dialog()  # Abre el diálogo de selección de archivo para cargar el modelo
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cargar el modelo: {str(e)}")



    def open_model_saver(self):
        try:
            model_data = {
                'model': self.result_window.model,
                'formula': self.result_window.formula_label.text(),
                'r_squared': getattr(self.result_window, 'r_squared', None),
                'mse': getattr(self.result_window, 'mse', None),
                'input_columns': self.columnas_entrada,
                'output_column': self.columna_salida,
                'description': self.result_window.text_box.toPlainText()
            }

            model_saver = ModelSaver(**model_data)
            model_saver.save_model_dialog()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar el modelo: {str(e)}")
    
    # Método para ocultar los detalles del modelo
    def hide_model_details(self):
        self.formula_label.setVisible(False)
        self.mse_label.setVisible(False)
        self.r_squared_label.setVisible(False)
        self.description_text.setVisible(False)

    # Método para mostrar los detalles del modelo
    def show_model_details(self):
        self.formula_label.setVisible(True)
        self.mse_label.setVisible(True)
        self.r_squared_label.setVisible(True)
        self.description_text.setVisible(True)

    def show_results(self):
        """
        Genera la ventana de resultados con la gráfica y habilita la funcionalidad de predicción.
        """
        from results_window import ResultWindow  # Asegúrate de que está correctamente importado
        try:
            # Crear la ventana de resultados y pasar el modelo generado
            self.result_window = ResultWindow(
                self.df, self.columnas_entrada, self.columna_salida
            )
            self.result_window.show()
            self.save_model_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al generar el modelo: {str(e)}")



