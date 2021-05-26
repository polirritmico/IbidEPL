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
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation version 2 of the License.
#
# IbidEPL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#########################################################################

""" 
En términos generales el plugin genera un objeto Book por cada
archivo leído, que contiene una lista de todas las notas en
notes_index[]. Cada nota contiene en primera instancia el id, el 
numero de llamado, el href y el texto extraídos desde el xhtml,
además de referencias a la nota siguiente y la anterior.
Las notas ibid solo referencian a notas ibid y las notas base
solo a notas base, para referencia a todas las notas está la
lista notes_index. Además las notas ibíd. referencian a su nota
base (parent).
Book además contiene funciones para manipular la estructura de
las notas.
"""

import sys
import os
import src.mainWindow
from src.book import Book


def run(bk):
    if bk.launcher_version() < 20170115:
        print("Este plugin requiere Sigil >0.9.8 \
        \n\nHaga clic en Aceptar para cerrar.")
        return -1

    selected_files = []
    for i in bk.selected_iter():
        selected_files.append(i)
    filename = selected_files[0][1]

    try:
        print("Leyendo archivo seleccionado...")
        html = bk.readfile(filename)
    except:
        print("ERROR: No se puede abrir el archivo seleccionado.")
        return -1

    book = Book(filename)
    book.readHTML(html)
    book.parseNotes()
    book.autocheckIbidNotes()

    try:
        _test = book.notes_index[0]
    except IndexError:
        print("ERROR: El archivo seleccionado no parece ser un archivo de notas.")
        return -1

    book.setParentsAndChilds()
    book.updateNextAndPrevNotes()
    book.updateNotesLabels()

    print("Archivo \"" + filename + "\" indexado exitosamente.")
    print("Abriendo interfaz QT...")

    dark_theme = False
    if (bk.launcher_version() >= 20200117) and bk.colorMode() == "dark":
        dark_theme = True

    path = os.path.join(bk._w.plugin_dir, bk._w.plugin_name, "src/")
    overwrite_xhtml = src.mainWindow.start(book, dark_theme, path, bk)

    if overwrite_xhtml:
        bk.writefile(filename, book.bookToXHTML())
        print("Archivo escrito correctamente.")
    else:
        print("No se han escrito cambios.")

    print("Pulse OK para volver a Sigil.")
    return 0


def main():
    # print("Error: Ejecutar desde Sigil.\n")
    # return -1
    filename = "testFiles/test_04.xhtml"

    file = open(filename, "r")
    html = file.read()
    file.close()

    book = Book(filename)
    book.readHTML(html)
    book.parseNotes()

    book.autocheckIbidNotes()
    book.setParentsAndChilds()
    book.updateNextAndPrevNotes()
    book.updateNotesLabels()

    print("Archivo \"" + filename + "\" indexado exitosamente.")
    print("Abriendo interfaz QT...")
    dark_theme = True
    path = "src/"
    overwrite_xhtml = src.mainWindow.start(book, dark_theme, path, None)

    if overwrite_xhtml:
        file = open("outTest_04.xhtml", "w")
        file.write(book.bookToXHTML())
        file.close()
        print("Archivo escrito correctamente.")
    else:
        print("No se han escrito cambios.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
