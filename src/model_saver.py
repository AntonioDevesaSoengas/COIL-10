import joblib
import joblib
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class ModelSaver:
    def __init__(self, model, formula, r_squared, mse, input_columns, output_column, description, graph=None):
        self.model = model
        self.formula = formula
        self.r_squared = r_squared
        self.mse = mse
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description
        self.graph = graph  

    def save_model_dialog(self):
        """Open a file dialog to save the model."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Guardar Modelo", "", "Archivos Joblib (*.joblib)", options=options
        )
        if file_path:
            self.save_model(file_path)

    def save_model(self, file_path):
        """
        Guarda el modelo en la ruta especificada.
        Si no se proporciona una descripción, usa un valor por defecto.
        """
        try:
            # Usa una descripción por defecto si el campo está vacío
            description = self.description if self.description.strip() else "No description provided."

            # Datos del modelo a guardar
            model_data = {
                'model': self.model,
                'formula': self.formula,
                'r_squared': self.r_squared,
                'mse': self.mse,
                'input_columns': self.input_columns,
                'output_column': self.output_column,
                'description': description,
                'graph': self.graph, 
            }
            # Guardar el modelo
            joblib.dump(model_data, file_path)
            QMessageBox.information(None, "Éxito", "Modelo guardado exitosamente.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo guardar el modelo: {str(e)}")

