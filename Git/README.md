# Git notes
## Git Commands
### Create a local git repo
```bash
#Create a local repo
git init
```
### Check repo status
```bash
#Check repo status
git status
```
### Stage files or list of files
```bash
#Stage all files/folders in active directory
git add . 
#Stage specific file
git add file.txt
```
### Commit changes
```bash
#Commit
git commit -m "<MESSAGE>"
```
### Unstage files
```bash
#Unstage files in local repo
git restore <FILE/DIRECTORY>
```
### Delete files
```bash
#In local directory and git repo
git rm <FILE/DIRECTORY>

#From remote repo only
git rm --cached <FILE/DIRECTORY>
```