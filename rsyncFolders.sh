#!/bin/bash

# rsync /c/DosyalarEmre/Teknik/FolderSync/folder1test/ /c/DosyalarEmre/Teknik/FolderSync/folder2test/

pythonFolder="/c/DosyalarEmre/Teknik/FolderSync/WorkingFolder/"
tempFolder="/c/DosyalarEmre/Teknik/FolderSync/syncTempFolder/"

echo "Bash: Cleaning up previous files"
fileVar='*.*'
rm -rf $tempFolder$fileVar

numargs=$#

searchW="$1"
replaceW="$2"

### Get the folders
# https://stackoverflow.com/questions/4210042/how-to-exclude-a-directory-in-find-command
#find . -type d
#find . -path './.git' -prune -o -type f -print >> $reportFolders1

logGit1="GitLog1.txt"
filesInMainGit1="FilesInMainGit1.txt"
filesInMain1="FilesInMain1.txt"
#foldersInMain1="FoldersInMain1.txt"

logGit2="GitLog2.txt"
filesInMainGit2="FilesInMainGit2.txt"
filesInMain2="FilesInMain2.txt"
#foldersInMain2="FoldersInMain2.txt"

cd $1
git status >> $tempFolder$logGit1
git ls-files >> $tempFolder$filesInMainGit1
find . -path './.git' -prune -o -type f -print >> $tempFolder$filesInMain1
#find . -path './.git' -prune -o -type d -print >> $tempFolder$foldersInMain1

cd $2
git status >> $tempFolder$logGit2
git ls-files >> $tempFolder$filesInMainGit2
find . -path './.git' -prune -o -type f -print >> $tempFolder$filesInMain2
#find . -path './.git' -prune -o -type d -print >> $tempFolder$foldersInMain2

### Begin Python ###
echo "Bash: Starting Python script"

cd $pythonFolder
python "./synchronizeFolders.py" $1 $2 $tempFolder

echo "Bash: Waiting for Python now"
pid=$!
wait $pid

echo "Bash: Completed Python Script"
### End Python ###
: '
# Bash alternative of operations, not working
# https://linoxide.com/linux-shell-script/read-file-line-by-line-in-bash-script/
operationId='operation*.txt'
operationFiles=$( ls $tempFolder$operationId )

for f in $operationFiles; do
	echo $f
	cat $f | while read y
	do
		#echo "Line contents are : $y "
		$y
	done
done
'
# https://linoxide.com/linux-command/wait-command-in-linux/
# https://askubuntu.com/questions/38108/how-to-change-directory-at-the-end-of-a-bash-script