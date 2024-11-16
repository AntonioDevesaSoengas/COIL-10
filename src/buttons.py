from PyQt5.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Button():
    
    def add_QPushButton(self,text:str,font_type:str,font_size:int,height:int,width:int,visibility:bool):
        button = QPushButton(text)
        button.setFont(QFont(font_type,font_size))
        if width == None:
            button.setMinimumHeight(height)
        if height == None:
            button.setMinimumWidth(width)
        else:
            button.setMinimumSize(width,height)
        button.setVisible(visibility)
        return button

    def add_QRadioButton(self,text:str,font_type:str,font_size:str,height:int,width:int,visibility:bool):
        button = QRadioButton(text)
        button.setFont(QFont(font_type,font_size))
        if width == None:
            button.setMinimumHeight(height)
        if height == None:
            button.setMinimumWidth(width)
        else:
            button.setMinimumSize(width,height)
        button.setVisible(visibility)
        return button