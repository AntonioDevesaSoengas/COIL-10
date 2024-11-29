from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QTextEdit, QWidget
from PyQt5.QtCore import Qt

class ModelWindow(QMainWindow):
    def __init__(self, model_data):
        super().__init__()
        self.setWindowTitle("Detalles del Modelo")
        self.setGeometry(100, 100, 600, 400)

        # Crear layout principal
        layout = QVBoxLayout()

        # Mostrar la fórmula del modelo
        formula_label = QLabel(f"Fórmula: {model_data['formula']}")
        formula_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(formula_label)

        # Mostrar el MSE
        mse_label = QLabel(f"MSE: {model_data.get('mse', 'N/A')}")
        mse_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(mse_label)

        # Mostrar el R²
        r_squared_label = QLabel(f"R²: {model_data.get('r_squared', 'N/A')}")
        r_squared_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(r_squared_label)

        # Mostrar la descripción
        description_text = QTextEdit()
        description_text.setText(model_data.get('description', 'Sin descripción disponible.'))
        description_text.setReadOnly(True)
        layout.addWidget(description_text)

        # Contenedor principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
