# Third-party library imports
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from sklearn.impute import SimpleImputer
from utils.helpers import LabelHelper, LayoutHelper

def detect_missing_values(viewer):
    """
    Detect missing values in the provided DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame to analyze for missing values.

    Returns:
        str: A message summarizing the missing values by column or 
             stating that the dataset is complete.
    """
    if viewer.df is not None:
        viewer.missing_data = viewer.df.isnull().sum()
        nan_values = viewer.missing_data[viewer.missing_data > 0]
        if viewer.missing_data.sum() != 0:
            layout = LayoutHelper()
            viewer.empty_values = True
            viewer.nan_data = True
            QMessageBox.warning(viewer, "Warning", "There were empty values detected")
            layout.edit_separator(viewer.sep, color="red")
            show_missing_values(viewer, nan_values)
            layout.edit_separator(viewer.separator, color="red")
            viewer.preprocessing_options.setCurrentIndex(0)
            viewer.preprocessing_options.setEnabled(True)
        else:
            viewer.empty_values = False

def show_missing_values(viewer, nan_values):
    label = LabelHelper()
    label.edit_label(viewer.nan_label, color="red")
    viewer.nan_label.setText(f"¡{nan_values[0]} empty values were detected!")
    viewer.nan_values.setText(f"{nan_values.to_string()}")
    viewer.nan_layout.insertWidget(2, viewer.nan_values)

def remove_missing_values(viewer):
    """
    Remove rows with missing values from the viewer's DataFrame.

    Parameters:
        viewer (DataViewer): Object with:
            - df (DataFrame): The dataset to process.
            - display_data_in_table: Method to update the table in the GUI.
    """
    if viewer.df is not None:
        viewer.df = viewer.df.dropna()
        viewer.display_data_in_table(viewer.df)
        QMessageBox.information(
            viewer,
            "Success",
            "Rows with missing values have been removed."
        )

def fill_missing_values(viewer, strategy='mean', constant_value=None):
    """
    Fill missing values in numeric columns of the viewer's DataFrame
    using the specified strategy.

    Parameters:
        viewer (DataViewer): Object with:
            - df (DataFrame): The dataset to process.
            - display_data_in_table: Method to update the table in the GUI.
        strategy (str): The strategy to use for filling missing values.
                        Options are 'mean', 'median', or 'constant'.
        constant_value (float, optional): The constant value to use if
                                           strategy is 'constant'.
    """
    if viewer.df is not None:
        # Apply only to numeric columns.
        numeric_cols = viewer.df.select_dtypes(include=["number"]).columns
        
        if strategy == 'mean':
            imputer = SimpleImputer(strategy="mean")
        elif strategy == 'median':
            imputer = SimpleImputer(strategy="median")
        elif strategy == 'constant':
            if constant_value is None:
                raise ValueError("constant_value must be provided when strategy is 'constant'")
            imputer = SimpleImputer(strategy="constant", fill_value=constant_value)
        else:
            raise ValueError("Invalid strategy. Choose 'mean', 'median', or 'constant'.")

        viewer.df[numeric_cols] = imputer.fit_transform(viewer.df[numeric_cols])
        viewer.display_data_in_table(viewer.df)

        if strategy == 'mean':
            QMessageBox.information(viewer, "Success", "Missing values filled with the mean in numeric columns.")
        elif strategy == 'median':
            QMessageBox.information(viewer, "Success", "Missing values filled with the median in numeric columns.")
        elif strategy == 'constant':
            QMessageBox.information(viewer, "Success", "Missing values filled with the specified constant value.")

def fill_with_mean(viewer):
    fill_missing_values(viewer, strategy='mean')

def fill_with_median(viewer):
    fill_missing_values(viewer, strategy='median')

def fill_with_constant(viewer):
    value, ok = QInputDialog.getDouble(
        viewer,
        "Fill with a Constant Value",
        "Enter the numeric value to fill:"
    )
    if ok:
        fill_missing_values(viewer, strategy='constant', constant_value=value)
