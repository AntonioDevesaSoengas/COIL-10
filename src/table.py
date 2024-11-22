# Third-party libraries
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt


class Table(QAbstractTableModel):
    """
    A custom table model for displaying pandas DataFrame data
    in a Qt-based table view.

    Attributes:
        data (pd.DataFrame): The DataFrame to be displayed in the table.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize the table model with the given DataFrame.

        Args:
            data (pd.DataFrame): The data to display in the table.
        """
        super().__init__()
        self.data = data

    def rowCount(self,parent=None) -> int:
        """
        Get the number of rows in the table.

        Returns:
            int: The number of rows in the DataFrame.
        """
        return len(self.data)

    def columnCount(self, parent=None) -> int:
        """
        Get the number of columns in the table.

        Returns:
            int: The number of columns in the DataFrame.
        """
        return len(self.data.columns)

    def data(self, index, role=Qt.DisplayRole):
        """
        Get the data for a specific cell in the table.

        Args:
            index (QModelIndex): The index of the cell.
            role (int): The role of the data (default: Qt.DisplayRole).

        Returns:
            str or None: The string representation of the cell's data,
            or None if the role is not Qt.DisplayRole.
        """
        if role == Qt.DisplayRole:
            return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Get the data for the table headers.

        Args:
            section (int): The section of the header (row or column index).
            orientation (Qt.Orientation): The orientation of the header
                (horizontal for columns, vertical for rows).
            role (int): The role of the data (default: Qt.DisplayRole).

        Returns:
            str or None: The header label as a string, or None if the role
            is not Qt.DisplayRole.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.data.columns[section]
            if orientation == Qt.Vertical:
                return str(self.data.index[section])
        return None

    def is_empty(self) -> bool:
        """
        Check if the table is empty.

        Returns:
            bool: True if the table has no rows and columns, False otherwise.
        """
        return self.columnCount() == 0 and self.rowCount() == 0
