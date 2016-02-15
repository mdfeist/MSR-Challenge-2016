import sys
from sets import Set

projects = []

class Project:
    def __init__(self):
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

    def getStats(self):
        output = self._dir

        libs = Set()
        author_names = Set()
        authors = {}

        # Get authors and libs used in project
        for commit in self._commits:
            author = commit.getAuthor()
            author_names.add(author)

            for f in commit.getFiles():
                for lib in f.getLibs().getHist():
                    libs.add(lib)

        for author in author_names:
            authors[author] = Author()
            authors[author].setName(author)

            author_libs = authors[author].getLibs()

            for lib in libs:
                author_libs.add(lib, 0)

        for commit in self._commits:
            name = commit.getAuthor()
            author = authors[name]

            for f in commit.getFiles():
                for hist, count in f.getHistogram().getHist().items():
                    author.getHistogram().add(hist, count)
                for lib, count in f.getLibs().getHist().items():
                    author.getLibs().add(lib, count)

        for key, author in authors.items():
            output += author.toStr("\t")


        return output

        #print(libs)


    def __str__(self):
        output = self._dir + "\n"
        output += "Number of Commits: " + str(len(self._commits)) + "\n"

        for commit in self._commits:
            output += commit.toStr("\t")

        return output
    
    def __repr__(self):
        return self.__str__()

class Author:
    def __init__(self):
        self._name = ""
        self._hist = Histogram()
        self._libs = Histogram()

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def getHistogram(self):
        return self._hist

    def getLibs(self):
        return self._libs

    def toStr(self, tab):
        output = tab + "Author: " + self._name + "\n"
        output += self._hist.toStr(tab + "\t")
        output += "\n"
        output += self._libs.toStr(tab + "\t")

        return output

    def __str__(self):
        return self.toStr("")
    
    def __repr__(self):
        return self.__str__()

class Commit:
    def __init__(self):
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

    def toStr(self, tab):
        output = tab + "Author: " + self._author + "\n"
        output += tab + "Commit ID: " + self._commit + "\n"
        output += tab + "Previous Commit ID: " + self._prevcommit + "\n"
        output += tab + "Number of Files: " + str(len(self._files)) + "\n"

        return output

    def __str__(self):
        return self.toStr("")
    
    def __repr__(self):
        return self.__str__()

class File:
    def __init__(self):
        self._local = ""
        self._remote = ""
        self._libs = Histogram()
        self._hist = Histogram()

    def setLocal(self, name):
        self._local = name

    def getLocal(self):
        return self._local

    def setRemote(self, name):
        self._remote = name

    def getRemote(self):
        return self._remote

    def getHistogram(self):
        return self._hist

    def getLibs(self):
        return self._libs

    def toStr(self, tab):
        output = tab + "Local File: " + self._local + "\n"
        output += tab + "Remote File: " + self._remote + "\n"

        output += self._hist.toStr(tab + "\t")
        output += self._libs.toStr(tab + "\t")

        return output

    def __str__(self):
        return self.toStr("")
    
    def __repr__(self):
        return self.__str__()

class Histogram:
    def __init__(self):
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

    def toStr(self, tab):
        output = ""

        for key, value in self._hist.iteritems():
            output += tab + key + ": " + str(value) + "\n"

        return output

    def __str__(self):
        return self.toStr("")
    
    def __repr__(self):
        return self.__str__()

def getStats(filename):
    current_project = None
    current_commit = None
    current_file = None
    hist_has_titles = False
    hist_tmp_titles = []
    with open(filename) as f:
        for line in f:
            if ("#PROJECT_START" in line):
                current_project = Project()
            if ("#PROJECT_END" in line):
                #print(current_project)
                projects.append(current_project)
            if ("#PROJECT_NAME" in line):
                name = line.split("|")[1].replace('\n','').strip()
                current_project.setDir(name)
            if ("#COMMIT_START" in line):
                current_commit = Commit()
            if ("#COMMIT_END" in line):
                #print(current_commit)
                current_project.addCommit(current_commit)
            if ("#AUTHOR" in line):
                name = line.split("|")[1].replace('\n','').strip()
                current_commit.setAuthor(name)
            if ("#COMMIT |" in line):
                commits = line.split("|")[1].replace('\n','').strip().split()
                current_commit.setCommitID(commits[0])

                if len(commits) > 1:
                    current_commit.setPrevCommitID(commits[1])
            if ("#FILE1" in line):
                current_file = File()

                name = line.split("|")[1].replace('\n','').strip()
                current_file.setLocal(name)
            if ("#FILE2" in line):
                name = line.split("|")[1].replace('\n','').strip()
                current_file.setRemote(name)
            if ("#STATS_END" in line):
                #print(current_file)
                current_commit.addFile(current_file)
            if ("#HISTOGRAM" in line):
                if not hist_has_titles:
                    split_str = line.split("|")
                    for i in range(1, len(split_str)-1):
                        hist_tmp_titles.append(split_str[i].strip())

                    hist_has_titles = True
                else:
                    hist = current_file.getHistogram()

                    split_str = line.split("|")
                    for i in range(0, len(hist_tmp_titles)):
                        name = hist_tmp_titles[i]
                        value = int(split_str[i+1].strip())
                        hist.add(name, value)

                    hist_has_titles = False
                    hist_tmp_titles = []
            if ("#LIB" in line):
                libs = current_file.getLibs()
                split_str = line.split("|")
                name = split_str[1].strip()
                value = int(split_str[2].strip())
                libs.add(name, value)




#files = ["out1.out", 
#        "out2.out",
#        "out3.out",
#        "out4.out",
#        "out5.out",
#        "out6.out",
#        "out7.out"]

files = ["test.out"]

for f in files:
    getStats(f)

print("Number of Projects: " + str(len(projects)))

for project in projects:
    print(project.getStats())