#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2021 Titivillus
# www.epublibre.org
# Distributed under the terms of the GNU General Public License v2

# Adaptado desde:
# https://github.com/PyQt5/PyQt/blob/master/QTextEdit/HighlightText.py

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor


def highlight(qtextedit, separator):
    if separator == "":
        return

    # Restablecemos el formato del texto
    cursor = qtextedit.textCursor()
    cursor.select(QTextCursor.Document)
    cursor.setCharFormat(QTextCharFormat())
    cursor.clearSelection()
    qtextedit.setTextCursor(cursor)

    # Definimos el color
    text_format = QTextCharFormat()
    text_format.setForeground(QColor("black"))
    text_format.setBackground(QColor("darkCyan"))

    # RegEx
    expression = QRegExp(separator)
    qtextedit.moveCursor(QTextCursor.Start)
    cursor = qtextedit.textCursor()

    # Ciclo de búsqueda y cambio del color
    pos = 0
    index = expression.indexIn(qtextedit.toPlainText(), pos)
    while index >= 0:
        cursor.setPosition(index)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                            len(separator))
        cursor.mergeCharFormat(text_format)
        pos = index + expression.matchedLength()
        index = expression.indexIn(qtextedit.toPlainText(), pos)
