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
        self.main_layout = QVBoxLayout()
        # Front/Back layout
        self.NBlayout = QHBoxLayout()

        # Welcome Message
        #-----------------------------------------------------------------------------------------------------------------------
        self.hello = QLabel("¡Hello!")
        self.hello.setAlignment(Qt.AlignCenter)
        self.hello.setStyleSheet("font-weight: bold;")
        self.welcome_message = QLabel("""Welcome to "our app", here you will be able to 
upload your own datasets and create a linear 
regression based on them""")
        self.welcome_message.setAlignment(Qt.AlignCenter)
        
        self.spacer = QSpacerItem(0,0)
        self.welcome_layout = QVBoxLayout()
        self.welcome_layout.addWidget(self.hello)
        self.welcome_layout.addItem(self.spacer)
        self.welcome_layout.addWidget(self.welcome_message)
        self.welcome_layout.setAlignment(Qt.AlignCenter)

        # Start Button
        self.start_label = QLabel("Click here to start\n👇")
        self.start_label.setAlignment(Qt.AlignCenter)
        self.start_button = QPushButton("Start My Linear Regresion")
        self.start_button.setStyleSheet("color:green; padding:10px")
        self.start_button.clicked.connect(self.first_step)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.start_button)
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.welcome_layout.addItem(self.spacer)
        self.welcome_layout.addItem(self.spacer)
        self.welcome_layout.addWidget(self.start_label)
        self.welcome_layout.addLayout(self.button_layout)
        self.main_layout.addLayout(self.welcome_layout)
        #-----------------------------------------------------------------------------------------------------------------------
        # FIRST STEP: Open file and display data
        #-----------------------------------------------------------------------------------------------------------------------
        self.first_step_layout = QVBoxLayout()
        # Botón para cargar archivo
        self.load_button = QPushButton('📂 Cargar Dataset', self)
        self.load_button.setFixedWidth(260)
        self.load_button.setStyleSheet("""
            QPushButton{
                background-color: green; color: white; padding: 10px;}
            QPushButton:hover{
                background-color: darkgreen; color: lightgrey;}
        """)
        self.load_button.clicked.connect(self.open_file_dialog)
        self.load_button.setVisible(False)
        self.first_step_layout.addWidget(self.load_button)

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
        self.first_step_layout.addWidget(self.back_button)

        # Label to display the path of the uploaded file
        self.file_label = QLabel('📂 Ruta del archivo cargado:')
        self.file_label.setFont(QFont('Arial', 10))
        self.file_label.setVisible(False)
        self.first_step_layout.addWidget(self.file_label)

        # Table to display data
        self.data_table = QTableWidget()
        self.data_table.setFont(QFont('Arial', 10))
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        self.data_table.setVisible(False)
        self.first_step_layout.addWidget(self.data_table)
        self.main_layout.addLayout(self.first_step_layout)
        #-----------------------------------------------------------------------------------------------------------------------
        # SECOND STEP: Nan values
        #-----------------------------------------------------------------------------------------------------------------------
        # Nan Layout
        self.nan_layout = QVBoxLayout()
        # Button for detecting non-existent values
        self.detect_button = QPushButton('🔍 Detectar', self)
        self.detect_button.clicked.connect(self.handle_detect_missing_values)
        self.detect_button.setVisible(False)
        self.nan_layout.addWidget(self.detect_button)

        # Drop-down menu for pre-processing options
        self.preprocessing_options = QComboBox(self)
        self.preprocessing_options.addItems([
            "🗑️ Eliminar Filas con Valores Inexistentes",
            "📊 Rellenar con la Media",
            "📊 Rellenar con la Mediana",
            "✏️ Rellenar con un Valor Constante"
        ])
        self.preprocessing_options.setVisible(False)
        self.nan_layout.addWidget(self.preprocessing_options)

        # Confirmation button to apply pre-processing
        self.apply_button = QPushButton('🟢 Aplicar Preprocesado', self)
        self.apply_button.setFont(QFont('Arial Black', 8))
        self.apply_button.setVisible(False)
        self.apply_button.clicked.connect(self.confirm_preprocessing)
        self.nan_layout.addWidget(self.apply_button)
        self.main_layout.addLayout(self.nan_layout)
        #-----------------------------------------------------------------------------------------------------------------------
        # THIRD STEP: Options for the linear regresion
        #-----------------------------------------------------------------------------------------------------------------------
        # Regresion Layout
        self.regresion_layout = QVBoxLayout()
        # Radio buttons to select the type of regression
        self.radio_simple = QRadioButton("Regresión Simple")
        self.radio_multiple = QRadioButton("Regresión Múltiple")
        self.radio_simple.setChecked(True)  # Por defecto, regresión simple
        self.radio_simple.toggled.connect(self.update_feature_selector)
        self.radio_multiple.toggled.connect(self.update_feature_selector)

        self.radio_simple.setVisible(False)
        self.radio_multiple.setVisible(False)

        self.radio_layout = QHBoxLayout()
        self.radio_layout.addWidget(self.radio_simple)
        self.radio_layout.addWidget(self.radio_multiple)
        self.regresion_layout.addLayout(self.radio_layout)

        # Column selector (features)
        self.feature_label = QLabel("Columnas de Entrada (Features)")
        self.feature_selector = QListWidget(self)
        self.feature_selector.setSelectionMode(QAbstractItemView.SingleSelection)  # Por defecto, solo una selección (regresión simple)
        self.feature_selector.setVisible(False)  
        self.feature_label.setVisible(False)
        self.regresion_layout.addWidget(self.feature_label)
        self.regresion_layout.addWidget(self.feature_selector)

        # Simple selector for the output column (target)
        self.target_label = QLabel("Columnas de Salida (Target)")
        self.target_selector = QListWidget(self)
        self.target_selector.setSelectionMode(QAbstractItemView.SingleSelection)  # Permitir selección unica para la salida
        self.target_selector.setVisible(False) 
        self.target_label.setVisible(False)
        self.regresion_layout.addWidget(self.target_label)
        self.regresion_layout.addWidget(self.target_selector)

        # Confirmation button
        self.confirm_button = QPushButton('✅ Confirmar selección', self)
        self.confirm_button.setFont(QFont('Arial Black', 10))
        self.confirm_button.setStyleSheet("""
            QPushButton{
                background-color: lightgreen; color: darkgrey;}
            QPushButton:hover{
                background-color: green; color: white;}
        """)
        self.confirm_button.setVisible(False)  
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.regresion_layout.addWidget(self.confirm_button)

        # Create Regression Model Button
        self.create_model_button = QPushButton('📈 Crear Modelo de Regresión', self)
        self.create_model_button.setFont(QFont('Arial Black', 10))
        self.create_model_button.setStyleSheet("""
            QPushButton{
                background-color: blue; color: white; padding: 10px;}
            QPushButton:hover{
                background-color: darkblue; color: lightgrey;}
        """)
        self.create_model_button.setVisible(False)  
        self.create_model_button.clicked.connect(self.show_results)
        self.regresion_layout.addWidget(self.create_model_button)
        self.main_layout.addLayout(self.regresion_layout)
        #-----------------------------------------------------------------------------------------------------------------------
        # Next and Back Buttons:
        #-----------------------------------------------------------------------------------------------------------------------
        #Return Button
        self.back_layout = QVBoxLayout()
        self.return_button = QPushButton("<- Back")
        self.return_button.setVisible(False)
        self.back_layout.addWidget(self.return_button)
        self.back_layout.setAlignment(Qt.AlignLeft)                
        self.NBlayout.addLayout(self.back_layout)


        # Next Button
        self.next_layout = QVBoxLayout()
        self.next_button = QPushButton("Next ->")
        self.next_button.clicked.connect(self.second_step)
        self.next_button.setVisible(False)
        self.next_button.setEnabled(False)
        self.next_layout.addWidget(self.next_button)
        self.next_layout.setAlignment(Qt.AlignRight)
        self.NBlayout.addLayout(self.next_layout)
        #-----------------------------------------------------------------------------------------------------------------------
        # Layouts
        #-----------------------------------------------------------------------------------------------------------------------
        # Configurar layout
        self.NBlayout.setAlignment(Qt.AlignBottom)
        self.main_layout.addLayout(self.NBlayout)
        self.setLayout(self.main_layout)
        self.setWindowTitle('Visualizador de Datasets')

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
                self.load_data(file_path)

    def load_data(self, file_path):
        try:
            data = import_data(file_path)
            if data is not None and not data.empty:
                self.df = data
                self.display_data_in_table(data)
                # Enable buttons if data is loaded correctly
                self.file_label.setText(f'📂 Archivo cargado: {file_path}')
                self.populate_selectors(data) 
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

        # Show file path
        self.file_label.setVisible(True)
        self.next_button.setEnabled(True)
        self.load_button.setVisible(False)
        self.back_button.setVisible(True)

        # Adjust Table Size
        # Ajustar tamaño de tabla
        self.data_table.resizeColumnsToContents()
        self.data_table.resizeRowsToContents()
        self.data_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.data_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def resizeEvent(self, event):
        # Adjust the size of the table when resizing the window
        window_width = self.width()
        
        if window_width < 1000:
            self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.data_table.resizeColumnsToContents()
            self.spacer.changeSize(0,20)
            self.hello.setFont(QFont("Arial", 25))  
            self.welcome_message.setFont(QFont("Arial", 18))
            self.start_label.setFont(QFont("Arial",12))
            self.start_button.setFont(QFont("Arial Black",12))
            self.start_button.setMaximumWidth(350)
            self.load_button.setFont(QFont('Arial Black', 12))
            self.load_button.setMaximumWidth(100)
            self.back_button.setFont(QFont('Arial Black', 12))
            self.back_button.setMaximumWidth(100)
            self.setMinimumSize(800,600)

        else:
            self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.spacer.changeSize(0,40)
            self.hello.setFont(QFont("Arial",45))
            self.welcome_message.setFont(QFont("Arial",35))
            self.start_label.setFont(QFont("Arial",14))
            self.start_button.setFont(QFont("Arial Black",18))
            self.start_button.setMaximumWidth(450)
            self.load_button.setFont(QFont('Arial Black', 16))
            self.load_button.setMaximumWidth(325)
            self.back_button.setFont(QFont('Arial Black', 16))
            self.back_button.setMaximumWidth(350)
            self.setMinimumSize(800, 600)

        super().resizeEvent(event)

    def populate_selectors(self, data):
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

    def clear_table_and_choose_file(self):
        # Clean up the table and select a new file
        file_path = self.open_file_dialog()
        if file_path and file_path != self.last_file_path:
            self.data_table.clear()

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
            # Success Message
            QMessageBox.information(self, "Éxito", "El modelo de regresión se ha creado correctamente.")
            self.result_window.show()
        
        except Exception as e:
            # Error Message
            QMessageBox.critical(self, "Error", f"Ocurrió un error al crear el modelo: {str(e)}")

    #---------------------------------------------------------------------------------------------------------------------------
    # Program Execution

    def layout_visibility(self,visibility:bool,layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if visibility == False:
                if item.widget():
                    item.widget().setVisible(False)  
                if isinstance(item, QSpacerItem):
                    layout.removeItem(item) 
                if item.layout():
                    self.layout_visibility(False, item.layout())
            else:
                if item.widget():
                    item.widget().setVisible(True)  
                if item.layout():
                    self.layout_visibility(True, item.layout())

    def first_step(self):
        self.layout_visibility(False,self.welcome_layout)
        self.layout_visibility(True, self.first_step_layout)
        self.back_button.setVisible(False)
        self.file_label.setVisible(False)
        self.next_button.setVisible(True)


    def second_step(self):
        self.layout_visibility(False, self.first_step_layout)
        self.layout_visibility(True, self.nan_layout)
        self.return_button.setVisible(True)
