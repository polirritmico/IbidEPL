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
    regex_search_list = ["Default", "Personalizada"]
    regex_search_entries = [r'(?i)(?:<*.?>)?(?:ib[íi]d(?:em)?)(?:</i>)?(?:[;\., ]*)?',
                            r'(?i)(?:<*.?>)?(?:ib[íi]d(?:em)?)(?:</i>)?(?:[;\., ]*)?']

    ibid_label_list = ["<i>Ibid</i>", "<i>Ibidem</i>",
                       "Ibid (redonda)", "Ibidem (redonda)",
                       "Ibíd (con tilde)", "Ibídem (con tilde)",
                       "Personalizada"]
    ibid_label_entries = ['<i xml:lang="la">Ibid</i>.',
                          '<i xml:lang="la">Ibidem</i>.',
                          '<span xml:lang="la">Ibid</span>.', '<span xml:lang="la">Ibidem</span>',
                          'Ibíd.', 'Ibídem.',
                          '<i xml:lang="la">Ibid</i>.']

    separator_label_list = ["Default", "Nada", "Personalizado"]
    separator_label_entries = ["TEXTO_ADICIONAL:", "", "SEPARADOR"]

    demo_nota = "Esto es una nota de texto; ibíd., texto posterior: menciona págs. 116-119"
    demo_base_note = "Esta es la nota base, pág. 75"

    regex = ""
    ibid_label = ""
    separator = ""

    cancel_regex = ""
    cancel_ibid_label = ""
    cancel_separator = ""
    cancel_regex_idx = 0
    cancel_ibid_label_idx = 0
    cancel_separator_idx = 0

    prefs = {}

    def __init__(self, parent, bk):
        self.bk = bk
        super(RegexDialog, self).__init__()
        uic.loadUi(os.path.join(bk._w.plugin_dir,
                                bk._w.plugin_name, "configWindow.ui"), self)

        # Set Icons
        if (bk.launcher_version() >= 20200117) and bk.colorMode() == "dark":
            theme = ":/dark-theme/"
        else:
            theme = ":/light-theme/"
        self.DialogAcceptButton.setIcon(QIcon(theme + "dialog-ok-apply.svg"))
        self.DialogCancelButton.setIcon(QIcon(theme + "dialog-cancel.svg"))

        # Connect Buttons
        self.DialogAcceptButton.clicked.connect(
            self.dialogAcceptButton_pressed)
        self.DialogDefaultButton.clicked.connect(
            self.dialogDefaultButton_pressed)
        self.DialogCancelButton.clicked.connect(
            self.dialogCancelButton_pressed)
        self.TestButton.clicked.connect(self.testButton_pressed)

        # Populate ComboBoxes
        self.RegexComboBox.addItems(self.regex_search_list)
        self.IbidLabelComboBox.addItems(self.ibid_label_list)
        self.SeparatorComboBox.addItems(self.separator_label_list)

        self.RegexComboBox.currentIndexChanged.connect(
            self.regexComboBox_newValue)
        self.IbidLabelComboBox.currentIndexChanged.connect(
            self.ibidLabelComboBox_newValue)
        self.SeparatorComboBox.currentIndexChanged.connect(
            self.separatorComboBox_newValue)

        # Texts
        self.OriginalNote.setText(self.demo_nota)

        # Load Prefs
        self.prefs = self.bk.getPrefs()

        # Set Defaults
        self.prefs.defaults["RegEx_combobox"] = "0"
        self.prefs.defaults["RegEx"] = self.regex_search_entries[0]
        self.prefs.defaults["Ibid_combobox"] = "0"
        self.prefs.defaults["Ibid"] = self.ibid_label_entries[0]
        self.prefs.defaults["Separator_combobox"] = "0"
        self.prefs.defaults["Separator"] = self.separator_label_entries[0]

        # Load Values
        self.regex = self.prefs["RegEx"]
        self.ibid_label = self.prefs["Ibid"]
        self.separator = self.prefs["Separator"]

        # Set Currents
        self.RegexComboBox.setCurrentIndex(int(self.prefs["RegEx_combobox"]))
        self.IbidLabelComboBox.setCurrentIndex(
            int(self.prefs["Ibid_combobox"]))
        self.SeparatorComboBox.setCurrentIndex(
            int(self.prefs["Separator_combobox"]))

        self.regexComboBox_newValue(self.RegexComboBox.currentIndex())
        self.ibidLabelComboBox_newValue(self.IbidLabelComboBox.currentIndex())
        self.separatorComboBox_newValue(self.SeparatorComboBox.currentIndex())

        self.RegexEntry.setText(self.regex)
        self.IbidLabelEntry.setText(self.ibid_label)
        self.SeparatorEntry.setText(self.separator)

        self.setCancelValues()

    def setCancelValues(self):
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

    def dialogAcceptButton_pressed(self):
        # Test REGEX
        if not self.passedRegexText():
            return

        # Get updated values from the entries
        self.prefs["RegEx_combobox"] = self.RegexComboBox.currentIndex()
        self.prefs["Ibid_combobox"] = self.IbidLabelComboBox.currentIndex()
        self.prefs["Separator_combobox"] = self.SeparatorComboBox.currentIndex()
        self.prefs["RegEx"] = self.RegexEntry.text()
        self.prefs["Ibid"] = self.IbidLabelEntry.text()
        self.prefs["Separator"] = self.SeparatorEntry.text()

        self.regex = self.prefs["RegEx"]
        self.ibid_label = self.prefs["Ibid"]
        self.separator = self.prefs["Separator"]

        self.bk.savePrefs(self.prefs)
        self.setCancelValues()
        self.close()

    def dialogDefaultButton_pressed(self):
        # Set defaults
        self.prefs["RegEx_combobox"] = self.prefs.defaults["RegEx_combobox"]
        self.prefs["Ibid_combobox"] = self.prefs.defaults["Ibid_combobox"]
        self.prefs["Separator_combobox"] = self.prefs.defaults["Separator_combobox"]
        self.prefs["RegEx"] = self.prefs.defaults["RegEx"]
        self.prefs["Ibid"] = self.prefs.defaults["Ibid"]
        self.prefs["Separator"] = self.prefs.defaults["Separator"]

        # Restauramos los valores
        self.RegexComboBox.setCurrentIndex(int(self.prefs["RegEx_combobox"]))
        self.IbidLabelComboBox.setCurrentIndex(
            int(self.prefs["Ibid_combobox"]))
        self.SeparatorComboBox.setCurrentIndex(
            int(self.prefs["Separator_combobox"]))
        self.regex = self.prefs["RegEx"]
        self.ibid_label = self.prefs["Ibid"]
        self.separator = self.prefs["Separator"]

        # Actualizamos
        self.RegexComboBox.setCurrentIndex(int(self.prefs["RegEx_combobox"]))
        self.IbidLabelComboBox.setCurrentIndex(
            int(self.prefs["Ibid_combobox"]))
        self.SeparatorComboBox.setCurrentIndex(
            int(self.prefs["Separator_combobox"]))

        self.regexComboBox_newValue(self.RegexComboBox.currentIndex())
        self.ibidLabelComboBox_newValue(self.IbidLabelComboBox.currentIndex())
        self.separatorComboBox_newValue(self.SeparatorComboBox.currentIndex())

        self.RegexEntry.setText(self.regex)
        self.IbidLabelEntry.setText(self.ibid_label)
        self.SeparatorEntry.setText(self.separator)

        self.bk.savePrefs(self.prefs)

    def dialogCancelButton_pressed(self):
        # Restauramos los valores guardados
        self.RegexComboBox.setCurrentIndex(self.cancel_regex_idx)
        self.IbidLabelComboBox.setCurrentIndex(self.cancel_ibid_label_idx)
        self.SeparatorComboBox.setCurrentIndex(self.cancel_separator_idx)
        self.regex = self.cancel_regex
        self.ibid_label = self.cancel_ibid_label
        self.separator = self.cancel_separator

        self.RegexEntry.setText(self.regex)
        self.IbidLabelEntry.setText(self.ibid_label)
        self.SeparatorEntry.setText(self.separator)

        self.close()

    def passedRegexText(self) -> bool:
        try:
            test = processIbidem(self.demo_nota, self.demo_base_note, self.RegexEntry.text(),
                                 self.IbidLabelEntry.text(), self.SeparatorEntry.text())
        except:
            QtWidgets.QMessageBox.warning(
                self, 'ERROR', 'Problemas con la REGEX, ajustar.')
            return False
        return True

    def testButton_pressed(self):
        if not self.passedRegexText():
            return

        _separator = self.SeparatorEntry.text()
        text = processIbidem(self.demo_nota, self.demo_base_note, self.RegexEntry.text(),
                             self.IbidLabelEntry.text(), _separator)
        self.ProccesedNote.setPlainText(text)

        highlight(self.ProccesedNote, _separator)

    def getSeparator(self):
        return self.separator

    def getIbidTag(self):
        return self.ibid_label

    def getRegex(self):
        return self.regex

    def showDialog(self):
        self.show()
