#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2021 Titivillus
# www.epublibre.org
# Distributed under the terms of the GNU General Public License v2

import re
from src.regex import REGEX_IBID, REGEX_PAGE_INFO_SPLIT, \
                      REGEX_RANGE_INI, REGEX_RANGE_END


class Note:
    def __init__(self, note_id, note_number, note_text, note_href, note_index):
        # Data
        self.id = note_id
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

        # Gui
        self.current_label = ""
        self.browserEntry = None

    def setParent(self, item):
        if item != self:
            self.parent = item
        else:
            self.parent = None

    def getChild(self):
        if len(self.childs) > 0:
            return self.childs[0]
        return None

    def toXHTML(self) -> str:
        note_top = '  <div class="nota">\n    <p id="'
        note_mid = '{}"><sup>[{}]</sup> {} <a href="{}">&lt;&lt;</a></p>\n'\
                   .format(self.id, self.number, self.text, self.href)
        note_btm = '  </div>\n\n'

        return note_top + note_mid + note_btm

    def ibidCheck(self) -> bool:
        if re.search(REGEX_IBID, self.text):
            self.is_ibid = True
        return self.is_ibid

    def changeText(self, new_text):
        self.text = new_text
        self.edited = True

        return self.text

    def processIbid(self, regex, ibid_tag, separator) -> str:
        if not self.is_ibid:
            return self.text

        # Restauramos el texto original para evitar repeticiones recursivas.
        if self.processed:
            self.text = self.original_text
        self.processed = True

        if ibid_tag != "":
            ibid_tag += " "

        separator = (" " + separator + " ") if separator != "" else " "

        splited_note = re.split(regex, self.text, 2)
        splited_note = list(filter(None, splited_note))
        has_added_text = True if len(splited_note) > 0 else False

        # Chequeamos si la nota parent tiene info de pág.
        parent_text = re.split(REGEX_PAGE_INFO_SPLIT, self.parent.text)
        parent_text = list(filter(None, parent_text))

        if has_added_text and len(parent_text) == 2:
            parent_text = parent_text[0].strip()
            separator = " "
        # Casos con "TEXTO_NOTA_BASE págs. x a y."
        elif has_added_text and len(parent_text) == 3 and \
                re.search(REGEX_RANGE_INI, parent_text[1]) is not None and \
                re.search(REGEX_RANGE_END, parent_text[2]) is not None:
            parent_text = str(parent_text[0])
        else:
            parent_text = self.parent.text

        if has_added_text:
            added_text = ""
            for line in splited_note:
                added_text = added_text + line
            self.text = ibid_tag + parent_text + separator + added_text
        else:
            self.text = ibid_tag + parent_text

        return self.text

    def restoreOriginalText(self):
        self.text = self.original_text
        self.edited = False
        self.processed = False

        return self.text
