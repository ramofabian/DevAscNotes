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
### See the diff in the commit
```bash
#Runs a diff and Shows all changes in the commit.
git diff
```
### show the commits content via cli
```bash
git show
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
### Merging branch into main
```bash
#1.Find source branch name
git branch
#2. Go to main branch
git checkout main
#3. Merge changes into main branch
git merge <SOURCE_BRANCH_NAME>
#4. Resolve all potential conflicts
#5. Stage the changes
git add .
#6. Commit the changes
git commit
```
### See commit history and logs
```bash
#Logs with details (press Q to quit from that view)
git logs
#See commit summary
git logs --oneline
```
### Load previous commits and create parallel changes
```bash
#1. See commit summary and identify the commit
git logs --oneline
#2. Load that commit
git checkout <COMMIT_ID>
#3. From there new commands can be done but those changes are untached from the main HEAD
#NOTE: to be able to merge those changes convert it to a branch with this command
git switch -c <NEW_BRANCH_NAME>
```
### Git revert (Prefred option)
```bash
#1. See commit summary and identify the commit
git logs --oneline
#2. revert that commit
git revert <COMMIT_ID>
#3. check commit status
git logs --oneline
#4. check commit status
git status
#NOTE: With revert commit history is not lost and new commit is added attached to HEAD with the same changes from the added commit ID
```
### Git reset
```bash
#1. See commit summary and identify the commit
git logs --oneline
#2. Reset that commit
git reset <COMMIT_ID>
#3. check commit status
git logs --oneline
#4. check commit status
git status
#NOTE: With reset commits between HEAD and the added commit ID will be orphaned and file changes will be unstaged.
```