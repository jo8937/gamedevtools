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

auth_token = os.getenv("EVER_TOKEN") # "your developer token"

# To access Sandbox service, set sandbox to True
# To access production (International) service, set both sandbox and china to False
# To access production (China) service, set sandbox to False and china to True
sandbox = True
china = False

# Initial development is performed on our sandbox server. To use the production
# service, change sandbox=False and replace your
# developer token above with a token from
# https://www.evernote.com/api/DeveloperToken.action
client = EvernoteClient(token=auth_token, sandbox=sandbox, china=china)

user_store = client.get_user_store()

version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)
print "Is my Evernote API version up to date? ", str(version_ok)
print ""
if not version_ok:
    exit(1)

note_store = client.get_note_store()

# List all of the notebooks in the user's account
notebooks = note_store.listNotebooks()
print "Found ", len(notebooks), " notebooks:"
for notebook in notebooks:
    print "  * ", notebook.name
    notebook = note_store.getNotebook(notebook.guid)

    notelist = note_store.findNotesMetadata(auth_token, NoteFilter(notebookGuid=notebook.guid), 0, 100, NotesMetadataResultSpec(includeTitle=True))
    for note in notelist.notes:
        print note.title

    #print note_store.listNotes(notebook.guid)

print
print "Creating a new note in the default notebook"
print
