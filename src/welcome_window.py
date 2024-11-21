from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from helpers import LabelHelper
from layouts import Layout
from buttons import Button


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = LabelHelper()
        self.layout = Layout()
        self.button = Button()

        # Main layout of the welcome window
        welcome_layout = QVBoxLayout()
        welcome_layout.setAlignment(Qt.AlignCenter)

        # Create labels using LabelHelper with bold text
        self.hello = LabelHelper.create_label(
            self,
            text="¡Hello!",
            font=("Arial", 25),
            bold=True
        )

        self.welcome_message = LabelHelper.create_label(
            self,
            text="""<div style='text-align: center;'>
                    Welcome to "our app", here you will be able to<br>
                    upload your own datasets and create a linear<br>
                    regression based on them
                    </div>""",
            font=("Arial", 18),
            bold=False
        )

        # Additional label to indicate that the user should click the button
        self.start_label = LabelHelper.create_label(
            self,
            text="Click here to start\n👇",
            font=("Arial", 12)
        )
        
        # Create and style the start button
        self.start_button = self.button.add_QPushButton(
            text="Start My Linear Regression",
            color="green",padding="10px",
            font_type="Arial",font_size=12
            )

        widgets = [self.hello, self.welcome_message,self.start_label,self.start_button]

        self.layout.add_Widget(welcome_layout,widgets)
        self.setLayout(welcome_layout)

    def resizeEvent(self, event):
        """Adjust fonts when the window is resized."""
        window_width = self.width()

        if window_width < 1000:
            self.hello.setFont(QFont("Arial", 25))
            self.welcome_message.setFont(QFont("Arial", 18))
            self.start_label.setFont(QFont("Arial", 12))
            self.start_button.setFont(QFont("Arial", 12))
        else:
            self.hello.setFont(QFont("Arial", 45))
            self.welcome_message.setFont(QFont("Arial", 35))
            self.start_label.setFont(QFont("Arial", 16))
            self.start_button.setFont(QFont("Arial", 16))

        super().resizeEvent(event)
