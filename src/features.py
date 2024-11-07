import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox, QInputDialog, QFileDialog, QListWidget, QAbstractItemView, QRadioButton, QHBoxLayout
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

    def initUI(self):
        # Layout principal
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

        # Botón para ir hacia atrás y elegir otro archivo
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

        # Tabla para mostrar los datos
        self.data_table = QTableWidget()
        self.data_table.setFont(QFont('Arial', 10))
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        layout.addWidget(self.data_table)

        # Etiqueta para mostrar la ruta del archivo cargado
        self.file_label = QLabel('📂 Ruta del archivo cargado:')
        self.file_label.setFont(QFont('Arial', 10))
        layout.addWidget(self.file_label)

        # Botón para detección de valores inexistentes
        self.detect_button = QPushButton('🔍 Detectar', self)
        self.detect_button.clicked.connect(self.handle_detect_missing_values)
        self.detect_button.setEnabled(False)
        layout.addWidget(self.detect_button)

        # Menú desplegable para opciones de preprocesado
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

        # Botón de confirmación para aplicar el preprocesado
        self.apply_button = QPushButton('🟢 Aplicar Preprocesado', self)
        self.apply_button.setFont(QFont('Arial Black', 8))
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.confirm_preprocessing)
        layout.addWidget(self.apply_button)

        # Radio buttons para seleccionar el tipo de regresión
        self.radio_simple = QRadioButton("Regresión Simple")
        self.radio_multiple = QRadioButton("Regresión Múltiple")
        self.radio_simple.setChecked(True)  # Por defecto, regresión simple
        self.radio_simple.toggled.connect(self.update_feature_selector)
        self.radio_multiple.toggled.connect(self.update_feature_selector)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_simple)
        radio_layout.addWidget(self.radio_multiple)
        layout.addLayout(radio_layout)

        # Selector de columnas (features)
        self.feature_selector = QListWidget(self)
        self.feature_selector.setSelectionMode(QAbstractItemView.SingleSelection)  # Por defecto, solo una selección (regresión simple)
        self.feature_selector.setEnabled(False)  # Inicia desactivado hasta que cargues datos
        layout.addWidget(QLabel("Columnas de Entrada (Features)"))
        layout.addWidget(self.feature_selector)

        # Selector simple para la columna de salida (target)
        self.target_selector = QListWidget(self)
        self.target_selector.setSelectionMode(QAbstractItemView.MultiSelection)  # Permitir selección múltiple para la salida
        self.target_selector.setEnabled(False)  # Inicia desactivado hasta que cargues datos
        layout.addWidget(QLabel("Columnas de Salida (Target)"))
        layout.addWidget(self.target_selector)

        # Botón de confirmación
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

        # Configurar layout
        self.setLayout(layout)
        self.setWindowTitle('Visualizador de Datasets')
        self.resize(800, 600)  # Tamaño de la ventana ajustado

    def open_file_dialog(self):
        # Abrir el explorador de archivos con QFileDialog de PyQt5
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo", "", 
                                                   "Archivos CSV (*.csv);;Archivos Excel (*.xlsx *.xls);;Bases de datos SQLite (*.sqlite *.db)")
        if file_path:
            if self.last_file_path == file_path:
                # Mostrar mensaje y opciones de confirmación si es el mismo archivo
                result = QMessageBox.question(self, "Advertencia", 
                    "Estás seleccionando el mismo archivo que ya has cargado. ¿Deseas cargarlo de nuevo?",
                    QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.No:
                    return
                elif result == QMessageBox.Yes:
                    self.load_data(file_path)  # Recargar el dataset directamente sin abrir el explorador
        
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
                # Habilitar botones si se cargan los datos correctamente
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

        # Ajustar tamaño de tabla
        self.data_table.resizeColumnsToContents()
        self.data_table.resizeRowsToContents()
        self.data_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.data_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Asegurarse de que la tabla ocupa todo el ancho del marco
        for j in range(len(data.columns)):
            self.data_table.setColumnWidth(j, self.data_table.width() // len(data.columns))  # Ajustar el ancho de cada columna

        # Deshabilitar boton Cargar Datasets
        self.load_button.setVisible(False)

    def resizeEvent(self, event):
        # Ajustar el tamaño de la tabla al redimensionar la ventana
        self.data_table.setFixedWidth(self.width() - 40)  # Ajustar con un margen
        super().resizeEvent(event)

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

        # Actualizar la selección de features basado en el tipo de regresión seleccionada
        self.update_feature_selector()

    def update_feature_selector(self):
        if self.radio_simple.isChecked():
            # Regresión simple: Solo una selección permitida
            self.feature_selector.setSelectionMode(QAbstractItemView.SingleSelection)
        else:
            # Regresión múltiple: Selección múltiple permitida
            self.feature_selector.setSelectionMode(QAbstractItemView.MultiSelection)

    def confirm_selection(self):
        # Obtener las selecciones de features
        selected_features = [item.text() for item in self.feature_selector.selectedItems()]
        # Obtener la selección de target
        selected_target = [item.text() for item in self.target_selector.selectedItems()]

        if not selected_features or not selected_target:
            QMessageBox.warning(self, "Selección incompleta", "Debes seleccionar al menos una columna de entrada y una de salida.")
            return

        # Mostrar mensaje de éxito con las selecciones
        QMessageBox.information(self, "Selección confirmada", f"Has seleccionado las columnas de entrada: {', '.join(selected_features)} y la columna de salida: {', '.join(selected_target)}.")

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

    # Función de Preprocesado para detectar Valores Inexistentes
    def handle_detect_missing_values(self):
        if self.df is not None:
            message = detect_missing_values(self.df)
            QMessageBox.information(self, "Detección de Valores Inexistentes", message)

    # Aplicar la opción de preprocesado seleccionada en el ComboBox
    def confirm_preprocessing(self):  # NUEVO: Confirmar y aplicar preprocesado
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

            # Volver a mostrar la tabla después del preprocesado
            self.display_data_in_table(self.df)  # Asegúrate de que se actualice la tabla con el nuevo contenido

            QMessageBox.information(self, "Éxito", "Preprocesado aplicado con éxito.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al aplicar el preprocesado: {str(e)}")
