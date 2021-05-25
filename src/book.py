#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from .note import Note


# RegExs para dividir data de las notas (id, llamada, texto y href)
REGEX_SPLIT_NOTE = r'<p id="(.*?)"><sup>\[(.*?)\]</sup>(.*?)<a href="(.*?)">&lt;&lt;</a></p>'


class Book:
    def __init__(self):
        self.file = None
        self.html_head = []
        self.html_body = []
        self.notes_index = []

        self.first_seems_ibid = False
        self.ibid_note_count = 0
        self.base_note_count = 0

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
        # Debe usarse setParentsAndChilds primero
        self.ibid_note_count = 0
        self.base_note_count = 0
        for note in self.notes_index:
            if note.is_ibid:
                self.ibid_note_count += 1
                note.current_label = str(self.ibid_note_count)
            else:
                self.base_note_count += 1
                note.current_label = str(self.base_note_count)

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

    def processAllIbids(self, regex, ibid_tag, separator):
        proc_count = 0
        for note in self.notes_index:
            if note.is_ibid:
                note.text = note.original_text
                note.text = note.processIbid(regex, ibid_tag, separator)
                note.processed = True
                proc_count += 1

        return str(proc_count)

    def ibidToNote(self, note):
        if not note.is_ibid:
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

    def getNextIbid(self, current_note, current_ibid):
        if current_ibid is not None:
            return current_ibid.next_note

        index = current_note.index
        while index < len(self.notes_index):
            if self.notes_index[index].is_ibid:
                return self.notes_index[index]
            index += 1
        return None

    def getPrevIbid(self, current_note, current_ibid):
        if current_ibid != None:
            return current_ibid.prev_note

        index = current_note.index
        while index > 0:
            if self.notes_index[index].is_ibid:
                return self.notes_index[index]
            index -= 1
        return None

    def bookToXHTML(self) -> str:
        head = "\n".join(self.html_head)
        body = "\n"
        for note in self.notes_index:
            body = body + note.toXHTML()
        footer = "</body>\n</html>"

        return head + body + footer
