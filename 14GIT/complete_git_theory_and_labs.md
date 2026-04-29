# Git: Complete Theory and Labs

## Purpose of This Guide

This guide combines the Git materials into one connected unit. It explains Git from the ground up, then moves into practical labs for local repositories, branches, merge, diff, remotes, fetch, pull, and team-style workflows.

The main goal is not to memorize commands. The goal is to understand what Git is tracking, where changes are located, and how code moves between a working folder, the staging area, the local repository, and a remote repository.

---

# 1. The Big Picture: What Git Is For

Git is a version control system. It helps answer questions like:

- What changed?
- Who changed it?
- When did it change?
- Why did it change?
- Can we go back to an earlier version?
- Can multiple people work on the same project without destroying each other's work?

A project without Git is just a folder full of files. A project with Git is a folder whose history is being recorded.

Think of Git like a lab notebook for code. The working directory is where experiments happen. A commit is a saved checkpoint. A branch is a separate line of development. A remote repository is a shared copy of the project stored somewhere else, such as GitHub, GitLab, Bitbucket, or a private server.

---

# 2. The Four Main Git Locations

A useful mental model is this sequence:

```text
1) Working directory
   ↓ git add
2) Staging area / Git index
   ↓ git commit
3) Local Git repository
   ↓ git push / git fetch / git pull
4) Remote Git repository
```

## 2.1 Working Directory

The working directory is the regular project folder you see and edit.

Example:

```bash
SampleProject/
├── file1.txt
├── main.py
└── README.md
```

When you edit a file, create a file, or delete a file, the change first exists only in the working directory.

## 2.2 Staging Area / Index

The staging area is Git's preparation table. It lets you choose exactly what will go into the next commit.

Command:

```bash
git add file1.txt
```

or:

```bash
git add .
```

`git add file1.txt` stages one file.

`git add .` stages changes under the current directory.

The staging area is useful because not every change in your folder must be committed at once. You may edit three files but only commit one logical part of the work.

## 2.3 Local Repository

The local repository is the hidden Git database inside the `.git/` folder. It stores commits, branches, object data, and repository metadata.

Command:

```bash
git commit -m "Describe the change"
```

A commit is a saved snapshot plus metadata.

## 2.4 Remote Repository

A remote repository is another copy of the repository, usually hosted online or on another machine.

Commands:

```bash
git push
git fetch
git pull
```

- `git push` sends local commits to a remote repository.
- `git fetch` downloads remote information without changing your current working branch.
- `git pull` downloads remote information and integrates it into your current branch.

---

# 3. First-Time Git Configuration

Before making commits, configure your name and email. Git records this information in commit metadata.

```bash
git config --global user.name "Learner"
git config --global user.email "email@example.com"
```

Check your configuration:

```bash
git config --global --list
```

Typical output:

```text
user.name=Learner
user.email=email@example.com
```

The `--global` flag means this configuration applies to your user account on this machine. You can also set repository-specific configuration without `--global` when needed.

---

# 4. Lab 1: Create a New Git Project

## Goal

Create a new project, initialize Git, stage a file, and make the first commit.

## Step 1: Create the Project Folder

```bash
mkdir SampleProject
cd SampleProject
```

## Step 2: Create a File

```bash
touch file1.txt
```

Add some content:

```bash
echo "Hello" > file1.txt
```

Check the file:

```bash
cat file1.txt
```

Expected output:

```text
Hello
```

## Step 3: Initialize Git

```bash
git init
```

This creates a hidden `.git/` directory. That directory is where Git stores the repository data.

Check hidden files:

```bash
ls -a
```

You should see:

```text
.  ..  .git  file1.txt
```

## Step 4: Check Status

```bash
git status
```

At this point, `file1.txt` is usually shown as **untracked**.

Untracked means: Git sees the file, but the file is not yet part of the repository history.

## Step 5: Stage the File

```bash
git add file1.txt
```

Check status again:

```bash
git status
```

Now the file is staged. It is ready to be committed.

## Step 6: Commit the File

```bash
git commit -m "First commit"
```

A commit saves a snapshot of the staged content.

## Step 7: View the History

```bash
git log
```

A more compact view:

```bash
git log --oneline
```

A useful graph view:

```bash
git log --oneline --graph --decorate --all
```

---

# 5. File States: Untracked, Modified, Staged, Committed

Git is easiest to understand if you can identify the state of each file.

| State | Meaning | Typical Command |
|---|---|---|
| Untracked | Git sees the file, but it is not part of history yet | `git add file` |
| Modified | A tracked file changed in the working directory | `git add file` |
| Staged | The change is prepared for the next commit | `git commit` |
| Committed | The change is saved in repository history | `git log` |

## Small Experiment

Start with the committed `file1.txt`.

```bash
echo "Hello again" >> file1.txt
git status
```

The file should be modified.

Now stage it:

```bash
git add file1.txt
git status
```

Now commit it:

```bash
git commit -m "Add second greeting"
git status
```

Now the working tree should be clean.

---

# 6. The `.gitignore` File

Some files should not be committed. Examples:

- passwords
- API keys
- `.env` files
- compiled binaries
- temporary files
- logs
- editor-specific files

A `.gitignore` file tells Git which files or patterns to ignore.

## Lab 2: Create and Use `.gitignore`

Create a private environment file:

```bash
echo "MY_SECRET_NAME=Learner" > .env
```

Check status:

```bash
git status
```

You may see `.env` as untracked. Usually, this should not be committed.

Create `.gitignore`:

```bash
echo ".env" > .gitignore
```

Check status again:

```bash
git status
```

Now `.env` should be hidden from normal Git status output, while `.gitignore` appears as a file that should be committed.

Stage and commit `.gitignore`:

```bash
git add .gitignore
git commit -m "Ignore environment file"
```

## Important Note

`.gitignore` prevents untracked files from being added accidentally. If a file was already committed earlier, adding it to `.gitignore` will not automatically remove it from Git history.

---

# 7. Commit Messages

A commit message should explain the reason for a change, not only describe the mechanical action.

Weak:

```text
Update file
```

Better:

```text
Add greeting example for first Git commit
```

## Short Commit Message

```bash
git commit -m "Add README"
```

## Longer Commit Message

If you run:

```bash
git commit
```

Git opens an editor so you can write a longer message. The usual structure is:

```text
Short summary line

Longer explanation of what changed and why.
Mention important context, limitations, or follow-up work.
```

---

# 8. Git Log and Commit Identifiers

Every commit has an object ID. In most Git repositories, this is a SHA-1 hash. Newer Git versions can also support SHA-256 repositories, but SHA-1 is still the common default.

A commit object includes information such as:

- the saved project tree
- parent commit or commits
- author
- committer
- timestamp
- commit message

The hash identifies the commit object. If the commit data changes, the hash changes.

Useful log commands:

```bash
git log
```

```bash
git log --oneline
```

```bash
git log --oneline --graph --decorate --all
```

```bash
git log --stat
```

```bash
git show HEAD
```

`HEAD` means the commit your current branch currently points to.

---

# 9. Git Does Not Track Empty Folders

Git tracks files, not empty folders.

If you want an otherwise empty folder to appear in the repository, a common convention is to place a small placeholder file inside it:

```bash
mkdir empty_folder
touch empty_folder/.gitkeep
git add empty_folder/.gitkeep
git commit -m "Keep empty folder structure"
```

`.gitkeep` is not a special Git feature. It is just a common naming convention.

---

# 10. The `git diff` Command

`git diff` shows differences. It helps you inspect changes before committing.

## 10.1 Working Directory vs Staging Area

```bash
git diff
```

This shows changes that are not yet staged.

## 10.2 Staging Area vs Last Commit

```bash
git diff --staged
```

Equivalent:

```bash
git diff --cached
```

This shows what will go into the next commit.

## 10.3 Compare Branches

```bash
git diff main..new_feature
```

This compares the tips of two branches.

## 10.4 Compare Commits

```bash
git diff commit1 commit2
```

Example:

```bash
git diff HEAD~1 HEAD
```

This compares the previous commit with the current commit.

## Lab 3: Practice `git diff`

Create a file and stage it:

```bash
echo "Initial content" > example.txt
git add example.txt
```

Now modify the file after staging:

```bash
echo "More changes" >> example.txt
```

Show unstaged changes:

```bash
git diff
```

Now stage the latest version:

```bash
git add example.txt
```

Show staged changes:

```bash
git diff --staged
```

Commit:

```bash
git commit -m "Add example diff file"
```

Make another change:

```bash
echo "Additional post-commit changes" >> example.txt
```

Review before committing:

```bash
git diff
```

The habit is simple: inspect before you save the checkpoint.

---

# 11. Branches

A branch is a movable pointer to a commit. Branches let you work on a feature, fix, or experiment without immediately changing the main line of development.

Common branch names:

- `main`
- `development`
- `feature/login`
- `feature/button`
- `hotfix/security-patch`

Older repositories may use `master` instead of `main`. In this guide, `main` is used as the default production branch name. If your repository uses `master`, replace `main` with `master` in the commands.

## 11.1 Create and Switch to a Branch

Modern command:

```bash
git switch -c new_feature
```

Older command:

```bash
git checkout -b new_feature
```

Both create a new branch and switch to it.

## 11.2 Switch Between Existing Branches

```bash
git switch main
```

Older command:

```bash
git checkout main
```

## 11.3 Show Branches

```bash
git branch
```

Show local and remote-tracking branches:

```bash
git branch -a
```

---

# 12. Lab 4: Branches and Separate Lines of Work

Make sure you are in `SampleProject`.

Check your branch:

```bash
git branch
```

If your branch is `master`, either use `master` in place of `main`, or rename it:

```bash
git branch -M main
```

## Step 1: Create a Feature Branch

```bash
git switch -c new_feature
```

## Step 2: Create a File on the Feature Branch

```bash
touch new_feature_branch.py
echo "print('Hello from feature branch')" > new_feature_branch.py
```

## Step 3: Stage and Commit

```bash
git add new_feature_branch.py
git commit -m "Add feature branch example"
```

## Step 4: View History

```bash
git log --oneline --graph --decorate --all
```

## Step 5: Switch Back to Main

```bash
git switch main
```

Notice that `new_feature_branch.py` may disappear from the working directory. That is normal. The file exists on the `new_feature` branch, not on `main` yet.

## Step 6: Make a Different Commit on Main

```bash
touch main_branch_file.py
echo "print('Hello from main branch')" > main_branch_file.py
git add main_branch_file.py
git commit -m "Add main branch example"
```

## Step 7: View the Branch Graph

```bash
git log --oneline --graph --decorate --all
```

You should see two lines of work.

---

# 13. Merging Branches

Merging brings changes from one branch into another branch.

The most important rule:

> Git merges into the branch you are currently on.

So if you want to bring `new_feature` into `main`, first switch to `main`.

```bash
git switch main
git merge new_feature
```

After the merge, the commits from `new_feature` become part of `main`.

## Lab 5: Merge a Feature Branch into Main

```bash
git switch main
git merge new_feature
```

Check the result:

```bash
ls
git log --oneline --graph --decorate --all
```

If there are no conflicts, Git completes the merge automatically.

---

# 14. Merge Conflicts

A merge conflict happens when Git cannot safely combine changes automatically.

Example: two branches edit the same line of the same file in different ways.

Git will mark the conflict inside the file like this:

```text
<<<<<<< HEAD
Text from current branch
=======
Text from branch being merged
>>>>>>> new_feature
```

You must manually choose the final version, remove the conflict markers, then stage and commit.

## General Conflict Resolution Steps

```bash
git status
```

Open the conflicted file and fix it.

Then:

```bash
git add conflicted_file.txt
git commit
```

If you want to stop the merge before finishing:

```bash
git merge --abort
```

---

# 15. Structured Git Workflow

Small projects can use only `main` and feature branches. Larger teams often use more structured branch flow.

## 15.1 Main Branch

Purpose: stable production-ready code.

Common practice: only tested and approved code is merged here. Releases are often tagged from this branch.

## 15.2 Development Branch

Purpose: integration branch for ongoing work.

Common practice: feature branches merge into `development`; after enough testing, `development` moves toward staging/release.

## 15.3 Feature Branches

Purpose: isolated work on one feature or task.

Examples:

```text
feature/login
feature/button
feature/report-export
```

Feature branches are usually created from `development` or `main`, depending on the team workflow.

## 15.4 Staging Branch

Purpose: final testing before production.

This branch should resemble what will be released soon.

## 15.5 Deployment Branch

Some workflows use a deployment branch for production-specific deployment configuration. Not every team uses this. Many teams deploy directly from `main`, from a release tag, or from CI/CD configuration.

## 15.6 Hotfix Branches

Purpose: emergency fix for production.

Hotfix branches are usually created from `main`, then merged back into both `main` and `development` so the fix is not lost in future work.

---

# 16. Example: Feature Branch Lifecycle

Scenario: A developer is adding a new feature called `Button`.

## Step 1: Start from the Development Branch

```bash
git switch development
git pull origin development
```

If the branch does not exist locally yet:

```bash
git fetch origin
git switch -c development origin/development
```

## Step 2: Create the Feature Branch

```bash
git switch -c feature/button
```

## Step 3: Work and Commit

```bash
# edit files
git add .
git commit -m "Add initial button functionality"
```

## Step 4: Keep the Feature Branch Updated

```bash
git switch development
git pull origin development
git switch feature/button
git merge development
```

This reduces surprise conflicts later.

Some teams prefer rebasing instead of merging:

```bash
git switch feature/button
git fetch origin
git rebase origin/development
```

Do not rebase shared branches unless your team expects that workflow.

## Step 5: Push the Feature Branch

```bash
git push -u origin feature/button
```

The `-u` sets the upstream branch, so future pushes can be done with:

```bash
git push
```

## Step 6: Open a Pull Request

On GitHub/GitLab/Bitbucket, open a pull request or merge request from:

```text
feature/button → development
```

A pull request is a review space. It lets the team discuss, test, and approve changes before merging.

## Step 7: Merge into Development

Usually this is done through the hosting service after review.

Command-line version:

```bash
git switch development
git merge feature/button
git push origin development
```

## Step 8: Move Toward Staging and Main

```bash
git switch staging
git pull origin staging
git merge development
git push origin staging
```

After staging is approved:

```bash
git switch main
git pull origin main
git merge staging
git push origin main
```

---

# 17. Remotes

A remote is a named connection to another repository.

The most common remote name is `origin`.

Check remotes:

```bash
git remote -v
```

Add a remote:

```bash
git remote add origin https://github.com/your-username/example-repo.git
```

Change a remote URL:

```bash
git remote set-url origin https://github.com/your-username/new-repo.git
```

Remove a remote:

```bash
git remote remove origin
```

---

# 18. Pushing Branches to a Remote

## Create a Branch

```bash
git switch -c new_branch
```

## Do Some Work

```bash
echo "cloned new_branch commit" >> file1.txt
```

## Stage the File

```bash
git add file1.txt
```

## Commit the Change

```bash
git commit -m "Add new branch commit example"
```

## Push the Branch

```bash
git push -u origin new_branch
```

This uploads the branch to the remote repository and sets the upstream relationship.

After that, you can usually use:

```bash
git push
```

while on that branch.

## Note About `git commit -am`

This command:

```bash
git commit -am "Message"
```

stages and commits modifications to already tracked files. It does **not** stage brand-new untracked files. For beginners, `git add` followed by `git commit` is clearer and safer.

---

# 19. Deleting Branches

## Delete a Local Branch Safely

```bash
git branch -d new_feature
```

This works only if the branch has already been merged.

## Force Delete a Local Branch

```bash
git branch -D new_feature
```

Use this carefully. It can delete work that has not been merged.

## Delete a Remote Branch

Recommended modern command:

```bash
git push origin --delete new_branch
```

Older equivalent:

```bash
git push origin :new_branch
```

Before deleting, make sure the branch is no longer needed or the work has been merged.

---

# 20. Fetch vs Pull

`git fetch` and `git pull` both communicate with a remote repository, but they are not the same.

## 20.1 `git fetch`

```bash
git fetch origin
```

Fetch downloads new commits, branches, and tags from the remote. It updates your remote-tracking branches, such as `origin/main`, but it does not change your current working branch.

Good for cautious work:

```bash
git fetch origin
git log --oneline --graph --decorate --all
git diff main..origin/main
```

This lets you inspect before merging.

## 20.2 `git pull`

```bash
git pull origin main
```

Pull is basically:

```bash
git fetch origin
git merge origin/main
```

or, depending on configuration:

```bash
git fetch origin
git rebase origin/main
```

`git pull` is convenient, but it changes your current branch by integrating remote work immediately. That is why `fetch` + inspect + merge is often better for learning and for careful collaboration.

---

# 21. Safe Remote Update Workflow

A cautious workflow looks like this:

```bash
git status
git fetch origin
git log --oneline --graph --decorate --all
git diff HEAD..origin/main
git merge origin/main
```

Meaning:

1. `git status`: check whether your working directory is clean.
2. `git fetch origin`: download remote information.
3. `git log --oneline --graph --decorate --all`: inspect the shape of history.
4. `git diff HEAD..origin/main`: inspect what would come in.
5. `git merge origin/main`: integrate the remote branch.

If you already understand what is happening and want the shorter command:

```bash
git pull origin main
```

---

# 22. Lab 6: Simulate a Remote Without GitHub

This lab works locally and does not require a GitHub account. It uses a bare repository to act like a remote server.

## Step 1: Create a Workspace

Move outside `SampleProject`:

```bash
cd ..
mkdir GitRemoteLab
cd GitRemoteLab
```

## Step 2: Create a Bare Repository

```bash
git init --bare remote-repo.git
```

A bare repository is not a normal working folder. It stores Git history and is suitable as a remote.

## Step 3: Clone It as User 1

```bash
git clone remote-repo.git user1
cd user1
```

Configure main branch if needed:

```bash
git switch -c main
```

Create a file:

```bash
echo "Hello" > file1.txt
git add file1.txt
git commit -m "Initial commit from user1"
git push -u origin main
```

## Step 4: Clone It as User 2

Open another terminal, or from the same terminal:

```bash
cd ..
git clone remote-repo.git user2
cd user2
```

If needed:

```bash
git switch main
```

User 2 now has the same history.

## Step 5: User 1 Makes a New Branch

```bash
cd ../user1
git switch -c feature/message
echo "Hello again" >> file1.txt
git add file1.txt
git commit -m "Add second greeting"
git push -u origin feature/message
```

## Step 6: User 2 Fetches and Reviews

```bash
cd ../user2
git fetch origin
git branch -a
git log --oneline --graph --decorate --all
```

User 2 can inspect the remote feature branch:

```bash
git diff main..origin/feature/message
```

## Step 7: User 2 Merges the Feature Branch

```bash
git merge origin/feature/message
```

Now User 2 has the feature work locally.

---

# 23. Lab 7: GitHub-Style Remote Workflow

This lab assumes you have a GitHub repository named `example-repo`.

## Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/example-repo.git
cd example-repo
```

## Step 2: Create a Feature Branch

```bash
git switch -c feature-branch
```

## Step 3: Make a Change

```bash
echo "Hello, World!" >> hello.txt
git add hello.txt
git commit -m "Add hello.txt with greeting"
```

## Step 4: Push the Branch

```bash
git push -u origin feature-branch
```

## Step 5: Open a Pull Request

Go to the GitHub repository page. GitHub usually detects the new branch and offers to create a pull request.

Open a pull request from:

```text
feature-branch → main
```

or, in a development workflow:

```text
feature-branch → development
```

## Step 6: Simulate Another Clone

```bash
cd ..
git clone https://github.com/your-username/example-repo.git example-repo-2
cd example-repo-2
```

Fetch and inspect:

```bash
git fetch origin
git log --oneline --graph --decorate --all
```

Merge a remote branch if appropriate:

```bash
git merge origin/feature-branch
```

---

# 24. Common Commands Reference

## Setup

```bash
git config --global user.name "Learner"
git config --global user.email "email@example.com"
git config --global --list
```

## Start a Repository

```bash
git init
git status
git add file.txt
git commit -m "Message"
```

## Inspect

```bash
git status
git status -s
git log
git log --oneline --graph --decorate --all
git diff
git diff --staged
git show HEAD
```

## Branch

```bash
git branch
git branch -a
git switch -c feature/name
git switch main
git merge feature/name
```

## Remote

```bash
git remote -v
git remote add origin URL
git push -u origin main
git push -u origin feature/name
git fetch origin
git pull origin main
```

## Delete Branches

```bash
git branch -d branch_name
git branch -D branch_name
git push origin --delete branch_name
```

---

# 25. Common Mistakes and Corrections

## Mistake 1: Using Invalid Alternative Syntax

Incorrect:

```bash
git add . / git add filename
```

Correct alternatives:

```bash
git add .
```

or:

```bash
git add filename
```

## Mistake 2: Forgetting Which Branch Receives the Merge

If you run:

```bash
git merge feature_branch
```

Git merges `feature_branch` into your **current** branch.

Always check:

```bash
git branch
```

## Mistake 3: Expecting `git commit -am` to Add New Files

`git commit -am` only stages modifications to already tracked files. It does not add brand-new files.

Safer beginner pattern:

```bash
git add .
git commit -m "Message"
```

## Mistake 4: Confusing `fetch` and `pull`

- `fetch`: downloads remote information but does not change your current branch.
- `pull`: downloads and integrates remote changes into your current branch.

For careful work:

```bash
git fetch origin
git log --oneline --graph --decorate --all
git merge origin/main
```

## Mistake 5: Assuming Git Tracks Empty Folders

Git tracks files. Use a placeholder such as `.gitkeep` if you need to preserve an empty folder structure.

---

# 26. Full Practice Sequence

This section gives one continuous practice path.

```bash
# 1. Create project
mkdir GitPracticeFull
cd GitPracticeFull

# 2. Initialize Git
git init
git branch -M main

# 3. Add first file
echo "Hello" > file1.txt
git status
git add file1.txt
git commit -m "Add first file"

# 4. Add another line
echo "Hello again" >> file1.txt
git diff
git add file1.txt
git diff --staged
git commit -m "Add second greeting"

# 5. Ignore .env
echo "SECRET=123" > .env
echo ".env" > .gitignore
git add .gitignore
git commit -m "Ignore env file"

# 6. Create feature branch
git switch -c feature/add-message
echo "some more changes" >> file1.txt
git add file1.txt
git commit -m "Add feature message"

# 7. Return to main and make separate change
git switch main
echo "Main branch note" > main_note.txt
git add main_note.txt
git commit -m "Add main branch note"

# 8. Inspect graph
git log --oneline --graph --decorate --all

# 9. Merge feature into main
git merge feature/add-message

# 10. Inspect final history
git log --oneline --graph --decorate --all
```

---

# 27. Student Deliverables

For a lab submission, provide evidence that the commands worked. A good submission should show:

1. The final project folder exists and contains the expected files.
2. `git status` shows a clean working tree after commits.
3. `git log --oneline --graph --decorate --all` shows the branch and merge history.
4. `.gitignore` exists and prevents `.env` from being tracked.
5. A feature branch was created, committed, and merged.
6. If a remote was used, `git remote -v` and `git branch -a` show the remote connection and remote-tracking branches.
7. For fetch/pull practice, show that remote changes were fetched, reviewed, and merged or pulled.

The exact number of screenshots is not important. The important part is that the evidence clearly demonstrates the work.

---

# 28. Final Mental Model

Git becomes much easier when you keep asking: where is the change right now?

```text
Edited but not staged?       Working directory
Prepared for commit?         Staging area / index
Saved as history?            Local repository
Shared with others?          Remote repository
```

Branches answer a different question:

```text
Which line of work am I on?
```

Remotes answer another:

```text
What work exists somewhere else?
```

Fetch and pull answer:

```text
Do I want to inspect remote work first, or integrate it immediately?
```

The safe habit is:

```bash
git status
git diff
git add
git diff --staged
git commit
git log --oneline --graph --decorate --all
```

That loop is the center of Git practice.
