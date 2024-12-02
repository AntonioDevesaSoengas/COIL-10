# Third-party libraries.
import joblib
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer

# Local libraries.
from model_window import ModelWindow


class ModelLoader(QWidget):
    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer

    def load_model_dialog(self):
        """Open a file dialog to select a saved model."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Model",
            "",
            "Joblib Files (*.joblib);;Pickle Files (*.pkl)",
            options=options
        )

        if file_path:
            return self.load_model(file_path)  # Return loaded model data

    def load_model(self, file_path):
        """Load the model from the specified file path."""
        try:
            model_data = joblib.load(file_path)

            # Show the confirmation message first
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Success")
            msg_box.setText("Model loaded successfully.")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.exec_()  # Show the message first

            # Slightly delay the opening of the model window
            QTimer.singleShot(100, lambda: self.open_model_window(model_data))

        except Exception as e:
            QMessageBox.critical(
                self.viewer,
                "Error",
                f"Could not load the model: {str(e)}"
            )

    def open_model_window(self, model_data):
        """Open the model window."""
        # Get the input columns from the loaded model
        input_columns = model_data.get('input_columns', [])  
        # Create a new instance of ModelWindow passing both arguments
        model_window = ModelWindow(model_data, input_columns)
        if hasattr(self.viewer, 'open_windows'):
            self.viewer.open_windows.append(model_window)
        else:
            self.viewer.open_windows = [model_window]

        # Show the model window
        self.viewer.open_windows[-1].show()
