import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox

# Función del botón
def show_message():
    input = text.text() 
    QMessageBox.information(window, "Mensaje", f"Has escrito: {input}")

# Inicializar
app = QApplication(sys.argv)

# Layout para organizar widgets (botones, cuadros de texto,...)
layout = QVBoxLayout()

# Ventana principal
window = QWidget()
window.setWindowTitle('Interfaz Gráfica PyQt')
window.resize(300,200)

# Cuadro de texto
text = QLineEdit()
text.setPlaceholderText('Buscar...')
layout.addWidget(text)

# Botón
button = QPushButton('Press')
button.clicked.connect(show_message)
layout.addWidget(button)

# Asignar layout a la ventana
window.setLayout(layout)

#Ejecución
window.show()
sys.exit(app.exec_())
