from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QMessageBox, QFileDialog, QHeaderView
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSignal
from utils.helpers import ButtonHelper, LabelHelper
from data_preparation.import_files import import_data

class LoadingDatasetWindow(QWidget):
    """
    Class to handle dataset loading functionality.
    """
    df_loaded = pyqtSignal(object)
    navigate_next = pyqtSignal(object)
    navigate_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = None
        self.last_file_path = None

        # Initialize UI components
        self.initUI()

    def initUI(self):
        """
        Set up the user interface components for loading datasets.
        """
        self.layout = QVBoxLayout()

        # ButtonHelper instance
        button_helper = ButtonHelper()

        # Load Dataset Button
        self.load_button = button_helper.add_QPushButton(
            text='\U0001F4C2 Load Dataset',
            font_type="Arial Black",
            font_size=12,
            width=None,
            height=40,
            visibility=True,
            background_color="green",
            color="white"
        )
        self.load_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.load_button)

        # LabelHelper instance
        label_helper = LabelHelper()

        # Label to display file path
        self.file_label = label_helper.create_label(
            parent=self,
            text="",
            font=("Arial", 10),
            visible=False
        )
        self.layout.addWidget(self.file_label)

        # Table to display data
        self.table_view = QTableView()
        self.table_view.setFont(QFont("Arial", 10))
        self.table_view.setVisible(False)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table_view)

        # Navigation buttons
        navigation_buttons = button_helper.create_navigation_buttons(
            on_next=self.go_next,
            on_back=self.go_back
        )
        self.layout.addLayout(navigation_buttons)

        # Set layout
        self.setLayout(self.layout)
        self.setWindowTitle("Loading Dataset")
        self.setMinimumSize(800, 600)

    def open_file_dialog(self):
        """
        Opens file dialog to select and load a dataset. Allows reloading a different dataset.
        """
        filters = (
            "CSV Files (*.csv);;Excel Files (*.xlsx *.xls);;SQLite Databases (*.sqlite *.db)"
        )
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", filters)
        if file_path:
            if self.last_file_path == file_path:
                result = QMessageBox.question(
                    self, "Warning",
                    "You are selecting the same file. Do you want to reload it?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if result == QMessageBox.No:
                    return
            
            # Update last file path and reload dataset
            self.last_file_path = file_path
            self.file_label.setText(f'\U0001F4C2 Loaded File: {file_path}')
            self.file_label.setVisible(True)
            self.load_data(file_path)

    def load_data(self, file_path):
        """
        Loads data from the selected file using the import_data function.
        Updates the table with the new dataset and checks for NaN values.
        """
        try:
            self.df = import_data(file_path)
            if self.df is not None and not self.df.empty:
                self.df_loaded.emit(self.df)
                self.display_data_in_table(self.df)
                # Check for NaN values
                if self.df.isnull().values.any():
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "The dataset contains missing values (NaN). Please handle them before proceeding."
                    )
            else:
                QMessageBox.warning(self, "Warning", "The file is empty or invalid.")
        except FileNotFoundError as fnf_error:
            QMessageBox.critical(self, "Error", str(fnf_error))
        except ValueError as val_error:
            QMessageBox.critical(self, "Error", str(val_error))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def display_data_in_table(self, data):
        """
        Displays the loaded data in the table view.
        """
        if data is not None:
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(data.columns.tolist())  # Establece los encabezados

            for row in data.itertuples(index=False):
                items = [QStandardItem(str(value)) for value in row]
                model.appendRow(items)

            self.table_view.setModel(model)
            self.table_view.setVisible(True)

    def go_next(self):
        """
        Emit signal to navigate to the next window.
        """
        if self.df is not None:
            self.navigate_next.emit(self.df)
        else:
            QMessageBox.warning(self, "Warning", "Please load a dataset before proceeding.")

    def go_back(self):
        """
        Emit signal to navigate to the previous window.
        """
        self.navigate_back.emit()
        
    def reset_state(self):
        """
        Resets the state of the window to its initial state.
        """
        self.df = None
        self.last_file_path = None
        self.file_label.setText("")
        self.file_label.setVisible(False)
        self.table_view.setModel(None)
        self.table_view.setVisible(False)

