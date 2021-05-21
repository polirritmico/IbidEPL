#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IbidEpl v0.4_beta

Una ayuda para manejar notas ibid.
Titivillus
"""

import sys
# import os
# import re
#import book
# import note
import gui
# import resources
from book import Book
# from note import Note


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
    # print("Error: Ejecutar desde Sigil.\n")
    # return -1

    book = Book()
    book.readFile("testFiles/test_01.xhtml")
    book.parseNotes()
    book.autocheckIbidNotes()
    book.setParentsAndChilds()
    book.updateNextAndPrevNotes()


if __name__ == "__main__":
    sys.exit(main())
