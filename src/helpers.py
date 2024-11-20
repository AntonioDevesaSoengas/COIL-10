# helpers.py
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont

class LabelHelper:
    @staticmethod
    def create_label(parent, text="", font=None, bold=False, html=False):
        """
        Crea una QLabel con el texto y la fuente especificados.
        
        :param parent: El widget padre.
        :param text: Texto a mostrar en la etiqueta.
        :param font: Tupla (familia, tamaño).
        :param bold: Booleano para activar la negrita.
        :param html: Booleano para interpretar el texto como HTML.
        :return: QLabel configurada.
        """
        label = QLabel(parent)
        if html:
            label.setText(text)  # Texto con etiquetas HTML
        else:
            label.setText(text)
            if font:
                qfont = QFont(font[0], font[1])
                qfont.setBold(bold)
                label.setFont(qfont)
            if bold:
                label.setStyleSheet("font-weight: bold;")
        return label
