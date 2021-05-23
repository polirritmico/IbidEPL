import sys
import src.configWindow
import src.resources
try:
    from PyQt5 import uic, QtWidgets
    from PyQt5.QtCore import Qt, QEvent, QTimer, QRegExp
    from PyQt5.QtWidgets import QTreeWidgetItem, QStyleFactory
    from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QIcon, QPalette
except Exception as e:
    print("Error en linea {}: ".format(sys.exc_info()[-1].tb_lineno), type(
        e).__name__, e, "\n\nEste plugin requiere Sigil >0.9.8 o PyQt5.")
    sys.exit()


class Window(QtWidgets.QDialog):
    def __init__(self, _book, dark_theme):
        super(Window, self).__init__()
        uic.loadUi("src/mainWindow.ui", self)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # Set icons
        # if platform.system() != "Linux":#import platform
        # Set dark or light mode
        # if (bk.launcher_version() >= 20200117) and bk.colorMode() == "dark":
        if dark_theme:
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
        self.ConfigButton.setIcon(QIcon(self.theme + "application-menu.svg"))
        self.AcceptButton.setIcon(QIcon(self.theme + "dialog-ok-apply.svg"))
        self.CancelButton.setIcon(QIcon(self.theme + "dialog-cancel.svg"))

        # GUI Connections
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
        self.IbidProcessButton.clicked.connect(self.processIbidButton_pressed)
        self.IbidProcessAllButton.clicked.connect(
            self.processAllIbidsButton_pressed)
        # Aditional buttons
        self.ConfigButton.clicked.connect(self.configButton_pressed)
        self.TagButton.clicked.connect(self.showTagButton_pressed)
        self.ShowOriginalIbid.clicked.connect(
            self.showOriginalIbidButton_pressed)
        self.IbidOriginalText.setVisible(False)
        # Dialog confirmation buttons
        self.AcceptButton.clicked.connect(self.acceptButton_pressed)
        self.CancelButton.clicked.connect(self.cancelButton_pressed)
        # QtextEdit
        self.IbidText.textChanged.connect(self.ibidTextChanged)
        # QTreeWidget: NoteBrowser
        self.NoteBrowser.itemClicked.connect(self.browserNoteItem_pressed)
        self.NoteBrowser.setColumnWidth(0, 80)
        self.NoteBrowser.setColumnWidth(1, 40)
        self.NoteBrowser.setColumnWidth(2, 120)
        # Setup Dialog
        self.config_window = src.configWindow.ConfigWindow(dark_theme)

        # Set init state
        self.book = _book
        self.notes_index = _book.notes_index
        self.populateNoteBrowser()
        self.current_note = self.notes_index[0]
        self.changeToNote(self.current_note)
        self.changeToIbid(self.current_note.getChild())
        self.NoteBrowser.setCurrentItem(self.current_note.browserEntry)

        # Run
        self.announce(str(len(self.notes_index)) +
                      " notas leídas desde " + self.book.file.name)
        self.show()

        if self.book.first_seems_ibid:
            QtWidgets.QMessageBox.warning(self,
                                          'Advertencia', 'La primera nota parece ser ibid')

    def populateNoteBrowser(self):
        self.NoteBrowser.clear()

        # Cabeceras QTreeWidget: Id, Número, Texto, Index (int)
        for note in self.notes_index:
            entry = [note.id_tag, note.number, note.text, str(note.index)]
            note.browserEntry = QTreeWidgetItem(entry)
            if note.is_ibid:
                parentEntry.addChild(note.browserEntry)
            else:
                parentEntry = note.browserEntry
                self.NoteBrowser.addTopLevelItem(note.browserEntry)

        self.NoteBrowser.expandAll()

    def announce(self, message):
        self.Messenger.setText(message)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateMessenger)
        if len(message) > 30:
            self.timer.start(3000)
        else:
            self.timer.start(2000)

    def updateMessenger(self):
        tag_count = "Ibíd. sin ajustar: "
        unedited_ibid_count = 0
        for note in self.notes_index:
            if note.is_ibid and not note.edited:
                unedited_ibid_count += 1

        self.Messenger.setText(tag_count + str(unedited_ibid_count))

    def changeToNote(self, note):
        self.current_note = note

        self.NoteIdEntry.setText(note.id_tag)
        self.NoteEntry.setText(note.number)
        current_note_label = note.current_label + \
            " de " + str(self.book.base_note_count)
        self.NoteCurrent.setText(current_note_label)
        self.NoteHrefEntry.setText(note.href)
        self.NoteText.setPlainText(note.text)

        # Select QTreeWidgetItem
        # self.NoteBrowser.setCurrentItem(note.browserEntry)

    def changeToIbid(self, note):
        if note == None:
            self.current_ibid = None
            self.IbidIdEntry.setText("")
            self.IbidEntry.setText("")
            self.IbidCurrent.setText("")
            self.IbidText.setPlainText("Sin ibid.")
            self.IbidOriginalText.setPlainText("Sin ibid.")
            self.IbidHrefEntry.setText("")
        else:
            self.current_ibid = note
            self.IbidText.setReadOnly(False)
            self.IbidIdEntry.setText(note.id_tag)
            self.IbidEntry.setText(note.number)
            ibid_current = note.current_label + \
                " de " + str(self.book.ibid_note_count)
            self.IbidCurrent.setText(ibid_current)
            self.IbidHrefEntry.setText(note.href)
            self.IbidText.setPlainText(note.text)

        # self.NoteBrowser.setCurrentItem(note.browserEntry)

    def browserNoteItem_pressed(self, item):
        # item.text es un array: 0 Id, 1 Número, 2 Texto, 3 Index
        target_index = int(item.text(3))
        target_note = self.notes_index[target_index]

        if target_note.is_ibid:
            self.changeToNote(target_note.parent)
            self.changeToIbid(target_note)
        else:
            self.changeToIbid(target_note.getChild())
            self.changeToNote(target_note)

    def ibidTextChanged(self):
        pass

    def nextNoteButton_pressed(self):
        target = self.current_note.next_note
        if target != None:
            self.changeToIbid(target.getChild())
            self.changeToNote(target)
        else:
            self.changeToIbid(self.current_note.getChild())
        self.NoteBrowser.setCurrentItem(self.current_note.browserEntry)

    def prevNoteButton_pressed(self):
        target = self.current_note.prev_note
        if target != None:
            self.changeToIbid(target.getChild())
            self.changeToNote(target)
        else:
            self.changeToIbid(self.current_note.getChild())
        self.NoteBrowser.setCurrentItem(self.current_note.browserEntry)

    def nextIbidButton_pressed(self):
        target = self.book.getNextIbid(self.current_note, self.current_ibid)
        if target != None:
            self.changeToNote(target.parent)
            self.changeToIbid(target)
            self.NoteBrowser.setCurrentItem(target.browserEntry)
        elif self.current_ibid is not None:
            self.NoteBrowser.setCurrentItem(self.current_ibid.browserEntry)

    def prevIbidButton_pressed(self):
        target = self.book.getPrevIbid(self.current_note, self.current_ibid)
        if target != None:
            self.changeToNote(target.parent)
            self.changeToIbid(target)
            self.NoteBrowser.setCurrentItem(target.browserEntry)
        elif self.current_ibid is not None:
            self.NoteBrowser.setCurrentItem(self.current_ibid.browserEntry)

    def noteToIbidButton_pressed(self):
        current = self.current_note
        if current.index == 0:
            return
        self.book.noteToIbid(current)
        self.changeToNote(current.parent)
        self.changeToIbid(current)

        self.populateNoteBrowser()
        self.NoteBrowser.setCurrentItem(current.browserEntry)
        self.announce("Nota \"" + str(current.id_tag) + "\" cambiada a ibíd.")

    def ibidToNoteButton_pressed(self):
        current = self.current_ibid
        if not current.is_ibid:
            return

        self.book.ibidToNote(current)
        self.changeToNote(current)
        self.changeToIbid(current.getChild())

        self.populateNoteBrowser()
        self.NoteBrowser.setCurrentItem(current.browserEntry)
        self.announce("Ibíd. \"" + str(current.id_tag) + "\" cambiado a nota.")

    def undoIbidButton_pressed(self):
        pass

    def showTagButton_pressed(self):
        pass

    def showOriginalIbidButton_pressed(self, checked):
        if checked:
            self.IbidOriginalText.setVisible(True)
            self.ShowOriginalIbid.setIcon(
                QIcon(self.theme + "view-hidden.svg"))
        else:
            self.IbidOriginalText.setVisible(False)
            self.ShowOriginalIbid.setIcon(
                QIcon(self.theme + "view-visible.svg"))

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
        self.close()


def theme_color(app):
    # supports_theming = (bk.launcher_version() >= 20200117)
    # if not supports_theming:
    #     return
    # if bk.colorMode() != "dark":
        # return

    dark_theme = QPalette()
    # sigil_colors = bk.color
    # dark_color = QColor(sigil_colors("Window"))
    dark_color = QColor("#31363b")
    disabled_color = QColor(127, 127, 127)
    dark_link_color = QColor(108, 180, 238)
    # text_color = QColor(sigil_colors("Text"))
    text_color = QColor("#eff0f1")
    dark_theme.setColor(dark_theme.Window, dark_color)
    dark_theme.setColor(dark_theme.WindowText, text_color)
    # dark_theme.setColor(dark_theme.Base, QColor(sigil_colors("Base")))
    dark_theme.setColor(dark_theme.Base, QColor("#232629"))
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
    # dark_theme.setColor(dark_theme.Highlight,QColor(sigil_colors("Highlight")))
    dark_theme.setColor(dark_theme.Highlight, QColor("#3daee9"))
    # dark_theme.setColor(dark_theme.HighlightedText,QColor(sigil_colors("HighlightedText")))
    dark_theme.setColor(dark_theme.HighlightedText, QColor("#eff0f1"))
    dark_theme.setColor(dark_theme.Disabled,
                        dark_theme.HighlightedText, disabled_color)

    app.setStyle(QStyleFactory.create("Fusion"))
    app.setPalette(dark_theme)


def run(book, dark_theme) -> bool:
    overwrite = False
    app = QtWidgets.QApplication(sys.argv)
    theme_color(app)
    window = Window(book, dark_theme)
    # Mostramos la GUI y esperamos Aceptar o Cancelar
    app.exec_()

    return overwrite
