# -*- coding: utf-8 -*-

from lxml import etree
from StringIO import StringIO

import sys
reload(sys)  
sys.setdefaultencoding('utf8')


class AllEntities:
    def __getitem__(self, key):
        #key is your entity, you can do whatever you want with it here
        return key    

p = etree.XMLParser(remove_blank_text=True, resolve_entities=True)
# p.parser.UseForeignDTD(True)
# p.entity = AllEntities()

def parseNoteXML(xmlFile):
    notes = parseNoteDictXML(xmlFile)
    texts = []
    for n in notes:
        c = n.get("content")
        texts.extend(c)

    return texts

def parseNoteDictXML(xmlFile):
    context = etree.iterparse(xmlFile, encoding='utf-8', strip_cdata=False)
    note_dict = {}
    notes = []
    for ind, (action, elem) in enumerate(context):
        text = elem.text
        if elem.tag == 'content':
            text = convertToPlaneText(elem)
        note_dict[elem.tag] = text
        if elem.tag == "note":
            notes.append(note_dict)
            note_dict = {}
    return notes

def parseNoteXMLString(xmlstring):
    texts = []
    context = etree.iterparse(StringIO(xmlstring))
    for ind, (action, elem) in enumerate(context):
        if elem.text:
            texts.append(elem.text)

    return texts

def convertToPlaneText(elem):
    text = []
    r = etree.parse(StringIO(elem.text.encode('utf-8')), p)
    for e in r.iter():
        try:
            text.append(e.text)
        except:
            print 'cannot print'
    return text

if __name__ == '__main__':
    txts = parseNoteXML("./source/Evernote.enex")
    for t in txts:
        print t
 