from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QTableView, QHBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from data_preparation.data_preprocessing import (
    detect_missing_values,
    fill_with_constant,
    fill_with_mean,
    fill_with_median,
    remove_missing_values
)
from utils.helpers import ButtonHelper

class DataPreprocessingWindow(QWidget):
    """
    Class to handle data preprocessing functionalities.
    """

    finished = pyqtSignal(object)
    navigate_next = pyqtSignal(object)
    navigate_back = pyqtSignal()
    
    def __init__(self, parent=None, dataframe=None):
        super().__init__(parent)
        self.df = dataframe  # DataFrame to preprocess
        self.nan_solved = False

        # Initialize UI components
        self.initUI()

    def initUI(self):
        """
        Set up the user interface components for data preprocessing.
        """
        self.layout = QVBoxLayout()
        
        button_helper = ButtonHelper()

        self.nan_label = QLabel("Preprocessing NaN Values")
        self.nan_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.nan_label)

        self.preprocessing_options = QComboBox()
        self.preprocessing_options.addItems([
            "Select an option...",
            "🗑️ Remove Rows with Missing Values",
            "📊 Fill with Mean",
            "📊 Fill with Median",
            "✏️ Fill with a Constant Value"
        ])
        self.preprocessing_options.currentIndexChanged.connect(self.update_apply_button)
        self.layout.addWidget(self.preprocessing_options)

        self.apply_button = QPushButton("🟢 Apply Preprocessing")
        self.apply_button.setFont(QFont("Arial Black", 10))
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.confirm_preprocessing)
        self.layout.addWidget(self.apply_button)

        # Add QTableView to display data
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)
        
        # Navigation buttons
        navigation_buttons = button_helper.create_navigation_buttons(
            on_next=self.go_next,
            on_back=self.go_back
        )
        self.layout.addLayout(navigation_buttons)

        self.setLayout(self.layout)
        self.setWindowTitle("Data Preprocessing")
        self.setMinimumSize(400, 300)

    def update_apply_button(self):
        """
        Enables or disables the apply button based on the selected option.
        """
        if self.preprocessing_options.currentIndex() == 0:
            self.apply_button.setEnabled(False)
        else:
            self.apply_button.setEnabled(True)

    def confirm_preprocessing(self):
        """
        Applies the selected preprocessing option to the DataFrame.
        """
        if self.df is None or self.df.empty:
            QMessageBox.warning(self, "Warning", "No dataset loaded for preprocessing.")
            return

        option = self.preprocessing_options.currentText()
        try:
            if option == "🗑️ Remove Rows with Missing Values":
                remove_missing_values(self)
            elif option == "📊 Fill with Mean":
                fill_with_mean(self)
            elif option == "📊 Fill with Median":
                fill_with_median(self)
            elif option == "✏️ Fill with a Constant Value":
                fill_with_constant(self)

            self.nan_solved = True
            QMessageBox.information(
                self, "Success", "Preprocessing applied successfully."
            )

            self.finished.emit(self.df)  # Emitir el DataFrame actualizado
            self.display_data_in_table(self.df)  # Actualizar la tabla en la ventana
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"An error occurred during preprocessing: {e}"
            )

    def get_dataframe(self):
        """
        Returns the preprocessed DataFrame.
        """
        return self.df

    def set_dataframe(self, dataframe):
        """
        Set the DataFrame to preprocess.
        """
        self.df = dataframe
        
    def display_data_in_table(self, data):
        """
        Displays the processed data in a table view.
        """
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(data.columns.tolist())
        
        for row in data.itertuples(index=False):
            items = [QStandardItem(str(value)) for value in row]
            model.appendRow(items)
        
        # Assuming self.table_view is defined in your class for displaying the data
        self.table_view.setModel(model)
        self.table_view.setVisible(True)

    def go_next(self):
        if self.df is not None:
            self.navigate_next.emit(self.df)
        else:
            QMessageBox.warning(self, "Warning", "Please apply preprocessing before proceeding.")

    def go_back(self):
        self.navigate_back.emit()

    