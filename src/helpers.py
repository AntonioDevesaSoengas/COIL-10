# Third-party libraries
from PyQt5.QtWidgets import QLabel, QPushButton, QRadioButton, QComboBox, QFrame, QWidget, QSpacerItem, QLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class LabelHelper:
    @staticmethod
    def create_label(parent, text="", font=None, bold=False, italic=False,
                     html=False, alignment=Qt.AlignCenter, background_color=None, word_wrap=False):
        """
        Creates a QLabel with the specified text, font, alignment, and styles.

        :param parent: The parent widget.
        :param text: Text to display in the label.
        :param font: Tuple (family, size).
        :param bold: Boolean to enable bold text.
        :param italic: Boolean to enable italic text.
        :param html: Boolean to interpret the text as HTML.
        :param alignment: Text alignment (Qt.AlignLeft, Qt.AlignCenter, etc.).
        :param background_color: Background color in CSS format (e.g., "#FFFFFF" or "red").
        :param word_wrap: Boolean to enable automatic text wrapping.
        :return: Configured QLabel.
        """
        label = QLabel(parent)
        if html:
            label.setText(text)  # Text with HTML tags
        else:
            label.setText(text)
            if font:
                qfont = QFont(font[0], font[1])
                qfont.setBold(bold)
                qfont.setItalic(italic)  # Enable italic
                label.setFont(qfont)

        # Set alignment
        label.setAlignment(alignment)

        # Enable word wrapping if specified
        label.setWordWrap(word_wrap)

        # Apply background color and styles if not using HTML
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

    @staticmethod
    def edit_label(label, text=None, font=None, bold=None, italic=None,
                   html=None, alignment=None, background_color=None, word_wrap=None):
        """
        Edits the properties of an existing QLabel.

        :param label: QLabel to modify.
        :param text: New text for the QLabel.
        :param font: Tuple (family, size).
        :param bold: Boolean to enable/disable bold text.
        :param italic: Boolean to enable/disable italic text.
        :param html: Boolean to interpret the text as HTML.
        :param alignment: New text alignment (Qt.AlignLeft, Qt.AlignCenter, etc.).
        :param background_color: New background color in CSS format.
        :param word_wrap: Boolean to enable/disable automatic text wrapping.
        """
        if html is not None:
            if html:
                label.setText(text)  # Text interpreted as HTML
            elif text is not None:
                label.setText(text)  # Text without HTML
        elif text is not None:
            label.setText(text)

        if font:
            qfont = QFont(font[0], font[1])
            if bold is not None:
                qfont.setBold(bold)
            if italic is not None:
                qfont.setItalic(italic)
            label.setFont(qfont)
        elif bold is not None or italic is not None:
            # Modify the current font if bold or italic is specified but no new font
            qfont = label.font()
            if bold is not None:
                qfont.setBold(bold)
            if italic is not None:
                qfont.setItalic(italic)
            label.setFont(qfont)

        if alignment is not None:
            label.setAlignment(alignment)

        if word_wrap is not None:
            label.setWordWrap(word_wrap)

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


class ButtonHelper:
    def add_QPushButton(self, text: str, font_type: str, font_size: int, width: int, height: int, visibility: bool,
                        background_color: str = None, color: str = None, padding: str = None):
        """
        Creates a QPushButton with the specified properties and optional stylesheet.

        :param text: Button text.
        :param font_type: Font family.
        :param font_size: Font size.
        :param width: Button width.
        :param height: Button height.
        :param visibility: Button visibility.
        :param background_color: Background color for the button.
        :param color: Text color for the button.
        :param padding: Padding for the button's content.
        :return: Configured QPushButton.
        """
        button = QPushButton(text)
        button.setFont(QFont(font_type, font_size))

        # Set size
        if height is not None or width is not None:
            if width is None:
                button.setMaximumHeight(height)
            elif height is None:
                button.setMaximumWidth(width)
            else:
                button.setFixedSize(width, height)

        # Apply visibility
        button.setVisible(visibility)

        # Build and apply stylesheet
        style = ""
        if background_color:
            style += f"background-color: {background_color};"
        if color:
            style += f"color: {color};"
        if padding:
            style += f"padding: {padding};"

        if style:  # Apply stylesheet only if there's something to apply
            button.setStyleSheet(style)

        return button

    def add_QRadioButton(self, text: str, font_type: str, font_size: str, width: int, height: int, visibility: bool):
        """
        Creates a QRadioButton with specified properties.
        """
        button = QRadioButton(text)
        button.setFont(QFont(font_type, font_size))
        if height is not None or width is not None:
            if width is None:
                button.setMaximumHeight(height)
            elif height is None:
                button.setMaximumWidth(width)
            else:
                button.setFixedSize(width, height)
        button.setVisible(visibility)
        return button

    def add_QComboBox(self, items: list, width: int, height: int, visibility: bool):
        """
        Creates a QComboBox with specified properties.
        """
        button = QComboBox()
        button.addItems(items)
        if height is not None or width is not None:
            if width is None:
                button.setMaximumHeight(height)
            elif height is None:
                button.setMaximumWidth(width)
            else:
                button.setFixedSize(width, height)
        button.setVisible(visibility)
        return button

    def set_QPushButton_hoverStyle(self, button, background_color: str, color: str):
        """
        Sets the QPushButton hover style.
        """
        StyleSheet = (
            "\nQPushButton{"
            f"background-color:{self.background_color};color:{self.color};padding:{self.padding};"
            "}QPushButton:hover{"
            f"background-color:{background_color};color:{color};"
            "}"
        )
        button.setStyleSheet(StyleSheet)

    def change_style(self, button, font_type: str, font_size: int, width: int, height: int):
        """
        Changes the QPushButton font and size.
        """
        button.setFont(QFont(font_type, font_size))
        if height is not None or width is not None:
            if width is None:
                button.setMaximumHeight(height)
            elif height is None:
                button.setMaximumWidth(width)
            else:
                button.setFixedSize(width, height)


class LayoutHelper:
    def layout_add_widget(self, layout, widgets: list):
        """
        Adds widgets into a layout.
        """
        for item in widgets:
            if isinstance(item, QWidget):
                layout.addWidget(item)
            elif isinstance(item, QFrame):
                layout.addWidget(item)
            elif isinstance(item, QLayout):
                if item.parent() is None:
                    layout.addLayout(item)
                else:
                    QMessageBox.warning(None, "Warning", "This layout already has a parent")
            elif isinstance(item, QSpacerItem):
                layout.addItem(item)
            else:
                QMessageBox.critical(None, "Error", "You are trying to add an undefined item")

    def layout_add_separator(self, type: str, width: int, visibility: bool):
        """
        Adds a separator (vertical or horizontal) to the layout.
        """
        separator = QFrame()
        if type.lower() == "vertical":
            separator.setFrameShape(QFrame.VLine)
        elif type.lower() == "horizontal":
            separator.setFrameShape(QFrame.HLine)
        if width is not None:
            separator.setLineWidth(width)
        separator.setVisible(visibility)
        return separator

    def layout_visibility(self, sublayouts: bool, visibility: bool, layout):
        """
        Controls the visibility of an entire layout, including widgets and sublayouts.

        :param sublayouts: Whether to apply visibility to sublayouts.
        :param visibility: True to show, False to hide.
        :param layout: The layout to modify.
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if item.widget():  # If the item is a widget
                item.widget().setVisible(visibility)

            elif item.layout() and sublayouts:  # If the item is another layout
                self.layout_visibility(True, visibility, item.layout())
