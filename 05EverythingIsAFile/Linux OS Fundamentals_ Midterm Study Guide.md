Linux OS Fundamentals: Midterm Study Guide

1. The Core Philosophy: "Everything is a File"

In Linux, the "Everything is a File" philosophy is the architectural cornerstone. It means that nearly all system components—from hardware devices and system memory to network connections—are represented as files within the filesystem.

Admin Insight: This uniformity is powerful because it allows a system administrator to use the same basic tools (like cat, grep, or redirects) to interact with diverse hardware. For example, you can use cat to read from a physical disk device file just as easily as you would a standard text file.

System Components Represented as Files:

* Regular files: Standard data files (text, binaries, images).
* Directories: Special files that serve as containers for other files.
* Sockets: Files that facilitate network-based inter-process communication (IPC).
* Pipes and FIFOs: Files used for IPC that allow data to flow in one direction (unidirectional).
* Devices: Hardware represented as files. Character devices handle data character-by-character (like a keyboard), while Block devices handle data in large chunks (like a hard drive).

Kernel and Device Interfaces The filesystem provides specific directories to serve as portals to the system hardware and the kernel itself.

Location	Purpose
/dev	Contains character and block device files representing physical hardware.
/proc	A virtual filesystem providing an interface to kernel data structures and process information.


--------------------------------------------------------------------------------


2. File Metadata and Access: Inodes vs. File Descriptors

Linux distinguishes between how a file is stored on disk and how it is accessed by an active process.

Admin Tip: To see the "truth" of a file, use the stat command. It displays detailed metadata including permissions, size, timestamps, and the Inode number. To see Inode numbers in a directory listing, use ls -i.

Internal Mechanics: Inodes vs. File Descriptors

Feature	Inode Number	File Descriptor
Primary Purpose	A data structure identifying files/directories at the filesystem level.	An abstract indicator (integer) used by the kernel to track a process's access to a file.
Scope/Uniqueness	Unique within the specific filesystem.	Unique only within a single process.
Persistence	Persists across reboots until the file is deleted.	Volatile; it ceases to exist once the process terminates.
Associated System Calls	Managed by the filesystem; viewed via stat.	Heavily used by read() and write() calls during execution.

Inode Attributes The Inode contains the vital statistics of a file, excluding the filename. Key data includes:

* File attributes (size, type).
* Disk block locations (where the data physically resides on the platter or SSD).
* Access permissions (Read/Write/Execute).
* Timestamps (Access, Modify, Change).


--------------------------------------------------------------------------------


3. Linking Mechanics: Hard Links vs. Soft (Symbolic) Links

Links allow a single file to be accessed from multiple locations or by multiple names.

Key Facts

* Hard Links (ln): These share the exact same Inode number as the source. Because they point to the same data on the disk, the data remains accessible as long as at least one hard link exists.
* Symbolic Links (ln -s): Also called "Soft Links," these function like a shortcut. They point to the path name of the target file, not the Inode.
* The "Dangling Link": If you delete the target file of a symbolic link, the link remains but points to a non-existent path. This is a "broken" or "dangling" link.
* Argument Order: Always remember the syntax is target followed by link_name.

Symbolic Link Syntax

ln -s target_file link_name



--------------------------------------------------------------------------------


4. File Management: Linux CLI vs. Python Programming

Modern systems administration often requires automating shell tasks using Python's os and shutil modules.

Command Mapping: Linux Shell vs. Python

Linux Command	Python Equivalent	Admin Note
ls / ls -l	os.listdir()	Lists directory contents.
pwd	os.getcwd()	"Get current working directory."
cd	os.chdir(path)	Changes the process's current directory.
mv	os.rename()	Used for both moving and renaming.
cp / cp -r	shutil.copy()	Use shutil for file-level copying.
rm	os.remove()	Deletes a single file.
rm -r	shutil.rmtree()	Warning: Recursively deletes a non-empty directory.
mkdir	os.mkdir()	Creates a single directory.
mkdir -p	os.makedirs()	Creates the full path, including missing parent directories.
chmod	os.chmod()	Changes permissions.
cat	print(open('f', 'r').read())	Opens, reads, and prints file contents.
touch	open('f', 'a').close()	Opens in append mode and closes to update timestamp/create file.

Gotcha: Directory Removal If you attempt to use os.remove() or os.rmdir() on a directory that contains files, Python will raise an error. You must use shutil.rmtree() to perform a recursive deletion, which is the equivalent of rm -r.


--------------------------------------------------------------------------------


5. Permissions, Ownership, and User Management

Linux uses a strict security model based on User (u), Group (g), and Others (o).

Permission Strings (e.g., -rwxr-xr--)

1. Leading Character: - (file), d (directory), l (link).
2. Next 9 Characters: Three triads representing u, g, and o.

Octal (Numerical) Notation Permissions are calculated as: Read=4, Write=2, Execute=1.

* 755: rwxr-xr-x (Owner: All; Group/Others: Read and Execute). Admin Tip: 755 is the standard for directories and executable scripts.
* 644: rw-r--r-- (Owner: Read/Write; Group/Others: Read only).
* rw-: Octal value 6.

Permissions on Directories

* Read (r): Allows you to list the files inside (via ls).
* Write (w): Allows you to create or delete files within that directory.
* Execute (x): The "pass-through" permission. It allows you to enter the directory (cd) and access its contents.

Management Commands

* useradd / usermod: Create or modify user accounts.
* passwd: Update a user's password.
* chown: Changes file ownership. Format: chown user:group filename.
* chgrp: Changes only the group ownership.
* sudo: Temporarily grants "root" (superuser) privileges to execute administrative tasks.


--------------------------------------------------------------------------------


6. I/O Redirection and the Pipeline

Data flow is managed via Standard File Descriptors:

* 0 (stdin): Standard Input (Keyboard).
* 1 (stdout): Standard Output (Screen).
* 2 (stderr): Standard Error (Error messages on screen).

Quick Reference: Redirection Operators

* >: Overwrites a file with output (creates the file if it doesn't exist).
* >>: Appends output to the end of a file.
* <: Redirects a file's content into a command as input.
* 2>: Redirects error messages to a file (crucial for logging).
* |: Piping. Connects the stdout of one command to the stdin of another. Pipes use half-duplex communication, meaning data flows in one direction only.

Chained Command Example

cat logs.txt | grep "ERROR" | wc -l


This reads the file, filters for "ERROR", and then counts the resulting lines.


--------------------------------------------------------------------------------


7. Essential Text Processing Utilities

* grep: Pattern searching. Use -i for case-insensitive searches.
* wc: Word count. Use -l for lines, -w for words, and -c for bytes/characters.
* sort: Alphabetical sorting. Use -n for numeric sorting.
* uniq: Removes adjacent duplicates. Admin Tip: Always sort your data before running uniq.
* head / tail: View the start or end of a file. Default is 10 lines. Change this with -n (e.g., tail -n 5 for the last 5 lines).
* ls -a: Lists all files, including hidden ones (those starting with a dot).
* tree -L [number]: Visualizes directory structure, limited to a specific depth of levels.


--------------------------------------------------------------------------------


8. Midterm Review: High-Probability Questions

1. What is the correct order of arguments for the ln -s command? Answer: target_file link_name
2. Which Python function should be used to create a directory path including all necessary parent directories? Answer: os.makedirs()
3. In Python, which mode is used with open() to append data to a file? Answer: 'a'
4. How do file descriptors and Inodes differ in persistence? Answer: Inodes persist across reboots; file descriptors cease to exist when a process terminates.
5. What command is used to locate the full path of an executable command? Answer: which
6. What does the PATH environment variable contain? Answer: A list of directories the shell searches for executable commands.
7. What happens if you use os.remove() on a directory that is not empty? Answer: It will raise an error; shutil.rmtree() must be used for recursive deletion.
8. Which directory contains interfaces to kernel data structures? Answer: /proc
