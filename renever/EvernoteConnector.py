# -*- coding: utf-8 -*-
#
# A simple Evernote API demo script that lists all notebooks in the user's
# account and creates a simple test note in the default notebook.
#
# Before running this sample, you must fill in your Evernote developer token.
#
# To run (Unix):
#   export PYTHONPATH=../../lib; python EDAMTest.py
#
import datetime
import os

from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

import settings
import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

import sys
reload(sys)  
sys.setdefaultencoding('utf8')


# Real applications authenticate with Evernote using OAuth, but for the
# purpose of exploring the API, you can get a developer token that allows
# you to access your own Evernote account. To get a developer token, visit
# https://SERVICE_HOST/api/DeveloperToken.action
#
# There are three Evernote services:
#
# Sandbox: https://sandbox.evernote.com/
# Production (International): https://www.evernote.com/
# Production (China): https://app.yinxiang.com/
#
# For more information about Sandbox and Evernote China services, please
# refer to https://dev.evernote.com/doc/articles/testing.php
# and https://dev.evernote.com/doc/articles/bootstrap.php

class EvernoteConnector():

    def __init__(self, sandbox=True):
        if sandbox:
            self.auth_token = os.getenv("EVER_TOKEN")  # "your developer token"
        else:
            self.auth_token = os.getenv("EVER_TOKEN_PRODUCTION") # "your developer token"

        self.client = EvernoteClient(token=self.auth_token, sandbox=sandbox, china=False)

        self.user_store = self.client.get_user_store()
        version_ok = self.user_store.checkVersion(
            "Evernote EDAMTest (Python)",
            UserStoreConstants.EDAM_VERSION_MAJOR,
            UserStoreConstants.EDAM_VERSION_MINOR
        )
        print "Is my Evernote API version up to date? ", str(version_ok)
        if not version_ok:
            exit(1)

        self.note_store = self.client.get_note_store()


    def get_note_dict_in_notebook(self, notebook_name="", stack_name=""):
        notebooks = self.note_store.listNotebooks()
        print "Found ", len(notebooks), " notebooks:"

        notedictlist = []
        for notebook in notebooks:
            if (notebook.stack and stack_name and notebook.stack.endswith(stack_name)) or \
                (notebook.name and notebook_name and notebook.name.endswith(notebook_name)):
                print notebook.name
                notebook = self.note_store.getNotebook(notebook.guid)
                notelist = self.note_store.findNotesMetadata(self.auth_token, NoteFilter(notebookGuid=notebook.guid), 0, 100, NotesMetadataResultSpec(includeTitle=True))
                for note in notelist.notes:
                    note_content = self.note_store.getNoteContent(note.guid)
                    d = {
                            "title":note.title,
                            "content_xml":note_content
                        }
                    notedictlist.append(d)

        return notedictlist

    def print_contents(self, noteguid):
        note = self.note_store.getNote(self.auth_token, noteguid, True,True,True,True)
        print note.content

    def create_edam_content(self, contents):

        if isinstance(contents, list):
            body = "<br/>\n".join(contents)
        else:
            body = contents

        edamContent = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>
{}
<br/>
</en-note>""".format(body)

        return edamContent

    def get_current_update_datetime(self):
        t = ['월', '화', '수', '목', '금', '토', '일']

        n = datetime.datetime.now()
        return n.strftime("%Y-%m-%d ("+t[n.weekday()]+") %H:%M:%S")

    def update_note(self, noteguid, contents):

        edamContent = self.create_edam_content(contents)
        print "------------- old ---------------"
        self.print_contents(noteguid)
        print "------------- new ---------------"
        print edamContent

        # update call

        note = Types.Note()
        note.guid = noteguid
        note.title = "Resource List : " + self.get_current_update_datetime()
        note.content = edamContent

        # Finally, send the new note to Evernote using the createNote method
        # The new Note object that is returned will contain server-generated
        # attributes such as the new note's unique GUID.
        #created_note = self.note_store.createNote(note)
        updated_note = self.note_store.updateNote(self.auth_token, note)

        print "Successfully created a new note with GUID: ", updated_note.guid
    #print note_store.listNotes(notebook.guid)


if __name__ == '__main__':
    ev = EvernoteConnector(sandbox=False)
    ev.update_note( os.getenv("EVER_NOTE_TARGET_GUID"), ["aaaa","bbbb","cccc"] )
