import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont   
from PyQt5.QtCore import Qt

class ResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        vertical_layout = QVBoxLayout()

        # Texto
        self.result_label = QLabel("Descripción de mi modelo:")
        self.result_label.setFont(QFont("Arial",9))
        # Descripcion del ususario
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Escriba aquí su descripción...")

        vertical_layout.addWidget(self.result_label)
        vertical_layout.addWidget(self.text_box)

        self.setLayout(vertical_layout)
        self.setWindowTitle("Results")
        self.setMinimumSize(800,600)

app = QApplication([])
result = ResultWindow()
result.show()
app.exec_() 
