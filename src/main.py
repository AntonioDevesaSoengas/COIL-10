import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from ui.loading_dataset import LoadingDatasetWindow
from ui.preprocess_data import DataPreprocessingWindow
from ui.columns_selection import ColumnSelectionWindow
from ui.welcome_window import WelcomeWindow
from ui.results_window import ResultWindow

class MainWindow(QMainWindow):
    """
    Main application window to handle the workflow.
    """
    def __init__(self):
        super().__init__()

        # Create a stacked widget to manage different windows
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize shared data
        self.df = None  # DataFrame to share between windows

        # Add all windows to the stack
        self.init_windows()

        # Set initial window
        self.stack.setCurrentIndex(0)

        # Window configuration
        self.setWindowTitle("Data Processing Workflow")
        self.setMinimumSize(800, 600)

    def init_windows(self):
        """
        Initialize and add all windows to the stack.
        """
        # Welcome Window
        self.welcome_window = WelcomeWindow()
        self.stack.addWidget(self.welcome_window)
        self.welcome_window.create_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        # Loading Dataset Window
        self.loading_window = LoadingDatasetWindow()
        self.loading_window.navigate_next.connect(self.go_to_preprocessing)
        self.loading_window.navigate_back.connect(self.go_to_welcome)
        self.stack.addWidget(self.loading_window)

        # Data Preprocessing Window
        self.preprocessing_window = DataPreprocessingWindow()
        self.preprocessing_window.navigate_next.connect(self.go_to_columns_selection)  # Avanzar a la siguiente ventana
        self.preprocessing_window.navigate_back.connect(self.go_to_loading)  # Retroceder a la ventana de carga
        self.stack.addWidget(self.preprocessing_window)
        
        # Column Selection Window
        self.column_selection_window = ColumnSelectionWindow(self)
        self.column_selection_window.navigate_back.connect(self.go_to_preprocessing_from_columns)
        self.stack.addWidget(self.column_selection_window)

    def go_to_columns_selection(self, df):
        """
        Navigate to the column selection window.
        """
        self.df = df  # Guardamos el DataFrame
        self.column_selection_window.set_dataframe(df)  # Pasar el DataFrame a la ventana de selección
        self.stack.setCurrentIndex(3)  # Mover a la ventana de selección de columnas

    def go_to_preprocessing_from_columns(self):
        """
        Navigate back to the preprocessing window from column selection.
        """
        self.stack.setCurrentIndex(2)  # Regresa a la ventana de preprocesado

    def go_to_loading(self):
        """
        Navigate back to the loading dataset window.
        """
        self.stack.setCurrentIndex(1)

    def go_to_preprocessing(self, df):
        """
        Navigate to the preprocessing window.
        """
        self.df = df
        self.preprocessing_window.set_dataframe(df)
        self.preprocessing_window.display_data_in_table(df)
        self.stack.setCurrentIndex(2)  # Move to preprocessing window
        
    def go_to_welcome(self):
        """
        Navigate back to the welcome window.
        """
        self.loading_window.reset_state()  # Reset the state of the loading window
        self.stack.setCurrentIndex(0)  # Move to welcome window

    def on_dataset_loaded(self, df):
        """
        Handle the dataset loaded signal from the LoadingDatasetWindow.
        """
        if df is not None:
            self.df = df
            self.loading_window.display_data_in_table(df)  # Display the table
        else:
            QMessageBox.warning(self, "Warning", "No dataset loaded. Please try again.")

    def create_result_window(self, df, input_columns, output_column):
        """
        Create the result window and display the model generation.
        """
        self.result_window = ResultWindow(df, input_columns, output_column)
        self.stack.addWidget(self.result_window)
        self.stack.setCurrentWidget(self.result_window)

def main():
    """
    Entry point for the application.
    """
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()