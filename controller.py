# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 16:25:04 2021

@author: Bosa
"""
import os
import shutil
import tools
import pandas as pd
from managers import SynchFolder

class Controller:
    """
    Class for controlling the operations. This class decides on which operation
    to execute, and then executes it
    """
    def __init__(self, folderA_, folderB_, aFileList):
        print("Python: Main controller running")

        FilesInMain1 = aFileList[0]
        FilesInMainGit1 = aFileList[2]
        GitLog1 = aFileList[4]

        FilesInMain2 = aFileList[1]
        FilesInMainGit2 = aFileList[3]
        GitLog2 = aFileList[5]

        self.folderA = SynchFolder(folderA_, FilesInMain1, FilesInMainGit1, GitLog1)
        self.folderB = SynchFolder(folderB_, FilesInMain2, FilesInMainGit2, GitLog2)

        self.__decideOperations__()
        self.__checkFolders__()
        self.__executeOperations__()

    def __decideOperations__(self):
        """
        Decides on which operation to execute. There is a little bit of maths 
        here, check the README.md for details

        Returns
        -------
        None.

        """
        print("Python: Deciding on operations")
        mergedDF = pd.merge(self.folderA.fileManager.fileDataFrame, self.folderB.fileManager.fileDataFrame, on = "File", how = "outer")
        clashArray = [0] * len(mergedDF.Type_x)
        '''
        nan is shown as float in the dataframe, therefore conversion to str is done
        '''

        '''
        Small mathematics for deciding on operations without using tens of if cases, instead label codes are used

        deleted = -10
        NaN = 0
        baseFile = 10
        modified = 20
        added = 30

        As an alternative approach, I built a neural network but computationwise, it was unncessary for such a simple case
        '''

        labelCode = {'deleted':-10, 'nan':0, 'baseFile': 10, 'modified': 20, 'added': 30}

        labelCodeArray_x = []
        labelCodeArray_y = []

        for i in range(0, len(clashArray)):
            v1 = str(mergedDF.Type_x.iloc[i])
            v2 = str(mergedDF.Type_y.iloc[i])
            labelCodeArray_x.append(labelCode[v1])
            labelCodeArray_y.append(labelCode[v2])

        logic1 = [item1+item2 for item1, item2 in zip(labelCodeArray_x, labelCodeArray_y)]
        logic2 = [item1*item2 for item1, item2 in zip(labelCodeArray_x, labelCodeArray_y)]

        operation = []

        for added, multiplied in zip(logic1, logic2):
            if (multiplied >= 300) or (multiplied <= -200):
                operation.append('Clash')
            elif multiplied == -100:
                operation.append('Delete')
            elif (added >= 0) and (multiplied != 100):
                operation.append('Copy')
            else:
                operation.append('DoNothing')

        labelCodeArray = [int(item1 > item2) for item1, item2 in zip(labelCodeArray_x, labelCodeArray_y)]

        mergedDF = mergedDF.assign(Code_x = labelCodeArray_x)
        mergedDF = mergedDF.assign(Code_y = labelCodeArray_y)
        mergedDF = mergedDF.assign(Direction = labelCodeArray)
        mergedDF = mergedDF.assign(Operation = operation)

        self.operationDF = mergedDF
        self.__copyDF__ = self.operationDF[self.operationDF.Operation == 'Copy']
        self.__deleteDF__ = self.operationDF[self.operationDF.Operation == 'Delete']

    def __checkFolders__(self):
        """
        Checks if any of the folders or subfolders that should be created 
        beforehand in case a file is going to be copied from the other folder

        Returns
        -------
        Adds lists to the object

        """
        # Tied to Create Folders -- alternative 1
        copyFoldersThatShouldBeInA = [tools.stripeFolder(item.File) \
                                      for x, item in self.__copyDF__.iterrows() if item.Direction == 0]
        copyFoldersThatShouldBeInB = [tools.stripeFolder(item.File) \
                                      for x, item in self.__copyDF__.iterrows() if item.Direction == 1]

        # the structure will be like: ['', 'someSubFolder/']
        self.__copyFoldersThatShouldBeInA__ = list(set(copyFoldersThatShouldBeInA))
        self.__copyFoldersThatShouldBeInB__ = list(set(copyFoldersThatShouldBeInB))

        # ----------------------------------------------------
        # Tied to Create Folders -- alternative 2

        copyFoldersTempA = list(set(copyFoldersThatShouldBeInA))
        copyFoldersTempB = list(set(copyFoldersThatShouldBeInB))

        copyFoldersTempA = [item for item in copyFoldersTempA if item != '']
        copyFoldersTempB = [item for item in copyFoldersTempB if item != '']

        copyFoldersThatAreNotInA = [item for item in copyFoldersTempA \
                                    if item not in self.folderA.folderManager.foldersInMain]
        copyFoldersThatAreNotInB = [item for item in copyFoldersTempB \
                                    if item not in self.folderB.folderManager.foldersInMain]

        self.__copyFoldersThatAreNotInA__ = copyFoldersThatAreNotInA
        self.__copyFoldersThatAreNotInB__ = copyFoldersThatAreNotInB

        self.__copyFoldersThatAreNotInA__.sort()
        self.__copyFoldersThatAreNotInB__.sort()

    def __executeOperations__(self):
        print("Python: Executing operations")
        # Create Folders -- alternative 1

        # This function does NOT have to be recursive for folders and subfolders etc
        # input list goes like follows in a sorted order
        # [someSubFolder/, someSubFolder/someSubSubFolder/, someSubFolder/someSubSubFolder/deepSubFolder]

        # Here there is a trick, I am not checking if the folder already exists
        # Python module os takes care of that with os.makedirs(exist_ok = True)

        '''
        print("Creating folders")
        if len(self.__copyFoldersThatShouldBeInA__) != 1:
            os.makedirs(self.__copyFoldersThatShouldBeInA__[-1], exist_ok=True)
            if len(self.__copyFoldersThatShouldBeInB__) != 1:
            os.makedirs(self.__copyFoldersThatShouldBeInB__[-1], exist_ok=True)
        '''

        # ----------------------------------------------------
        # Create Folders -- alternative 2: Safer approach, hopefully!
        print("Creating folders")
        if len(self.__copyFoldersThatAreNotInA__) != 0:
            os.makedirs(self.__copyFoldersThatAreNotInA__[-1], exist_ok=True)

        if len(self.__copyFoldersThatAreNotInB__) != 0:
            os.makedirs(self.__copyFoldersThatAreNotInB__[-1], exist_ok=True)

        # Copy Files
        print("Copying files")
        for i, row in self.__copyDF__.iterrows():
            if row.Direction == 1:
                srcFile = self.folderA.mainFolder + row.File
                destFile = self.folderB.mainFolder + row.File
            else:
                srcFile = self.folderB.mainFolder + row.File
                destFile = self.folderA.mainFolder + row.File

            shutil.copy2(srcFile, destFile)

        # Delete Files
        print("Deleting files")
        for i, row in self.__deleteDF__.iterrows():
            if row.Direction == 1:
                path = self.folderA.mainFolder  + row.File
            else:
                path = self.folderB.mainFolder  + row.File

            os.unlink(path)
