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

        # self.max_note_label = str(parent_count)
        # self.max_ibid_label = str(ibid_count)

        # Set Icons
        #self.loadIcons()

        # Connect buttons
        # Navigation buttons
        self.NoteNextButton.clicked.connect(self.nextNoteButton_pressed)
        self.NotePrevButton.clicked.connect(self.prevNoteButton_pressed)
        self.IbidNextButton.clicked.connect(self.nextIbidButton_pressed)
        self.IbidPrevButton.clicked.connect(self.prevIbidButton_pressed)
        # Note/ibid switches buttons
        self.NoteToIbidButton.clicked.connect(self.noteToIbidButton_pressed)
        self.IbidToNoteButton.clicked.connect(self.ibidToNoteButton_pressed)
        # Edit ibid buttons
        self.IbidUndoButton.clicked.connect(self.undoIbidButton_pressed)
        self.IbidReplaceButton.clicked.connect(self.ibidReplaceButton_pressed)
        self.IbidAutoProcButton.clicked.connect(self.processIbidButton_pressed)
        self.IbidAutoProcAllButton.clicked.connect(
            self.processAllIbidsButton_pressed)
        # Aditional buttons
        self.RegexSelectorButton.clicked.connect(self.configButton_pressed)
        self.TagButton.clicked.connect(self.showTagButton_pressed)
        self.ShowOriginalIbid.clicked.connect(
            self.showOriginalIbidButton_pressed)
        self.IbidOriginalText.setVisible(False)
        # Dialog confirmation buttons
        self.AcceptButton.clicked.connect(self.acceptButton_pressed)
        self.CancelButton.clicked.connect(self.cancelButton_pressed)

        # QtextEdit
        # self.IbidText.textChanged.connect(self.ibidTextChanged)

        # QTreeWidget: NoteBrowser
        # self.NoteBrowser.itemClicked.connect(self.BrowserNoteItem_pressed)
        self.NoteBrowser.setColumnWidth(0, 80)
        self.NoteBrowser.setColumnWidth(1, 40)
        self.NoteBrowser.setColumnWidth(2, 120)

        # self.populateNoteBrowser()

        # Regex Dialog
        # self.options_dialog = RegexDialog(self, self.bk)

        # Run
        # self.changeToNote(notes_index[0])
        #self.announce(str(len(notes_index)) + " notas leídas desde " + file)
        self.show()
        if book.first_seems_ibid:
            QtWidgets.QMessageBox.warning(self,
                                          'Advertencia', 'La primera nota parece ser ibid')

    def nextNoteButton_pressed(self):
        pass

    def prevNoteButton_pressed(self):
        pass

    def nextIbidButton_pressed(self):
        pass

    def prevIbidButton_pressed(self):
        pass

    def noteToIbidButton_pressed(self):
        pass

    def ibidToNoteButton_pressed(self):
        pass

    def undoIbidButton_pressed(self):
        pass

    def showTagButton_pressed(self):
        pass

    def showOriginalIbidButton_pressed(self):
        pass

    def configButton_pressed(self):
        pass

    def processIbidButton_pressed(self):
        pass

    def processAllIbidsButton_pressed(self):
        pass

    def ibidReplaceButton_pressed(self):
        pass

    def acceptButton_pressed(self):
        pass

    def cancelButton_pressed(self):
        pass

    def loadIcons(self, bk):
        # if platform.system() != "Linux":#import platform
        # Set dark or light mode
        # if (bk.launcher_version() >= 20200117) and bk.colorMode() == "dark":
        if True:
            self.theme = ":/dark-theme/"
        else:
            self.theme = ":/light-theme/"

        self.NoteToIbidButton.setIcon(
            QIcon(self.theme + "format-indent-more.svg"))
        self.TagButton.setIcon(QIcon(self.theme + "format-text-code.svg"))
        self.NotePrevButton.setIcon(QIcon(self.theme + "go-previous.svg"))
        self.NoteNextButton.setIcon(QIcon(self.theme + "go-next.svg"))
        self.IbidToNoteButton.setIcon(
            QIcon(self.theme + "format-indent-less.svg"))
        self.ShowOriginalIbid.setIcon(QIcon(self.theme + "view-visible.svg"))
        self.IbidUndoButton.setIcon(QIcon(self.theme + "edit-undo.svg"))
        self.IbidPrevButton.setIcon(QIcon(self.theme + "go-previous.svg"))
        self.IbidNextButton.setIcon(QIcon(self.theme + "go-next.svg"))
        self.RegexSelectorButton.setIcon(
            QIcon(self.theme + "application-menu.svg"))
        self.AcceptButton.setIcon(QIcon(self.theme + "dialog-ok-apply.svg"))
        self.CancelButton.setIcon(QIcon(self.theme + "dialog-cancel.svg"))


def theme_color(bk, app):
    # supports_theming = (bk.launcher_version() >= 20200117)
    # if not supports_theming:
    #     return
    # if bk.colorMode() != "dark":
        # return
    try:
        from PyQt5.QtGui import QColor, QPalette
        from PyQt5.QtWidgets import QStyleFactory
    except ImportError:
        return

    dark_theme = QPalette()
    sigil_colors = bk.color
    dark_color = QColor(sigil_colors("Window"))
    disabled_color = QColor(127, 127, 127)
    dark_link_color = QColor(108, 180, 238)
    text_color = QColor(sigil_colors("Text"))
    dark_theme.setColor(dark_theme.Window, dark_color)
    dark_theme.setColor(dark_theme.WindowText, text_color)
    dark_theme.setColor(dark_theme.Base, QColor(sigil_colors("Base")))
    dark_theme.setColor(dark_theme.AlternateBase, dark_color)
    dark_theme.setColor(dark_theme.ToolTipBase, dark_color)
    dark_theme.setColor(dark_theme.ToolTipText, text_color)
    dark_theme.setColor(dark_theme.Text, text_color)
    dark_theme.setColor(dark_theme.Disabled, dark_theme.Text, disabled_color)
    dark_theme.setColor(dark_theme.Button, dark_color)
    dark_theme.setColor(dark_theme.ButtonText, text_color)
    dark_theme.setColor(dark_theme.Disabled,
                        dark_theme.ButtonText, disabled_color)
    dark_theme.setColor(dark_theme.BrightText, Qt.red)
    dark_theme.setColor(dark_theme.Link, dark_link_color)
    dark_theme.setColor(dark_theme.Highlight,
                        QColor(sigil_colors("Highlight")))
    dark_theme.setColor(dark_theme.HighlightedText,
                        QColor(sigil_colors("HighlightedText")))
    dark_theme.setColor(dark_theme.Disabled,
                        dark_theme.HighlightedText, disabled_color)

    app.setStyle(QStyleFactory.create("Fusion"))
    app.setPalette(dark_theme)


def run(book) -> bool:
    save_file = False
    app = QtWidgets.QApplication(sys.argv)
    # theme_color(app)
    window = Window(book)
    # Mostramos la GUI y esperamos Aceptar o Cancelar
    app.exec_()

    return save_file
