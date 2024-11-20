# welcome_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from helpers import LabelHelper

class WelcomeWindow(QWidget):
    # Señal para indicar que el usuario ha hecho clic en "Start"
    start_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        # Layout principal de la ventana de bienvenida
        layout = QVBoxLayout()
        
        # Crear etiquetas usando LabelHelper con negrita
        self.hello = LabelHelper.create_label(
            parent=self,
            text="Hello",
            font=("Arial", 25),
            bold=True
        )
        
        self.welcome_message = LabelHelper.create_label(
            parent=self,
            text="""Welcome to "our app", here you will be able to 
upload your own datasets and create a linear 
regression based on them""",
            font=("Arial", 18),
            bold=False
        )
        
        # Etiqueta adicional para indicar al usuario que haga clic en el botón
        self.start_label = QLabel("Click here to start\n👇")
        self.start_label.setAlignment(Qt.AlignCenter)
        self.start_label.setFont(QFont("Arial", 12))  # Tamaño de fuente ajustado

        # Agregar espaciadores superiores e inferiores con addStretch()
        layout.addStretch()  # Espaciador superior
        
        # Agregar etiquetas al layout principal
        layout.addWidget(self.hello, alignment=Qt.AlignCenter)
        layout.addWidget(self.welcome_message, alignment=Qt.AlignCenter)
        layout.addWidget(self.start_label, alignment=Qt.AlignCenter)
        
        # Botón de inicio
        self.start_button = QPushButton("Start My Linear Regression")
        self.start_button.setStyleSheet("color: green; padding: 10px;")
        self.start_button.setFont(QFont("Arial", 12))
        self.start_button.clicked.connect(self.on_start_clicked)
        
        # Agregar botón al layout principal
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        
        layout.addStretch()  # Espaciador inferior
        
        self.setLayout(layout)
        self.setWindowTitle('Welcome')
        self.setMinimumSize(800, 600)
    
    def on_start_clicked(self):
        """Emite la señal start_clicked cuando el botón es presionado."""
        self.start_clicked.emit()

    def resizeEvent(self, event):
        """Ajusta las fuentes cuando la ventana es redimensionada."""
        window_width = self.width()
        
        if window_width < 1000:
            self.hello.setFont(QFont("Arial", 25))
            self.welcome_message.setFont(QFont("Arial", 18))
            self.start_label.setFont(QFont("Arial", 12))
            self.start_button.setFont(QFont("Arial", 12))
        else:
            self.hello.setFont(QFont("Arial", 45))
            self.welcome_message.setFont(QFont("Arial", 35))
            self.start_label.setFont(QFont("Arial", 16))
            self.start_button.setFont(QFont("Arial", 16))
        
        super().resizeEvent(event)
