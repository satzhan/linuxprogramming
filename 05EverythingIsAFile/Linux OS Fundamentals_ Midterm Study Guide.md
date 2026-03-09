# Linux Programming Midterm Study Guide

## 1. Navigation and File Management
* [cite_start]**Current Location:** Use `pwd` to print the current working directory[cite: 84, 85].
* [cite_start]**Changing Directories:** * `cd` changes directories[cite: 87].
    * [cite_start]`cd ..` moves up one directory level[cite: 88].
    * [cite_start]`cd ~` changes to your home directory[cite: 89, 90].
* **Listing Contents:**
    * [cite_start]`ls -a` shows hidden files[cite: 86].
    * [cite_start]`ls -i` displays inode numbers[cite: 99].
    * [cite_start]`tree -L` visualizes the directory structure but limits the display to a specific depth[cite: 89, 91].
* **Searching:**
    * [cite_start]`find` is used to search for files and directories[cite: 92].
    * [cite_start]`which` shows the full path of shell commands[cite: 93].
* **File Manipulation:**
    * [cite_start]`touch` creates a file if it doesn't exist, or updates its timestamp if it does[cite: 103].
    * [cite_start]`mkdir -p` creates a directory path, including any missing parent directories[cite: 104].
    * [cite_start]`rmdir` removes an empty directory[cite: 105, 106].
    * [cite_start]`cp` copies files [cite: 107][cite_start], while `cp -r` copies directories recursively[cite: 108].
    * [cite_start]`rm` removes files [cite: 109][cite_start], and `rm -r` recursively deletes a directory and its contents[cite: 110].
    * [cite_start]`stat` displays detailed file information like permissions, size, timestamps, and inodes[cite: 100].
* [cite_start]**Shell Globbing:** `*` matches any string of characters [cite: 114][cite_start], while `?` matches exactly one character[cite: 115].
* [cite_start]**Environment:** The `$PATH` variable contains a list of directories searched for executable commands [cite: 116][cite_start]; you can view it with `echo $PATH`[cite: 118].

## 2. Text Processing, Pipes, and Redirection
* **Text Commands:**
    * [cite_start]`cat` displays file contents[cite: 73]; [cite_start]`cat -n` displays them with line numbers[cite: 73].
    * [cite_start]`less` is used to view a long text file one screen at a time[cite: 113].
    * [cite_start]`wc` counts lines, words, characters, or bytes[cite: 75]. [cite_start]`wc -l` counts only lines[cite: 76].
    * [cite_start]`sort` sorts lines of text[cite: 77]. [cite_start]`sort -n` is used for numeric sorting[cite: 78].
    * [cite_start]`grep` searches for patterns[cite: 79]; [cite_start]`grep -i` makes the search case-insensitive[cite: 80].
    * [cite_start]`head` shows the top 10 lines by default[cite: 81]; [cite_start]`head -n 20` shows the first 20[cite: 130].
    * [cite_start]`tail` displays the end of a file[cite: 82]; [cite_start]`tail -n 20` displays the last 20 lines[cite: 83].
    * [cite_start]`uniq` removes adjacent duplicate lines (usually used after sorting)[cite: 129].
* **Pipes (`|`):**
    * [cite_start]A pipe (`|`) allows the output of one process to become the input of another[cite: 61, 63]. 
    * [cite_start]This is a form of Inter-Process Communication (IPC) that creates a half-duplex communication channel[cite: 64, 73]. 
    * [cite_start]You can chain multiple commands together (e.g., `command1 | command2 | command3`)[cite: 133].
* **Redirection:**
    * [cite_start]**File Descriptors:** Standard input (stdin) is `0` [cite: 67][cite_start], standard output (stdout) is `1` [cite: 71][cite_start], and standard error (stderr) is `2`[cite: 71].
    * [cite_start]`>` overwrites or creates a file with the output[cite: 69].
    * [cite_start]`>>` appends output to an existing file[cite: 68].
    * [cite_start]`<` reads input from a file[cite: 70].
    * [cite_start]`2>` redirects standard error (stderr) to a file[cite: 127, 128].

## 3. Users, Groups, and Permissions
* **User Management:**
    * [cite_start]The Superuser (root) has the highest level of permissions[cite: 48]. [cite_start]`sudo` temporarily grants administrative privileges to a regular user[cite: 56].
    * [cite_start]`useradd` adds a new user account [cite: 51][cite_start], `usermod` modifies it [cite: 52][cite_start], and `passwd` changes the password[cite: 53].
    * [cite_start]`whoami` prints the current user's username [cite: 119][cite_start], `id` displays UID/GID and group memberships [cite: 121][cite_start], and `groups` shows the groups the current user belongs to[cite: 120].
    * [cite_start]`last` shows the last logins in the system[cite: 57].
    * [cite_start]`/etc/passwd` contains user accounts and info [cite: 122][cite_start], while `/etc/group` contains group definitions and GIDs[cite: 123].
* **Permissions:**
    * [cite_start]`r` (read): Allows reading file contents[cite: 38, 39]. [cite_start]Octal value: `4`[cite: 44].
    * [cite_start]`w` (write): Allows creating or deleting files inside a directory[cite: 45]. [cite_start]Octal value: `2`[cite: 44].
    * [cite_start]`x` (execute): Allows entering a directory[cite: 40]. [cite_start]Octal value: `1`[cite: 44].
    * [cite_start]*Example:* Octal `755` represents `rwxr-xr-x` [cite: 44][cite_start], and `rw-` represents `6`[cite: 44].
* **Changing Ownership & Permissions:**
    * [cite_start]`chmod` modifies permissions (e.g., `chmod u+x` adds execute permission for the user/owner)[cite: 44].
    * [cite_start]`chown` changes the owner of files/directories[cite: 54].
    * [cite_start]`chgrp` changes the group[cite: 60, 61].

## 4. "Everything is a File", Inodes, and Links
* **"Everything is a File" Concept:**
    * [cite_start]In Linux, all system components are represented as files, which simplifies interaction with system components using standard tools[cite: 24, 30]. [cite_start]Programs themselves are *not* considered a file type under this specific concept[cite: 26].
    * [cite_start]`/dev` contains character and block device files[cite: 27]. [cite_start]Character devices handle data character by character[cite: 33].
    * [cite_start]`/proc` provides interfaces to kernel data structures[cite: 31].
    * [cite_start]Sockets facilitate network communication between processes [cite: 37][cite_start], and Pipes/FIFOs allow data to flow in one direction for IPC[cite: 28].
* **Inodes vs. File Descriptors:**
    * [cite_start]**Inodes:** A data structure storing file attributes and disk block locations[cite: 8, 18]. [cite_start]They are unique within the filesystem [cite: 9] [cite_start]and persist until the file is deleted[cite: 19].
    * [cite_start]**File Descriptors:** An abstract indicator for kernel file access[cite: 10]. [cite_start]They are unique only within a single process [cite: 13] [cite_start]and cease to exist when the process terminates[cite: 14]. [cite_start]System calls like `read()` and `write()` use file descriptors[cite: 15, 16].
* **Links:**
    * [cite_start]**Symbolic Links (`ln -s`):** Creates a "soft" link pointing to a path name[cite: 2]. [cite_start]If the target is deleted, the link becomes broken (dangling)[cite: 101, 102].
    * [cite_start]**Hard Links (`ln`):** Shares the same inode as the original file[cite: 95, 96]. 

## 5. Python Equivalents of Linux Commands
[cite_start]The `os` and `shutil` Python modules provide similar file/directory operations[cite: 22]:
* [cite_start]`ls` -> `os.listdir()` [cite: 22]
* [cite_start]`pwd` -> `os.getcwd()` [cite: 124]
* [cite_start]`cd path` -> `os.chdir(path)` [cite: 125]
* [cite_start]`mkdir` -> `os.mkdir()` [cite: 22]
* [cite_start]`mv` -> `os.rename()` [cite: 21]
* [cite_start]`rm` -> `os.remove()` [cite: 22]
* [cite_start]`rm -r` -> `shutil.rmtree()` (removes non-empty directories) [cite: 23]
* [cite_start]`cp` -> `shutil.copy()` [cite: 126]
* [cite_start]`chmod` -> `os.chmod()` [cite: 23]
* [cite_start]`touch file.txt` -> `open('file.txt', 'a').close()` [cite: 19, 20]
