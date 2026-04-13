Project initialization

1) Create a folder for the project and name it SampleProject.

```
$ mkdir SampleProject
```


2) Create some files inside the project folder.

```
$ cd SampleProject
$ touch file1.txt
```


3) Run the git init command, which initializes the current folder as a Git-controlled repository.

```
$ git init
```

4) Run the git add . command to mark the files to be version controlled. The names of the files to be added to the Git repository come after the git add command. The . means adding all files in the current directory.

```
$ git add . / git add filename
```

5) Run git status to preview the commit.
```
$ git status
```

6) Run the following git commit command to commit the marked files into the repository. This step saves the changes as a snapshot.

```
$ git commit -m "First commit."
```


7) .gitignore

a) create .env
b) write your name
c) create .gitignore at a root folder of your project
d) add a line .env

8) git commit -> allows to write a longer comments

9) git status
shows unstaged files (red)
stagged files (gree)
already commited files are snapshots and are hidden from git status command
git status --short or -s for less output

10) git log
Options: git log --oneline --graph --decorate --color --all


