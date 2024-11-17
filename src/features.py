import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from import_files import import_data
from data_preprocessing import *
from table import Table
from buttons import Button

class DataViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.df = None
        self.last_file_path = None
        self.columnas_entrada = []
        self.columna_salida = []
        self.data_table = None
        self.move = 1

    def initUI(self):
        # Principal layout        
        self.main_layout = QVBoxLayout()
        # Front/Back layout
        self.NBlayout = QHBoxLayout()
        self.button = Button()

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
        self.start_button.clicked.connect(self.delete_welcome)

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
        self.load_button = self.button.add_QPushButton('📂 Cargar Dataset',"Arial",12,243,None,False)
        self.button.set_StyleSheet(self.load_button,"green","white","10px")
        self.button.set_QPushButton_hoverStyle(self.load_button,"darkgreen","lightgrey")
        self.load_button.clicked.connect(self.open_file_dialog)
        self.first_step_layout.addWidget(self.load_button)

        # Button to go back and choose another file
        self.back_button = self.button.add_QPushButton("🔄️ Elegir otro archivo","Arial Black",12,262,None,False)
        self.button.set_StyleSheet(self.back_button,"orange","white","10px")
        self.button.set_QPushButton_hoverStyle(self.back_button,"darkorange","lightgrey")
        self.back_button.clicked.connect(self.clear_table_and_choose_file)
        self.first_step_layout.addWidget(self.back_button)

        # Label to display the path of the uploaded file
        self.file_label = QLabel('📂 Ruta del archivo cargado:')
        self.file_label.setFont(QFont('Arial', 10))
        self.file_label.setVisible(False)
        self.first_step_layout.addWidget(self.file_label)

        # Table to display data
        self.table_view = QTableView()
        self.table_view.setFont(QFont("Arial",10))
        self.table_view.setVisible(False)
        self.first_step_layout.addWidget(self.table_view)
        self.main_layout.addLayout(self.first_step_layout) 
        #-----------------------------------------------------------------------------------------------------------------------
        # SECOND STEP: Nan values
        #-----------------------------------------------------------------------------------------------------------------------
        # Nan Layout
        self.nan_layout = QVBoxLayout()
        # Button for detecting non-existent values
        self.detect_button = self.button.add_QPushButton("🔍 Detectar","Arial",10,None,None,False)
        self.detect_button.clicked.connect(self.handle_detect_missing_values)
        self.nan_layout.addWidget(self.detect_button)

        # Drop-down menu for pre-processing options
        items = ["🗑️ Eliminar Filas con Valores Inexistentes","📊 Rellenar con la Media","📊 Rellenar con la Mediana",
            "✏️ Rellenar con un Valor Constante"]
        self.preprocessing_options = self.button.add_QComboBox(items,None,None,False)
        self.nan_layout.addWidget(self.preprocessing_options)

        # Confirmation button to apply pre-processing
        self.apply_button = self.button.add_QPushButton("🟢 Aplicar Preprocesado","Arial Black",8,None,None,False)
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
        self.confirm_button = self.button.add_QPushButton("✅ Confirmar selección","Arial Black",10,None,None,False)
        self.button.set_StyleSheet(self.confirm_button,"lightgreen","lightblack","5px")
        self.button.set_QPushButton_hoverStyle(self.confirm_button,"green","white")
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.regresion_layout.addWidget(self.confirm_button)

        # Create Regression Model Button
        self.create_model_button = self.button.add_QPushButton("📈 Crear Modelo de Regresión","Arial Black",10,None,None,False)
        self.button.set_StyleSheet(self.create_model_button,"lightblue","lightblack","10px")
        self.button.set_QPushButton_hoverStyle(self.create_model_button,"blue","white")  
        self.create_model_button.clicked.connect(self.show_results)
        self.regresion_layout.addWidget(self.create_model_button)
        self.main_layout.addLayout(self.regresion_layout)
        #-----------------------------------------------------------------------------------------------------------------------
        # Next and Back Buttons:
        #-----------------------------------------------------------------------------------------------------------------------
        #Return Button
        self.back_layout = QVBoxLayout()
        self.return_button = QPushButton("<- Back")
        self.return_button.clicked.connect(self.back)
        self.return_button.setVisible(False)
        self.back_layout.addWidget(self.return_button)
        self.back_layout.setAlignment(Qt.AlignLeft)                
        self.NBlayout.addLayout(self.back_layout)


        # Next Button
        self.next_layout = QVBoxLayout()
        self.next_button = QPushButton("Next ->")
        self.next_button.clicked.connect(self.next)
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
            self.df = import_data(file_path)
            if self.df is not None and not self.df.empty:
                self.display_data_in_table(self.df)
                # Enable buttons if data is loaded correctly
                self.file_label.setText(f'📂 Archivo cargado: {file_path}')
                self.populate_selectors(self.df) 
            else:
                QMessageBox.warning(self, "Advertencia", "El archivo está vacío o no se pudo cargar correctamente.")
        except pd.errors.EmptyDataError:
            QMessageBox.critical(self, "Error", "El archivo CSV está vacío. Por favor, selecciona otro archivo.")
        except pd.errors.ParserError:
            QMessageBox.critical(self, "Error", "El archivo CSV está corrupto o tiene un formato inválido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {str(e)}")

    def display_data_in_table(self, data):
        self.data_table = Table(self.df)
        self.table_view.setModel(self.data_table)

        # Show file path
        self.file_label.setVisible(True)
        self.load_button.setVisible(False)
        self.back_button.setVisible(True)
        self.next_button.setEnabled(True)

        # Adjust Table Size
        self.table_view.resizeColumnsToContents()
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def resizeEvent(self, event):
        # Adjust the size of the table when resizing the window
        window_width = self.width()
        
        if window_width < 1000:
            self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.table_view.resizeColumnsToContents()
            # Welcome
            self.spacer.changeSize(0,20)
            self.hello.setFont(QFont("Arial", 25))  
            self.welcome_message.setFont(QFont("Arial", 18))
            self.start_label.setFont(QFont("Arial",12))
            self.button.change_style(self.start_button,"Arial Black",12,300,50)
            self.button.change_style(self.load_button,"Arial Black",12,243,None)
            self.button.change_style(self.back_button,"Arial Black",12,262,None)
            self.setMinimumSize(800,600)

        else:
            self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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
            self.load_data()

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

    def layout_visibility(self,sublayouts:bool,visibility:bool,layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if visibility == False:
                if item.widget():
                    item.widget().setVisible(False)  
                if isinstance(item, QSpacerItem):
                    layout.removeItem(item) 
                if item.layout() and sublayouts == True:
                    self.layout_visibility(True,False, item.layout())
            else:
                if item.widget():
                    item.widget().setVisible(True)  
                if item.layout() and sublayouts == True:
                    self.layout_visibility(True,True, item.layout())

    def delete_welcome(self):
        self.layout_visibility(True,False,self.welcome_layout)
        self.drive_through()

    def next(self):
        if self.move < 3:
            self.move += 1
            self.drive_through()
                        
    def back(self):
        if self.move > 1:
            self.move -= 1
            self.drive_through()
            
    def drive_through(self):
        self.layout_visibility(True,False,self.main_layout)
        self.layout_visibility(True,True,self.NBlayout)
        if self.move == 1:
            self.layout_visibility(True,True, self.first_step_layout)
            self.back_button.setVisible(False)
            self.file_label.setVisible(False)
            self.return_button.setEnabled(False)
            if self.data_table is None:
                self.next_button.setEnabled(False)
            else:
                self.next_button.setEnabled(True)
            
        elif self.move == 2:
            self.layout_visibility(True,True, self.nan_layout)
            self.table_view.setVisible(True)
            self.return_button.setEnabled(True)
            self.next_button.setEnabled(True)
        else:
            self.layout_visibility(True,True, self.regresion_layout)
            self.next_button.setEnabled(False)