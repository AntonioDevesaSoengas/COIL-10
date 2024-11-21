import sys
from PyQt5.QtWidgets import QApplication
from features import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DataViewer()
    viewer.show()
    sys.exit(app.exec_())