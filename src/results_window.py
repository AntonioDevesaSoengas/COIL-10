import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont   
from PyQt5.QtCore import Qt
from features import DataViewer
from scikit_learn import regresion_lineal

class ResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.main_window = DataViewer
        

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
    def Regresion_lineal(self):
        regresion_lineal(self.main_window.df,self.main_window.columnas_entrada,self.main_window.columna_salida)
        


app = QApplication([])
result = ResultWindow()
result.show()
app.exec_() 
main_window = DataViewer()
print(main_window.df)
