try:
    from PyQt5 import uic, QtWidgets
    from PyQt5.QtCore import Qt, QEvent, QTimer, QRegExp
    from PyQt5.QtWidgets import QTreeWidgetItem
    from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QIcon
except Exception as e:
    print("Error en linea {}: ".format(sys.exc_info()[-1].tb_lineno), type(
        e).__name__, e, "\n\nEste plugin requiere Sigil >0.9.8 o PyQt5.")
    sys.exit()


class RegexDialog(QtWidgets.QDialog):
    def __init__(self, dark_theme):
        pass

    def regexComboBox_newValue(self):
        pass

    def ibidLabelComboBox_newValue(self):
        pass

    def separatorComboBox_newValue(self):
        pass

    def testButton_pressed(self):
        pass

    def acceptButton_pressed(self):
        pass

    def defaultButton_pressed(self):
        pass

    def cancelButton_pressed(self):
        self.close()

    def showDialog(self):
        self.show()
