import joblib
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox

class ModelLoader(QWidget):
    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer

    def load_model_dialog(self):
        """Open a file dialog to select a saved model."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Modelo", "", "Archivos Joblib (*.joblib);;Pickle Files (*.pkl)", options=options
        )

        if file_path:
            return self.load_model(file_path)  # Return loaded model data

    def load_model(self, file_path):
        """Load the model from the specified file path."""
        try:
            model_data = joblib.load(file_path)  # Load model data
            return model_data  # Return loaded model data
        except Exception as e:
            QMessageBox.critical(self.viewer, "Error", f"No se pudo cargar el modelo: {str(e)}")
            return None