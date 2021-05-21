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

    bk.writefile(file, html_header + html_body + html_foot)


def main():
        # print("Error: Ejecutar desde Sigil.\n")
        # return -1
    filename = "testFiles/test_01.xhtml"
    book = Book()
    book.readFile(filename)
    book.parseNotes()

    book.autocheckIbidNotes()
    book.setParentsAndChilds()
    book.updateNextAndPrevNotes()

    print("Archivo \"" + filename + "\" indexado exitosamente.")
    print("Abriendo interfaz QT...")
    overwrite_xhtml = gui.run()

    if overwrite_xhtml:
        file = open("outTest_01.xhtml", "w")
        file.write(book.bookToXHTML())
        file.close()
        print("Archivo escrito correctamente.")
    else:
        print("No se han escrito cambios.")

    print("Pulse OK para volver a Sigil.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
