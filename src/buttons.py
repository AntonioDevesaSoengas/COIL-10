from PyQt5.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Button():
    # Function to add a QPushButton 
    def add_QPushButton(self,text:str,font_type:str,font_size:int,width:int,height:int,visibility:bool):
        button = QPushButton(text)
        button.setFont(QFont(font_type,font_size))
        if height is not None or width is not None:
            if width is None:
                button.setMaximumHeight(height)
            elif height is None:
                button.setMaximumWidth(width)
            else:
                button.setFixedSize(width,height)
        button.setVisible(visibility)
        return button

    # Function to add a QRadioButton
    def add_QRadioButton(self,text:str,font_type:str,font_size:str,width:int,height:int,visibility:bool):
        button = QRadioButton(text)
        button.setFont(QFont(font_type,font_size))
        if height is not None or width is not None:
            if width == None:
                button.setMaximumHeight(height)
            elif height == None:
                button.setMaximumWidth(width)
            else:
                button.setFixedSize(width,height)
        button.setVisible(visibility)
        return button
    
    # Function to add a QComboBox
    def add_QComboBox(self,items:list,width:int,height:int,visibility:bool):
            button = QComboBox()
            button.addItems(items)
            if height is not None or width is not None:
                if width == None:
                    button.setMaximumHeight(height)
                elif height == None:
                    button.setMaximumWidth(width)
                else:
                    button.setFixedSize(width,height)
            button.setVisible(visibility)
            return button

    # Function to set the Button Style Sheet
    def set_StyleSheet(self,button,background_color:str,color:str,padding:str):
        button.setStyleSheet(f"background-color:{background_color}; color: {color}; padding: {padding};")
        self.background_color = background_color
        self.color = color
        self.padding = padding

    # Function to set the QPushButton Style Sheet when hover
    def set_QPushButton_hoverStyle(self,button,background_color:str,color:str):
        StyleSheet = "\nQPushButton{"+f"background-color:{self.background_color};color:{self.color};padding:{self.padding};"+"}QPushButton:hover{"+f"background-color:{background_color};color:{color};"+"}"
        button.setStyleSheet(StyleSheet)

    # Function to change the Button Font and Size
    def change_style(self,button,font_type:str,font_size:int,width:int,height:int):
        button.setFont(QFont(font_type,font_size))
        if height is not None or width is not None:
            if width == None:
                button.setMaximumHeight(height)
            elif height == None:
                button.setMaximumWidth(width)
            else:
                button.setFixedSize(width,height)
        