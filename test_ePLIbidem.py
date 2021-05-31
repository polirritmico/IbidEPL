#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2021 Titivillus
# www.epublibre.org
# Distributed under the terms of the GNU General Public License v2

import unittest
import os
from src.book import Book
from src.note import Note
from src.configWindow import REGEX_SPLIT
from hashlib import sha512


class TestInputs(unittest.TestCase):
    def setUp(self):
        self.compendium = []
        for filename in sorted(os.listdir("testFiles/")):
            file = open(("testFiles/" + filename), "r")
            html = file.read()
            file.close()
            book = Book("testFiles/" + filename)
            book.readHTML(html)
            self.compendium.append(book)

    def test_head_readed(self):
        for book in self.compendium:
            self.assertEqual('<?xml version="1.0" encoding="utf-8"?>',
                             book.html_head[0])

    def test_body_readed(self):
        for book in self.compendium:
            self.assertEqual('  <div class="nota">', book.html_body[0])

    def test_count_file_notes_lines_readed(self):
        for book in self.compendium:
            if book.filename == "testFiles/test_01.xhtml":
                self.assertEqual(9, len(list(filter(None, book.html_body))))
            elif book.filename == "testFiles/test_02.xhtml":
                self.assertEqual(24, len(list(filter(None, book.html_body))))
            elif book.filename == "testFiles/test_03.xhtml":
                self.assertEqual(234, len(list(filter(None, book.html_body))))
            elif book.filename == "testFiles/test_04.xhtml":
                self.assertEqual(309, len(list(filter(None, book.html_body))))
            elif book.filename == "testFiles/test_05.xhtml":
                self.assertEqual(378, len(list(filter(None, book.html_body))))
            elif book.filename == "testFiles/test_06.xhtml":
                self.assertEqual(390, len(list(filter(None, book.html_body))))
            else:
                continue

    def test_get_extra_data_from_html(self):
        for book in self.compendium:
            if book.filename != "testFiles/notas.xhtml":
                continue
            book.parseNotes()
            expected = [
                # '<p class="item">I. «Colonización» y «Colonias»</p>',
                '<p class="item">II. «Colonialismo» e «Imperios coloniales»</p>',
                '<p>Caso más complicado</p>',
                '<p class="item">III. Épocas del colonialismo</p>',
                '<p class="item">IV. Conquista, resistencia y colaboración</p>',
                '<p class="item">V. El estado colonial</p>',
                '<p class="item">VI. Formas económicas coloniales</p>',
                '<p class="item">VII. Sociedades coloniales"</p>',
                '<p class="item">VIII. Colonialismo y cultura indígena</p>',
                '<p class="item">IX. Pensamiento colonialista y cultura colonial</p>'
            ]
            test_text = book.getExtraTextFromHtml()
            self.assertEqual(9, len(test_text))
            for case in range(len(expected)):
                self.assertEqual(test_text[case].entry, expected[case])

    def test_check_extra_Data_position(self):
        for book in self.compendium:
            if book.filename != "testFiles/notas.xhtml":
                continue
            book.parseNotes()
            expected = [
                book.notes_index[2],
                book.notes_index[2],
                book.notes_index[5],
                book.notes_index[8],
                book.notes_index[11],
                book.notes_index[14],
                book.notes_index[16],
                book.notes_index[19],
                book.notes_index[22],
            ]
            test_text = book.getExtraTextFromHtml()
            for case in range(len(expected)):
                self.assertEqual(test_text[case].note_ref, expected[case])

class TestProcess(unittest.TestCase):
    def setUp(self):
        self.compendium = []
        for filename in sorted(os.listdir("testFiles/")):
            file = open(("testFiles/" + filename), "r")
            html = file.read()
            file.close()
            book = Book("testFiles/" + filename)
            book.readHTML(html)
            book.parseNotes()
            book.autocheckIbidNotes()
            book.updateParentsAndChilds()
            book.updateNextAndPrevNotes()

            self.compendium.append(book)

    def test_notes_processed_count(self):
        for book in self.compendium:
            if book.filename == "testFiles/test_01.xhtml":
                self.assertEqual(3, len(book.notes_index))
            elif book.filename == "testFiles/test_02.xhtml":
                self.assertEqual(8, len(book.notes_index))
            elif book.filename == "testFiles/test_03.xhtml":
                self.assertEqual(78, len(book.notes_index))
            elif book.filename == "testFiles/test_04.xhtml":
                self.assertEqual(103, len(book.notes_index))
            elif book.filename == "testFiles/test_05.xhtml":
                self.assertEqual(126, len(book.notes_index))
            elif book.filename == "testFiles/test_06.xhtml":
                self.assertEqual(130, len(book.notes_index))
            else:
                continue

    def test_case_notes_parse_data(self):
        for book in self.compendium:
            if book.filename == "testFiles/test_01.xhtml":
                self.assertEqual("1", book.notes_index[0].number)
                self.assertEqual("Nota 1. <cite>Esta es una cita</cite>",
                                 book.notes_index[0].original_text)
                self.assertEqual("Section0001.xhtml#rf1",
                                 book.notes_index[0].href)
                self.assertEqual(0, book.notes_index[0].index)
            elif book.filename == "testFiles/test_02.xhtml":
                self.assertEqual("nt6", book.notes_index[5].id)
                self.assertEqual("6", book.notes_index[5].number)
                self.assertEqual("iBid.,. y más malformmaciones pág 50-150. Lorem Ipsum. Texto para confundir escribidme, escribídme 2021-2012. caçitulo 234.",
                                 book.notes_index[5].original_text)
                self.assertEqual("../Text/Section0001.xhtml#rf6",
                                 book.notes_index[5].href)
                self.assertEqual(5, book.notes_index[5].index)
            elif book.filename == "testFiles/test_03.xhtml":
                self.assertEqual("nt55", book.notes_index[54].id)
                self.assertEqual("55", book.notes_index[54].number)
                self.assertEqual("Dolores Ibárruri y otros, <i>Guerra y revolución en España 1936-1939</i>, pp. 33-34.",
                                 book.notes_index[54].original_text)
                self.assertEqual("1.xhtml#rf55",
                                 book.notes_index[54].href)
                self.assertEqual(54, book.notes_index[54].index)
            elif book.filename == "testFiles/test_04.xhtml":
                self.assertEqual("nt12", book.notes_index[11].id)
                self.assertEqual("12", book.notes_index[11].number)
                self.assertEqual("Ibid.", book.notes_index[11].original_text)
                self.assertEqual("5.xhtml#rf12",
                                 book.notes_index[11].href)
                self.assertEqual(11, book.notes_index[11].index)
            elif book.filename == "testFiles/test_05.xhtml":
                self.assertEqual("nt64", book.notes_index[63].id)
                self.assertEqual("64", book.notes_index[63].number)
                self.assertEqual('Kossert, <cite xml:lang="de">Ostpreussen: Geschichte und Mythos</cite>, pág. 212. Con la idea de mantener la producción agrícola frente a la competitividad de los países recién fundados de la Europa oriental, los gobiernos prusianos y del Reich instauraron programas conocidos como Osthilfe (Programa de Ayuda al Este) y el Ostpreußen-Hilfe (Programa de Ayuda a Prusia Oriental) durante los años veinte. Por lo que tocaba a la estimulación de la economía, aquellos programas resultaron en general y relativamente poco efectivos. Sin embargo, sirvieron para fortalecer la posición de la aristocracia terrateniente. Véase Hans Mommsen, <cite xml:lang="en">The Rise and Fall of Weimar Democracy</cite> (Chapel Hill, 1996); págs. <span class="nosep">229, 286-287;</span> y Peukert, <cite xml:lang="en">The Weimar Republic</cite>, pág. 121.',
                                 book.notes_index[63].original_text)
                self.assertEqual("../Text/Capitulo01.xhtml#rf64",
                                 book.notes_index[63].href)
                self.assertEqual(63, book.notes_index[63].index)
            elif book.filename == "testFiles/test_06.xhtml":
                self.assertEqual("nt7", book.notes_index[6].id)
                self.assertEqual("7", book.notes_index[6].number)
                self.assertEqual('La frase citada es del general de división Erich Marcks: véase su «Aus dem Operationsentwurf des Generalmajors Marcks für die Aggression gegen die Sowjetunion, 5. August 1940», en Erhard Moritz (ed.), <cite xml:lang="de">Fall Barbarossa: Dokumente zur Vorbereitung der fachistischen Wehrmacht auf die Aggression gegen die Sowjetunion (1940/41)</cite> (Berlín, 1970), Document&nbsp;31, pág. 122. Para otros estudios clave, véase «Operationsstudie des Gruppenleiterse Heer in der Abteilung Landesverteidigung im OKW für die Aggression gegen die Sowjetunion (Loßberg-Studie), 15. September 1940», en ibíd., Document&nbsp;32, págs. 126-134; Stahel, <cite xml:lang="de">Operation Barbarossa</cite>, págs. 55-60; y Klink, «Die Landkriegführung», págs <span class="nosep">285-287.</span>',
                                 book.notes_index[6].original_text)
                self.assertEqual("../Text/Capitulo02.xhtml#rf7",
                                 book.notes_index[6].href)
                self.assertEqual(6, book.notes_index[6].index)
            else:
                continue

    def test_first_seems_ibid_check(self):
        for book in self.compendium:
            if book.filename == "testFiles/test_01.xhtml":
                self.assertFalse(book.first_seems_ibid)
            elif book.filename == "testFiles/test_02.xhtml":
                self.assertFalse(book.first_seems_ibid)
            elif book.filename == "testFiles/test_03.xhtml":
                self.assertFalse(book.first_seems_ibid)
            elif book.filename == "testFiles/test_04.xhtml":
                self.assertFalse(book.first_seems_ibid)
            elif book.filename == "testFiles/test_05.xhtml":
                self.assertTrue(book.first_seems_ibid)
            elif book.filename == "testFiles/test_06.xhtml":
                self.assertFalse(book.first_seems_ibid)
            else:
                continue

    def test_parents_of_first_note_are_None(self):
        for book in self.compendium:
            self.assertEqual(None, book.notes_index[0].parent)

    def test_check_parents_of_ibid_notes_are_not_None(self):
        for book in self.compendium:
            # la primera puede ser ibid, test anterior
            for i in range(1, len(book.notes_index)):
                note = book.notes_index[i]
                if note.is_ibid:
                    self.assertNotEqual(note.parent, None)

    def test_update_next_and_prev_base_notes(self):
        for book in self.compendium:
            note = book.notes_index[0]
            count = 0
            while True:
                count += 1
                note = note.next_note
                if note == None:
                    break

            if book.filename == "testFiles/test_01.xhtml":
                self.assertEqual(2, count)
            elif book.filename == "testFiles/test_02.xhtml":
                self.assertEqual(3, count)
            elif book.filename == "testFiles/test_03.xhtml":
                self.assertEqual(49, count)
            elif book.filename == "testFiles/test_04.xhtml":
                self.assertEqual(43, count)
            elif book.filename == "testFiles/test_05.xhtml":
                self.assertEqual(106, count)
            elif book.filename == "testFiles/test_06.xhtml":
                self.assertEqual(119, count)
            else:
                continue

    def test_autocheck_ibid_notes_method(self):
        for book in self.compendium:
            ibid_count = 1 if book.first_seems_ibid else 0
            for note in book.notes_index:
                if note.is_ibid == True:
                    ibid_count += 1

            if book.filename == "testFiles/test_01.xhtml":
                self.assertEqual(1, ibid_count)
            elif book.filename == "testFiles/test_02.xhtml":
                self.assertEqual(5, ibid_count)
            elif book.filename == "testFiles/test_03.xhtml":
                self.assertEqual(29, ibid_count)
            elif book.filename == "testFiles/test_04.xhtml":
                self.assertEqual(60, ibid_count)
            elif book.filename == "testFiles/test_05.xhtml":
                self.assertEqual(21, ibid_count)
            elif book.filename == "testFiles/test_06.xhtml":
                self.assertEqual(11, ibid_count)
            else:
                continue

    def test_set_notes_labels(self):
        for book in self.compendium:
            book.updateNotesLabels()
            for note in book.notes_index:
                self.assertNotEqual("", note.current_label, "\nError en libro: " +
                                    book.filename + "\nNota: " + str(note.id))

    def test_count_total_ibid(self):
        for book in self.compendium:
            book.updateNotesLabels()
            if book.filename == "testFiles/test_01.xhtml":
                expected = 1
            elif book.filename == "testFiles/test_02.xhtml":
                expected = 5
            elif book.filename == "testFiles/test_03.xhtml":
                expected = 29
            elif book.filename == "testFiles/test_04.xhtml":
                expected = 60
            elif book.filename == "testFiles/test_05.xhtml":
                # 21 pero primera nota es ibid
                expected = 20
            elif book.filename == "testFiles/test_06.xhtml":
                expected = 11
            else:
                continue

            self.assertEqual(expected, book.ibid_note_count)


class TestNoteOperations(unittest.TestCase):
    def setUp(self):
        self.compendium = []
        for filename in sorted(os.listdir("testFiles/")):
            file = open(("testFiles/" + filename), "r")
            html = file.read()
            file.close()
            book = Book("testFiles/" + filename)
            book.readHTML(html)
            
            book.parseNotes()
            book.autocheckIbidNotes()
            book.updateParentsAndChilds()
            book.updateNextAndPrevNotes()
            book.updateNotesLabels()
            self.compendium.append(book)

    def test_case_process_ibidem(self):
        for book in self.compendium:
            if book.filename == "testFiles/test_01.xhtml":
                expected = 'Ibíd: Nota 1. <cite>Esta es una cita</cite> SEPARADOR 1.1'
                index = 1
            elif book.filename == "testFiles/test_02.xhtml":
                expected = 'Ibíd: Nulla facilisi. Nulla libero. Vivamus pharetra <em>posuere</em> sapien. <del>Nam consectetuer</del>. Sed aliquam, nunc eget euismod ullamcorper, lectus nunc ullamcorper orci, fermentum bibendum enim nibh eget ipsum. SEPARADOR y más malformmaciones pág 50-150. Lorem Ipsum. Texto para confundir escribidme, escribídme 2021-2012. caçitulo 234.'
                index = 5
                # print(expected)
            elif book.filename == "testFiles/test_03.xhtml":
                expected = 'Ibíd: Sobre el establecimiento de los primeros Regulares, véase Carlos Martínez de Campos, <i>España bélica. El siglo <small>XX</small>. Marruecos</i>, pp. 105-106. SEPARADOR p. 156.'
                index = 23
            elif book.filename == "testFiles/test_04.xhtml":
                expected = 'Ibíd: AGA, Sección África, Fondo Marruecos, Caja 81/1100.'
                index = 11
            elif book.filename == "testFiles/test_05.xhtml":
                expected = 'Ibíd: Moeller, <cite xml:lang="en">German Peasants and Agrarian Policy, <span class="nosep">1914-1924,</span></cite> pág. 4. El resto del análisis se basa en esta fuente, salvo que se indique lo contrario. SEPARADOR pág. 123.'
                index = 120
            elif book.filename == "testFiles/test_06.xhtml":
                expected = 'Ibíd: Hartmann, <cite xml:lang="de">Wehrmacht im Ostkrieg</cite>, pág. 39. SEPARADOR pág. 55.'
                index = 33
            else:
                continue

            regex = REGEX_SPLIT
            out = book.notes_index[index].processIbid(regex, "Ibíd:", "SEPARADOR")
            self.assertEqual(
                expected, out, "\nError nota: " + book.notes_index[index].id + " en archivo " + book.filename)

    def test_case_process_ibidem2(self):
            for book in self.compendium:
                if book.filename == "testFiles/test_04.xhtml":
                    expected = 'Ibíd: AGA, Sección África, Fondo Marruecos, Caja 81/1150.'
                    index = 2
                    regex = REGEX_SPLIT
                    out = book.notes_index[index].processIbid(regex, "Ibíd:", "SEPARADOR")
                    self.assertEqual(
                        expected, out, "\nError nota: " + book.notes_index[index].id + " en archivo " + book.filename)

    def test_case_pepito(self):
            nota_base = Note("nt171",
                             "18",
                             'S. Rushdie, «“Commonwealth Literature” Does not Exist», en S.&nbsp;Rushdie, <cite>Imaginary Homelands: Essays and Criticism <span class="nosep">1981-1991</span></cite>, Londres, 1992, p. 65.',
                             "../Text/Capitulo_08.xhtml#rf171",
                             35)

            nota_ibid = Note("nt172", "19", "<i>Ibid.</i>, p. 64.", 
                             "../Text/Capitulo_08.xhtml#rf172" ,36)

            nota_ibid.is_ibid = True
            nota_ibid.parent = nota_base
            nota_base.childs.append(nota_ibid)

            libro = Book("test_pepito")
            libro.notes_index.append(nota_base)
            libro.notes_index.append(nota_ibid)
            libro.ibid_note_count = 1
            libro.base_note_count = 1

            regex = REGEX_SPLIT
            ibid_tag = ""
            separator = ""
            
            expected = 'S. Rushdie, «“Commonwealth Literature” Does not Exist», en S.&nbsp;Rushdie, <cite>Imaginary Homelands: Essays and Criticism <span class="nosep">1981-1991</span></cite>, Londres, 1992, p. 65. p. 64.'
            output = nota_ibid.processIbid(regex, ibid_tag, separator)

            self.assertEqual(expected, output)
  
    def test_ibid_to_note(self):
        for book in self.compendium:
            if book.filename == "testFiles/test_01.xhtml":
                note = book.notes_index[1]
                prev_note = book.notes_index[0]
                next_note = book.notes_index[2]
                childs = 0
            elif book.filename == "testFiles/test_02.xhtml":
                note = book.notes_index[3]
                prev_note = book.notes_index[1]
                next_note = book.notes_index[6]
                childs = 2
            elif book.filename == "testFiles/test_03.xhtml":
                note = book.notes_index[23]
                prev_note = book.notes_index[20]
                next_note = book.notes_index[24]
                childs = 0
            elif book.filename == "testFiles/test_04.xhtml":
                note = book.notes_index[11]
                prev_note = book.notes_index[10]
                next_note = book.notes_index[12]
                childs = 0
            elif book.filename == "testFiles/test_05.xhtml":
                note = book.notes_index[120]
                prev_note = book.notes_index[119]
                next_note = book.notes_index[122]
                childs = 1
            elif book.filename == "testFiles/test_06.xhtml":
                note = book.notes_index[32]
                prev_note = book.notes_index[31]
                next_note = book.notes_index[34]
                childs = 1
            else:
                continue

            book.ibidToNote(note)
            msg = "Error en nota " + note.id + " del libro " + book.filename

            self.assertIsNone(note.parent, msg)
            self.assertEqual(note.prev_note, prev_note, msg)
            self.assertEqual(note.next_note, next_note, msg)
            self.assertEqual(len(note.childs), childs, msg)

    def test_note_to_ibid(self):
        for book in self.compendium:
            if book.filename == "testFiles/test_01.xhtml":
                note = book.notes_index[2]
                prev_note = book.notes_index[1]
                next_note = None
            elif book.filename == "testFiles/test_02.xhtml":
                note = book.notes_index[1]
                prev_note = None
                next_note = book.notes_index[2]
            elif book.filename == "testFiles/test_03.xhtml":
                note = book.notes_index[24]
                prev_note = book.notes_index[23]
                next_note = book.notes_index[25]
            elif book.filename == "testFiles/test_04.xhtml":
                note = book.notes_index[27]
                prev_note = book.notes_index[25]
                next_note = book.notes_index[29]
            elif book.filename == "testFiles/test_05.xhtml":
                note = book.notes_index[122]
                prev_note = book.notes_index[121]
                next_note = None
            elif book.filename == "testFiles/test_06.xhtml":
                note = book.notes_index[35]
                prev_note = book.notes_index[33]
                next_note = book.notes_index[70]
            else:
                continue

            book.noteToIbid(note)
            msg = "Error en nota " + note.id + " del libro " + book.filename

            self.assertIsNotNone(note.parent, msg)
            self.assertEqual(note.prev_note, prev_note, msg)
            self.assertEqual(note.next_note, next_note, msg)
            self.assertEqual(len(note.childs), 0, msg)

    def test_get_next_ibid(self):
        for book in self.compendium:
            if book.filename == "testFiles/test_01.xhtml":
                current_note = book.notes_index[0]
                current_ibid = book.notes_index[1]
                expected = None
            elif book.filename == "testFiles/test_02.xhtml":
                current_note = book.notes_index[0]
                current_ibid = None
                expected = book.notes_index[2]
            elif book.filename == "testFiles/test_03.xhtml":
                current_note = book.notes_index[67]
                current_ibid = book.notes_index[70]
                expected = None
            elif book.filename == "testFiles/test_04.xhtml":
                current_note = book.notes_index[62]
                current_ibid = None
                expected = book.notes_index[65]
            elif book.filename == "testFiles/test_05.xhtml":
                current_note = book.notes_index[59]
                current_ibid = book.notes_index[60]
                expected = book.notes_index[78]
            elif book.filename == "testFiles/test_06.xhtml":
                current_note = book.notes_index[111]
                current_ibid = book.notes_index[112]
                expected = None
            else:
                continue

            test_outcome = book.getNextIbid(current_note, current_ibid)
            msg = "\nBook: " + book.filename + "\nNote: " + current_note.id
            self.assertEqual(test_outcome, expected, msg)

    def test_note_to_xhtml(self):
        for book in self.compendium:
            if book.filename == "testFiles/test_01.xhtml":
                note = book.notes_index[1]
                out = '  <div class="nota">\n    <p id="nt2"><sup>[2]</sup> Ibid 1.1 <a href="Section0001.xhtml#rf2">&lt;&lt;</a></p>\n  </div>\n\n'
            elif book.filename == "testFiles/test_02.xhtml":
                note = book.notes_index[1]
                out = '  <div class="nota">\n    <p id="nt2"><sup>[2]</sup> Nulla facilisi. Nulla libero. Vivamus pharetra <em>posuere</em> sapien. <del>Nam consectetuer</del>. Sed aliquam, nunc eget euismod ullamcorper, lectus nunc ullamcorper orci, fermentum bibendum enim nibh eget ipsum. <a href="../Text/Section0001.xhtml#rf2">&lt;&lt;</a></p>\n  </div>\n\n'
            elif book.filename == "testFiles/test_03.xhtml":
                note = book.notes_index[51]
                out = '  <div class="nota">\n    <p id="nt52"><sup>[52]</sup> <i>Ibid</i>., p. 651. <a href="1.xhtml#rf52">&lt;&lt;</a></p>\n  </div>\n\n'
            elif book.filename == "testFiles/test_04.xhtml":
                note = book.notes_index[102]
                out = '  <div class="nota">\n    <p id="nt103"><sup>[103]</sup> Ibíd. <a href="5.xhtml#rf101">&lt;&lt;</a></p>\n  </div>\n\n'
            elif book.filename == "testFiles/test_05.xhtml":
                note = book.notes_index[4]
                out = '  <div class="nota">\n    <p id="nt5"><sup>[5]</sup> Gerlach y Werth, «State Violence – Violent Societies», pág. 173. <a href="../Text/Capitulo01.xhtml#rf5">&lt;&lt;</a></p>\n  </div>\n\n'
            elif book.filename == "testFiles/test_06.xhtml":
                note = book.notes_index[67]
                out = '  <div class="nota">\n    <p id="nt68"><sup>[68]</sup> Kay, <cite xml:lang="en">Exploitation, Resettlement, Mass Murder</cite>, pág. 61. <a href="../Text/Capitulo02.xhtml#rf68">&lt;&lt;</a></p>\n  </div>\n\n'
            else:
                continue

            self.assertEqual(note.toXHTML(), out)

    def test_book_to_xhtml(self):
        regex = REGEX_SPLIT
        for book in self.compendium:
            if book.filename == "testFiles/test_01.xhtml":
                book.notes_index[1].processIbid(regex, "Ibíd:", "SEPARADOR:")
                expected_xhtml = """<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n\n<html xml:lang="es" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n  <title>Notas</title>\n  <link href="../Styles/epl.css" rel="stylesheet" type="text/css"/>\n  <link href="../Styles/style.css" rel="stylesheet" type="text/css"/>\n</head>\n\n<!-- este documento es opcional, debe eliminarse de ser innecesario--><!-- para vincular cada nota («nt1», «nt2»… «ntX»), debe adaptarse la numeración consecutiva de las referencias («rf1», «rf2»… «rfX»), así como el nombre del archivo en el que se encuentran (Section0001.xhtml, Section0002.xhtml, etc.)--><!-- en caso de libros con gran cantidad de notas, se recomienda dividirlas en varios archivos (título sólo en el primero)-->\n<body>\n  <h1>Notas</h1>\n\n  <div class="nota">\n    <p id="nt1"><sup>[1]</sup> Nota 1. <cite>Esta es una cita</cite> <a href="Section0001.xhtml#rf1">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt2"><sup>[2]</sup> Ibíd: Nota 1. <cite>Esta es una cita</cite> SEPARADOR: 1.1 <a href="Section0001.xhtml#rf2">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt3"><sup>[3]</sup> Nota 2 <a href="Section0001.xhtml#rf3">&lt;&lt;</a></p>\n  </div>\n</body>\n</html>"""
                xhtml = book.bookToXHTML()
                self.assertEqual(xhtml, expected_xhtml)

    def test_book_with_extra_data_to_xhtml(self):
        expected_string = """<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es">\n<head>\n  <title>Notas</title>\n  <link href="../Styles/epl.css" rel="stylesheet" type="text/css"/>\n  <link href="../Styles/style.css" rel="stylesheet" type="text/css"/>\n</head>\n\n<body>\n  <h1>Notas</h1>\n\n  <p class="item">I. «Colonización» y «Colonias»</p>\n\n  <div class="nota">\n    <p id="nt1"><sup>[1]</sup> Para un repaso de los principales debates al respecto, véase D.&nbsp;Rothermund, «The Self-Consciousness of Post-Imperial Nations: A Cross-national Comparison», en <cite>India Quarterly</cite> 67 (2011), pp. 1-18. <a href="../Text/Capitulo_01.xhtml#rf1">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt2"><sup>[2]</sup> Véase O. Brunner, W. Conze y R.&nbsp;Koselleck (eds.), <cite>Geschichtliche Grundbegriffe. Historisches Lexikon zur politisch-sozialen Sprache in Deutschland</cite>, 7 vols., Stuttgart, <span class="nosep">1972-1992,</span> y en particular el artículo sobre «Imperialismo» de J. Fisch <i>et al.</i> (Vol. 3, 1982, pp. 171-236). <a href="../Text/Capitulo_01.xhtml#rf2">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt3"><sup>[3]</sup> M. I. Finley, <cite>Colonies: An Attempt at a Typology</cite>, en <cite>Transactions of the Royal Historical Society</cite>, 5.ª serie, 26 (1976), pp.&nbsp;167-188. <a href="../Text/Capitulo_01.xhtml#rf3">&lt;&lt;</a></p>\n  </div>\n\n  <p class="item">II. «Colonialismo» e «Imperios coloniales»</p>\n\n  <p>Caso más complicado</p>\n\n  <div class="nota">\n    <p id="nt16"><sup>[1]</sup> Ph. D. Curtin, «The Black Experience of Colonialism and Imperialism», en S.&nbsp;<span class="nosep">W. Mintz</span> (ed.), <cite>Slavery, Colonialism, and Racism</cite>, Nueva York, 1974, p. 23. <a href="../Text/Capitulo_02.xhtml#rf16">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt17"><sup>[2]</sup> Véase M. Winter, <cite>Egyptian Society under Ottoman Rule <span class="nosep">1517-1798</span></cite>, Londres, 1992, p.&nbsp;30. <a href="../Text/Capitulo_02.xhtml#rf17">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt18"><sup>[3]</sup> E. W. Said, <cite>Kultur und Imperialismus. Einbildungskraft und Politik im Zeitalter der Macht</cite>, Fráncfort, 1994, p.&nbsp;44 [ed. cast.: <cite>Cultura e imperialismo</cite>, Barcelona, Debate, 2018]. <a href="../Text/Capitulo_02.xhtml#rf18">&lt;&lt;</a></p>\n  </div>\n\n  <p class="item">III. Épocas del colonialismo</p>\n\n  <div class="nota">\n    <p id="nt25"><sup>[1]</sup> Véase, en general, W. Reinhard, <cite>Geschichte der europäischen Expansion</cite>, 4 vols., Stuttgart, <span class="nosep">1983-1990,</span> así como Kleine Geschichte des Kolonialismus, Stuttgart, 2008. <a href="../Text/Capitulo_03.xhtml#rf25">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt26"><sup>[2]</sup> A. Girault, <cite>Principes de colonisation et de législation coloniale</cite>, vol. 1, París, 1921, p.&nbsp;17. <a href="../Text/Capitulo_03.xhtml#rf26">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt27"><sup>[3]</sup> Véase por ejemplo los títulos de Osterhammel y Petersson, y Wendt en la «Bibliografía», así como G.&nbsp;<span class="nosep">B. Magee</span> y A. S. Thompson, <cite>Empire and Globalisation: Networks of People, Goods and Capital in the British World, c. <span class="nosep">1850-1914</span></cite>, Cambridge, 2010. <a href="../Text/Capitulo_03.xhtml#rf27">&lt;&lt;</a></p>\n  </div>\n\n  <p class="item">IV. Conquista, resistencia y colaboración</p>\n\n  <div class="nota">\n    <p id="nt60"><sup>[1]</sup> D. W. Meinig, The Shaping of America: A Geographical Perspective on 500&nbsp;Years of History, vol. 1, New Haven, 1986, p. 65. <a href="../Text/Capitulo_04.xhtml#rf60">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt61"><sup>[2]</sup> Véase J. H. Elliott, «The Seizure of Overseas Territories by the European Powers», en H.&nbsp;Pohl (ed.), <cite>The European Discovery of the World and its Economic Effects on Pre-Industrial Society, <span class="nosep">1500-1800</span></cite>, Stuttgart, 1990, pp. 51-54. <a href="../Text/Capitulo_04.xhtml#rf61">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt62"><sup>[3]</sup> J. Iliffe, <cite>A Modern History of Tanganyika</cite>, Cambridge, 1979, p.&nbsp;117. <a href="../Text/Capitulo_04.xhtml#rf62">&lt;&lt;</a></p>\n  </div>\n\n  <p class="item">V. El estado colonial</p>\n\n  <div class="nota">\n    <p id="nt83"><sup>[1]</sup> Véase M. H. Fisher, <cite>Indirect Rule in India: Residents and the Residency System <span class="nosep">1764-1858</span></cite>, Delhi, 1991. <a href="../Text/Capitulo_05.xhtml#rf83">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt84"><sup>[2]</sup> Véase J. M. Gullick, <cite>Rulers and Residents: Influence and Power in the Malay States <span class="nosep">1870-1920</span></cite>, Singapur, 1992. <a href="../Text/Capitulo_05.xhtml#rf84">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt85"><sup>[3]</sup> <cite>Report of the Indian Statutory Commission</cite>, <i>op. cit.</i>, p.&nbsp;112. <a href="../Text/Capitulo_05.xhtml#rf85">&lt;&lt;</a></p>\n  </div>\n\n  <p class="item">VI. Formas económicas coloniales</p>\n\n  <div class="nota">\n    <p id="nt107"><sup>[1]</sup> Véase A. G. Hopkins, <cite>An Economic History of West Africa</cite>, Londres, 1973, p.&nbsp;126. <a href="../Text/Capitulo_06.xhtml#rf107">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt108"><sup>[2]</sup> Véase el repaso general de C. Coquery-Vidrovitch, «Les conditions de la dépendance: Histoire du sous-développement», en C. Coquery-Vidrovitch y A.&nbsp;Forest (eds.), <cite>Décolonisations et nouvelles dépendances</cite>, Lille, 1986, pp. 25-48. <a href="../Text/Capitulo_06.xhtml#rf108">&lt;&lt;</a></p>\n  </div>\n\n  <p class="item">VII. Sociedades coloniales"</p>\n\n  <div class="nota">\n    <p id="nt125"><sup>[1]</sup> Véase, por ejemplo, A.&nbsp;<span class="nosep">L. Stoler,</span> «Rethinking Colonial Categories: European Communities and the Boundaries of Rule», en <cite>Comparative Studies in Society and History</cite> 31 (1989), pp. 134-161, y un estudio sobre una familia escocesa activa a escala global: E. Rothschild, <cite>The Inner Life of Empires: An Eighteenthcentury History</cite>, Princeton, 2011. <a href="../Text/Capitulo_07.xhtml#rf125">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt126"><sup>[2]</sup> J. S. Furnivall, <cite>Netherlands India: A Study of a Plural Economy</cite>, Cambridge, 1944, p.&nbsp;446, y también Colonial Policy and Practice, op. cit., pp. 303-312. <a href="../Text/Capitulo_07.xhtml#rf126">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt127"><sup>[3]</sup> J. S. Furnivall, <cite>Netherlands India: A Study of a Plural Economy</cite>, Cambridge, 1944, p.&nbsp;446, y también Colonial Policy and Practice, op. cit., pp. 303-312. pp.&nbsp;135-139. <a href="../Text/Capitulo_07.xhtml#rf127">&lt;&lt;</a></p>\n  </div>\n\n  <p class="item">VIII. Colonialismo y cultura indígena</p>\n\n  <div class="nota">\n    <p id="nt154"><sup>[1]</sup> V. S. Naipaul, <cite>The Overcrowded Barracoon and Other Articles</cite>, Londres, 1972, p.&nbsp;37. <a href="../Text/Capitulo_08.xhtml#rf154">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt155"><sup>[2]</sup> N. Wachtel, <cite>The Vision of the Vanquished: The Spanish Conquest of Peru through Indian Eyes, <span class="nosep">1530-1570</span></cite>, Hassocs, Sussex, 1977, p.&nbsp;85. <a href="../Text/Capitulo_08.xhtml#rf155">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt156"><sup>[3]</sup> Véase D. Lombard, <cite>Le carrefour javanais: Essai <span class="nosep">d’histoire</span> globale</cite>, vol. 1, París, 1990, pp.&nbsp;79-81. <a href="../Text/Capitulo_08.xhtml#rf156">&lt;&lt;</a></p>\n  </div>\n\n  <p class="item">IX. Pensamiento colonialista y cultura colonial</p>\n\n  <div class="nota">\n    <p id="nt173"><sup>[1]</sup> Véase, por ejemplo, A.&nbsp;<span class="nosep">L. Conklin,</span> <cite>A Mission to Civilize: The Republican Idea of Empire in France and West Africa, <span class="nosep">1895-1930</span></cite>, Stanford, 1997. <a href="../Text/Capitulo_09.xhtml#rf173">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt174"><sup>[2]</sup> Véase A. Memmi, <cite>Portrait du colonisé</cite>, nueva edición París, 1973, p.&nbsp;49. <a href="../Text/Capitulo_09.xhtml#rf174">&lt;&lt;</a></p>\n  </div>\n</body>\n</html>"""
        # expected = sha512(expected_string.encode("utf-8"))
        for book in self.compendium:
            if book.filename == "testFiles/notas.xhtml":
                book.getExtraTextFromHtml()
                book.notes_index[19].processIbid(REGEX_SPLIT, "", "")
                result_string = book.bookToXHTML()
                # result = sha512(result_string.encode("utf-8"))
                
                self.assertEqual(expected_string, result_string)
                # self.assertEqual(expected, result)



class TestQT5(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
