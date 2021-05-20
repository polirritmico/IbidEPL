# # import sys
# # import os
# import re
# from plugin import REGEX_IBID
# # from note import Note
# # from book import Book


# class Note:
#     def __init__(self, note_id, note_number, note_text, note_href, note_index):
#         # Data
#         self.id_tag = note_id
#         self.number = note_number
#         # text sin strip por comportamiento extraño de la REGEX
#         self.text = note_text
#         self.original_text = note_text.strip()
#         self.href = note_href
#         self.index = note_index

#         # Collection and Control
#         self.childs = []
#         self.is_ibid = False
#         self.parent = None
#         self.next_note = None
#         self.prev_note = None

#         self.edited = False
#         self.processed = False

#         # Ui
#         self.current_label = ""
#         self.browserEntry = None

#     def setParent(self, item):
#         if item != self:
#             self.parent = item
#         else:
#             self.parent = None

#     def toXHTML(self) -> str:
#         note_top = '  <div class="nota">\n    <p id="'
#         note_mid = self.id_tag + '"><sup>[' + self.number + ']</sup> ' + \
#             self.text + ' <a href="' + self.href + '">&lt;&lt;</a></p>\n'
#         note_btm = '  </div>\n\n'

#         return note_top + note_mid + note_btm

#     def ibidCheck(self) -> bool:
#         if re.search(REGEX_IBID, self.text):
#             self.is_ibid = True
#         return self.is_ibid

#     def processIbidem(self, regex, ibid_tag, separator) -> str:
#         if not self.is_ibid:
#             return self.text
#         if regex == "":
#             regex = REGEX_IBID
#             # regex = r'(?i)(?:<*.?>)?(?:ib[íi]d(?:em)?)(?:</i>)?(?:[;\., ]*)?'

#         splited_note = re.split(regex, self.text)
#         splited_note = list(filter(None, splited_note))

#         has_added_text = True if len(splited_note) > 0 else False
#         if has_added_text:
#             added_text = ""
#             for line in splited_note:
#                 added_text = added_text + line
#             self.text = ibid_tag + " " + self.parent.text + " " + \
#                 separator + " " + added_text
#         else:
#             self.text = ibid_tag + " " + self.parent.text

#         return self.text
