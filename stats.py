import sys

class Project:
    def __init__():
        self._dir = ""
        self._commits = []

    def setDir(self, name):
        self._dir = name

    def getDir(self):
        return self._dir

    def addCommit(self, commit):
        self._commits.append(commit)

    def getCommits(self):
        return self._commits


class Commit:
    def __init__():
        self._author = ""
        self._commit = ""
        self._prevcommit = ""
        self._files = []

    def setAuthor(self, name):
        self._author = name

    def getAuthor(self):
        return self._author

    def setCommitID(self, commit):
        self._commit = commit

    def getCommitID(self):
        return self._commit

    def setPrevCommitID(self, commit):
        self._prevcommit = commit

    def getPrevCommitID(self):
        return self._prevcommit

    def addFile(self, f):
        self._files.append(f)

    def getFiles(self):
        return self._files

class File:
    def __init__():
        self._local = ""
        self._remote = ""
        self._libs = {}
        self._hist = Histogram()

class Histogram:
    def __init__():
        self._hist = {}

    def add(self, name, value):
        if name in self._hist:
            self._hist[name] += value
        else:
            self._hist[name] = value

    def get(self, name):
        return self._hist[name]

    def getHist(self):
        return self._hist

filename = sys.argv[1]

projects = []
current_project = None
current_commit = None

with open(filename) as f:
    for line in f:
        if ("#PROJECT_START" in line):