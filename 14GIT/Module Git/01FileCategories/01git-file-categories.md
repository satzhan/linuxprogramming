# Git File Categories and Commands

## File Categories

Git categorizes files into three main types:

1. **Tracked Files**: Files that are part of your project and are managed by Git.
2. **Ignored Files**: Files explicitly told to be ignored by Git.
3. **Untracked Files**: Files in your working directory that are neither tracked nor ignored.

## Tracked Files

Tracked files are the core of your project. They can be in different states:
- Already committed to the repository
- Staged for commit
- Changed but not yet staged

## Ignored Files

Ignored files are specified in the `.gitignore` file. This file can be present in any directory and affects all subdirectories.

Example `.gitignore` rules:

```
*.o       # Ignore all files with .o extension
!important.o  # Don't ignore important.o
```

## Untracked Files

These are all other files in your working directory that are neither tracked nor ignored.

## Important Commands

1. Adding files to `.gitignore`:
   ```
   echo "*.o" >> .gitignore
   ```

2. Forcing addition of an ignored file:
   ```
   git add -f important.pdf
   ```

3. Checking the status of your files:
   ```
   git status
   ```

## Common Pitfalls

- Be cautious with broad ignore rules that might accidentally ignore files you want to track.
- Remember to use the `-f` option when adding a file that matches an ignore pattern but should be tracked.

