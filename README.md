# FolderSynchronizer

FolderSync is an automation script aimed to synchronize two folders in Windows using Python, Git and Bash scripting. It is neither a synchronizing tool that creates a copy of one folder to another nor a version controlling system. Instead, it **applies** the *changes* that took place in each folder onto another. If I modify fileX in folderA, and deleted fileY in folderB, the script will delete fileY in folderA, and copy the modified fileX from folderA to folderB. Also, I want to leave some folders untouched in either folderA or folderB, and do not want to synchronize. 

### Steps:
1. Git repos are needed for both of the folders to track the changes. 
2. Bash Script rsyncFolders.sh will generate Git status reports and folder trees.
3. Generated files will be read by Python script (synchronizeFolders.py) to determine which operations to execute. 
4. Python script will then execute these operations. When the operations are executed, then the folders are in sync. 

### Further Steps:
1. Remove Git repos at this point, and create new Git repos (Why? Because I do not want to have version history of large video files, raw images etc, I just want to know if these files are modified or deleted or newly added.).
2. Add a GUI to ask user for clashing cases, i.e. a file with the same name but different content add to both of the folders etc).
3. Add detailed design document.
