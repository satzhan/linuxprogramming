# Lab: Working with a Development Branch

## Objective
In this lab, you will practice creating and working with branches in Git. You'll create a new repository, add files, create a development branch, make changes, and observe how Git manages files across different branches.

## Prerequisites
- Git installed on your system
- Basic familiarity with command line interface

## Steps

### 1. Initialize the Repository

```bash
# Create a new directory for your project
mkdir my_git_project
cd my_git_project

# Initialize the repository
git init

# Configure Git with your name and email
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 2. Add Initial Files

```bash
# Create and add content to two files
echo "This is file 1" > file1.txt
echo "This is file 2" > file2.txt

# Stage and commit the files
git add file1.txt file2.txt
git commit -m "Initial commit with two files"
```

### 3. Create and Checkout Development Branch

```bash
# Create a new branch named 'development'
git branch development

# Switch to the development branch
git checkout development

# Verify you're on the development branch
git branch
```

### 4. Modify Files in Development Branch

```bash
# Modify an existing file
echo "This is an update to file 1" >> file1.txt

# Create a new file
echo "This is file 3, created in the development branch" > file3.txt

# Stage and commit the changes
git add file1.txt file3.txt
git commit -m "Updated file1 and added file3 in development branch"

# List files in the directory
ls

# List files tracked by Git
git ls-files
```

### 5. Switch Back to Master Branch

```bash
# Checkout the master branch
git checkout master

# List files in the directory
ls

# List files tracked by Git
git ls-files
```

## Expected Results

- After step 4, when on the development branch, you should see three files (file1.txt, file2.txt, file3.txt) both in the directory listing and in git ls-files.
- After step 5, when you switch back to the master branch, you should only see two files (file1.txt, file2.txt) in both the directory listing and git ls-files. The changes made in the development branch (including the new file3.txt) will not be visible in the master branch.

## Discussion Questions

1. What differences did you notice in the file listings between the development and master branches?
2. Why do you think Git behaves this way when switching between branches?
3. How might this branching behavior be useful in a real-world development scenario?

## Additional Challenge

Try merging the development branch into the master branch. What happens to the file listings after the merge?

```bash
git checkout master
git merge development
ls
git ls-files
```

Observe and discuss the results.
