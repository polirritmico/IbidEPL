#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.note import Note
from src.highlight import highlight
try:
    from PyQt5 import uic, QtWidgets
    from PyQt5.QtCore import QEvent, QTimer
    from PyQt5.QtWidgets import QTreeWidgetItem
    from PyQt5.QtGui import QIcon
except Exception as e:
    print("Error en linea {}: ".format(sys.exc_info()[-1].tb_lineno), type(
        e).__name__, e, "\n\nEste plugin requiere Sigil >0.9.8 y PyQt5.")
    sys.exit()


class ConfigWindow(QtWidgets.QDialog):
    def __init__(self, dark_theme):
        super(ConfigWindow, self).__init__()
        #uic.loadUi(os.path.join(bk._w.plugin_dir, bk._w.plugin_name, "Regex_dialog.ui"), self)
        uic.loadUi("src/configWindow.ui", self)
        # Set Icons
        # if (bk.launcher_version() >= 20200117) and bk.colorMode() == "dark":
        if dark_theme:
            theme = ":/dark-theme/"
        else:
            theme = ":/light-theme/"
        self.DialogAcceptButton.setIcon(QIcon(theme + "dialog-ok-apply.svg"))
        self.DialogCancelButton.setIcon(QIcon(theme + "dialog-cancel.svg"))

        # Connect Buttons
        self.DialogAcceptButton.clicked.connect(self.acceptButton_pressed)
        self.DialogDefaultButton.clicked.connect(self.defaultButton_pressed)
        self.DialogCancelButton.clicked.connect(self.cancelButton_pressed)
        self.TestButton.clicked.connect(self.testButton_pressed)

        self.regex_search_list = ["Default", "Personalizada"]
        self.regex_search_entries = [r'(?i)(?:<*.?>)?(?:ib[íi]d(?:em)?)(?:</i>)?(?:[;\., ]*)?',
                                     r'(?i)(?:<*.?>)?(?:ib[íi]d(?:em)?)(?:</i>)?(?:[;\., ]*)?']

        self.ibid_label_list = [
                "<i>Ibid</i>", "<i>Ibidem</i>",
                "Ibid (redonda)", "Ibidem (redonda)",
                "Ibíd (con tilde)", "Ibídem (con tilde)",
                "Personalizada"]
        self.ibid_label_entries = [
                '<i xml:lang="la">Ibid</i>.',
                '<i xml:lang="la">Ibidem</i>.',
                '<span xml:lang="la">Ibid</span>.', '<span xml:lang="la">Ibidem</span>',
                'Ibíd.', 'Ibídem.',
                '<i xml:lang="la">Ibid</i>.']

        self.separator_label_list = ["Default", "Nada", "Personalizado"]
        self.separator_label_entries = ["TEXTO_ADICIONAL:", "", "SEPARADOR"]

        self.demo_nota = "Esto es una nota de texto; ibíd., texto posterior: menciona págs. 116-119"
        self.demo_base_note = "Esta es la nota base, pág. 75"

        self.regex = ""
        self.ibid_label = ""
        self.separator = ""

        self.cancel_regex = ""
        self.cancel_ibid_label = ""
        self.cancel_separator = ""
        self.cancel_regex_idx = 0
        self.cancel_ibid_label_idx = 0
        self.cancel_separator_idx = 0

        # Populate ComboBoxes
        self.RegexComboBox.addItems(self.regex_search_list)
        self.IbidLabelComboBox.addItems(self.ibid_label_list)
        self.SeparatorComboBox.addItems(self.separator_label_list)

        self.RegexComboBox.currentIndexChanged.connect(self.regexComboBox_newValue)
        self.IbidLabelComboBox.currentIndexChanged.connect(self.ibidLabelComboBox_newValue)
        self.SeparatorComboBox.currentIndexChanged.connect(self.separatorComboBox_newValue)

        # Texts
        self.OriginalNote.setText(self.demo_nota)

        # Load Values
        self.regex = r'(?i)(?:<*.?>)?(?:ib[íi]d(?:em)?)(?:</i>)?(?:[;\., ]*)?'
        self.ibid_label = '<i xml:lang="la">Ibid</i>.'
        self.separator = 'TEXTO_ADICIONAL:'

        # Set Currents
        # self.RegexComboBox.setCurrentIndex(self.prefs["RegEx_combobox"])
        # self.IbidLabelComboBox.setCurrentIndex(self.prefs["Ibid_combobox"])
        # self.SeparatorComboBox.setCurrentIndex(self.prefs["Separator_combobox"])

        self.regexComboBox_newValue(self.RegexComboBox.currentIndex())
        self.ibidLabelComboBox_newValue(self.IbidLabelComboBox.currentIndex())
        self.separatorComboBox_newValue(self.SeparatorComboBox.currentIndex())

        self.RegexEntry.setText(self.regex)
        self.IbidLabelEntry.setText(self.ibid_label)
        self.SeparatorEntry.setText(self.separator)

        self.saveCancelValues()

    def saveCancelValues(self):
        # Set cancel values
        self.cancel_regex_idx = self.RegexComboBox.currentIndex()
        self.cancel_ibid_label_idx = self.IbidLabelComboBox.currentIndex()
        self.cancel_separator_idx = self.SeparatorComboBox.currentIndex()
        self.cancel_regex = self.regex
        self.cancel_ibid_label = self.ibid_label
        self.cancel_separator = self.separator

    def regexComboBox_newValue(self, index):
        if index == len(self.regex_search_entries) - 1:
            self.RegexEntry.setEnabled(True)
        else:
            self.RegexEntry.setEnabled(False)
        
        self.RegexEntry.setText(self.regex_search_entries[index])

    def ibidLabelComboBox_newValue(self, index):
        if index == len(self.ibid_label_entries) - 1:
            self.IbidLabelEntry.setEnabled(True)
        else:
            self.IbidLabelEntry.setEnabled(False)
        
        self.IbidLabelEntry.setText(self.ibid_label_entries[index])

    def separatorComboBox_newValue(self, index):
        if index == len(self.separator_label_entries) - 1:
            self.SeparatorEntry.setEnabled(True)
        else:
            self.SeparatorEntry.setEnabled(False)
        
        self.SeparatorEntry.setText(self.separator_label_entries[index])

    def testButton_pressed(self):
        # setup simple test enviroment
        parent = Note("nt1", "1", self.demo_base_note, "href", 1)
        child = Note("nt2", "2", self.demo_nota, "href", 2)
        child.parent = parent
        child.is_ibid = True

        test = child.processIbid(self.RegexEntry.text(),
                self.IbidLabelEntry.text(), self.SeparatorEntry.text())
        self.ProccesedNote.setPlainText(test)

        highlight(self.ProccesedNote, self.SeparatorEntry.text())

    def acceptButton_pressed(self):
        self.regex = self.RegexEntry.text()
        self.ibid_label = self.IbidLabelEntry.text()
        self.separator = self.SeparatorEntry.text()

        self.close()

    def defaultButton_pressed(self):
        pass

    def cancelButton_pressed(self):
        self.reject()

    def showDialog(self):
        self.show()
