# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 16:15:32 2021

@author: Bosa
"""
import re

def stripeFolder(givenFilePath):
    """
    Retrieves the folder from a given full file path

    Parameters
    ----------
    givenFilePath : A file path like: c:/someFolder/someFile.txt
        DESCRIPTION.

    Returns
    -------
    newString : Folder of the given file: c:/someFolder/

    """
    temp = re.split(r'/', givenFilePath)
    newString = ''
    for i in range(0, len(temp) - 1):
        newString += temp[i] + '/'
    #return newString[:-1]
    return newString

def cleanUp(pattern, someString):
    """
    Splits the given string with the given pattern, takes the last part of
    the splitted string. It is used for cleaning file names, i.e. :
        "./bash.pdf" --> "bash.pdf"

    Parameters
    ----------
    pattern : a pattern to split the string, regex works: r'^\.\/' --> "./"
    someString : string to be splitted: "./bash.pdf" 

    Returns
    -------
    Last of the splitted string: "bash.pdf"

    """
    x = re.split(pattern, someString)
    return re.sub(r'\n', '', x[-1])
