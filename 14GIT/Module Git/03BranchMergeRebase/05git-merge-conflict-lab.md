# Git Merge Conflict Resolution Lab

## Objective
In this lab, you'll create a Git repository, create a merge conflict, and then resolve it. This will give you hands-on experience with Git's merge conflict resolution process.

## Prerequisites
- Git installed on your system
- Basic familiarity with Git commands

## Steps

### 1. Set up the repository

```bash
# Create a new directory and initialize a Git repository
mkdir merge-conflict-lab
cd merge-conflict-lab
git init

# Create an initial file and commit it
echo "Initial content" > file.txt
git add file.txt
git commit -m "Initial commit"
```

### 2. Create and switch to a new branch

```bash
git branch feature-branch
git checkout feature-branch
```

### 3. Make changes in the feature branch

```bash
echo "Feature branch change" > file.txt
git commit -am "Change in feature branch"
```

### 4. Switch back to main and make a different change

```bash
git checkout main
echo "Main branch change" > file.txt
git commit -am "Change in main branch"
```

### 5. Attempt to merge the feature branch into main

```bash
git merge feature-branch
```

You should see a message indicating a merge conflict.

### 6. Resolve the conflict

Open `file.txt` in a text editor. You should see something like:

```
<<<<<<< HEAD
Main branch change
=======
Feature branch change
>>>>>>> feature-branch
```

Edit the file to resolve the conflict. For example, you might change it to:

```
Resolved content combining main and feature changes
```

### 7. Stage and commit the resolved file

```bash
git add file.txt
git commit -m "Resolved merge conflict"
```

### 8. Verify the resolution

```bash
git status
cat file.txt
```

You should see that there are no more conflicts and the file contains the resolved content.

## Conclusion

Congratulations! You've successfully created a merge conflict and resolved it. This process demonstrates how Git handles conflicting changes and how you can manually resolve them.

## Additional Exercises

1. Try creating a conflict with multiple files.
2. Experiment with Git's `mergetool` to resolve conflicts.
3. Practice using `git log` to understand the commit history after resolving a conflict.
