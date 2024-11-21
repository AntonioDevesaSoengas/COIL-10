from PyQt5.QtWidgets import *

class Layout():
    #Function to add Widgets into a Layout
    def add_Widget(self,layout,widgets:list):
        for item in widgets:
            if isinstance(item,QWidget):
                layout.addWidget(item)
            elif isinstance(item,QFrame):
                layout.addWidget(item)
            elif isinstance(item,QLayout):
                if item.parent() is None:
                    layout.addLayout(item)
                else:
                    QMessageBox.warning(None,"Warning","This layout already has a parent")
            elif isinstance(item,QSpacerItem):
                layout.addItem(item)
            else:
                QMessageBox.critical(None,"Error","You are traing to add a non defined item")

    def add_separator(self,type:str,width:int,visibility:bool):
        separator = QFrame()
        if type.lower() == "vertical":
            separator.setFrameShape(QFrame.VLine)
        elif type.lower() == "horizontal":
            separator.setFrameShape(QFrame.HLine)
        if width is not None:
            separator.setLineWidth(width)
        separator.setVisible(visibility)
        return separator