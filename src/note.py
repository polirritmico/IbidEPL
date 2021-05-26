#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
#
# IbidEpl v0.4_beta
# Una ayuda para manejar notas ibid.
#
# Copyright (C) 2021 Titivillus
# www.epublibre.org
#
# This file is part of IbidEPL.
#
# IbidEPL is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IbidEPL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#########################################################################

import re

# Regex para encontrar ibids
REGEX_IBID = r'(?i)(ib[íi]d(em)?)[;\., (</i>)]'


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
        note_mid = self.id_tag + '"><sup>[' + self.number + ']</sup> ' + \
            self.text + ' <a href="' + self.href + '">&lt;&lt;</a></p>\n'
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
        # Si no restauramos al original se repite el mismo string
        if self.processed:
            self.text = self.original_text
        self.processed = True

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

    def restoreOriginalText(self):
        self.text = self.original_text
        self.edited = False
        self.processed = False

        return self.text
