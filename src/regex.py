#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2021 Titivillus
# www.epublibre.org
# Distributed under the terms of the GNU General Public License v2


# book.py
# RegExs para dividir data de las notas (id, llamada, texto y href)
REGEX_SPLIT_NOTE = r'<p id=\"(.*?)\"><sup>\[(.*?)\]</sup>(.*?)<a href=\"(.*?)\">&lt;&lt;</a></p>'


# configWindow.py
# Utilizada en note.processIbid() para dividir llamada ibíd del agregado.
REGEX_SPLIT_IBID = r'(?i)(?:<.*?>)?(?:ib[ií]d(?:em)?)[ .,;:<](?:<)?(?:/.*?>)?(?:[ .,;:])*'


# note.py
# Regex para encontrar ibids
REGEX_IBID = r'(?i)(ib[íi]d(em)?)[;\., (</i>)]'

# Regex para analizar notas base (detecta si tienen info de pág. al final)
REGEX_PAGE_INFO_SPLIT = r'(?i) (pp?[aá]?(?:gs|g)?(?:ina)?s?(?:\.)?(?: |(?:&nbsp;))\d+(?:-?\d*))(?:\.)?'

# Regex para casos "págs. X a Y.", "pag A y B", "pags X-Y.", etc.
REGEX_RANGE_INI = r'(?i)p[aá]g(?:s)?(?:\.)?(?: |(?:&nbsp;))(?:\d+)'
REGEX_RANGE_END = r'(?i)(?: |(?:&nbsp;))?[ya,-](?: |(?:&nbsp;))?(?:\d+)\.$'