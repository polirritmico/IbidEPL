from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor

def highlight(qtextedit, separator):
    separator_highlight = separator
    
    if separator_highlight == "":
        return
    
    # Definimos el color
    fmt = QTextCharFormat()
    fmt.setForeground(QColor("black"))
    fmt.setBackground(QColor("darkCyan"))
    
    # Restablecemos el color
    cursor = qtextedit.textCursor()
    cursor.select(QTextCursor.Document)
    cursor.setCharFormat(QTextCharFormat())
    cursor.clearSelection()
    qtextedit.setTextCursor(cursor)
    
    # Regular
    expression = QRegExp(separator_highlight)
    qtextedit.moveCursor(QTextCursor.Start)
    cursor = qtextedit.textCursor()

    # Ciclo de búsqueda y cambio del color
    pos = 0
    index = expression.indexIn(qtextedit.toPlainText(), pos)
    while index >= 0:
        cursor.setPosition(index)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                            len(separator_highlight))
        cursor.mergeCharFormat(fmt)
        pos = index + expression.matchedLength()
        index = expression.indexIn(qtextedit.toPlainText(), pos)