#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IbidEpl v0.4_beta

Una ayuda para manejar notas ibid.
Titivillus

"""

# import sys
# import os
# import re
import book
# import resources
try:
    from PyQt5 import uic, QtWidgets
    from PyQt5.QtCore import Qt, QEvent, QTimer, QRegExp
    from PyQt5.QtWidgets import QTreeWidgetItem
    from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QIcon
except Exception as e:
    print("Error en linea {}: ".format(sys.exc_info()[-1].tb_lineno), type(
        e).__name__, e, "\n\nEste plugin requiere Sigil >0.9.8 o PyQt5.")
    sys.exit()


class GUI(QtWidgets.QDialog):
    pass


def run(bk):
    if not bk.launcher_version() >= 20170115:
        print("Este plugin requiere Sigil >0.9.8 \
            \n\nHaga clic en Aceptar para cerrar.")
        return -1

    selected_files = []
    for i in bk.selected_iter():
        selected_files.append(i)
    file = selected_files[0][1]


def main():
    print("Error: Ejecutar desde Sigil.\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
