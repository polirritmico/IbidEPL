import sys
# import os
# import re
# from note import *
# from note import Note
# from book import Book
# from plugin import REGEX_SPLIT_NOTE
try:
    from PyQt5 import uic, QtWidgets
    from PyQt5.QtCore import Qt, QEvent, QTimer, QRegExp
    from PyQt5.QtWidgets import QTreeWidgetItem
    from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QIcon
except Exception as e:
    print("Error en linea {}: ".format(sys.exc_info()[-1].tb_lineno), type(
        e).__name__, e, "\n\nEste plugin requiere Sigil >0.9.8 o PyQt5.")
    sys.exit()


class Window(QtWidgets.QDialog):
    def __init__(self, book):
        super(Window, self).__init__()
        uic.loadUi("IbidEpl.ui", self)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.show()


def run(book) -> bool:
    save_file = False
    app = QtWidgets.QApplication(sys.argv)
    # theme_color(app)
    window = Window(book)
    # Mostramos la GUI y esperamos Aceptar o Cancelar
    app.exec_()

    return save_file
