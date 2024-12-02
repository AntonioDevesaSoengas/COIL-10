# Third-party libraries.
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

# Local libraries.
from utils.helpers import LabelHelper


class WelcomeWindow(QWidget):
    """
    A QWidget-based class representing the welcome window of the application.

    Attributes:
        start_clicked (pyqtSignal): A signal emitted when the start button is clicked.
    """

    # Signal to indicate that the user has clicked "Start".
    start_clicked = pyqtSignal()

    def __init__(self, parent=None):
        """
        Initialize the WelcomeWindow with an optional parent widget.

        Args:
            parent (QWidget): The parent widget for this window. Default is None.
        """
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Set up the user interface for the welcome window.
        This includes labels, a button, and layout configuration.
        """
        # Main layout of the welcome window.
        layout = QVBoxLayout()

        # Create labels using LabelHelper with bold text.
        self.hello = LabelHelper.create_label(
            parent=self,
            text="¡Hello!",
            font=("Arial", 25),
            bold=True,
            visible=True
        )

        self.welcome_message = LabelHelper.create_label(
            parent=self,
            text="""<div style='text-align: center;'>
                    Welcome to "our app", here you will be able to<br>
                    upload your own datasets and create a linear<br>
                    regression based on them
                    </div>""",
            font=("Arial", 18),
            bold=False,
            visible=True
        )

        # Additional label to indicate that the user should click the button.
        self.start_label = LabelHelper.create_label(
            parent=self,
            text="Click here to start\n👇",
            font=("Arial", 12),
            visible=True
        )

        # Add top and bottom spacers with addStretch().
        layout.addStretch()  # Top spacer

        # Add labels to the main layout.
        layout.addWidget(self.hello, alignment=Qt.AlignCenter)
        layout.addSpacing(10)  # Space between "hello" and "welcome_message"
        layout.addWidget(self.welcome_message, alignment=Qt.AlignCenter)
        # Space between "welcome_message" and "start_label".
        layout.addSpacing(20)
        layout.addWidget(self.start_label, alignment=Qt.AlignCenter)

        # Create and style the start button.
        self.start_button = QPushButton("Start My Linear Regression")
        self.start_button.setStyleSheet("color: green; padding: 10px;")
        self.start_button.setFont(QFont("Arial", 12))
        self.start_button.clicked.connect(self.on_start_clicked)

        # Add the button to the main layout.
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        layout.addStretch()  # Bottom spacer

        # Configure the window.
        self.setLayout(layout)
        self.setWindowTitle("Welcome")

    def on_start_clicked(self):
        """
        Emit the start_clicked signal when the start button is pressed.
        """
        self.start_clicked.emit()

    def resizeEvent(self, event):
        """
        Adjust font sizes dynamically when the window is resized.

        Args:
            event (QResizeEvent): The resize event triggered by resizing the window.
        """
        window_width = self.width()

        if window_width < 1000:
            self.hello.setFont(QFont("Arial", 25))
            self.welcome_message.setFont(QFont("Arial", 18))
            self.start_label.setFont(QFont("Arial", 12))
            self.start_button.setFont(QFont("Arial", 12))
            self.setMinimumSize(800,600)
        else:
            self.hello.setFont(QFont("Arial", 45))
            self.welcome_message.setFont(QFont("Arial", 35))
            self.start_label.setFont(QFont("Arial", 16))
            self.start_button.setFont(QFont("Arial", 16))
            self.setMinimumSize(800,600)

        super().resizeEvent(event)
