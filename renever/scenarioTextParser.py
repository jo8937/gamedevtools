# -*- coding: utf-8 -*-

import os

from enexParser import parseNoteXML, parseNoteXMLString

#dirlist = os.listdir("source")
from EvernoteConnector import EvernoteConnector
from collections import Counter


class Paragraph(object):
    def __init__(self):
        self.textlist = None
        pass

    def fromEnex(self, filepath='source/Evernote.enex'):
        self.textlist = parseNoteXML(filepath)


    def fromServer(self):
        self.textlist = []
        ev = EvernoteConnector()
        notes = ev.get_note_dict_in_notebook()
        for n in notes:
            xml = n.get("content_xml")
            txt = parseNoteXMLString(xml)
            self.textlist.extend(txt)

    def trace(self):
        l = []
        for t in self.textlist:
            s = Statement(t)
            if s.chara:
                l.append( s.scgset() )
                #print s.chara, s.cloth, s.emo

        c = Counter(l)
        for k, cnt in c.most_common():
            print cnt, ",".join(k)

class Statement(object):

    chara = ""
    cloth = ""
    emo = ""
    line = ""

    def __init__(self, line):
        if line is None:
            return
        self.line = line
        if line.strip().startswith(("/","#",u"／",u"＃")):
            tpl = line[1:].split()
            if tpl and len(tpl) > 2:
                self.chara = tpl[0]
                self.cloth = tpl[1]
                self.emo = tpl[2]
    def scgset(self):
        return (self.chara, self.cloth, self.emo)

if __name__ == '__main__':
    p = Paragraph()
    p.fromServer()
    p.trace()