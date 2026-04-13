# Comprehensive Git Command Guide

## Table of Contents
1. [Reverting Commits](#reverting-commits)
2. [Resetting Commits](#resetting-commits)
3. [Tidying Repositories](#tidying-repositories)
4. [Who Is to Blame?](#who-is-to-blame)
5. [Bisecting to Find Bugs](#bisecting-to-find-bugs)

## Reverting Commits

The `git revert` command is used to undo changes introduced by a specific commit by creating a new commit that reverses those changes.

### Syntax:
```
git revert <commit_name>
```

### Examples:
```
git revert HEAD      # Revert the most recent commit
git revert HEAD~     # Revert the previous commit
git revert HEAD~2    # Revert the commit two steps back
git revert <hash>    # Revert a specific commit using its hash
git revert <tag>     # Revert a commit referenced by a tag
```

### Effects of `git revert`:
- Creates a new commit that undoes the changes
- Updates the working directory
- Doesn't remove any commits from history

## Resetting Commits

The `git reset` command is used to move the current branch to a different commit, optionally modifying the working directory and index.

### Basic Syntax:
```
git reset <commit>
```

### Example:
```
git reset HEAD~2     # Move the current branch back two commits
```

### Reset Options:
- `--soft`: Moves the branch pointer but doesn't change the index or working directory
- `--mixed` (default): Updates the index but not the working directory
- `--hard`: Updates both the index and working directory

### Examples with Options:
```
git reset --soft HEAD~1   # Move branch back one commit, keep changes staged
git reset --mixed HEAD~1  # Move branch back one commit, unstage changes
git reset --hard HEAD~1   # Move branch back one commit, discard all changes
```

### Use Case: Creating a Work Branch
To move speculative work to a new branch while resetting the main branch:

```
git branch work           # Create a new branch named 'work'
git reset --hard HEAD~3   # Move the current branch back three commits
git checkout work         # Switch to the new 'work' branch
```

## Tidying Repositories

As your project grows, you may need to optimize and compact your repository. Git provides several commands for maintenance and error checking.

### Git Garbage Collection

The `git gc` command optimizes your repository by removing unnecessary files and compressing objects.

#### Syntax:
```
git gc
```

#### Example:
```
# Check repository size before gc
$ du -shc .git
47M     .git
47M     total

# Run garbage collection
$ git gc
Counting objects: 8, done.
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), done.
Total 8 (delta 2), reused 0 (delta 0)

# Check repository size after gc
$ du -shc .git
29M     .git
29M     total
```

### Checking Repository Integrity

The `git fsck` command checks the integrity of your repository and can find certain types of errors.

#### Syntax:
```
git fsck
```

### Pruning Unnecessary Objects

The `git prune` command removes unnecessary objects that are not reachable from any branch, tag, or other reference.

#### Syntax:
```
git prune [-n]
```

#### Examples:
```
# Dry run to see what would be pruned
$ git prune -n

# Actually prune unnecessary objects
$ git prune
```

Note: It's generally safe to use `git prune`, but it's a good practice to run it with the `-n` option first to see what would be removed.

## Who Is to Blame?

The `git blame` command is used to show who last modified each line of a file, when the modification was made, and the commit hash for that change.

### Basic Syntax:
```
git blame <file>
```

### Example:
```
$ git blame file2

f60c0c21 (A Smart Guy 2009-12-31 13:50:15 -0600 1) file2
4b4bf2c5 (A Smart Guy 2009-12-31 13:50:15 -0600 2) another line for file2
```

### Advanced Usage:
You can specify a range of lines and other parameters for more targeted blame information.

#### Syntax for line range:
```
git blame -L <start>,<end> <file>
```

#### Example with line range:
```
$ git blame -L 3107,3121 kernel/sched/core.c

e220d2dc kernel/sched.c      (Peter Zijlstra      2009-05-23 18:28:55 +0200 3107)
e418e1c2 kernel/sched.c      (Christoph Lameter   2006-12-10 02:20:23 -0800 3108) #ifdef CONFIG_SMP
6eb57e0d kernel/sched.c      (Suresh Siddha       2011-10-03 15:09:01 -0700 3109)       rq->idle_balance = idle_cpu(cpu);
7caff66f kernel/sched/core.c (Daniel Lezcano      2014-01-06 12:34:38 +0100 3110)       trigger_load_balance(rq);
e418e1c2 kernel/sched.c      (Christoph Lameter   2006-12-10 02:20:23 -0800 3111) #endif
265f22a9 kernel/sched/core.c (Frederic Weisbecker 2013-05-03 03:39:05 +0200 3112)       rq_last_tick_reset(rq);
^1da177e kernel/sched.c      (Linus Torvalds      2005-04-16 15:20:36 -0700 3113) }
^1da177e kernel/sched.c      (Linus Torvalds      2005-04-16 15:20:36 -0700 3114)
265f22a9 kernel/sched/core.c (Frederic Weisbecker 2013-05-03 03:39:05 +0200 3115) #ifdef CONFIG_NO_HZ_FULL
265f22a9 kernel/sched/core.c (Frederic Weisbecker 2013-05-03 03:39:05 +0200 3116) /**
265f22a9 kernel/sched/core.c (Frederic Weisbecker 2013-05-03 03:39:05 +0200 3117)  * scheduler_tick_max_deferment
265f22a9 kernel/sched/core.c (Frederic Weisbecker 2013-05-03 03:39:05 +0200 3118)  *
265f22a9 kernel/sched/core.c (Frederic Weisbecker 2013-05-03 03:39:05 +0200 3119)  * Keep at least one tick per second when
265f22a9 kernel/sched/core.c (Frederic Weisbecker 2013-05-03 03:39:05 +0200 3120)  * active task is running because the sch
265f22a9 kernel/sched/core.c (Frederic Weisbecker 2013-05-03 03:39:05 +0200 3121)  * yet completely support full dynticks
```

## Bisecting to Find Bugs

Git's bisect feature is a powerful tool for finding the commit that introduced a bug. It uses a binary search algorithm to efficiently locate the problematic commit, even in large repositories with many commits.

### Basic Bisect Process

1. Start the bisect process:
   ```
   $ git bisect start
   ```

2. Mark the current commit as bad:
   ```
   $ git bisect bad
   ```

3. Mark a known good commit:
   ```
   $ git bisect good V_10
   ```

4. Git will checkout a commit halfway between the good and bad commits. Test your code and mark it as good or bad:
   ```
   $ git bisect good
   ```
   or
   ```
   $ git bisect bad
   ```

5. Repeat step 4 until Git identifies the first bad commit.

6. After finding the bug, reset to your original state:
   ```
   $ git bisect reset
   ```

### Example Bisect Process

```
$ git bisect start
$ git bisect bad
$ git bisect good V_10
Bisecting: 4136 revisions left to test after this
[b9caaabb995c6ff103e2457b9a36930b9699de7c] Merge branch 'master' of git://git.kernel.org/pub/scm/linux/kernel/git/holtmann/bluetooth-next-2.6

$ git bisect good
Bisecting: 60 revisions left to test after this
[5d48a1c20268871395299672dce5c1989c9c94e4] Staging: hv: check return value of device_register()

$ git bisect bad
Bisecting: 3 revisions left to test after this
[b57a68dcd9030515763133f79c5a4a7c572e45d6] Staging: hv: blkvsc: fix up driver_data usage

$ git bisect good
Bisecting: 1 revisions left to test after this
[511bda8fe1607ab2e4b2f3b008b7cfbffc2720b1] Staging: hv: add the Hyper-V virtual network driver

$ git bisect good
Bisecting: 0 revisions left to test after this
[621d7fb7597e8cc2e24e6b0ca67118b452675d90] Staging: hv: netvsc: fix up driver_data usage

$ git bisect reset
```

### Automated Bisecting

If you have a script that can automatically test for the presence of the bug, you can automate the bisect process:

1. Create a script (e.g., `my_script.sh`) that returns 0 for a good version and 1-127 for a bad version.

2. Run the automated bisect:
   ```
   $ git bisect run ./my_script.sh
   ```

### Bisect Visualization

You can review the bisection history using:
```
$ git bisect log
```
or
```
$ git bisect visualize
```

### Best Practices

- Make small, incremental commits to make bisecting more effective.
- Large commits with many changes can make it harder to pinpoint the exact cause of a bug.
- Automated testing scripts can greatly speed up the bisecting process.

The bisect feature is particularly useful for large projects where manually checking each commit would be time-consuming. It can significantly reduce debugging time by narrowing down the search space for the bug-introducing commit.
