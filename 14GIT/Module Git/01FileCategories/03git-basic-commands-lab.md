# Git Basic Commands Lab Exercise

## Step 1: Initialize and Configure Repository

```bash
mkdir git_lab
cd git_lab
git init
git config --local user.name "Your Name"
git config --local user.email "your.email@example.com"
```

## Step 2: Add and Commit Initial Files

```bash
echo "File 1 content" > file1.txt
echo "File 2 content" > file2.txt
git add file1.txt file2.txt
git commit -m "Initial commit with two files"
```

## Step 3: Remove a File

```bash
git rm file2.txt
git diff
```

## Step 4: Rename a File

```bash
git mv file1.txt renamed_file1.txt
git diff
```

## Step 5: Commit Changes and View History

```bash
git commit -m "Removed file2.txt and renamed file1.txt"
git log
git ls-files
```

## Step 6: Add New Files and Ignore One

```bash
echo "File 3 content" > file3.txt
echo "File 4 content" > file4.txt
echo "file4.txt" > .gitignore
git add .gitignore
git commit -m "Added .gitignore"
echo "New content" >> renamed_file1.txt
git ls-files
```

## Step 7: Explore git ls-files Options

```bash
git ls-files -t
git ls-files -o
man git ls-files
```

## Step 8: Add New Files and Commit

```bash
git add file3.txt renamed_file1.txt
git commit -m "Added file3.txt and modified renamed_file1.txt"
git ls-files --stage
git log
```

