# Exploring Changes with git diff (Lab Exercise)

## Objective
In this lab, you'll gain hands-on experience using `git diff` to explore changes between different versions of a project. You'll learn how to compare commits, view statistics, and focus on specific parts of a repository.

## Prerequisites
- Git installed on your system
- Basic knowledge of Git commands
- A terminal or command prompt

## Lab Steps

### Step 1: Clone a Large Repository

For this lab, we'll use the Git project repository itself to have a rich history to explore.

```bash
git clone https://github.com/git/git.git
cd git
```

### Step 2: Explore Tags

First, let's see what tags are available in the repository:

```bash
git tag
```

This will show a list of all tags in the repository. Tags often represent release versions.

### Step 3: Compare Two Versions

Let's compare two versions of the Git project:

```bash
git diff v2.35.0 v2.36.0
```

This will show all changes between these two versions. The output might be very long.

### Step 4: View a Summary of Changes

To get a more manageable overview:

```bash
git diff --stat v2.35.0 v2.36.0
```

This will show a summary of changes, including the number of lines added or removed in each file.

### Step 5: Focus on a Specific Directory

Now, let's look at changes in a particular directory:

```bash
git diff v2.35.0 v2.36.0 Documentation
```

This will show changes only in the Documentation directory between these versions.

### Step 6: Examine a Specific File

To see changes in a specific file:

```bash
git diff v2.35.0 v2.36.0 README.md
```

### Step 7: Compare Working Directory to Last Commit

If you make some changes to the repository, you can see the differences:

```bash
# Make a change to README.md
echo "# Test change" >> README.md

# See the difference
git diff README.md
```

### Step 8: Compare Staged Changes

Stage the change and see how to view staged differences:

```bash
git add README.md
git diff --cached README.md
```

## Bonus Exercises

1. Use `git diff` with the `--word-diff` option to see word-level changes instead of line-level changes.

2. Try using `git diff` with `--color-words` to highlight changed words.

3. Explore the `git show` command to view changes introduced by a specific commit.

## Conclusion

In this lab, you've learned how to:
- Compare different versions of a project using `git diff`
- View summary statistics of changes
- Focus on changes in specific directories or files
- Compare working directory and staged changes to the last commit

These skills are crucial for understanding the evolution of a project and for effective code review processes.

## Further Reading

- Git documentation on `git diff`: https://git-scm.com/docs/git-diff
- Pro Git Book, Chapter on Git Tools - Revision Selection: https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection
