import joblib
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget

class ModelSaver(QWidget):
    def __init__(self, model, formula, r_squared, mse, input_columns, output_column, description):
        super().__init__()
        self.model = model
        self.formula = formula
        self.r_squared = r_squared
        self.mse = mse
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description

    def save_model_dialog(self):
        """Abrir un cuadro de diálogo para seleccionar la ubicación de guardado."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Modelo", "", "Archivos Joblib (*.joblib)", options=options
        )
        if file_path:
            self.save_model(file_path)

    def save_model(self, file_path):
        """Guarda el modelo en el archivo especificado."""
        try:
            model_data = {
                'model': self.model,
                'formula': self.formula,
                'r_squared': self.r_squared,
                'mse': self.mse,
                'input_columns': self.input_columns,
                'output_column': self.output_column,
                'description': self.description
            }
            joblib.dump(model_data, file_path)
            QMessageBox.information(self, "Guardado exitoso", "El modelo se ha guardado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar el modelo: {str(e)}")