from PyQt5.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Button():
    # Function to add a QPushButton 
    
    def add_QPushButton(
        self,text :str = "",font_type: str = "Arial",font_size: int = 12,
        width: int = None,height: int = None,visibility:bool = True,
        background_color: str = "",color:str = "",padding:str = ""
    ):
        button = QPushButton(text)

        # Establecer la fuente si se proporcionó
        if font_type or font_size:
            # Si alguno de los parámetros de fuente es None, QFont los manejará con valores predeterminados
            button.setFont(QFont(font_type, font_size if font_size else 12))

            # Ajustar el tamaño del botón
        if width is not None and height is not None:
            button.setFixedSize(width, height)
        elif width is not None:
            button.setFixedWidth(width)
        elif height is not None:
            button.setFixedHeight(height)
        
        # Establecer la visibilidad
        button.setVisible(visibility)
        
        # Construir el estilo CSS
        style = ""
        if background_color:
            style += f"background-color: {background_color}; "
        if color:
            style += f"color: {color}; "
        if padding:
            style += f"padding: {padding};"
        
        # Aplicar el estilo al botón si se ha definido alguno
        if style:
            button.setStyleSheet(style)

        self.background_color = background_color
        self.color = color
        self.padding = padding
        
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


    # Function to set the QPushButton Style Sheet when hover
    def set_QPushButton_hoverStyle(self,button,background_color:str,color:str):
        StyleSheet = "\nQPushButton{"+f"background-color:{self.background_color};color:{self.color};padding:{self.padding};"+"}QPushButton:hover{"+f"background-color:{background_color};color:{color};"+"}"
        button.setStyleSheet(StyleSheet)
