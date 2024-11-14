import pickle
import joblib
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QWidget

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
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.save_button = QPushButton('Guardar Modelo')
        self.save_button.clicked.connect(self.save_model_dialog)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.setWindowTitle("Guardar Modelo de Regresión Lineal")
        self.show()

    def save_model_dialog(self):
        # Abrir un cuadro de diálogo para seleccionar el archivo de guardado
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Modelo", "", "Pickle Files (*.pkl);;Joblib Files (*.joblib)", options=options)
        
        if file_path:
            self.save_model(file_path)

    def save_model(self, file_path):
        # Empaquetar la información del modelo en un diccionario
        model_data = {
            'model': self.model,
            'formula': self.formula,
            'r_squared': self.r_squared,
            'mse': self.mse,
            'input_columns': self.input_columns,
            'output_column': self.output_column,
            'description': self.description
        }

        # Intentar guardar el archivo con manejo de errores
        try:
            if file_path.endswith('.pkl'):
                with open(file_path, 'wb') as f:
                    pickle.dump(model_data, f)
            elif file_path.endswith('.joblib'):
                joblib.dump(model_data, file_path)

            # Confirmación de éxito
            QMessageBox.information(self, "Éxito", "El modelo ha sido guardado correctamente.")
        
        except Exception as e:
            # Notificar en caso de error
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar el modelo: {str(e)}")
