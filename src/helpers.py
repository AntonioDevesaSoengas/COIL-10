from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LabelHelper:
    @staticmethod
    def create_label(self, text="", font=None, bold=False, italic=False, 
                     html=False, alignment=Qt.AlignCenter, background_color=None):
        """
        Crea una QLabel con el texto, fuente, alineación y estilos especificados.
        
        :param text: Texto a mostrar en la etiqueta.
        :param font: Tupla (familia, tamaño).
        :param bold: Booleano para activar la negrita.
        :param italic: Booleano para activar la cursiva.
        :param html: Booleano para interpretar el texto como HTML.
        :param alignment: Alineación del texto (Qt.AlignLeft, Qt.AlignCenter, etc.).
        :param background_color: Color de fondo en formato CSS (e.g., "#FFFFFF" o "red").
        :param word_wrap: Booleano para activar el ajuste automático de texto.
        :return: QLabel configurada.
        """
        label = QLabel()
        if html:
            label.setText(text)  # Texto con etiquetas HTML
        else:
            label.setText(text)
            if font:
                qfont = QFont(font[0], font[1])
                qfont.setBold(bold)
                qfont.setItalic(italic)  # Activar cursiva
                label.setFont(qfont)
        
        # Configurar alineación
        label.setAlignment(alignment)

        # Aplicar estilo de fondo y negrita si no es HTML
        style = ""
        if background_color:
            style += f"background-color: {background_color};"
        if bold and not html:
            style += "font-weight: bold;"
        if italic and not html:
            style += "font-style: italic;"
        if style:
            label.setStyleSheet(style)
        
        return label
