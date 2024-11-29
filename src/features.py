import sys
import pandas as pd
from PyQt5.QtWidgets import (
                            QWidget, QVBoxLayout, QHBoxLayout,
                            QSpacerItem, QLabel, QTableView, QRadioButton,
                            QListWidget, QAbstractItemView, QPushButton, 
                            QFileDialog, QHeaderView, QTextEdit
                            )
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from import_files import import_data
from data_preprocessing import *
from table import Table
from helpers import LabelHelper, ButtonHelper, LayoutHelper
from welcome_window import WelcomeWindow


class DataViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.df = None
        self.last_file_path = None
        self.columnas_entrada = []
        self.columna_salida = []
        self.empty_values = False
        self.data_table = None
        self.nan_solved = False
        self.move = 1
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.spacer_layout = QHBoxLayout()
        self.spacer = QSpacerItem(0, 0)
        self.NBlayout = QHBoxLayout()
        self.button = ButtonHelper()
        self.layout = LayoutHelper()
        self.label = LabelHelper()
        self.setup_welcome_window()
        self.setup_steps_guide()
        self.setup_first_step()
        self.setup_nan_step()
        self.setup_regression_step()
        self.setup_model_details_step()  
        self.setup_navigation_buttons()
        self.finalize_layout()

    # Funcion que ejecuta la ventana de bienvenida
    def setup_welcome_window(self):
        self.welcome_window = WelcomeWindow()
        self.welcome_window.start_clicked.connect(self.delete_welcome)
        
    # Funcion que contiene los pasos del programa
    def setup_steps_guide(self):
        self.steps_layout = QVBoxLayout()
        self.steps_label = LabelHelper.create_label(
            parent=self,
            font=("Times New Roman",12),
            text="STEPS:",
            alignment=Qt.AlignLeft,
            bold=True
        )

        self.steps_separator = self.layout.add_separator("horizontal",None,
            False
        )

        self.first_step = LabelHelper.create_label(
            font=("Arial",9),
            parent=self,
            alignment=Qt.AlignLeft,
            italic=True
        )

        self.second_step = LabelHelper.create_label(
            font=("Arial",9),
            parent=self,
            alignment=Qt.AlignLeft,
            italic=True
        )

        self.third_step = LabelHelper.create_label(
            font=("Arial",9),
            parent=self,
            alignment=Qt.AlignLeft,
            italic=True
        )
        self.third_step.setMinimumWidth(250)

        self.layout_separator = self.layout.add_separator("vertical",None,
            False
        )

        items_steps_layout = [self.steps_label,self.steps_separator,
            self.first_step,self.second_step,self.third_step
        ]
        self.layout.add_widget(self.steps_layout,items_steps_layout)
        self.steps_layout.setAlignment(Qt.AlignTop)

        # Ocultar el diseño de pasos completo
        self.layout.layout_visibility(True, False, self.steps_layout)

    #-------------------------------------------------------------------------
    # FIRST STEP: Open file and display data
    #-------------------------------------------------------------------------
    def setup_first_step(self):
        self.first_step_layout = QVBoxLayout()

        # Botón para cargar archivo
        self.load_button = self.button.add_QPushButton('📂 Cargar Dataset',
            "Arial Black",12,243,None,False,
            background_color="green",color="white",padding="10px"
        )
        self.button.set_QPushButton_hoverStyle(self.load_button,"darkgreen","lightgrey")
        self.load_button.clicked.connect(self.open_file_dialog)

        # Botón para cargar modelo
        self.load_model_button = self.button.add_QPushButton('📦 Cargar Modelo',
            "Arial Black",12,243,None,False,
            background_color="blue",color="white",padding="10px"
        )
        self.button.set_QPushButton_hoverStyle(self.load_model_button,"darkblue","lightgrey")
        self.load_model_button.clicked.connect(self.open_model_dialog)

        # Botón para elegir otro archivo
        self.back_button = self.button.add_QPushButton("🔄️ Elegir otro archivo","Arial Black",12,262,None,False,
                                                       background_color="orange",color="white",padding="10px")
        self.button.set_QPushButton_hoverStyle(self.back_button,"darkorange","lightgrey")
        self.back_button.clicked.connect(self.clear_table_and_choose_file)

        # Etiqueta para mostrar la ruta del archivo cargado
        self.file_label = LabelHelper.create_label(
            parent=self,
            text="📂 Ruta del archivo cargado:",
            font=("Arial",10)
        )
        self.file_label.setVisible(False)

        # Tabla para mostrar los datos
        self.table_view = QTableView()
        self.table_view.setFont(QFont("Arial",10))
        self.table_view.setVisible(False)

        # Añadir los widgets al layout del primer paso
        items_setup_first_step = [self.load_button, self.load_model_button, self.back_button, self.file_label, self.table_view]
        self.layout.add_widget(self.first_step_layout, items_setup_first_step)
    #-------------------------------------------------------------------------
    # SECOND STEP: Nan values
    #-------------------------------------------------------------------------
    def setup_nan_step(self):
        self.nan_layout = QVBoxLayout()

        self.sep = self.layout.add_separator("horizontal",None,False,)

        self.nan_label = self.label.create_label(
            parent=self,
            font=("Arial",12),
            alignment=Qt.AlignLeft,
            bold=True,
            )

        self.nan_values = self.label.create_label(
            parent=self,
            font=("Arial",10),
            alignment=Qt.AlignLeft
        )

        self.separator = self.layout.add_separator("horizontal",
        None,False)

        # Drop-down menu for pre-processing options
        self.option_label = self.label.create_label(self,"Choose an option for preprocessing nan values:",font=("Arial",8),alignment=Qt.AlignLeft)
        items = ["Select an option...","🗑️ Eliminar Filas con Valores Inexistentes","📊 Rellenar con la Media","📊 Rellenar con la Mediana",
                "✏️ Rellenar con un Valor Constante"]
        self.preprocessing_options = self.button.add_QComboBox(items,None,None,False)
        self.preprocessing_options.currentIndexChanged.connect(self.preprocessing_button)

        # Confirmation button to apply pre-processing
        self.apply_button = self.button.add_QPushButton("🟢 Aplicar Preprocesado","Arial Black",8,None,None,False,enabled=False)
        self.apply_button.clicked.connect(self.confirm_preprocessing)
        widgets = [self.sep,self.nan_label,self.separator,self.option_label,self.preprocessing_options,self.apply_button]
        self.layout.add_widget(self.nan_layout,widgets)
    #-------------------------------------------------------------------------
    # THIRD STEP: Options for the linear regresion
    #-------------------------------------------------------------------------
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
        radio_button = [self.radio_simple,self.radio_multiple]
        self.layout.add_widget(self.radio_layout,radio_button)

        # Column selector (features)
        self.feature_label = QLabel("Columnas de Entrada (Features)")
        self.feature_selector = QListWidget(self)
        self.feature_selector.setSelectionMode(QAbstractItemView.SingleSelection)  # Por defecto, solo una selección (regresión simple)
        self.feature_selector.setVisible(False)  
        self.feature_label.setVisible(False)

        # Simple selector for the output column (target)
        self.target_label = QLabel("Columnas de Salida (Target)")
        self.target_selector = QListWidget(self)
        self.target_selector.setSelectionMode(QAbstractItemView.SingleSelection)  # Permitir selección unica para la salida
        self.target_selector.setVisible(False) 
        self.target_label.setVisible(False)

        # Confirmation button
        self.confirm_button = self.button.add_QPushButton("✅ Confirmar selección","Arial Black",10,None,None,False,
                                                          background_color="lightgreen",color="lightblack",padding="5px")
        self.button.set_QPushButton_hoverStyle(self.confirm_button,"green","white")
        self.confirm_button.clicked.connect(self.confirm_selection)

        # Create Regression Model Button
        self.create_model_button = self.button.add_QPushButton("📈 Crear Modelo de Regresión","Arial Black",10,None,None,False,
                                                               background_color="lightblue",color="lightblack",padding="10px")
        self.button.set_QPushButton_hoverStyle(self.create_model_button,"blue","white")  
        self.create_model_button.clicked.connect(self.show_results)

        widgets = [self.radio_layout,self.feature_label,self.feature_selector,
                   self.target_label,self.target_selector,self.confirm_button,
                   self.create_model_button
        ]
        self.layout.add_widget(self.regresion_layout,widgets)

    # -------------------------------------------------------------------------
    # Display Model Details
    # -------------------------------------------------------------------------
    def setup_model_details_step(self):
        """
        Sets up the UI components to display the details of a loaded regression model.
        """
        self.model_details_layout = QVBoxLayout()

        # Label for displaying the formula
        self.formula_label = LabelHelper.create_label(
            parent=self,
            text="Fórmula del Modelo: ",
            font=("Arial", 10),
            alignment=Qt.AlignLeft
        )

        # Label for displaying MSE
        self.mse_label = LabelHelper.create_label(
            parent=self,
            text="MSE: ",
            font=("Arial", 10),
            alignment=Qt.AlignLeft
        )

        # Label for displaying R²
        self.r_squared_label = LabelHelper.create_label(
            parent=self,
            text="R²: ",
            font=("Arial", 10),
            alignment=Qt.AlignLeft
        )

        # Text box for model description
        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Descripción del modelo cargado...")
        self.description_text.setReadOnly(True)

        # Add widgets to the layout
        widgets = [self.formula_label, self.mse_label, self.r_squared_label, self.description_text]
        self.layout.add_widget(self.model_details_layout, widgets)

        # Make the layout initially invisible
        self.layout_visibility(True, False, self.model_details_layout)

    #-------------------------------------------------------------------------
    # Next and Back Buttons:
    #-------------------------------------------------------------------------
    #Return Button
    def setup_navigation_buttons(self):
        self.back_layout = QVBoxLayout()
        self.return_button = QPushButton("<- Back")
        self.return_button.clicked.connect(self.back)
        self.return_button.setVisible(False)
        self.back_layout.addWidget(self.return_button)
        self.back_layout.setAlignment(Qt.AlignLeft)                

        # Next Button
        self.next_layout = QVBoxLayout()
        self.next_button = QPushButton("Next ->")
        self.next_button.clicked.connect(self.next)
        self.next_button.setVisible(False)
        self.next_button.setEnabled(False)
        self.next_layout.addWidget(self.next_button)
        self.next_layout.setAlignment(Qt.AlignRight)

        nav_buttons = [self.back_layout,self.next_layout]
        self.layout.add_widget(self.NBlayout,nav_buttons)

        # Configurar alineación para los botones "Next" y "Back"
        self.NBlayout.setAlignment(Qt.AlignBottom)

    def finalize_layout(self):
        

        layouts = [self.welcome_window,self.first_step_layout,self.nan_layout,
                    self.regresion_layout,self.NBlayout
        ]

        self.layout.add_widget(self.main_layout,layouts)

        # Añadir espaciadores y finalizar la estructura de la ventana
        items_spacer_layout = [self.steps_layout,self.layout_separator,self.main_layout]
        self.layout.add_widget(self.spacer_layout,items_spacer_layout)
        self.setLayout(self.spacer_layout)

        # Configurar las propiedades básicas de la ventana
        self.setWindowTitle('Visualizador de Datasets')
        self.setMinimumSize(800,600)

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

    
    def open_model_dialog(self):
        """
        Open a file dialog to load a model and display its details in a new window.
        """
        from model_loader import ModelLoader
        from model_window import ModelWindow

        # Create an instance of ModelLoader
        model_loader = ModelLoader(self)
        model_data = model_loader.load_model_dialog()  # Load model data

        if model_data:  # If model data is successfully loaded
            try:
                # Open a new window to display the model details
                self.model_window = ModelWindow(model_data)
                self.model_window.show()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Ocurrió un error al mostrar los detalles del modelo: {str(e)}")

    def load_data(self, file_path):
        try:
            self.df = import_data(file_path)
            if self.df is not None and not self.df.empty:
                self.display_data_in_table(self.df)
                # Enable buttons if data is loaded correctly
                self.file_label.setText(f'📂 Archivo cargado: {file_path}')
                detect_missing_values(self)
                self.populate_selectors(self.df) 
            else:
                QMessageBox.warning(self, "Advertencia", "El archivo está vacío o no se pudo cargar correctamente.")
        except pd.errors.EmptyDataError:
            QMessageBox.critical(self, "Error", "El archivo CSV está vacío. Por favor, selecciona otro archivo.")
        except pd.errors.ParserError:
            QMessageBox.critical(self, "Error", "El archivo CSV está corrupto o tiene un formato inválido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {str(e)}")

    
    def display_loaded_model(self, model_data):
        """
        Updates the UI to display details of a loaded model, including its formula,
        metrics, and description. It also hides the irrelevant sections of the interface.
        """
        # Ensure the regression step layout is displayed
        self.layout_visibility(True, False, self.main_layout)
        self.layout_visibility(True, True, self.model_details_layout)

        # Update labels and metrics
        self.formula_label.setText(f"Fórmula: {model_data['formula']}")
        self.mse_label.setText(f"MSE: {model_data.get('mse', 'N/A')}")
        self.r_squared_label.setText(f"R²: {model_data.get('r_squared', 'N/A')}")
        self.description_text.setText(model_data.get('description', 'Sin descripción disponible.'))

        # Hide irrelevant sections
        self.load_button.setVisible(False)
        self.load_model_button.setVisible(False)
        self.back_button.setVisible(False)
        self.preprocessing_options.setVisible(False)
        self.apply_button.setVisible(False)
        self.feature_selector.setVisible(False)
        self.target_selector.setVisible(False)
        self.confirm_button.setVisible(False)
        self.create_model_button.setVisible(False)

        # Adjust steps guide
        self.steps_guide()
        self.label.edit_label(
            self.third_step,
            text="Modelo cargado correctamente.",
            background_color="lightgreen",
            bold=True,
            padding="5px",
        )



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

    def preprocessing_button(self):
        if self.preprocessing_options.currentIndex() == 0:
            self.apply_button.setEnabled(False)
        else:
            self.apply_button.setEnabled(True)
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

            self.nan_data = False
            self.next_button.setEnabled(True)
            self.nan_solved = True
            self.label.edit_label(self.nan_label,text="There are no more empty values :)",color="green")
            self.layout.edit_separator(self.sep,color="green")
            self.layout.edit_separator(self.separator,color="green")
            self.nan_values.setVisible(False)
            self.nan_layout.removeWidget(self.nan_values)
            self.preprocessing_options.setEnabled(False)
            self.apply_button.setEnabled(False)

            # Redisplay the table after preprocessing
            self.display_data_in_table(self.df)  # Make sure the table is updated with the new content
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

    #-------------------------------------------------------------------------
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
        self.layout_separator.setVisible(True)
        self.drive_through()

    def next(self):
        if self.move < 3:
            if self.empty_values == True:
                self.move += 1
            else:
                self.move += 2
            self.drive_through()
                        
    def back(self):
        if self.move > 1:
            if self.empty_values == True:
                self.move -= 1
            else:
                self.move -= 2
            self.drive_through()
            
    def drive_through(self):
        self.layout_visibility(True,False,self.main_layout)
        self.layout_visibility(True,True,self.NBlayout)
        if self.move == 1:
            self.steps_guide()
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
            self.steps_guide()
            self.layout_visibility(True,True, self.nan_layout)
            self.table_view.setVisible(True)
            self.return_button.setEnabled(True)

            # Asegura que el botón de cargar datos siga oculto
            self.back_button.setVisible(False)
            self.file_label.setVisible(False)
            if self.nan_solved == False:
                self.next_button.setEnabled(False)
            else:
                self.next_button.setEnabled(True)
        
        elif self.move == 3:  # Paso 3: Crear modelo
            self.steps_guide()
            self.layout_visibility(True, True, self.regresion_layout)
            self.next_button.setEnabled(False)
            self.return_button.setEnabled(True)

    def steps_guide(self):
        text1 = "1. Load dataset or Load model"
        text2 = "2. Delete empty values"
        text3 = "3. Create linear regression model"
        if self.move == 1:
            self.label.edit_label(self.first_step,
            text=text1,
            background_color="lightgreen",
            bold=True,
            padding="5px"
            )
            self.label.edit_label(self.second_step,text="")
            self.label.edit_label(self.third_step,text="")

        elif self.move == 2:
            if self.nan_data == True:
                self.next_button.setEnabled(False)
            else:
                self.next_button.setEnabled(True)
            self.label.edit_label(self.second_step,
            text=text2,
            background_color="lightgreen",
            bold=True,
            padding="5px",
            )
            self.label.edit_label(self.first_step,text1)
            self.label.edit_label(self.third_step,text="")

        else:
            if self.empty_values == True:
                self.label.edit_label(self.third_step,
                text=text3,
                background_color="lightgreen",
                bold=True,
                padding="5px"
                )
                self.label.edit_label(self.second_step,text2)
            else:
                self.label.edit_label(self.third_step,
                text="2. Create linear regression model",
                background_color="lightgreen",
                bold=True,
                padding="5px"
                )
                self.second_step.setVisible(False)
            self.label.edit_label(self.first_step,text1)
            
    #-------------------------------------------------------------------------