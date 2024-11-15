import joblib
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget

class ModelLoader(QWidget):
    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer
    
    def load_model_dialog(self):
        # Abrir el cuadro de diálogo para seleccionar el archivo del modelo
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Modelo", "", "Joblib Files (*.joblib);;Pickle Files (*.pkl)", options=options)
        
        # Si se selecciona un archivo válido, cargar el modelo
        if file_path:
            self.load_model(file_path)

    def load_model(self, file_path):
        try:
            # Intentar cargar el modelo guardado
            model_data = joblib.load(file_path)
            self.update_ui_with_model(model_data)
            QMessageBox.information(self.viewer, "Éxito", "Modelo cargado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self.viewer, "Error", f"No se pudo cargar el modelo: {str(e)}")
    
    def update_ui_with_model(self, model_data):
        # Actualizar la interfaz con los datos del modelo
        self.viewer.formula_label.setText(f"Fórmula: {model_data['formula']}")
        self.viewer.mse_label.setText(f"MSE: {model_data['mse']}")
        self.viewer.r_squared_label.setText(f"R²: {model_data['r_squared']}")
        self.viewer.description_text.setText(model_data['description'])
        
        # Ocultar secciones no necesarias para el modelo
        self.viewer.hide_data_loading_sections()

