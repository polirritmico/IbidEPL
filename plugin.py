#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
#
# ePLIbidem v0.4
# Una ayuda para manejar notas ibid.
#
# Copyright (C) 2021 Titivillus
# www.epublibre.org
#
# This file is part of ePLIbidem.
#
# ePLIbidem is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation version 2 of the License.
#
# ePLIbidem is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#########################################################################

# En términos generales el plugin genera un objeto Book (desde el archivo
# xhtml) que contiene una lista de todas las notas en notes_index[]. Cada
# nota contiene parseados los datos del texto además de referencias a la
# nota siguiente y la anterior. Las notas ibíd. solo referencian a notas
# ibíd. y las notas base solo a notas base. Para referencia a todas las
# notas está la lista notes_index.
#
# Además, las notas tienen una referencia parent que apunta a None en las
# notas que no son ibíd. y a la nota base en las ibíd.
# Book contiene funciones para manipular la estructura de las notas (por 
# ejemplo nota a ibíd. o viceversa) y Note funciones para cambiar su
# propia data.
#
# Para probar el código se ha separado su dependencia a Sigil creando la
# clase CopyBK que imita los métodos y variables que el plugin necesita de
# bookcontainer. A futuro se podría implementar una versión standalone
# implementando la clase e integrando una librería para seleccionar,
# extraer y modificar archivos del epub.

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
    book.getExtraTextFromHtml()
    try:
        book.autocheckIbidNotes()
        _test = book.notes_index[0]
    except IndexError:
        print("ERROR: El archivo seleccionado no parece ser un archivo de notas.")
        return -1

    book.updateParentsAndChilds()
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
    filename = "testFiles/notas.xhtml"

    file = open(filename, "r")
    html = file.read()
    file.close()

    book = Book(filename)
    book.readHTML(html)
    book.parseNotes()
    book.getExtraTextFromHtml()

    book.autocheckIbidNotes()
    book.updateParentsAndChilds()
    book.updateNextAndPrevNotes()
    book.updateNotesLabels()

    print("Archivo \"" + filename + "\" indexado exitosamente.")
    print("Abriendo interfaz QT...")
    dark_theme = True
    path = "src/"
    overwrite_xhtml = src.mainWindow.start(book, dark_theme, path, None)

    if overwrite_xhtml:
        file = open("outTest.xhtml", "w")
        file.write(book.bookToXHTML())
        file.close()
        print("Archivo escrito correctamente.")
    else:
        print("No se han escrito cambios.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
