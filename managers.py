# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 11:00:19 2021

@author: Bosa
"""
import re
import pandas as pd
import tools

class SynchFolder:
    """
    Class for a folder tobbe synchronized. Consists of just the FileManager,
    FolderManager and TopFolder.
    """
    def __init__(self, folderTop, filesInMain, filesInMainGit, gitLog):
        self.folderManager = FolderManager(filesInMain, filesInMainGit)
        self.fileManager = FileManager(gitLog, filesInMainGit, self.folderManager.foldersGitIgnore)
        self.mainFolder = folderTop

class FolderManager:
    """
    Class for managing folders, takes the text files generated from bash script
    and finds out which folders are in git repo, which folders are under the 
    main folder, and as difference of both which are not tracked by git
    """
    def __init__(self, filesInMain, filesInMainGit):
        self.__filesInMainRaw__ = filesInMain
        self.__filesInMainGitRaw__ = filesInMainGit
        self.__cleanFiles__()
        self.__getFolderStructure__()

    def __cleanFiles__(self):
        newArray1 = []
        newArray2 = []
        pattern = r'^\.\/'

        f = open(self.__filesInMainRaw__)
        for line in f:
            newArray1.append(tools.cleanUp(pattern, line))
        f.close()
        self.filesInMain = newArray1

        f = open(self.__filesInMainGitRaw__)
        for line in f:
            newArray2.append(tools.cleanUp(pattern, line))
        f.close()
        self.filesInMainGit = newArray2

    def __getFolderStructure__(self):
        foldersInMain = [item for item in self.filesInMain if r'/' in item]
        foldersInMainGit = [item for item in self.filesInMainGit if r'/' in item]

        self.foldersInMain = list({tools.stripeFolder(item) for item in foldersInMain})
        self.foldersInMainGit = list({tools.stripeFolder(item) for item in foldersInMainGit})
        self.foldersGitIgnore = [value for value in self.foldersInMain \
                                 if value not in self.foldersInMainGit]

        self.foldersInMain.sort()
        self.foldersInMainGit.sort()
        self.foldersGitIgnore.sort()

class FileManager:
    """
    Class for determining which operations took place on the files, i.e. if the
    file is deleted, modified, not tracked or not changed (= base file)
    """
    def __init__(self, reportFile, treeFile, ignoreFolderList):
        self.reportFile = reportFile
        self.treeFile = treeFile
        self.ignoreFolderList = ignoreFolderList
        self.__analyzeLogs__()
        self.__folderTree__()
        self.generateDataFrame()

    def __folderTree__(self):
        self.folderTree = []
        f = open(self.treeFile)
        for line in f:
            self.folderTree.append(re.sub(r'\n', '', line))
        f.close()

    def __analyzeLogs__(self):
        modified = []
        deleted = []
        added = []
        ignored = self.ignoreFolderList
        trigger = 0
        f = open(self.reportFile)

        for line in f:

            if "modified:" in line:
                modified.append(line)

            if "deleted: " in line:
                deleted.append(line)

            if "Untracked files:" in line:
                trigger = 1
                # trigger.append(1)
            if "no changes added to commit" in line:
                trigger = 0
                # trigger.append(-1)

            if trigger == 1:
                added.append(line)

        f.close()
        pattern = r':\s+'

        self.modified = [tools.cleanUp(pattern, item) for item in modified]
        self.deleted = [tools.cleanUp(pattern, item) for item in deleted]
        temp = [tools.cleanUp(r'\t', item) for item in added if '\t' in item]
        self.added = [item for item in temp if item not in ignored]
        self.ignored = ignored

    def generateDataFrame(self):
        """
        This function generates the dataframe based on the file modifications

        Returns
        -------
        None. Adds a dataframe to the object

        """
        labelArray = []

        # At this level ignored files are excluded
        for item in self.added:
            self.folderTree.append(item)

        for item in self.folderTree:
            if item in self.modified:
                labelArray.append('modified')
            elif item in self.deleted:
                labelArray.append('deleted')
            elif item in self.ignored:
                labelArray.append('ignored')
            elif item in self.added:
                labelArray.append('added')
            else:
                labelArray.append('baseFile')

        df = pd.DataFrame(list(zip(self.folderTree, labelArray)), \
                          columns=['File', 'Type'])
        self.fileDataFrame = df
