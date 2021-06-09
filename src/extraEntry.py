#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2021 Titivillus
# www.epublibre.org
# Distributed under the terms of the GNU General Public License v2

class ExtraEntry:
    def __init__(self, _entry, _note_ref):
        self.entry = _entry
        self.note_ref = _note_ref

    def getEntry(self) -> str:
        return "  {}\n\n".format(self.entry)
