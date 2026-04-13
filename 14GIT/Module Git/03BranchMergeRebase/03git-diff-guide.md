# Git Diff Command Guide

Git provides powerful differencing capabilities through its `git diff` command. This guide explains various ways to use `git diff` to compare different versions of your project.

## Basic Usage

### Compare Working Directory to Last Commit

To see changes in your working directory that are not yet staged:

```
$ git diff
```

This shows differences between the current working version of your project and the last commit.

### Compare Working Directory to a Specific Commit

To compare your current working version with an earlier commit:

```
$ git diff earlier_commit
```

Replace `earlier_commit` with a commit hash or branch name.

### Compare Staged Changes to Last Commit

To see differences between staged changes and the last commit:

```
$ git diff --cached
```

or, in Git versions 1.6.1 and later:

```
$ git diff --staged
```

If you don't specify a commit, it defaults to `HEAD`.

### Compare Two Commits

To see differences between any two commits:

```
$ git diff one_commit another_commit
```

Replace `one_commit` and `another_commit` with commit hashes or branch names.

## Advanced Usage

### Ignore Whitespace

To ignore whitespace differences:

```
$ git diff --ignore-all-space
```

### Generate Statistics

For brief statistics instead of detailed differences:

```
$ git diff --stat
```

or

```
$ git diff --numstat
```

### Limit Diff to Specific Directory

To show differences only in a specific directory:

```
$ git diff v4.2.1 v4.2.2 path/to/directory
```

### Show Statistics for a Specific Directory

To show brief statistics for changes in a specific directory:

```
$ git diff --stat v4.2.1 v4.2.2 path/to/directory
```

## Best Practices

1. Use `git diff` before committing to review your changes.
2. Utilize `git diff --cached` to double-check your staged changes before committing.
3. When comparing branches or commits, use meaningful references (tags, branch names) instead of raw commit hashes for better readability.
4. Use the `--stat` option for a quick overview of changes across many files.
5. Combine options like `--ignore-all-space` with directory-specific diffs for focused code reviews.

Remember, `git diff` is a powerful tool for understanding changes in your Git repository. It's essential for code reviews, tracking project evolution, and maintaining a clear history of your project's development.
