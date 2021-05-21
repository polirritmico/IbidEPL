#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
from book import Book
from note import Note


class TestInputs(unittest.TestCase):
    def setUp(self):
        self.compendium = []
        for file in sorted(os.listdir("testFiles/")):
            book = Book()
            book.readFile("testFiles/" + file)
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
            if book.file.name == "testFiles/test_01.xhtml":
                self.assertEqual(9, len(list(filter(None, book.html_body))))
            elif book.file.name == "testFiles/test_02.xhtml":
                self.assertEqual(24, len(list(filter(None, book.html_body))))
            elif book.file.name == "testFiles/test_03.xhtml":
                self.assertEqual(234, len(list(filter(None, book.html_body))))
            elif book.file.name == "testFiles/test_04.xhtml":
                self.assertEqual(309, len(list(filter(None, book.html_body))))
            elif book.file.name == "testFiles/test_05.xhtml":
                self.assertEqual(378, len(list(filter(None, book.html_body))))
            elif book.file.name == "testFiles/test_06.xhtml":
                self.assertEqual(390, len(list(filter(None, book.html_body))))
            else:
                self.assertTrue(False, "No open file: " + book.file.name)


class TestProcess(unittest.TestCase):
    def setUp(self):
        self.compendium = []
        for file in sorted(os.listdir("testFiles/")):
            book = Book()
            book.readFile("testFiles/" + file)
            book.parseNotes()
            book.setParentsAndChilds()
            book.updateNextAndPrevNotes()

            self.compendium.append(book)

    def test_notes_processed_count(self):
        for book in self.compendium:
            if book.file.name == "testFiles/test_01.xhtml":
                self.assertEqual(3, len(book.notes_index))
            elif book.file.name == "testFiles/test_02.xhtml":
                self.assertEqual(8, len(book.notes_index))
            elif book.file.name == "testFiles/test_03.xhtml":
                self.assertEqual(78, len(book.notes_index))
            elif book.file.name == "testFiles/test_04.xhtml":
                self.assertEqual(103, len(book.notes_index))
            elif book.file.name == "testFiles/test_05.xhtml":
                self.assertEqual(126, len(book.notes_index))
            elif book.file.name == "testFiles/test_06.xhtml":
                self.assertEqual(130, len(book.notes_index))
            else:
                self.assertTrue(False, "No open file: " + book.file.name)

    def test_case_notes_parse_data(self):
        for book in self.compendium:
            if book.file.name == "testFiles/test_01.xhtml":
                self.assertEqual("1", book.notes_index[0].number)
                self.assertEqual("Nota 1. <cite>Esta es una cita</cite>",
                                 book.notes_index[0].original_text)
                self.assertEqual("Section0001.xhtml#rf1",
                                 book.notes_index[0].href)
                self.assertEqual(0, book.notes_index[0].index)
            elif book.file.name == "testFiles/test_02.xhtml":
                self.assertEqual("nt6", book.notes_index[5].id_tag)
                self.assertEqual("6", book.notes_index[5].number)
                self.assertEqual("iBid.,. y más malformmaciones pág 50-150. Lorem Ipsum. Texto para confundir escribidme, escribídme 2021-2012. caçitulo 234.",
                                 book.notes_index[5].original_text)
                self.assertEqual("../Text/Section0001.xhtml#rf6",
                                 book.notes_index[5].href)
                self.assertEqual(5, book.notes_index[5].index)
            elif book.file.name == "testFiles/test_03.xhtml":
                self.assertEqual("nt55", book.notes_index[54].id_tag)
                self.assertEqual("55", book.notes_index[54].number)
                self.assertEqual("Dolores Ibárruri y otros, <i>Guerra y revolución en España 1936-1939</i>, pp. 33-34.",
                                 book.notes_index[54].original_text)
                self.assertEqual("1.xhtml#rf55",
                                 book.notes_index[54].href)
                self.assertEqual(54, book.notes_index[54].index)
            elif book.file.name == "testFiles/test_04.xhtml":
                self.assertEqual("nt12", book.notes_index[11].id_tag)
                self.assertEqual("12", book.notes_index[11].number)
                self.assertEqual("Ibid.", book.notes_index[11].original_text)
                self.assertEqual("5.xhtml#rf12",
                                 book.notes_index[11].href)
                self.assertEqual(11, book.notes_index[11].index)
            elif book.file.name == "testFiles/test_05.xhtml":
                self.assertEqual("nt64", book.notes_index[63].id_tag)
                self.assertEqual("64", book.notes_index[63].number)
                self.assertEqual('Kossert, <cite xml:lang="de">Ostpreussen: Geschichte und Mythos</cite>, pág. 212. Con la idea de mantener la producción agrícola frente a la competitividad de los países recién fundados de la Europa oriental, los gobiernos prusianos y del Reich instauraron programas conocidos como Osthilfe (Programa de Ayuda al Este) y el Ostpreußen-Hilfe (Programa de Ayuda a Prusia Oriental) durante los años veinte. Por lo que tocaba a la estimulación de la economía, aquellos programas resultaron en general y relativamente poco efectivos. Sin embargo, sirvieron para fortalecer la posición de la aristocracia terrateniente. Véase Hans Mommsen, <cite xml:lang="en">The Rise and Fall of Weimar Democracy</cite> (Chapel Hill, 1996); págs. <span class="nosep">229, 286-287;</span> y Peukert, <cite xml:lang="en">The Weimar Republic</cite>, pág. 121.',
                                 book.notes_index[63].original_text)
                self.assertEqual("../Text/Capitulo01.xhtml#rf64",
                                 book.notes_index[63].href)
                self.assertEqual(63, book.notes_index[63].index)
            elif book.file.name == "testFiles/test_06.xhtml":
                self.assertEqual("nt7", book.notes_index[6].id_tag)
                self.assertEqual("7", book.notes_index[6].number)
                self.assertEqual('La frase citada es del general de división Erich Marcks: véase su «Aus dem Operationsentwurf des Generalmajors Marcks für die Aggression gegen die Sowjetunion, 5. August 1940», en Erhard Moritz (ed.), <cite xml:lang="de">Fall Barbarossa: Dokumente zur Vorbereitung der fachistischen Wehrmacht auf die Aggression gegen die Sowjetunion (1940/41)</cite> (Berlín, 1970), Document&nbsp;31, pág. 122. Para otros estudios clave, véase «Operationsstudie des Gruppenleiterse Heer in der Abteilung Landesverteidigung im OKW für die Aggression gegen die Sowjetunion (Loßberg-Studie), 15. September 1940», en ibíd., Document&nbsp;32, págs. 126-134; Stahel, <cite xml:lang="de">Operation Barbarossa</cite>, págs. 55-60; y Klink, «Die Landkriegführung», págs <span class="nosep">285-287.</span>',
                                 book.notes_index[6].original_text)
                self.assertEqual("../Text/Capitulo02.xhtml#rf7",
                                 book.notes_index[6].href)
                self.assertEqual(6, book.notes_index[6].index)
            else:
                self.assertTrue(False, "No open file: " + book.file.name)

    def test_first_seems_ibid_check(self):
        for book in self.compendium:
            if book.file.name == "testFiles/test_01.xhtml":
                self.assertFalse(book.first_seems_ibid)
            elif book.file.name == "testFiles/test_02.xhtml":
                self.assertFalse(book.first_seems_ibid)
            elif book.file.name == "testFiles/test_03.xhtml":
                self.assertFalse(book.first_seems_ibid)
            elif book.file.name == "testFiles/test_04.xhtml":
                self.assertFalse(book.first_seems_ibid)
            elif book.file.name == "testFiles/test_05.xhtml":
                self.assertTrue(book.first_seems_ibid)
            elif book.file.name == "testFiles/test_06.xhtml":
                self.assertFalse(book.first_seems_ibid)
            else:
                self.assertTrue(False, "No open file: " + book.file.name)

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

            if book.file.name == "testFiles/test_01.xhtml":
                self.assertEqual(2, count)
            elif book.file.name == "testFiles/test_02.xhtml":
                self.assertEqual(3, count)
            elif book.file.name == "testFiles/test_03.xhtml":
                self.assertEqual(49, count)
            elif book.file.name == "testFiles/test_04.xhtml":
                self.assertEqual(43, count)
            elif book.file.name == "testFiles/test_05.xhtml":
                self.assertEqual(106, count)
            elif book.file.name == "testFiles/test_06.xhtml":
                self.assertEqual(119, count)
            else:
                self.assertTrue(False, "No open file: " + book.file.name)

    def test_autocheck_ibid_notes_method(self):
        for book in self.compendium:
            ibid_count = 1 if book.first_seems_ibid else 0
            for note in book.notes_index:
                if note.is_ibid == True:
                    ibid_count += 1

            if book.file.name == "testFiles/test_01.xhtml":
                self.assertEqual(1, ibid_count)
            elif book.file.name == "testFiles/test_02.xhtml":
                self.assertEqual(5, ibid_count)
            elif book.file.name == "testFiles/test_03.xhtml":
                self.assertEqual(29, ibid_count)
            elif book.file.name == "testFiles/test_04.xhtml":
                self.assertEqual(60, ibid_count)
            elif book.file.name == "testFiles/test_05.xhtml":
                self.assertEqual(21, ibid_count)
            elif book.file.name == "testFiles/test_06.xhtml":
                self.assertEqual(11, ibid_count)
            else:
                self.assertTrue(False, "No open file: " + book.file.name)

    def test_set_notes_labels(self):
        for book in self.compendium:
            book.updateNotesLabels()
            for note in book.notes_index:
                self.assertNotEqual("", note.current_label, "\nError en libro: " +
                                    book.file.name + "\nNota: " + str(note.id_tag))


class TestNoteOperations(unittest.TestCase):
    def setUp(self):
        self.compendium = []
        for file in sorted(os.listdir("testFiles/")):
            book = Book()
            book.readFile("testFiles/" + file)
            book.parseNotes()
            book.autocheckIbidNotes()
            book.setParentsAndChilds()
            book.updateNextAndPrevNotes()
            self.compendium.append(book)

    def test_case_process_ibidem(self):
        for book in self.compendium:
            if book.file.name == "testFiles/test_01.xhtml":
                expected = 'Ibíd: Nota 1. <cite>Esta es una cita</cite> SEPARADOR 1.1'
                index = 1
            elif book.file.name == "testFiles/test_02.xhtml":
                expected = 'Ibíd: Nulla facilisi. Nulla libero. Vivamus pharetra <em>posuere</em> sapien. <del>Nam consectetuer</del>. Sed aliquam, nunc eget euismod ullamcorper, lectus nunc ullamcorper orci, fermentum bibendum enim nibh eget ipsum. SEPARADOR y más malformmaciones pág 50-150. Lorem Ipsum. Texto para confundir escrme, escrme 2021-2012. caçitulo 234.'
                index = 5
                # print(expected)
            elif book.file.name == "testFiles/test_03.xhtml":
                expected = 'Ibíd: Sobre el establecimiento de los primeros Regulares, véase Carlos Martínez de Campos, <i>España bélica. El siglo <small>XX</small>. Marruecos</i>, pp. 105-106. SEPARADOR p. 156.'
                index = 23
            elif book.file.name == "testFiles/test_04.xhtml":
                expected = 'Ibíd: AGA, Sección África, Fondo Marruecos, Caja 81/1100.'
                index = 11
            elif book.file.name == "testFiles/test_05.xhtml":
                expected = 'Ibíd: Moeller, <cite xml:lang="en">German Peasants and Agrarian Policy, <span class="nosep">1914-1924,</span></cite> pág. 4. El resto del análisis se basa en esta fuente, salvo que se indique lo contrario. SEPARADOR pág. 123.'
                index = 120
            elif book.file.name == "testFiles/test_06.xhtml":
                expected = 'Ibíd: Hartmann, <cite xml:lang="de">Wehrmacht im Ostkrieg</cite>, pág. 39. SEPARADOR pág. 55.'
                index = 33
            else:
                self.assertTrue(False, "No open file: " + book.file.name)

            out = book.notes_index[index].processIbidem(
                "", "Ibíd:", "SEPARADOR")
            self.assertEqual(
                expected, out, "\nError nota: " + book.notes_index[index].id_tag)

    def test_ibid_to_note(self):
        for book in self.compendium:
            if book.file.name == "testFiles/test_01.xhtml":
                note = book.notes_index[1]
                prev_note = book.notes_index[0]
                next_note = book.notes_index[2]
                childs = 0
            elif book.file.name == "testFiles/test_02.xhtml":
                note = book.notes_index[3]
                prev_note = book.notes_index[1]
                next_note = book.notes_index[6]
                childs = 2
            elif book.file.name == "testFiles/test_03.xhtml":
                note = book.notes_index[23]
                prev_note = book.notes_index[20]
                next_note = book.notes_index[24]
                childs = 0
            elif book.file.name == "testFiles/test_04.xhtml":
                note = book.notes_index[11]
                prev_note = book.notes_index[10]
                next_note = book.notes_index[12]
                childs = 0
            elif book.file.name == "testFiles/test_05.xhtml":
                note = book.notes_index[120]
                prev_note = book.notes_index[119]
                next_note = book.notes_index[122]
                childs = 1
            elif book.file.name == "testFiles/test_06.xhtml":
                note = book.notes_index[32]
                prev_note = book.notes_index[31]
                next_note = book.notes_index[34]
                childs = 1
            else:
                self.assertTrue(False, "No open file: " + book.file.name)

            book.ibidToNote(note)
            msg = "Error en nota " + note.id_tag + " del libro " + book.file.name

            self.assertIsNone(note.parent, msg)
            self.assertEqual(note.prev_note, prev_note, msg)
            self.assertEqual(note.next_note, next_note, msg)
            self.assertEqual(len(note.childs), childs, msg)

    def test_note_to_ibid(self):
        for book in self.compendium:
            if book.file.name == "testFiles/test_01.xhtml":
                note = book.notes_index[2]
                prev_note = book.notes_index[1]
                next_note = None
            elif book.file.name == "testFiles/test_02.xhtml":
                note = book.notes_index[1]
                prev_note = None
                next_note = book.notes_index[2]
            elif book.file.name == "testFiles/test_03.xhtml":
                note = book.notes_index[24]
                prev_note = book.notes_index[23]
                next_note = book.notes_index[25]
            elif book.file.name == "testFiles/test_04.xhtml":
                note = book.notes_index[27]
                prev_note = book.notes_index[25]
                next_note = book.notes_index[29]
            elif book.file.name == "testFiles/test_05.xhtml":
                note = book.notes_index[122]
                prev_note = book.notes_index[121]
                next_note = None
            elif book.file.name == "testFiles/test_06.xhtml":
                note = book.notes_index[35]
                prev_note = book.notes_index[33]
                next_note = book.notes_index[70]
            else:
                self.assertTrue(False, "No open file: " + book.file.name)

            book.noteToIbid(note)
            msg = "Error en nota " + note.id_tag + " del libro " + book.file.name

            self.assertIsNotNone(note.parent, msg)
            self.assertEqual(note.prev_note, prev_note, msg)
            self.assertEqual(note.next_note, next_note, msg)
            self.assertEqual(len(note.childs), 0, msg)

    def test_note_to_xhtml(self):
        for book in self.compendium:
            if book.file.name == "testFiles/test_01.xhtml":
                note = book.notes_index[1]
                out = '  <div class="nota">\n    <p id="nt2"><sup>[2]</sup> Ibid 1.1 <a href="Section0001.xhtml#rf2">&lt;&lt;</a></p>\n  </div>\n\n'
            elif book.file.name == "testFiles/test_02.xhtml":
                note = book.notes_index[1]
                out = '  <div class="nota">\n    <p id="nt2"><sup>[2]</sup> Nulla facilisi. Nulla libero. Vivamus pharetra <em>posuere</em> sapien. <del>Nam consectetuer</del>. Sed aliquam, nunc eget euismod ullamcorper, lectus nunc ullamcorper orci, fermentum bibendum enim nibh eget ipsum. <a href="../Text/Section0001.xhtml#rf2">&lt;&lt;</a></p>\n  </div>\n\n'
            elif book.file.name == "testFiles/test_03.xhtml":
                note = book.notes_index[51]
                out = '  <div class="nota">\n    <p id="nt52"><sup>[52]</sup> <i>Ibid</i>., p. 651. <a href="1.xhtml#rf52">&lt;&lt;</a></p>\n  </div>\n\n'
            elif book.file.name == "testFiles/test_04.xhtml":
                note = book.notes_index[102]
                out = '  <div class="nota">\n    <p id="nt103"><sup>[103]</sup> Ibíd. <a href="5.xhtml#rf101">&lt;&lt;</a></p>\n  </div>\n\n'
            elif book.file.name == "testFiles/test_05.xhtml":
                note = book.notes_index[4]
                out = '  <div class="nota">\n    <p id="nt5"><sup>[5]</sup> Gerlach y Werth, «State Violence – Violent Societies», pág. 173. <a href="../Text/Capitulo01.xhtml#rf5">&lt;&lt;</a></p>\n  </div>\n\n'
            elif book.file.name == "testFiles/test_06.xhtml":
                note = book.notes_index[67]
                out = '  <div class="nota">\n    <p id="nt68"><sup>[68]</sup> Kay, <cite xml:lang="en">Exploitation, Resettlement, Mass Murder</cite>, pág. 61. <a href="../Text/Capitulo02.xhtml#rf68">&lt;&lt;</a></p>\n  </div>\n\n'
            else:
                self.assertTrue(False, "No open file: " + book.file.name)

            self.assertEqual(note.toXHTML(), out)

    def test_book_to_xhtml(self):
        for book in self.compendium:
            if book.file.name == "testFiles/test_01.xhtml":
                book.notes_index[1].processIbidem("", "Ibíd:", "SEPARADOR:")
                expected_xhtml = """<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n\n<html xml:lang="es" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n  <title>Notas</title>\n  <link href="../Styles/epl.css" rel="stylesheet" type="text/css"/>\n  <link href="../Styles/style.css" rel="stylesheet" type="text/css"/>\n</head>\n\n<!-- este documento es opcional, debe eliminarse de ser innecesario--><!-- para vincular cada nota («nt1», «nt2»… «ntX»), debe adaptarse la numeración consecutiva de las referencias («rf1», «rf2»… «rfX»), así como el nombre del archivo en el que se encuentran (Section0001.xhtml, Section0002.xhtml, etc.)--><!-- en caso de libros con gran cantidad de notas, se recomienda dividirlas en varios archivos (título sólo en el primero)-->\n<body>\n  <h1>Notas</h1>\n\n  <div class="nota">\n    <p id="nt1"><sup>[1]</sup> Nota 1. <cite>Esta es una cita</cite> <a href="Section0001.xhtml#rf1">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt2"><sup>[2]</sup> Ibíd: Nota 1. <cite>Esta es una cita</cite> SEPARADOR: 1.1 <a href="Section0001.xhtml#rf2">&lt;&lt;</a></p>\n  </div>\n\n  <div class="nota">\n    <p id="nt3"><sup>[3]</sup> Nota 2 <a href="Section0001.xhtml#rf3">&lt;&lt;</a></p>\n  </div>\n\n</body>\n</html>"""
                xhtml = book.bookToXHTML()
                self.assertEqual(xhtml, expected_xhtml)

    #     # for book in self.compendium:
    #     #     if book.file.name == "testFiles/test_01.xhtml":
    #     #         pass
    #     #     elif book.file.name == "testFiles/test_02.xhtml":
    #     #         pass
    #     #     elif book.file.name == "testFiles/test_03.xhtml":
    #     #         pass
    #     #     elif book.file.name == "testFiles/test_04.xhtml":
    #     #         pass
    #     #     elif book.file.name == "testFiles/test_05.xhtml":
    #     #         pass
    #     #     elif book.file.name == "testFiles/test_06.xhtml":
    #     #         pass
    #     #     else:
    #     #         self.assertTrue(False, "No open file: " + book.file.name)


if __name__ == '__main__':
    unittest.main()
