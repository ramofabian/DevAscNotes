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
### List all branches
```bash
#List branches 
git branch
#List branches with details
git branch -r
```
### Create a branch
```bash
#Create a branch  
git branch <BRANCH_NAME>
#Create a branch a switch to that branch inmediatily  
git checkout -b <BRANCH_NAME>
#Switch to a already exisiting branch
git checkout <BRANCH_NAME>
```