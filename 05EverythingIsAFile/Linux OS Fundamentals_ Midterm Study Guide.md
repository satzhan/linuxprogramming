# Linux Programming Midterm Study Guide

## 1. Navigation and File Management
* **Current Location:** * Use `pwd` to print the current working directory.
* **Changing Directories:** * `cd` changes directories.
    * `cd ..` moves up one directory level.
    * `cd ~` changes to your home directory.
* **Listing Contents:** * `ls -a` shows hidden files.
    * `ls -i` displays inode numbers.
    * `tree -L` visualizes the directory structure but limits the display to a specific depth.
* **Searching:** * `find` is used to search for files and directories.
    * `which` shows the full path of shell commands.
* **File Manipulation:** * `touch` creates a file if it doesn't exist, or updates its timestamp if it does.
    * `mkdir -p` creates a directory path, including any missing parent directories.
    * `rmdir` removes an empty directory.
    * `cp` copies files.
    * `cp -r` copies directories recursively.
    * `rm` removes files.
    * `rm -r` recursively deletes a directory and its contents.
    * `stat` displays detailed file information like permissions, size, timestamps, and inodes.
* **Shell Globbing:** * `*` matches any string of characters.
    * `?` matches exactly one character.
* **Environment:** * The `$PATH` variable contains a list of directories searched for executable commands.
    * You can view it with `echo $PATH`.

## 2. Text Processing, Pipes, and Redirection
* **Text Commands:** * `cat` displays file contents.
    * `cat -n` displays them with line numbers.
    * `less` is used to view a long text file one screen at a time.
    * `wc` counts lines, words, characters, or bytes.
    * `wc -l` counts only lines.
    * `sort` sorts lines of text.
    * `sort -n` is used for numeric sorting.
    * `grep` searches for patterns.
    * `grep -i` makes the search case-insensitive.
    * `head` shows the top 10 lines by default.
    * `head -n 20` shows the first 20.
    * `tail` displays the end of a file.
    * `tail -n 20` displays the last 20 lines.
    * `uniq` removes adjacent duplicate lines.
* **Pipes (`|`):** * A pipe (`|`) allows the output of one process to become the input of another.
    * This is a form of Inter-Process Communication (IPC) that creates a half-duplex communication channel.
    * You can chain multiple commands together.
* **Redirection:** * Standard input (stdin) is `0`.
    * Standard output (stdout) is `1`.
    * Standard error (stderr) is `2`.
    * `>` overwrites or creates a file with the output.
    * `>>` appends output to an existing file.
    * `<` reads input from a file.
    * `2>` redirects standard error (stderr) to a file.

## 3. Users, Groups, and Permissions
* **User Management:** * The Superuser (root) has the highest level of permissions.
    * `sudo` temporarily grants administrative privileges to a regular user.
    * `useradd` adds a new user account.
    * `usermod` modifies it.
    * `passwd` changes the password.
    * `whoami` prints the current user's username.
    * `id` displays UID/GID and group memberships.
    * `groups` shows the groups the current user belongs to.
    * `last` shows the last logins in the system.
    * `/etc/passwd` contains user accounts and info.
    * `/etc/group` contains group definitions and GIDs.
* **Permissions:** * `r` (read) allows reading file contents.
    * `w` (write) allows creating or deleting files inside a directory.
    * `x` (execute) allows entering a directory.
    * Octal `755` represents `rwxr-xr-x`.
    * `rw-` represents `6`.
* **Changing Ownership & Permissions:** * `chmod` modifies permissions.
    * `chown` changes the owner of files/directories.
    * `chgrp` changes the group.

## 4. "Everything is a File", Inodes, and Links
* **"Everything is a File" Concept:** * In Linux, all system components are represented as files, which simplifies interaction with system components using standard tools.
    * Programs themselves are not considered a file type under this specific concept.
    * `/dev` contains character and block device files.
    * Character devices handle data character by character.
    * `/proc` provides interfaces to kernel data structures.
    * Sockets facilitate network communication between processes.
    * Pipes/FIFOs allow data to flow in one direction for IPC.
* **Inodes vs. File Descriptors:** * Inodes are a data structure storing file attributes and disk block locations.
    * They are unique within the filesystem and persist until the file is deleted.
    * File descriptors are an abstract indicator for kernel file access.
    * They are unique only within a single process and cease to exist when the process terminates.
    * System calls like `read()` and `write()` use file descriptors.
* **Links:** * Symbolic Links (`ln -s`) create a "soft" link pointing to a path name.
    * If the target is deleted, the link becomes broken (dangling).
    * Hard Links (`ln`) share the same inode as the original file.

## 5. Python Equivalents of Linux Commands
* `ls` -> `os.listdir()`.
* `pwd` -> `os.getcwd()`.
* `cd path` -> `os.chdir(path)`.
* `mkdir` -> `os.mkdir()`.
* `mv` -> `os.rename()`.
* `rm` -> `os.remove()`.
* `rm -r` -> `shutil.rmtree()`.
* `cp` -> `shutil.copy()`.
* `chmod` -> `os.chmod()`.
* `touch file.txt` -> `open('file.txt', 'a').close()`.
