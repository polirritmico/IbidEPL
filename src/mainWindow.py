import sys
import src.configWindow
import src.resources
try:
    from PyQt5 import uic, QtWidgets
    from PyQt5.QtCore import Qt, QEvent, QTimer
    from PyQt5.QtWidgets import QTreeWidgetItem, QStyleFactory
    from PyQt5.QtGui import QColor, QIcon, QPalette
except Exception as e:
    print("Error en linea {}: ".format(sys.exc_info()[-1].tb_lineno), type(
        e).__name__, e, "\n\nEste plugin requiere Sigil >0.9.8 o PyQt5.")
    sys.exit()


class Window(QtWidgets.QDialog):
    def __init__(self, _book, dark_mode):
        super(Window, self).__init__()
        uic.loadUi("src/mainWindow.ui", self)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # Set icons
        # if platform.system() != "Linux":#import platform
        # if (bk.launcher_version() >= 20200117) and bk.colorMode() == "dark":
        if dark_mode:
            self.theme = ":/dark-theme/"
        else:
            self.theme = ":/light-theme/"

        self.NoteToIbidButton.setIcon(QIcon(self.theme + "format-indent-more.svg"))
        self.TagButton.setIcon(QIcon(self.theme + "format-text-code.svg"))
        self.NotePrevButton.setIcon(QIcon(self.theme + "go-previous.svg"))
        self.NoteNextButton.setIcon(QIcon(self.theme + "go-next.svg"))
        self.IbidToNoteButton.setIcon(QIcon(self.theme + "format-indent-less.svg"))
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
        # Note/ibid to ibid/note buttons
        self.NoteToIbidButton.clicked.connect(self.noteToIbidButton_pressed)
        self.IbidToNoteButton.clicked.connect(self.ibidToNoteButton_pressed)
        # Edit ibid buttons
        self.IbidUndoButton.clicked.connect(self.undoIbidButton_pressed)
        self.IbidReplaceButton.clicked.connect(self.ibidReplaceButton_pressed)
        self.IbidProcessButton.clicked.connect(self.processIbidButton_pressed)
        self.IbidProcessAllButton.clicked.connect(self.processAllIbidsButton_pressed)
        # Aditional buttons
        self.ConfigButton.clicked.connect(self.configButton_pressed)
        self.TagButton.clicked.connect(self.showTagButton_pressed)
        self.ShowOriginalIbid.clicked.connect(self.showOriginalIbidButton_pressed)
        # Dialog confirmation buttons
        self.AcceptButton.clicked.connect(self.acceptButton_pressed)
        self.CancelButton.clicked.connect(self.cancelButton_pressed)
        # QtextEdit
        self.IbidText.textChanged.connect(self.ibidTextChanged)
        self.IbidOriginalText.setVisible(False)
        # QTreeWidget: NoteBrowser
        self.NoteBrowser.itemClicked.connect(self.browserNoteItem_pressed)
        self.NoteBrowser.setColumnWidth(0, 80)
        self.NoteBrowser.setColumnWidth(1, 40)
        self.NoteBrowser.setColumnWidth(2, 120)

        # Setup Dialog
        self.config_window = src.configWindow.ConfigWindow(dark_mode)

        # Setup
        self.book = _book
        self.notes_index = _book.notes_index
        self.current_note = self.notes_index[0]
        self.tag_html = False

        self.populateNoteBrowser()
        self.changeToNote(self.current_note)
        self.changeToIbid(self.current_note.getChild())
        self.NoteBrowser.setCurrentItem(self.current_note.browserEntry)

        # Run
        self.announce(str(len(self.notes_index)) +
                " notas leídas desde " + self.book.file.name)
        self.show()

        if self.book.first_seems_ibid:
            QtWidgets.QMessageBox.warning(
                self, 'Advertencia', 'La primera nota parece ser ibid')

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

    def wheelEvent(self, e):
        # FIX soltar ctrl poder escribir
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            self.NoteText.setReadOnly(True)
            self.IbidText.setReadOnly(True)

    def changeToNote(self, note):
        self.current_note = note
        self.NoteIdEntry.setText(note.id_tag)
        self.NoteEntry.setText(note.number)
        self.NoteCurrent.setText(note.current_label + " de " +
                str(self.book.base_note_count))
        self.NoteHrefEntry.setText(note.href)
        self.NoteText.setPlainText(note.text)

    def changeToIbid(self, note):
        if note is None:
            self.current_ibid = None
            self.IbidIdEntry.setText("")
            self.IbidEntry.setText("")
            self.IbidCurrent.setText("")
            self.IbidText.setPlainText("Sin ibid.")
            self.IbidOriginalText.setPlainText("Sin ibid.")
            self.IbidHrefEntry.setText("")
            return

        self.current_ibid = note
        self.IbidIdEntry.setText(note.id_tag)
        self.IbidEntry.setText(note.number)
        ibid_current = note.current_label + \
            " de " + str(self.book.ibid_note_count)
        self.IbidCurrent.setText(ibid_current)
        self.IbidOriginalText.setPlainText(note.original_text)
        self.IbidHrefEntry.setText(note.href)

        if self.tag_html:
            self.IbidText.setReadOnly(True)
            self.IbidText.setText(note.text)
        else:
            self.IbidText.setReadOnly(False)
            self.IbidText.setPlainText(note.text)

    def ibidTextChanged(self):
        pass

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

    def nextNoteButton_pressed(self):
        target = self.current_note.next_note
        if target is not None:
            self.changeToIbid(target.getChild())
            self.changeToNote(target)
        else:
            self.changeToIbid(self.current_note.getChild())
        self.NoteBrowser.setCurrentItem(self.current_note.browserEntry)

    def prevNoteButton_pressed(self):
        target = self.current_note.prev_note
        if target is not None:
            self.changeToIbid(target.getChild())
            self.changeToNote(target)
        else:
            self.changeToIbid(self.current_note.getChild())
        self.NoteBrowser.setCurrentItem(self.current_note.browserEntry)

    def nextIbidButton_pressed(self):
        target = self.book.getNextIbid(self.current_note, self.current_ibid)
        if target is not None:
            self.changeToNote(target.parent)
            self.changeToIbid(target)
            self.NoteBrowser.setCurrentItem(target.browserEntry)
        elif self.current_ibid is not None:
            self.NoteBrowser.setCurrentItem(self.current_ibid.browserEntry)

    def prevIbidButton_pressed(self):
        target = self.book.getPrevIbid(self.current_note, self.current_ibid)
        if target is not None:
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

        self.announce('Nota \"' + str(current.id_tag) + '\" cambiada a ibíd.')

    def ibidToNoteButton_pressed(self):
        current = self.current_ibid
        if current is None:
            return

        self.book.ibidToNote(current)
        self.changeToNote(current)
        self.changeToIbid(current.getChild())

        self.populateNoteBrowser()
        self.NoteBrowser.setCurrentItem(current.browserEntry)
        self.announce("Ibíd. \"" + str(current.id_tag) + "\" cambiado a nota.")

    def undoIbidButton_pressed(self):
        if self.current_ibid is None:
            return

        if self.current_ibid.edited or self.current_ibid.processed:
            self.current_ibid.browserEntry.setText(
                2, self.current_ibid.restore())
            self.changeToIbid(self.current_ibid)
            self.announce("Restaurado ibid. " + self.current_ibid.id_tag)
        else:
            self.announce("La nota ibíd. no ha sido alterada.")

    def showTagButton_pressed(self, checked):
        self.tag_html = checked
        self.changeToNote(self.current_note)
        self.changeToIbid(self.current_ibid)

    def showOriginalIbidButton_pressed(self, checked):
        if checked:
            self.IbidOriginalText.setVisible(True)
            self.ShowOriginalIbid.setIcon(QIcon(self.theme + "view-hidden.svg"))
        else:
            self.IbidOriginalText.setVisible(False)
            self.ShowOriginalIbid.setIcon(QIcon(self.theme + "view-visible.svg"))

    def configButton_pressed(self):
        self.config_window.showDialog()

    def processIbidButton_pressed(self):
        if self.current_ibid is None:
            return

        self.current_ibid.processIbid(self.config_window.regex,
                                      self.config_window.ibid_label,
                                      self.config_window.separator)
        self.current_ibid.processed = True
        self.has_change = True

        self.changeToIbid(self.current_ibid)
        self.current_ibid.browserEntry.setText(2, self.current_ibid.text)
        self.IbidUndoButton.setEnabled(True)

        # self.IbidText.setStyleSheet("")
        self.announce("Ibid procesado sin guardar")

    def processAllIbidsButton_pressed(self):
        proc_count = self.book.processAllIbids(
            self.config_window.regex, self.config_window.ibid_label,
            self.config_window.separator)

        self.populateNoteBrowser()
        self.changeToNote(self.notes_index[0])
        self.changeToIbid(self.notes_index[0].getChild())
        self.NoteBrowser.setCurrentItem(self.current_note.browserEntry)

        self.announce("Se han modificado " + proc_count + " notas")

    def ibidReplaceButton_pressed(self):
        if self.current_ibid is None:
            return
        self.current_ibid.changeText(self.IbidText.toPlainText())
        self.current_ibid.browserEntry.setText(2, self.current_ibid.text)

        self.announce("Modificada la nota ibíd. " + self.current_ibid.id_tag)

    def acceptButton_pressed(self):
        global overwrite
        overwrite = True
        self.accept()

    def cancelButton_pressed(self):
        global overwrite
        overwrite = False
        self.reject()


def theme_color(app):
    # supports_theming = (bk.launcher_version() >= 20200117)
    # if not supports_theming:
    #     return
    # if bk.colorMode() != "dark":
    #     return

    dark_mode = QPalette()
    # sigil_colors = bk.color
    # dark_color = QColor(sigil_colors("Window"))
    dark_color = QColor("#31363b")
    disabled_color = QColor(127, 127, 127)
    dark_link_color = QColor(108, 180, 238)
    # text_color = QColor(sigil_colors("Text"))
    text_color = QColor("#eff0f1")
    dark_mode.setColor(dark_mode.Window, dark_color)
    dark_mode.setColor(dark_mode.WindowText, text_color)
    # dark_mode.setColor(dark_mode.Base, QColor(sigil_colors("Base")))
    dark_mode.setColor(dark_mode.Base, QColor("#232629"))
    dark_mode.setColor(dark_mode.AlternateBase, dark_color)
    dark_mode.setColor(dark_mode.ToolTipBase, dark_color)
    dark_mode.setColor(dark_mode.ToolTipText, text_color)
    dark_mode.setColor(dark_mode.Text, text_color)
    dark_mode.setColor(dark_mode.Disabled, dark_mode.Text, disabled_color)
    dark_mode.setColor(dark_mode.Button, dark_color)
    dark_mode.setColor(dark_mode.ButtonText, text_color)
    dark_mode.setColor(dark_mode.Disabled,
                       dark_mode.ButtonText, disabled_color)
    dark_mode.setColor(dark_mode.BrightText, Qt.red)
    dark_mode.setColor(dark_mode.Link, dark_link_color)
    # dark_mode.setColor(dark_mode.Highlight,QColor(sigil_colors("Highlight")))
    dark_mode.setColor(dark_mode.Highlight, QColor("#3daee9"))
    # dark_mode.setColor(dark_mode.HighlightedText,QColor(sigil_colors("HighlightedText")))
    dark_mode.setColor(dark_mode.HighlightedText, QColor("#eff0f1"))
    dark_mode.setColor(dark_mode.Disabled,
                       dark_mode.HighlightedText, disabled_color)

    app.setStyle(QStyleFactory.create("Fusion"))
    app.setPalette(dark_mode)


def run(book, dark_mode) -> bool:
    global overwrite
    overwrite = False
    app = QtWidgets.QApplication(sys.argv)
    theme_color(app)
    window = Window(book, dark_mode)
    # Mostramos la GUI y esperamos Aceptar o Cancelar
    app.exec_()

    return overwrite
