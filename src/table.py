from PyQt5.QtCore import QAbstractTableModel, Qt
import pandas as pd

class Table(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.data.columns)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.data.columns[section]
            if orientation == Qt.Vertical:
                return str(self.data.index[section])
        return None

    def is_empty(self):
            return self.columnCount == 0 and self.rowCount == 0