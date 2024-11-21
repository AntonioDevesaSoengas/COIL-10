import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QSpacerItem, QLabel, QTableView, QRadioButton,
    QListWidget, QAbstractItemView, QPushButton,
    QFileDialog, QHeaderView, QStackedWidget,QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from import_files import import_data
from data_preprocessing import *
from table import Table
from buttons import Button
from helpers import LabelHelper
from welcome_window import WelcomeWindow
from load_data_window import LoadData
from preprocessing_window import PreProcessing


class DataViewer(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configuración inicial de la ventana principal
        self.setWindowTitle("Linear Regression App")
        self.resize(800, 600)
        
        # Layout principal vertical
        self.main_layout = QVBoxLayout()
        
        # QStackedWidget para manejar diferentes ventanas
        self.stack = QStackedWidget()

        # Instanciar las ventanas que se agregarán al stack
        self.welcome = WelcomeWindow()
        self.load_data = LoadData(on_data_loaded=self.data_loaded_callback)
        self.preprocessing = PreProcessing()
        
        # Conectar el botón de inicio para navegar a la siguiente página
        self.welcome.start_button.clicked.connect(self.show_load_data)

        # Agregar las ventanas al stack
        self.stack.addWidget(self.welcome)      # Índice 0
        self.stack.addWidget(self.load_data)    # Índice 1
        self.stack.addWidget(self.preprocessing)
        # Agrega más ventanas aquí si las tienes

        # Agregar el stack al layout principal
        self.main_layout.addWidget(self.stack)

        # Agregar los botones de navegación
        self.add_navigation_buttons()

        # Establecer el layout principal
        self.setLayout(self.main_layout)

    def add_navigation_buttons(self):
        """Crea y agrega los botones de navegación al layout principal."""
        # Crear un layout horizontal para los botones
        nav_layout = QHBoxLayout()

        # Instanciar la clase Button para crear botones estilizados
        self.button_helper = Button()

        # Crear el botón "Anterior"
        self.prev_button = self.button_helper.add_QPushButton(
            text="Anterior",
            font_type="Arial",
            font_size=12,
            width=120,
            height=40,
            background_color="#CCCCCC",
            color="black",
            padding="5px",
            visibility=False
        )
        self.prev_button.clicked.connect(self.go_previous)

        # Crear el botón "Siguiente"
        self.next_button = self.button_helper.add_QPushButton(
            text="Siguiente",
            font_type="Arial",
            font_size=12,
            width=120,
            height=40,
            background_color="#4CAF50",
            color="white",
            padding="5px",
            visibility=False
        )
        self.next_button.clicked.connect(self.go_next)

        # Inicialmente, deshabilitar el botón "Anterior" ya que estamos en la primera página
        self.prev_button.setEnabled(False)

        # Agregar el botón "Anterior" al layout alineado a la izquierda
        nav_layout.addWidget(self.prev_button, alignment=Qt.AlignLeft)

        # Agregar un espaciador flexible para separar los botones
        nav_layout.addStretch()

        # Agregar el botón "Siguiente" al layout alineado a la derecha
        nav_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

        # Agregar el layout de navegación al layout principal
        self.main_layout.addLayout(nav_layout)

        # Conectar la señal de cambio de página para actualizar el estado de los botones
        self.stack.currentChanged.connect(self.update_navigation_buttons)


    def data_loaded_callback(self, df):
        """Callback que se ejecuta cuando los datos han sido cargados."""
        # Habilitar el botón "Siguiente" ya que los datos han sido cargados
        self.next_button.setEnabled(True)

    def show_load_data(self):
        """Navega a la ventana de carga de datos."""
        self.stack.setCurrentWidget(self.load_data)

    def show_preprocessing(self):
        """Navega a la ventana de preprocesamiento."""
        self.stack.setCurrentWidget(self.preprocessing)

    def go_previous(self):
        """Navega a la página anterior en el stack."""
        current_index = self.stack.currentIndex()
        if current_index > 1:
            self.stack.setCurrentIndex(current_index - 1)

    def go_next(self):
        """Navega a la página siguiente en el stack."""
        current_index = self.stack.currentIndex()
        if current_index == 1:  # Si estamos en LoadData
            df = self.load_data.actualizar_datos()
            if df is None:
                QMessageBox.warning(self, "Error", "No hay datos cargados. Por favor, carga un archivo primero.")
                return
            self.preprocessing.set_dataframe(df)
            self.stack.setCurrentWidget(self.preprocessing)
        elif current_index < self.stack.count() - 1:
            self.stack.setCurrentIndex(current_index + 1)

    def update_navigation_buttons(self):
        """Actualiza el estado de los botones de navegación según la página actual."""
        current_index = self.stack.currentIndex()
        total_pages = self.stack.count()

        # Mostrar u ocultar botones según la página actual
        if current_index == 0:
            self.prev_button.setVisible(False)
            self.next_button.setVisible(True)
            self.next_button.setText("Siguiente")
        elif current_index == 1:
            self.prev_button.setVisible(True)
            self.next_button.setVisible(True)
            self.next_button.setText("Siguiente")
        elif current_index == 2:
            self.prev_button.setVisible(True)
            self.next_button.setVisible(False)
        else:
            self.prev_button.setVisible(True)
            self.next_button.setVisible(True)

        # Configurar habilitación de botones
        if current_index == 0:
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(True)
        elif current_index == total_pages - 1:
            self.next_button.setEnabled(False)
            self.prev_button.setEnabled(True)
        else:
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = DataViewer()
    viewer.show()
    sys.exit(app.exec_())
