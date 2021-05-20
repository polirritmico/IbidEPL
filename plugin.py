#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
IbidEPL v0.4
"""

import sys
import os
import re
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


# RegExs para detectar ibids y para dividir la info de las notas.
# (id, llamada, texto y href)
REGEX_IBID = r'(?i)(ib[íi]d(em)?)[;\., (</i>)]'
REGEX_SPLIT_NOTE = r'<p id="(.*?)"><sup>\[(.*?)\]</sup>(.*?)<a href="(.*?)">&lt;&lt;</a></p>'


class Book:
    def __init__(self):
        self.file = None
        self.html_head = []
        self.html_body = []
        self.notes_index = []

        self.first_seems_ibid = False

    def readFile(self, _file):
        self.file = open(_file, "r")
        html = self.file.read()
        self.file.close()
        html = html.split('\n')

        reading_header = True
        for line in html:
            if reading_header and line == '  <div class="nota">':
                reading_header = False
                self.html_body.append(line)
            elif reading_header:
                self.html_head.append(line)
            elif line != "</body>" and line != "</html>":
                self.html_body.append(line)

    def getNotesFromHtml(self) -> list:
        notes_raw = []
        for line in self.html_body:
            # find() tiene output -1 cuando es not found
            if line.find("<p id") != -1:
                notes_raw.append(line.lstrip())
        return notes_raw

    def parseNotes(self):
        notes_raw = self.getNotesFromHtml()

        for index in range(len(notes_raw)):
            raw_note = re.split(REGEX_SPLIT_NOTE, notes_raw[index])
            # quitamos saltos vacíos: [""]
            raw_note = list(filter(None, raw_note))
            note = Note(raw_note[0], raw_note[1],
                        raw_note[2], raw_note[3], index)
            self.notes_index.append(note)

        self.autocheckIbidNotes()

    def autocheckIbidNotes(self):
        for note in self.notes_index:
            note.ibidCheck()
        self.first_seems_ibid = self.notes_index[0].is_ibid
        self.notes_index[0].is_ibid = False

    def setParentsAndChilds(self):
        parent = None
        for note in self.notes_index:
            note.childs.clear()
            note.text = note.text.strip()

            if note.is_ibid:
                parent.childs.append(note)
                note.setParent(parent)
            else:
                parent = note
                note.setParent(None)

    def updateNotesLabels(self):
        # Debe usarse setPArentsAndChilds primero
        note_label_count = 0
        ibid_label_count = 0
        for note in self.notes_index:
            if note.is_ibid:
                ibid_label_count += 1
                note.current_label = str(ibid_label_count)
            else:
                note_label_count += 1
                note.current_label = str(note_label_count)

    def updateNextAndPrevNotes(self):
        # Obtenemos los next y prev de cada nota
        # (prev/next ibid, o prev/next nota segun corresponda)
        prev_note = None
        prev_ibid = None

        first_note = True
        first_ibid = True

        for current_note in self.notes_index:
            if first_note:
                current_note.prev_note = None
                current_note.next_note = None
                prev_note = current_note
                first_note = False
                continue
            elif first_ibid and current_note.is_ibid:
                current_note.prev_note = None
                current_note.next_note = None
                prev_ibid = current_note
                first_ibid = False
                continue

            if current_note.is_ibid:
                prev_ibid.next_note = current_note
                current_note.prev_note = prev_ibid
                current_note.next_note = None
                prev_ibid = current_note
            else:
                prev_note.next_note = current_note
                current_note.prev_note = prev_note
                current_note.next_note = None
                prev_note = current_note

    def ibidToNote(self, note):
        if note.is_ibid == False:
            return

        note.is_ibid = False
        self.setParentsAndChilds()
        self.updateNotesLabels()
        self.updateNextAndPrevNotes()

    def noteToIbid(self, note):
        if note.is_ibid:
            return

        note.is_ibid = True
        self.setParentsAndChilds()
        self.updateNotesLabels()
        self.updateNextAndPrevNotes()

    def bookToXHTML(self) -> str:
        head = "\n".join(self.html_head)
        body = "\n"
        for note in self.notes_index:
            body = body + note.toXHTML()
        footer = "</body>\n</html>"

        return head + body + footer


class Note:
    def __init__(self, note_id, note_number, note_text, note_href, note_index):
        # Data
        self.id_tag = note_id
        self.number = note_number
        # text sin strip por comportamiento extraño de la REGEX
        self.text = note_text
        self.original_text = note_text.strip()
        self.href = note_href
        self.index = note_index

        # Collection and Control
        self.childs = []
        self.is_ibid = False
        self.parent = None
        self.next_note = None
        self.prev_note = None

        self.edited = False
        self.processed = False

        # Ui
        self.current_label = ""
        self.browserEntry = None

    def setParent(self, item):
        if item != self:
            self.parent = item
        else:
            self.parent = None

    def toXHTML(self) -> str:
        note_top = '  <div class="nota">\n    <p id="'
        note_mid = self.id_tag + '"><sup>[' + self.number + ']</sup> ' + \
            self.text + ' <a href="' + self.href + '">&lt;&lt;</a></p>\n'
        note_btm = '  </div>\n\n'

        return note_top + note_mid + note_btm

    def ibidCheck(self) -> bool:
        if re.search(REGEX_IBID, self.text):
            self.is_ibid = True
        return self.is_ibid

    def processIbidem(self, regex, ibid_tag, separator) -> str:
        if not self.is_ibid:
            return self.text
        if regex == "":
            regex = r'(?i)(?:<*.?>)?(?:ib[íi]d(?:em)?)(?:</i>)?(?:[;\., ]*)?'

        splited_note = re.split(regex, self.text)
        splited_note = list(filter(None, splited_note))

        has_added_text = True if len(splited_note) > 0 else False
        if has_added_text:
            added_text = ""
            for line in splited_note:
                added_text = added_text + line
            self.text = ibid_tag + " " + self.parent.text + " " + \
                separator + " " + added_text
        else:
            self.text = ibid_tag + " " + self.parent.text

        return self.text


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
