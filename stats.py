import sys
import os
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
        dump = self._dir
        histogram_csv = "Project, Author, Do, For, Inheritance, Generic, Try, Catch, While, ForEach, Interface, Class, If, \n"
        histogram_stats_csv = "Project, Author, Generic, Catch/Try, Try/If, Inheritance/Class, Interface/Class, \n"
        libs_csv = ""
        libs_stats_csv = "Project, Author, Percent of Libs Used, \n"
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

        # Create authors and set up lib histogram
        for author in author_names:
            authors[author] = Author()
            authors[author].setName(author)

            author_libs = authors[author].getLibs()

            for lib in libs:
                author_libs.add(lib, 0)

        # Get libs and histogram for each author
        for commit in self._commits:
            name = commit.getAuthor()
            author = authors[name]

            for f in commit.getFiles():
                for hist, count in f.getHistogram().getHist().items():
                    author.getHistogram().add(hist, count)
                for lib, count in f.getLibs().getHist().items():
                    author.getLibs().add(lib, count)

        # Get Stats
        # Get dump of authors
        for key, author in authors.items():
            # Get dump for author
            dump += author.toStr("\t")

            # Get Histogram and stats
            hist = author.getHistogram().getHist()

            histogram_csv += self._dir + ", " + author.getName().replace(",", "") + ", "
            histogram_stats_csv += self._dir + ", " + author.getName().replace(",", "") + ", "

            if len(hist) < 1:
                histogram_csv += "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,"
                histogram_stats_csv += "0, 0, 0, 0, 0,"
            else:
                for value in hist.itervalues():
                    histogram_csv += str(value) + ", "

                histogram_stats_csv += str(hist["Generic"]) + ", "
                
                if hist["Try"] == 0:
                    histogram_stats_csv += "0, "
                else:
                    histogram_stats_csv += str(hist["Catch"]/float(hist["Try"])) + ", "
                
                if hist["If"] == 0:
                    histogram_stats_csv += "0, "
                else:
                    histogram_stats_csv += str(hist["Try"]/float(hist["If"])) + ", "
                
                if hist["Class"] == 0:
                    histogram_stats_csv += "0, "
                else:
                    histogram_stats_csv += str(hist["Inheritance"]/float(hist["Class"])) + ", "
                
                if hist["Class"] == 0:
                    histogram_stats_csv += "0, "
                else:
                    histogram_stats_csv += str(hist["Interface"]/float(hist["Class"])) + ", "

            histogram_csv += "\n"
            histogram_stats_csv += "\n"

            # Libs
            libs_hist = author.getLibs().getHist()

            if libs_csv == "":
                libs_csv += "Project, Author, "
                for name in libs_hist:
                    libs_csv += name + ", "

                libs_csv += "\n"

            if len(libs_hist) > 0:
                libs_csv += self._dir + ", " + author.getName().replace(",", "") + ", "
                libs_stats_csv += self._dir + ", " + author.getName().replace(",", "") + ", "

                count = 0
                total = 0
                touched = 0
                for value in libs_hist.itervalues():
                    libs_csv += str(value) + ", "

                    if value > 0:
                        touched += 1
                    count += 1

                    total += value

                libs_stats_csv += str((100.0*touched)/float(count)) + ", "

                libs_csv += "\n"
                libs_stats_csv += "\n"

        #Libs

        return (dump, histogram_csv, histogram_stats_csv, libs_csv, libs_stats_csv)

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
            if ("#STATS_START" in line):
                hist_has_titles = False
                hist_tmp_titles = []
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
                        v = split_str[i+1].strip()

                        if not v.isdigit():
                            break

                        value = int(v)
                        hist.add(name, value)

                    hist_has_titles = False
                    hist_tmp_titles = []
            if ("#LIB" in line):
                libs = current_file.getLibs()
                split_str = line.split("|")
                name = split_str[1].strip()
                value = int(split_str[2].strip())
                libs.add(name, value)


def mergeProjectCSV(csv):
    title = csv.split('\n', 1)[0]
    csv = csv.replace(title, "")
    csv = title + csv
    return os.linesep.join([s for s in csv.splitlines() if s])


files = ["out1.out", 
        "out2.out",
        "out3.out",
        "out4.out",
        "out5.out",
        "out6.out",
        "out7.out"]

#files = ["test.out"]

print("Gathering Dump Data ...")
for f in files:
    getStats(f)
print("Number of Projects: " + str(len(projects)))
print("Gathering Stats ...")

dump_file = open('dump.out', 'w')
hist_file = open('histogram.csv', 'w')
hist_stats_file = open('histogram_stats.csv', 'w')
libs_stats_file = open('libs_stats.csv', 'w')

hist_csv = ""
hist_stats_csv = ""

libs_stats_csv = ""

for project in projects:
    #print(project.getStats()[2])
    stats = project.getStats()
    
    dump_file.write(stats[0])

    hist_csv += stats[1]
    hist_stats_csv += stats[2]

    libs_file = open('libsOutput/' + project.getDir().replace("/", "") + '.csv', 'w')
    libs_file.write(stats[3])

    libs_stats_csv += stats[4]

hist_file.write(mergeProjectCSV(hist_csv))
hist_stats_file.write(mergeProjectCSV(hist_stats_csv))
libs_stats_file.write(mergeProjectCSV(libs_stats_csv))