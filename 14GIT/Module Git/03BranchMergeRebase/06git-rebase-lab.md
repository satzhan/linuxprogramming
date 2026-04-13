# Git Rebase Lab Exercise

## Objective
In this lab, you'll create a Git repository, simulate parallel development on different branches, and then use the rebase command to integrate changes. This will help you understand how rebasing works and its effects on commit history.

## Prerequisites
- Git installed on your system
- Basic familiarity with Git commands

## Steps

### 1. Set up the repository

```bash
# Create a new directory and initialize a Git repository
mkdir rebase-lab
cd rebase-lab
git init

# Create an initial file and commit it
echo "Initial content" > file.txt
git add file.txt
git commit -m "Initial commit"
```

### 2. Create and switch to a feature branch

```bash
git checkout -b feature
```

### 3. Make changes in the feature branch

```bash
echo "Feature change 1" >> file.txt
git commit -am "Feature commit 1"
echo "Feature change 2" >> file.txt
git commit -am "Feature commit 2"
```

### 4. Switch back to main and make different changes

```bash
git checkout main
echo "Main change 1" >> file.txt
git commit -am "Main commit 1"
echo "Main change 2" >> file.txt
git commit -am "Main commit 2"
```

### 5. View the commit history

```bash
git log --oneline --graph --all
```

Note the diverging history between main and feature branches.

### 6. Perform the rebase

```bash
git checkout feature
git rebase main
```

### 7. Resolve any conflicts if they occur

If conflicts occur, Git will pause the rebase. Edit the conflicting files, then:

```bash
git add <conflicting-file>
git rebase --continue
```

Repeat this process until the rebase is complete.

### 8. View the updated commit history

```bash
git log --oneline --graph --all
```

Observe how the feature branch commits now appear after the main branch commits.

### 9. Examine the changes in the files

```bash
cat file.txt
```

Verify that all changes from both branches are present.

## Conclusion

You've successfully performed a rebase operation. Notice how the commit history has changed:
- The feature branch commits are now based on the latest main commit.
- The commit hashes for the feature branch have changed.
- The linear history makes it appear as if the feature work was done after the main branch changes.

## Additional Exercises

1. Try creating a more complex branching structure and practice rebasing.
2. Experiment with interactive rebasing using `git rebase -i`.
3. Simulate a scenario where rebasing causes issues for collaborators, and discuss how to avoid or mitigate these problems.

## Important Notes

- Rebasing rewrites commit history. This can cause issues if the branch has been shared with others.
- Always communicate with your team before rebasing shared branches.
- Consider using merge instead of rebase for public branches.
- After rebasing, force-pushing (`git push --force`) may be necessary if the branch was previously pushed to a remote repository. Use this with caution.
