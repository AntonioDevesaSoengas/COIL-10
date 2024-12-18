from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QAbstractItemView, QRadioButton, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class ColumnSelectionWindow(QWidget):
    """
    Class to handle column selection for regression models.
    """
    
    selection_done = pyqtSignal(list, list)
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.df = None  # DataFrame to select columns from
        self.input_columns = []
        self.output_column = []

        # Initialize UI components
        self.initUI()

    def initUI(self):
        """
        Set up the user interface components for column selection.
        """
        self.layout = QVBoxLayout()

        # Title label
        self.title_label = QLabel("Select Columns for Regression")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Radio buttons for regression type
        self.radio_layout = QHBoxLayout()
        self.radio_simple = QRadioButton("Simple Regression")
        self.radio_multiple = QRadioButton("Multiple Regression")
        self.radio_simple.setChecked(True)
        self.radio_simple.toggled.connect(self.update_selection_mode)
        self.radio_layout.addWidget(self.radio_simple)
        self.radio_layout.addWidget(self.radio_multiple)
        self.layout.addLayout(self.radio_layout)

        # Input columns list
        self.input_label = QLabel("Input Columns (Features):")
        self.layout.addWidget(self.input_label)
        self.input_selector = QListWidget()
        self.input_selector.setSelectionMode(QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.input_selector)

        # Output column list
        self.output_label = QLabel("Output Column (Target):")
        self.layout.addWidget(self.output_label)
        self.output_selector = QListWidget()
        self.output_selector.setSelectionMode(QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.output_selector)

        # Confirm button
        self.confirm_button = QPushButton("✅ Confirm Selection")
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.layout.addWidget(self.confirm_button)
        
        # Botón para generar el modelo
        self.generate_model_button = QPushButton("Generate Model")
        self.generate_model_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.generate_model_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)
        self.generate_model_button.clicked.connect(self.generate_model)
        self.layout.addWidget(self.generate_model_button)

        # Set layout
        self.setLayout(self.layout)
        self.setWindowTitle("Column Selection")
        self.setMinimumSize(600, 400)

        # Populate selectors
        self.populate_selectors()

    def populate_selectors(self):
        """
        Populate the input and output selectors with DataFrame columns.
        """
        if self.df is not None:
            columns = self.df.columns.tolist()
            self.input_selector.addItems(columns)
            self.output_selector.addItems(columns)

    def update_selection_mode(self):
        """
        Update the selection mode based on the selected regression type.
        """
        if self.radio_simple.isChecked():
            self.input_selector.setSelectionMode(QAbstractItemView.SingleSelection)
        else:
            self.input_selector.setSelectionMode(QAbstractItemView.MultiSelection)

    def set_dataframe(self, dataframe):
        """
        Set the DataFrame for column selection.
        """
        self.df = dataframe

        if self.df is not None:
            columns = self.df.columns.tolist()
            self.input_selector.clear()
            self.input_selector.addItems(columns)
            self.output_selector.clear()
            self.output_selector.addItems(columns)

    def confirm_selection(self):
        """
        Confirm the selected columns and validate the choices.
        """
        self.input_columns = [item.text() for item in self.input_selector.selectedItems()]
        self.output_column = [item.text() for item in self.output_selector.selectedItems()]

        if not self.input_columns:
            QMessageBox.warning(self, "Warning", "You must select at least one input column.")
            return

        if not self.output_column:
            QMessageBox.warning(self, "Warning", "You must select an output column.")
            return

        self.selection_done.emit(self.input_columns, self.output_column)

        QMessageBox.information(
            self,
            "Selection Confirmed",
            f"Input columns: {', '.join(self.input_columns)}\nOutput column: {', '.join(self.output_column)}"
        )
    
    def get_selections(self):
        """
        Returns the selected input and output columns.
        """
        return self.input_columns, self.output_column
    
    def generate_model(self):
        """
        Emits the selected input and output columns to create the model.
        """
        input_columns = [item.text() for item in self.input_selector.selectedItems()]
        output_column = [item.text() for item in self.output_selector.selectedItems()]

        if not input_columns or not output_column:
            QMessageBox.warning(self, "Warning", "Please select input and output columns.")
            return

        if len(output_column) > 1:
            QMessageBox.warning(self, "Warning", "Only one output column can be selected.")
            return

        # Llama a create_result_window en MainWindow
        self.main_window.create_result_window(self.df, input_columns, output_column)

