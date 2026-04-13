# Git Bisect Lab Exercise

## Objective
Learn how to use git bisect to efficiently find a commit that introduced a bug in a repository with many commits.

## Exercise Instructions

1. Initialize a new Git repository:
   ```
   mkdir git-bisect-lab
   cd git-bisect-lab
   git init
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

2. Create a script to generate 64 commits, with one commit introducing a "bug":
   ```bash
   #!/bin/bash
   
   for i in {1..64}
   do
     if [ $i -eq 37 ]; then
       echo "BAD" > file$i.txt
     else
       echo "Content $i" > file$i.txt
     fi
     git add file$i.txt
     git commit -m "Add file $i"
   done
   ```
   Save this script as `generate_commits.sh` and make it executable:
   ```
   chmod +x generate_commits.sh
   ```

3. Run the script to generate the commits:
   ```
   ./generate_commits.sh
   ```

4. Start the git bisect process:
   ```
   git bisect start
   ```

5. Mark the current (last) commit as bad:
   ```
   git bisect bad
   ```

6. Mark the first commit as good:
   ```
   git bisect good HEAD~63
   ```

7. Manual Bisection:
   - Git will checkout a commit halfway between the good and bad commits.
   - Check if the "bug" exists in the current state:
     ```
     grep BAD *.txt
     ```
   - If you find "BAD", mark the commit as bad:
     ```
     git bisect bad
     ```
   - If you don't find "BAD", mark the commit as good:
     ```
     git bisect good
     ```
   - Repeat until Git identifies the first bad commit.

8. Automated Bisection:
   Create a script named `check_bug.sh`:
   ```bash
   #!/bin/bash
   
   if grep -q BAD *.txt; then
     exit 1  # Bug found
   else
     exit 0  # No bug
   fi
   ```
   Make it executable:
   ```
   chmod +x check_bug.sh
   ```
   Run automated bisection:
   ```
   git bisect run ./check_bug.sh
   ```

9. Check the bisection log:
   ```
   git bisect log
   ```

10. Reset the bisection:
    ```
    git bisect reset
    ```

## Solution

Here's what you should expect:

1. The repository will have 64 commits, with the 37th commit introducing the "bug".

2. Manual bisection should take about 6 steps (log2(64) ≈ 6).

3. Automated bisection will quickly find the buggy commit.

4. The bisect log should show something like this:
   ```
   git bisect start
   # bad: [<hash>] Add file 64
   git bisect bad <hash>
   # good: [<hash>] Add file 1
   git bisect good <hash>
   # bad: [<hash>] Add file 37
   git bisect bad <hash>
   # good: [<hash>] Add file 36
   git bisect good <hash>
   # first bad commit: [<hash>] Add file 37
   ```

5. The commit that introduced the "bug" should be the one with the message "Add file 37".

This exercise demonstrates how git bisect can efficiently locate a problematic commit in a large number of commits, both manually and using an automated script.
