# Third-party library imports
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from sklearn.impute import SimpleImputer


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
            QMessageBox.warning(viewer,"Warning","There were empty values detected")
            viewer.nan_label.setText(f"¡{nan_values[0]} empty values were detected!")
            viewer.nan_values.setText(f"{nan_values.to_string()}")

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


def fill_with_mean(viewer):
    """ 
    Fill missing values in numeric columns of the viewer's DataFrame
    with their mean.

    Parameters:
        viewer (DataViewer): Object with:
            - df (DataFrame): The dataset to process.
            - display_data_in_table: Method to update the table in the GUI.
    """
    if viewer.df is not None:
        # Apply only to numeric columns.
        num_cols = viewer.df.select_dtypes(include=["number"]).columns
        imputer = SimpleImputer(strategy="mean")
        viewer.df[num_cols] = imputer.fit_transform(viewer.df[num_cols])
        viewer.display_data_in_table(viewer.df)
        QMessageBox.information(
            viewer,
            "Success",
            "Missing values have been filled with the mean in numeric columns."
        )


def fill_with_median(viewer):
    """
    Fill missing values in numeric columns of the viewer's DataFrame
    with their median.

    Parameters:
        viewer (DataViewer): Object with:
            - df (DataFrame): The dataset to process.
            - display_data_in_table: Method to update the table in the GUI.
    """
    if viewer.df is not None:
        # Apply only to numeric columns.
        numeric_cols = viewer.df.select_dtypes(include=["number"]).columns
        imputer = SimpleImputer(strategy="median")
        viewer.df[numeric_cols] = imputer.fit_transform(
            viewer.df[numeric_cols])
        viewer.display_data_in_table(viewer.df)
        QMessageBox.information(
            viewer,
            "Success",
            "Missing values filled with the median in numeric columns."
        )


def fill_with_constant(viewer):
    """
    Fill missing values in numeric columns of the viewer's DataFrame
    with a user-specified constant value.

    Parameters:
        viewer (DataViewer): Object with:
            - df (DataFrame): The dataset to process.
            - display_data_in_table: Method to update the table in the GUI.
    """
    # Open a dialog to get a numeric value from the user.
    # Returns the value and whether the user confirmed or canceled.
    value, ok = QInputDialog.getDouble(
        viewer,
        "Fill with a Constant Value",
        "Enter the numeric value to fill:"
    )
    if ok and viewer.df is not None:
        # Apply only to numeric columns.
        numeric_cols = viewer.df.select_dtypes(include=["number"]).columns
        imputer = SimpleImputer(strategy="constant", fill_value=value)
        viewer.df[numeric_cols] = imputer.fit_transform(
            viewer.df[numeric_cols])
        viewer.display_data_in_table(viewer.df)
        QMessageBox.information(
            viewer,
            "Success",
            "Missing values filled with the specified constant value."
        )
