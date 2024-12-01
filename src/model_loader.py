import joblib
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer
from model_window import ModelWindow


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
            model_data = joblib.load(file_path)

            # Mostrar el mensaje de confirmación primero
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Éxito")
            msg_box.setText("Modelo cargado exitosamente.")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.exec_()  # Mostramos el mensaje primero

            # Retrasar ligeramente la apertura de la ventana del modelo
            QTimer.singleShot(100, lambda: self.open_model_window(model_data))

        except Exception as e:
            QMessageBox.critical(self.viewer, "Error", f"No se pudo cargar el modelo: {str(e)}")

    def open_model_window(self, model_data):
        """Abre la ventana del modelo."""
        # Obtener las columnas de entrada del modelo cargado
        columnas_entrada = model_data.get('input_columns', [])  # Cambia 'input_columns' por la clave correcta si es diferente

        # Crear una nueva instancia de ModelWindow pasando ambos argumentos
        if hasattr(self.viewer, 'open_windows'):
            self.viewer.open_windows.append(ModelWindow(model_data, columnas_entrada))
        else:
            self.viewer.open_windows = [ModelWindow(model_data, columnas_entrada)]

        # Mostrar la ventana del modelo
        self.viewer.open_windows[-1].show()

