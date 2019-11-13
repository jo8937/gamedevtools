# -*- coding: utf-8 -*-

import os
import re

from EnexParser import parseNoteXML, parseNoteXMLString

#dirlist = os.listdir("source")
from EvernoteConnector import EvernoteConnector
from collections import Counter

import sys
reload(sys)
sys.setdefaultencoding('utf8')


from ScenarioTextParser import *

def execute_sync():
    p = Paragraph()
    p.fromServer()
    p.updateServerMetadata()

def execute_command():
    import argparse

    parser = argparse.ArgumentParser(description='Find original log from guid')
    parser.add_argument('cmd', help="log file path", choices = ["sync","trace"])
    # parser.add_argument('--fieldname', help='fieldname that ', default="guid")
    args = parser.parse_args()

    if args.cmd == "sync":
        execute_sync()
    else:
        print args.cmd , " command not implements"

if __name__ == '__main__':
    execute_command()
