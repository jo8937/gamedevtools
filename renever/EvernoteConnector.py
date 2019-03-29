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
import os

from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

import settings
import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

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

    def __init__(self):
        self.auth_token = os.getenv("EVER_TOKEN") # "your developer token"

        self.client = EvernoteClient(token=self.auth_token, sandbox=True, china=False)

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


    def get_note_dict_in_notebook(self, notebook_name="1차완료"):
        notebooks = self.note_store.listNotebooks()
        print "Found ", len(notebooks), " notebooks:"

        notedictlist = []
        for notebook in notebooks:
            print notebook.name
            if notebook.name.endswith(notebook_name):
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

    #print note_store.listNotes(notebook.guid)


if __name__ == '__main__':
    ev = EvernoteConnector()
    notelist = ev.get_note_dict_in_notebook()
    for n in notelist:
        print n