#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2021 Titivillus
# www.epublibre.org
# Distributed under the terms of the GNU General Public License v2


# book.py
# RegExs para dividir data de las notas (id, llamada, texto y href)
REGEX_SPLIT_NOTE = r'<p id=\"(.*?)\"><sup>\[(.*?)\]</sup>(.*?)<a href=\"(.*?)\">&lt;&lt;</a></p>'

# RegEx para obtener datos extras dentro de un tag p o h.
REGEX_GET_EXTRA_ENTRIES = r'<[ph](?! id=\")(?:.*?)>'


# configWindow.py
# Utilizada en note.processIbid() para dividir llamada ibíd del agregado.
REGEX_SPLIT_IBID = r'(?i)(?:<.*?>)?(?:ib[ií]d(?:em)?)[ .,;:<](?:<)?(?:/.*?>)?(?:[ .,;:])*'


# note.py
# Regex para encontrar ibids
REGEX_IBID = r'(?i)(ib[íi]d(em)?)[;\., (</i>)]'

# Regex para analizar notas base (detecta si tienen info de pág. al final)
REGEX_PAGE_INFO_SPLIT = r'(?i) (pp?[aá]?(?:gs|g)?(?:ina)?s?(?:\.)?(?: |(?:&nbsp;))\d+(?:-?\d*))(?:\.)?'