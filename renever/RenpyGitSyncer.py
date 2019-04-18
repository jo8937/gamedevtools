# -*- coding: utf-8 -*-
import logging
import os
import re

from EnexParser import parseNoteXML, parseNoteXMLString

#dirlist = os.listdir("source")
from EvernoteConnector import EvernoteConnector
from collections import Counter

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

class RenpyGitSyncer(object):
    def __init__(self):
        self.log = logging.getLogger("RenpyGitSyncer")
        pass

    def getEvernoteConnector(self):
        if self.ev is None:
            self.ev = EvernoteConnector(False)
        return self.ev

    def fromServer(self):
        self.textlist = []
        ev = self.getEvernoteConnector()
        notes = ev.get_note_dict_in_tag("renpydraft")
        for n in notes:
            xml = n.get("content_xml")
            txt = parseNoteXMLString(xml)
            self.textlist.extend(txt)

    def git_sync(self, sourcepath, remoteurl, branch):
        from git import Repo, cmd
        if not os.path.exists(sourcepath):
            self.download_source(sourcepath, remoteurl, branch)

        try:
            g = cmd.Git(sourcepath)
            repo = Repo(sourcepath)
            remote = repo.remote('origin')
            l = remote.pull()
            self.log.info([f.commit.message for f in l])

            if repo.active_branch.name <> branch:
                self.log.info("switch %s to %s ... " % (repo.active_branch.name, branch))
                # stashid =  datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%H-%M-%S")
                # repo.git.stash.drop( stashid )
                repo.git.checkout('HEAD', b=branch)
            else:
                repo.git.reset("--hard", "origin/" + branch)

        except:
            self.log.error("git error...", exc_info=True)
            if os.path.exists(sourcepath):
                self.log.error("remove path [%s] and clone again...", sourcepath)
                import shutil
                shutil.rmtree(sourcepath)
            self.download_source(sourcepath, remoteurl, branch)

            # git clone

    def download_source(self, sourcepath, remoteurl, branch):
        from git import Repo, cmd
        self.log.info("start clone from %s ... to ...  %s" % (remoteurl, sourcepath))
        # self.log.info( g.clone(remoteurl, b = branch) )
        repo = Repo.clone_from(remoteurl, sourcepath, branch=branch)
        heads = repo.heads
        self.log.info(heads)

      
if __name__ == '__main__':
    p = RenpyGitSyncer()
    #p.fromServer()
    p.git_sync("/game/renpytools","https://github.com/jo8937/renpytools","master")
    #p.updateServerMetadata()
