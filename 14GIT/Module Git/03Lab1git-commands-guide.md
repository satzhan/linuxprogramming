# Git Basic Operations Lab Assignment

## Objective
In this lab, you will learn how to set up a simple Git repository, make changes, commit them, and view the history of your project. You'll use basic Git commands to manage your files and understand how Git tracks changes.

## Prerequisites
- Git installed on your system
- Basic knowledge of command-line operations

## Lab Steps

### 1. Initialize the Repository
First, create a new directory for your project and initialize it as a Git repository.

```bash
mkdir git-lab
cd git-lab
git init
```

Verify that the `.git` directory has been created.

### 2. Configure Author Information
Set up your author name and email for this repository.

```bash
git config --local user.name "Your Name"
git config --local user.email "your.email@example.com"
```

### 3. Create and Add Files
Create two simple text files and add them to the repository.

```bash
echo "Hello, Git!" > file1.txt
echo "Learning Git is fun!" > file2.txt
git add file1.txt file2.txt
```

### 4. Make Your First Commit
Commit the added files to the repository.

```bash
git commit -m "Initial commit with two files"
```

### 5. Modify a File and View Differences
Make a change to one of the files and use `git diff` to see the differences.

```bash
echo "This is a new line." >> file1.txt
git diff
```

Observe the output showing the changes you made.

### 6. Stage the Modified File
Add the changed file to the staging area.

```bash
git add file1.txt
```

Run `git diff` again and notice that there's no output now. Then run:

```bash
git diff --staged
```

Observe the difference in output.

### 7. Commit the Changes
Commit the staged changes.

```bash
git commit -m "Added a new line to file1.txt"
```

### 8. View Commit History
Examine the history of your repository.

```bash
git log
```

Review the commit history, noting the commit messages and other details.

## Additional Exploration
Throughout this lab, take time to explore the contents of the `.git` directory. Look at the files that are created or modified after each Git command. This will help you understand how Git internally manages your project's version control.

## Reflection Questions
1. What happens in the `.git` directory when you initialize a repository?
2. How does the output of `git diff` change before and after staging a file?
3. What information can you see in the `git log` output?
4. How might frequent, small commits benefit a project compared to infrequent, large commits?

## Conclusion
You've now experienced the basic workflow of Git, including initializing a repository, making changes, committing those changes, and viewing the project history. These fundamental operations form the basis of version control with Git.
