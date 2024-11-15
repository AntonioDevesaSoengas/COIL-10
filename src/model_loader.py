import joblib
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from PyQt5.QtWidgets import QLabel, QTextEdit

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
        self.viewer.formula_label.setText(f"Fórmula: {model_data['formula']}")
        self.viewer.mse_label.setText(f"MSE: {model_data.get('mse', 'No disponible')}")
        self.viewer.r_squared_label.setText(f"R²: {model_data.get('r_squared', 'No disponible')}")
        self.viewer.description_text.setText(model_data.get('description', ''))
        
        # Hacer visibles los detalles del modelo
        self.show_model_details()

    def show_model_details(self):
        # Mostrar etiquetas para el modelo cargado
        self.viewer.formula_label.setVisible(True)
        self.viewer.mse_label.setVisible(False)
        self.viewer.r_squared_label.setVisible(False)
        self.viewer.description_text.setVisible(True)

    def hide_data_loading_sections(self):
        # Ocultar las secciones de la interfaz que no se necesitan al cargar un modelo
        self.viewer.load_button.setVisible(False)
        self.viewer.detect_button.setVisible(False)
        self.viewer.preprocessing_options.setVisible(False)
        self.viewer.apply_button.setVisible(False)
        self.viewer.feature_selector.setVisible(False)
        self.viewer.target_selector.setVisible(False)
        self.viewer.confirm_button.setVisible(False)
