# Third-party libraries.
import joblib
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class ModelSaver:
    """
    A class to handle saving linear regression models and their metadata.

    Attributes:
        model: The linear regression model to be saved.
        formula (str): The formula used in the model.
        r_squared (float): The R-squared value of the model.
        mse (float): The Mean Squared Error of the model.
        input_columns (list): List of input feature column names.
        output_column (str): The name of the output column.
        description (str): Description of the model.
        graph: (Optional) Graphical representation associated with the model.
    """

    def __init__(
        self,
        model,
        formula,
        r_squared,
        mse,
        input_columns,
        output_column,
        description,
        graph=None
    ):
        """
        Initialize the ModelSaver with model details.
        """
        self.model = model
        self.formula = formula
        self.r_squared = r_squared
        self.mse = mse
        self.input_columns = input_columns
        self.output_column = output_column
        self.description = description
        self.graph = graph

    def save_model_dialog(self):
        """
        Open a file dialog to save the model.

        This method allows the user to choose a file path and name
        to save the serialized model using Joblib.

        Returns:
            None
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save Model",
            "",
            "Joblib Files (*.joblib)",
            options=options
        )
        if file_path:
            self.save_model(file_path)

    def save_model(self, file_path):
        """
        Save the model to the specified file path.

        Serializes the model along with its metadata and saves it using Joblib.
        If the description is empty or consists solely of whitespace, a default
        description is used.

        Args:
            file_path (str): The file path where the model will be saved.

        Raises:
            Exception: If there is an error during the saving process.

        Returns:
            None
        """
        try:
            # Use a default description if the provided description is empty.
            description = (
                self.description.strip()
                if self.description.strip()
                else "No description provided."
            )

            # Data of the model to save.
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

            # Save the model using Joblib.
            joblib.dump(model_data, file_path)

            # Prepare success message.
            success_title = "Success"
            success_message = "Model saved successfully."
            QMessageBox.information(
                None,
                success_title,
                success_message
            )
        except Exception as e:
            # Prepare error message.
            error_title = "Error"
            error_message = f"Could not save the model: {str(e)}"
            QMessageBox.critical(
                None,
                error_title,
                error_message
            )