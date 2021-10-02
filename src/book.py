#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2021 Titivillus
# www.epublibre.org
# Distributed under the terms of the GNU General Public License v2

import re
from src.note import Note
from src.regex import REGEX_SPLIT_NOTE, REGEX_GET_EXTRA_ENTRIES


class Book:
    def __init__(self, name):
        self.filename = name

        self.html_head = []
        self.html_body = []
        self.extra_entries = []
        self.notes_index = []

        self.first_seems_ibid = False
        self.ibid_note_count = 0
        self.base_note_count = 0

    def readHTML(self, html):
        html = html.splitlines()

        reading_header = True
        for line in html:
            if reading_header and line == '  <div class="nota">':
                reading_header = False
                self.html_body.append(line)
            elif reading_header:
                self.html_head.append(line)
            elif line != "</body>" and line != "</html>":
                self.html_body.append(line)

    def parseNotes(self):
        notes_raw = self.getNotesFromHtml()

        for index in range(len(notes_raw)):
            raw_note = re.split(REGEX_SPLIT_NOTE, notes_raw[index])
            # quitamos saltos vacíos: [""]
            raw_note = list(filter(None, raw_note))
            note = Note(raw_note[0], raw_note[1],
                        raw_note[2], raw_note[3], index)
            self.notes_index.append(note)

    def getNotesFromHtml(self) -> list:
        notes_raw = []
        note_buff = ""
        in_div = False
        for line in self.html_body:
            line = line.lstrip()
            if in_div and line == '</div>':
                in_div = False
                notes_raw.append(note_buff)
                note_buff = ""
            elif in_div: 
                note_buff += line
            elif line == '<div class="nota">':
                in_div = True

        return notes_raw

    def getExtraTextFromHtml(self) -> list:
        reference_note = Note
        index = 0
        in_div = False
        for line in self.html_body:
            # find() retorna -1 si no encuentra la búsqueda
            if in_div and line.find('<p id') != -1:
                reference_note = self.notes_index[index]
                index += 1
            elif in_div and line.find('</div>') != -1:
                in_div = False
            elif not in_div and line.find('<div class="nota">') != -1:
                in_div = True
            elif not in_div and line.find('<') != -1:
                entry = ExtraEntry(str.strip(line), reference_note)
                self.extra_entries.append(entry)

        return self.extra_entries

    def autocheckIbidNotes(self):
        for note in self.notes_index:
            note.ibidCheck()
        self.first_seems_ibid = self.notes_index[0].is_ibid
        self.notes_index[0].is_ibid = False

    def updateParentsAndChilds(self):
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

    def updateNextAndPrevNotes(self):
        # Obtenemos los next y prev de cada nota
        # (notas e ibíd. tienen cadenas independientes)
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

    def updateNotesLabels(self):
        # Debe usarse updateParentsAndChilds primero
        self.ibid_note_count = 0
        self.base_note_count = 0
        for note in self.notes_index:
            if note.is_ibid:
                self.ibid_note_count += 1
                note.current_label = str(self.ibid_note_count)
            else:
                self.base_note_count += 1
                note.current_label = str(self.base_note_count)

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
        self.updateParentsAndChilds()
        self.updateNotesLabels()
        self.updateNextAndPrevNotes()

    def noteToIbid(self, note):
        if note.is_ibid:
            return

        note.is_ibid = True
        self.updateParentsAndChilds()
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
        if current_ibid is not None:
            return current_ibid.prev_note

        index = current_note.index
        while index > 0:
            if self.notes_index[index].is_ibid:
                return self.notes_index[index]
            index -= 1
        return None

    def bookToXHTML(self) -> str:
        has_extra = True if len(self.extra_entries) > 0 else False
        prev_data = None

        head = "\n".join(self.html_head)
        body = "\n"
        for note in self.notes_index:
            body = body + note.toXHTML()
            if not has_extra:
                continue
            for line in self.extra_entries:
                if note == line.note_ref:
                    body = body + line.getEntry()
        body = body.rstrip()
        footer = "\n</body>\n</html>"

        return head + body + footer


class ExtraEntry:
    def __init__(self, _entry, _note_ref):
        self.entry = _entry
        self.note_ref = _note_ref

    def getEntry(self) -> str:
        return "  {}\n\n".format(self.entry)
