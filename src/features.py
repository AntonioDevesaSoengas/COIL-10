import sys
import pandas as pd
from PyQt5.QtWidgets import (
                            QWidget, QVBoxLayout, QHBoxLayout,
                            QSpacerItem, QLabel, QTableView, QRadioButton,
                            QListWidget, QAbstractItemView, QPushButton, 
                            QFileDialog, QHeaderView
                            )
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from import_files import import_data
from data_preprocessing import *
from table import Table
from buttons import Button
from helpers import LabelHelper
from welcome_window import WelcomeWindow

class DataViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.df = None
        self.last_file_path = None
        self.columnas_entrada = []
        self.columna_salida = []
        self.data_table = None
        self.move = 1
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.spacer_layout = QHBoxLayout()
        self.spacer = QSpacerItem(0, 0)
        self.NBlayout = QHBoxLayout()
        self.button = Button()
        self.setup_welcome_window()
        self.setup_steps_guide()
        self.setup_first_step()
        self.setup_nan_step()
        self.setup_regression_step()
        self.setup_navigation_buttons()
        self.finalize_layout()

    # Funcion que ejecuta la ventana de bienvenida
    def setup_welcome_window(self):
        self.welcome_window = WelcomeWindow()
        self.welcome_window.start_clicked.connect(self.delete_welcome)
        self.main_layout.addWidget(self.welcome_window)
        
    # Funcion que contiene los pasos del programa
    def setup_steps_guide(self):
        self.steps_layout = QVBoxLayout()
        self.steps_label = LabelHelper.create_label(
            parent=self,
            text="STEPS",
            alignment=Qt.AlignLeft,
            bold=True
        )

        self.first_step = LabelHelper.create_label(
            parent=self,
            text="1. Load Dataset",
            alignment=Qt.AlignLeft,
            italic=True
        )

        self.second_step = LabelHelper.create_label(
            parent=self,
            text="2. Delete Empty Values",
            alignment=Qt.AlignLeft,
            italic=True
        )

        self.third_step = LabelHelper.create_label(
            parent=self,
            text="3. Create Linear Regression",
            alignment=Qt.AlignLeft,
            italic=True
        )

        self.steps_layout.addWidget(self.steps_label)
        self.steps_layout.addWidget(self.first_step)
        self.steps_layout.addWidget(self.second_step)
        self.steps_layout.addWidget(self.third_step)
        self.spacer_layout.addLayout(self.steps_layout)
        self.steps_layout.setAlignment(Qt.AlignTop)

        # Ocultar el diseño de pasos completo
        self.layout_visibility(True, False, self.steps_layout)

        #-----------------------------------------------------------------------------------------------------------------------
        # FIRST STEP: Open file and display data
        #-----------------------------------------------------------------------------------------------------------------------
    def setup_first_step(self):
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
        self.file_label = LabelHelper.create_label(
            parent=self,
            text="📂 Ruta del archivo cargado:",
            font=("Arial",10)
        )
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
    def setup_nan_step(self):
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
    def setup_regression_step(self):
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
    def setup_navigation_buttons(self):
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

    def finalize_layout(self):
        # Configurar alineación para los botones "Next" y "Back"
        self.NBlayout.setAlignment(Qt.AlignBottom)

        # Añadir el diseño de navegación (Next y Back) al diseño principal
        self.main_layout.addLayout(self.NBlayout)

        # Añadir espaciadores y finalizar la estructura de la ventana
        self.spacer_layout.addLayout(self.main_layout)
        self.setLayout(self.spacer_layout)

        # Configurar las propiedades básicas de la ventana
        self.setWindowTitle('Visualizador de Datasets')
        self.setMinimumSize(800, 600)

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

        # Mostrar únicamente la tabla y elementos relevantes
        self.table_view.setVisible(True)

        # Show file path
        self.file_label.setVisible(True)
        self.load_button.setVisible(False)
        self.next_button.setEnabled(True)

        if self.move == 1:  # Solo mostrar el botón en el paso 1
            self.back_button.setVisible(True)
        else:  # Ocultar en pasos posteriores
            self.back_button.setVisible(False)

        # Adjust Table Size
        self.table_view.resizeColumnsToContents()
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        if self.width() > 1000:
            self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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
    def layout_visibility(self, sublayouts: bool, visibility: bool, layout):
        """
        Controla la visibilidad de un diseño completo, incluyendo widgets y sublayouts.

        Args:
            sublayouts (bool): Si se debe aplicar la visibilidad a sublayouts.
            visibility (bool): True para mostrar, False para ocultar.
            layout: El diseño (layout) que queremos modificar.
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            
            if item.widget():  # Si el elemento es un widget
                item.widget().setVisible(visibility)
            
            elif item.layout() and sublayouts:  # Si el elemento es otro layout
                self.layout_visibility(True, visibility, item.layout())

    def delete_welcome(self):
        """Oculta la ventana de bienvenida y muestra el siguiente paso."""
        self.welcome_window.setVisible(False)
        self.layout_visibility(True,True,self.steps_layout)
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
            self.file_label.setVisible(False)
            self.return_button.setEnabled(False)
            if self.data_table is None:
                self.back_button.setVisible(False)
                self.next_button.setEnabled(False)
            else:
                self.load_button.setVisible(False)
                self.next_button.setEnabled(True)
            
        elif self.move == 2:
            self.layout_visibility(True,True, self.nan_layout)
            self.table_view.setVisible(True)
            self.return_button.setEnabled(True)
            self.next_button.setEnabled(True)

            # Asegura que el botón de cargar datos siga oculto
            self.back_button.setVisible(False)
            self.file_label.setVisible(True)
        
        elif self.move == 3:  # Paso 3: Crear modelo
            self.layout_visibility(True, True, self.regresion_layout)
            self.next_button.setEnabled(False)