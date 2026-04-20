# Linux Programming: Complete Theory and Labs

## How to Use This Document

This document combines the main Linux course ideas into one place and fills in a few gaps that often confuse students. It is organized in the same order a beginner usually needs:

1. big picture
2. basic navigation and file work
3. text processing
4. pipes and redirection
5. `cut` and `paste`
6. users, groups, permissions, and `umask`
7. optional extension: sockets and “everything is a file”

Each section has:
- theory
- command examples
- common mistakes
- one or more labs

The goal is not just to memorize commands. The goal is to understand what kind of problem each command solves.

---

# 0. Big Picture: What Linux Is Trying to Teach You

Before learning commands, it helps to understand the layers of a computer system.

## 0.1 A Simple System View

A useful mental model is:

- **Hardware level**: CPU, RAM, storage, devices
- **Operating system level**: kernel, drivers, resource control
- **Program level**: applications, services, scripts, commands
- **User level**: the person asking the system to do work

The **kernel** is the core part of the operating system. It manages access to memory, files, CPU time, devices, and process execution.

The **shell** is the text interface that lets you run programs.

When you type something in the terminal, you are usually asking the shell to start a program.

## 0.2 Linux Commands Are Usually Small Programs

In Linux, many commands are small tools that do one job well.

Examples:
- `ls` lists files
- `pwd` prints your current directory
- `grep` searches text
- `sort` sorts lines
- `wc` counts lines, words, or bytes

This is one of the main Linux ideas:

> Build powerful workflows by combining small tools.

## 0.3 Command Syntax

Most commands follow this pattern:

```bash
command [arguments] [options]
```

Examples:

```bash
ls -l /etc
grep -n "ERROR" application.log
cp file1.txt backup.txt
```

- **command**: the program name
- **arguments**: the thing the program acts on
- **options / flags**: switches that modify behavior, usually beginning with `-`

## 0.4 A Small Analogy

Think of the shell like a workshop manager.

- you give an instruction
- the manager finds the tool
- the tool does one task
- the result comes back to the screen or to a file

That is why Linux feels command-heavy: you are controlling lots of small tools directly.

---

# 1. Filesystem Navigation and Basic File Manipulation

This is the first real survival skill in Linux: knowing where you are, what exists there, and how to move around safely.

## 1.1 Paths: Absolute vs Relative

A **path** tells Linux where something is.

### Absolute path
Starts from root:

```bash
/etc/passwd
/home/student/project
```

### Relative path
Starts from your current location:

```bash
./notes.txt
../project
subdir/file.txt
```

### Important shortcuts

- `/` = root of the filesystem
- `~` = your home directory
- `.` = current directory
- `..` = parent directory

## 1.2 Core Navigation Commands

### `pwd`
Print working directory.

```bash
pwd
```

Shows your current location.

### `ls`
List files and directories.

```bash
ls
ls -l
ls -a
ls -lh
ls -R
```

Useful flags:
- `-l` long format
- `-a` include hidden files
- `-h` human-readable sizes
- `-R` recursive

### `cd`
Change directory.

```bash
cd /etc
cd ~
cd ..
cd -
```

Useful cases:
- `cd` or `cd ~` goes home
- `cd ..` goes up one level
- `cd -` returns to previous directory

### `which`
Find where a command lives.

```bash
which python3
which ls
```

### `man`
Open a command’s manual page.

```bash
man ls
man grep
```

This is how you learn commands independently.

## 1.3 Basic File and Directory Commands

### `mkdir`
Create directories.

```bash
mkdir project
mkdir -p project/src/assets
```

`-p` creates parents if needed.

### `rmdir`
Remove an empty directory.

```bash
rmdir old_empty_dir
```

### `touch`
Create an empty file or update a file timestamp.

```bash
touch notes.txt
```

### `cp`
Copy files or directories.

```bash
cp source.txt backup.txt
cp -r website website_backup
```

### `mv`
Move or rename.

```bash
mv old.txt new.txt
mv file.txt docs/
```

### `rm`
Remove files.

```bash
rm notes.txt
rm -r old_project
```

Be careful:
- `rm` deletes files
- `rm -r` deletes directories recursively
- there is no recycle bin in normal shell usage

## 1.4 Hidden Files

Files that start with a dot are hidden by default.

Examples:
- `.bashrc`
- `.gitignore`
- `.config`

To see them:

```bash
ls -a
```

## 1.5 `tree` and `find`

### `tree`
Shows directory structure visually.

```bash
tree
tree -a
tree -L 2
```

### `find`
Searches for files and directories.

```bash
find . -name "*.txt"
find /etc -name "*.conf"
```

Use `find` when:
- you do not know where a file is
- `tree` is not installed
- you want pattern-based searching

## 1.6 Common Beginner Mistakes

1. Forgetting where you are before creating files
2. Mixing relative and absolute paths
3. Running `rm -r` too casually
4. Forgetting hidden files exist
5. Assuming `tree` is always installed

---

## Lab 1A: Warm-Up Directory Structure

### Objective
Create and verify a small directory structure.

### Steps

```bash
mkdir AssignmentRoot
cd AssignmentRoot
mkdir SubDir1 SubDir2
cd SubDir1
touch file1.txt
cd ../SubDir2
touch file2.txt
cd ..
```

Verify:

```bash
tree .
```

If `tree` is unavailable:

```bash
find .
```

### Deliverable
Show the final structure of `AssignmentRoot`.

---

## Lab 1B: Basic Programming Project Structure

### Objective
Create a small project layout.

### Steps

```bash
mkdir -p MyProject1/{Images,Code,Configs}
touch MyProject1/Images/{logo.png,banner.png}
touch MyProject1/Code/{main.py,utils.py}
touch MyProject1/Configs/settings.conf
```

Verify:

```bash
tree MyProject1
```

### Deliverable
Show the final tree for `MyProject1`.

---

## Lab 1C: Hidden Files and Git-Like Structure

### Objective
Practice hidden files and nested directory creation.

### Steps

```bash
mkdir -p MyProject2/{Images,Code,Configs}
touch MyProject2/Configs/.secret_key
touch MyProject2/{.config,.database_connection}

tree -a MyProject2
```

Now simulate a Git-like folder:

```bash
mkdir -p MyProject3/{Images,Code,Configs,.git/{hooks,info,objects,refs}}
touch MyProject3/.git/{config,HEAD,description}
tree -a MyProject3
```

### Deliverable
Show both project structures with hidden files visible.

---

## Lab 1D: Home Lab — Personal Website Structure

### Objective
Create a clean project layout using relative paths.

### Steps

```bash
mkdir -p ~/my_website/{home,about,portfolio,css,js,images/{home,about,portfolio}}
touch ~/my_website/home/index.html
touch ~/my_website/about/about.html
touch ~/my_website/portfolio/projects.html
touch ~/my_website/css/styles.css
touch ~/my_website/js/script.js
mkdir -p ~/my_website/portfolio/{project1,project2}
touch ~/my_website/portfolio/project1/index.html
touch ~/my_website/portfolio/project2/index.html
touch ~/my_website/portfolio/project{1,2}/description.txt
touch ~/my_website/images/home/hero.jpg
touch ~/my_website/images/about/profile.jpg
touch ~/my_website/images/portfolio/{project1.jpg,project2.jpg}
touch ~/my_website/README.md
```

Verify:

```bash
find ~/my_website -name "*.html"
tree ~/my_website
```

### Deliverable
Show:
- all `.html` files found with `find`
- full project tree

---

# 2. Dotfiles and Shell Customization

This section is useful because it teaches students that Linux configuration is often just text editing.

## 2.1 What Are Dotfiles?

Dotfiles are configuration files whose names start with a dot.

Examples:
- `.bashrc`
- `.profile`
- `.gitconfig`

They are used to customize behavior.

## 2.2 Useful Ideas Students Should Learn

- configuration is often plain text
- always back up config files before editing
- apply changes with `source ~/.bashrc`
- changes to your shell are personal unless you edit system-wide files

## 2.3 Personal vs System-Wide Changes

### Personal
Affects only your account:

```bash
nano ~/.bashrc
```

### System-wide
Affects everyone and usually needs `sudo`:

```bash
sudo nano /etc/motd
```

In managed labs, students may not have permission to edit system-wide files.

## 2.4 Aliases

Aliases create shortcuts for long commands.

Example additions to `~/.bashrc`:

```bash
alias ll='ls -alF'
alias h='history'
alias c='clear'
```

Then apply changes:

```bash
source ~/.bashrc
```

## 2.5 Prompt Customization

The shell prompt is the text before your cursor.

You can customize it to show useful information like time, directory, Git branch, and username.

A simple example:

```bash
get_current_time() {
    date +"%d-%m-%Y %H:%M:%S"
}
PS1="[\$(get_current_time)] \u@\h:\w\\$ "
```

## 2.6 Important Caution

Do not tell beginners to blindly paste large prompt scripts into `.bashrc` without:
- backing up first
- opening a new terminal to test
- keeping a recovery copy

---

## Lab 2A: Safe Alias Customization

### Objective
Create useful aliases in `.bashrc`.

### Steps

```bash
cp ~/.bashrc ~/.bashrc.backup
nano ~/.bashrc
```

Add:

```bash
alias ll='ls -alF'
alias h='history'
alias c='clear'
```

Apply:

```bash
source ~/.bashrc
```

Test:

```bash
ll
h
c
```

### Deliverable
Show the alias lines in `.bashrc` and show the aliases working.

---

## Lab 2B: Add Time to the Prompt

### Objective
Understand prompt customization without breaking the shell.

### Steps

Append to `~/.bashrc`:

```bash
get_current_time() {
    date +"%d-%m-%Y %H:%M:%S"
}
PS1="[\$(get_current_time)] \u@\h:\w\\$ "
```

Apply:

```bash
source ~/.bashrc
```

### Deliverable
Show the new prompt.

---

## Optional Lab 2C: Message of the Day

Only do this if students have `sudo` and are allowed to make system-wide changes.

```bash
sudo cp /etc/motd /etc/motd.backup
sudo nano /etc/motd
```

Add a message and test by opening a new terminal.

### Better classroom note
In shared or cloud lab environments, prefer personal customization over editing `/etc/motd`.

---

# 3. Text Processing Fundamentals

This is where Linux starts becoming powerful.

A lot of Linux work is really text work.

## 3.1 `cat`

Display file contents.

```bash
cat hello.txt
cat -n hello.txt
```

Useful for:
- quick inspection
- small files
- piping output into another command

## 3.2 `echo`

Print text or variables.

```bash
echo "Hello, World!"
NAME="Alice"
echo "$NAME"
```

Useful for:
- testing
- creating tiny files
- printing variables in shell scripts

## 3.3 `wc`

Count lines, words, bytes, or characters.

```bash
wc hello.txt
wc -l hello.txt
wc -w hello.txt
wc -c hello.txt
```

## 3.4 `sort`

Sort lines.

```bash
sort names.txt
sort -n numbers.txt
sort -r names.txt
```

## 3.5 `grep`

Search for patterns.

```bash
grep "ERROR" application.log
grep -i "warning" application.log
grep -n "TODO" todo.txt
```

## 3.6 `head` and `tail`

Look at the beginning or end of files.

```bash
head application.log
head -n 5 application.log
tail application.log
tail -n 20 application.log
```

These are especially useful for logs.

## 3.7 A Key Habit

Students often try to read whole files all the time.

Usually better:
- `head` first
- `tail` if it is a log
- `grep` to narrow
- `cat` only when the file is small

---

## Lab 3A: Basic Text Command Practice

### Setup
Create some simple files.

```bash
echo "Hello, World!" > hello.txt
echo "Welcome to Linux text manipulation." >> hello.txt
printf "Alice\nBob\nCharlie\nDavid\n" > names.txt
printf "9\n5\n20\n1\n14\n" > numbers.txt
printf "TODO: Fix login bug\nBuy groceries\nTODO: Add tests\n" > todo.txt
printf "2026-01-01 INFO: App started\n2026-01-01 ERROR: DB failed\n2026-01-01 WARNING: Low memory\n" > logfile.txt
```

### Tasks

```bash
cat hello.txt
cat -n hello.txt
sort names.txt
sort -n numbers.txt
grep "TODO" todo.txt
wc -l logfile.txt
head -n 2 hello.txt
tail -n 2 hello.txt
```

### Deliverable
Show command outputs for each task.

---

## Lab 3B: Log Analysis

If you have the provided generator:

```bash
python3 log_generator.py
```

This should create `application.log`.

### Tasks

#### INFO logs

```bash
grep "INFO" application.log > info_logs.txt
wc -l info_logs.txt
```

#### WARNING logs

```bash
grep "WARNING" application.log > warning_logs.txt
wc -l warning_logs.txt
```

#### ERROR logs

```bash
grep "ERROR" application.log > error_logs.txt
wc -l error_logs.txt
sort error_logs.txt | uniq > sorted_errors.txt
head -n 10 sorted_errors.txt
```

#### DEBUG logs

```bash
grep "DEBUG" application.log > debug_logs.txt
wc -l debug_logs.txt
```

#### Top recurring errors

```bash
grep "ERROR" application.log | sort | uniq -c | sort -nr | head -n 5 > top_errors.txt
cat top_errors.txt
```

### Deliverable
Provide:
- counts for each log level
- top 5 recurring error messages

---

# 4. Pipes, Redirection, and File Descriptors

This is one of the most important ideas in Linux.

## 4.1 Standard Streams

Every process usually starts with three standard streams:

- `stdin`  = file descriptor 0
- `stdout` = file descriptor 1
- `stderr` = file descriptor 2

By default:
- input comes from keyboard
- output goes to terminal
- errors also go to terminal

## 4.2 Redirection

Redirection changes where input or output goes.

### Output redirection `>`
Overwrite a file:

```bash
echo "Hello" > output.txt
```

### Append redirection `>>`
Append to a file:

```bash
echo "Again" >> output.txt
```

### Input redirection `<`
Use a file as input:

```bash
sort < numbers.txt
```

### Error redirection `2>`
Send errors to a file:

```bash
grep "needle" missing_file.txt 2> error.txt
```

### Combine stdout and stderr

```bash
command > all_output.txt 2>&1
```

This means: send stderr wherever stdout is currently going.

## 4.3 Pipes `|`

A pipe sends the output of one command into the input of another.

```bash
cat logfile.txt | grep "ERROR"
```

More usefully:

```bash
grep "ERROR" logfile.txt | wc -l
```

That means:
1. `grep` finds matching lines
2. those lines go through the pipe
3. `wc -l` counts them

## 4.4 Why Pipes Matter

Without pipes, you would need many temporary files.

With pipes, you can connect tools directly.

This is the Linux style:
- one tool produces
- another filters
- another counts
- another sorts

## 4.5 `stderr` vs `stdout`

Students often miss this distinction.

- `stdout` is regular output
- `stderr` is error output

This matters because you may want to save results but still see errors separately.

## 4.6 A Common Style Note

These are both valid:

```bash
cat file.txt | grep "ERROR"
grep "ERROR" file.txt
```

For a single file, the second one is usually cleaner.

Use `cat ... |` when:
- input is coming from something dynamic
- you are already in a longer pipeline
- you want to make data flow explicit for teaching

## 4.7 `tee` and `/dev/null`

### `tee`
Show output and save it at the same time.

```bash
grep "ERROR" application.log | tee errors.txt
```

### `/dev/null`
Throw output away.

```bash
command > /dev/null 2>&1
```

Useful when you want silence.

---

## Lab 4A: Redirection Practice

### Tasks

```bash
echo "Hello, World!" > output.txt
echo "Hello again!" >> output.txt
cat output.txt
sort < numbers.txt > sorted_numbers.txt
cat sorted_numbers.txt
grep "TODO" todo.txt > todo_only.txt
cat todo_only.txt
```

### Deliverable
Show the contents of:
- `output.txt`
- `sorted_numbers.txt`
- `todo_only.txt`

---

## Lab 4B: Pipe Practice

### Tasks

```bash
grep "ERROR" logfile.txt | wc -l
grep "TODO" todo.txt | cat -n
sort names.txt | head -n 3
grep "INFO" application.log | wc -l
```

### Deliverable
Show the output of each pipeline.

---

## Lab 4C: Separate Standard Output and Standard Error

Use a command that produces an error.

```bash
ls real_file.txt missing_file.txt > stdout.txt 2> stderr.txt
```

Then inspect both:

```bash
cat stdout.txt
cat stderr.txt
```

### Deliverable
Show what went to `stdout.txt` and what went to `stderr.txt`.

---

# 5. `cut` and `paste`

Now we move from general text tools to column-based manipulation.

These commands are especially useful when data is organized by lines and fields.

## 5.1 `cut`

`cut` extracts parts of each line.

### Common options

- `-d` delimiter
- `-f` field number(s)
- `-c` character positions
- `--complement` inverse selection

### Examples

Given:

```text
apple,red,5
banana,yellow,6
cherry,red,20
```

Extract field 2:

```bash
cut -d, -f2 data.txt
```

Output:

```text
red
yellow
red
```

### Concept

Each line is treated independently.

If you use `-d, -f2`, then for every line:
1. split on comma
2. keep the second field
3. print it

### Character-based cut

```bash
cut -c1-3 names.txt
```

### Good use cases

- CSV-like text
- colon-separated data
- selecting columns from command output

## 5.2 `paste`

`paste` merges lines side by side.

### Common options

- `-d` custom delimiter
- `-s` serial mode

### Example: merge two files

`file1.txt`

```text
apple
banana
cherry
```

`file2.txt`

```text
red
yellow
red
```

Command:

```bash
paste -d, file1.txt file2.txt
```

Output:

```text
apple,red
banana,yellow
cherry,red
```

### Example: turn one file into two columns

`file3.txt`

```text
1
2
3
4
5
6
```

Command:

```bash
paste - - < file3.txt
```

Output:

```text
1    2
3    4
5    6
```

### Example: put all lines on one line

```bash
paste -s -d',' file1.txt
```

Output:

```text
apple,banana,cherry
```

## 5.3 The Critical Caveat: Alignment

`paste` does **not** match rows by key.

It only combines line 1 with line 1, line 2 with line 2, and so on.

That means `paste` is correct only when the files are already aligned.

If rows belong together by a key such as username, then you must make sure they are in the same order first.

For teaching, this is an excellent place to explain the difference between:
- **line-based merging** (`paste`)
- **key-based joining** (`join`, databases, spreadsheets)

We keep the lab centered on `cut` and `paste`, but students should know the limitation.

## 5.4 A Small Efficiency Note

Original example idea:

```bash
cut -d',' -f1,2 books.csv | grep "Software Engineering"
```

Cleaner form:

```bash
grep "Software Engineering" books.csv | cut -d',' -f1,2
```

Why this is usually better:
- `grep` narrows the data first
- `cut` works on fewer lines
- the intent is clearer

---

## Lab 5A: Basic `cut` Practice

Using `data.txt`:

```text
apple,red,5
banana,yellow,6
cherry,red,20
```

### Tasks

```bash
cut -d, -f1 data.txt
cut -d, -f2 data.txt
cut -d, -f3 data.txt
cut -d, -f1,2 data.txt
```

### Deliverable
Show the output for each command.

---

## Lab 5B: Basic `paste` Practice

Using:
- `file1.txt`
- `file2.txt`
- `file3.txt`

### Tasks

```bash
paste file1.txt file2.txt
paste -d, file1.txt file2.txt
paste - - < file3.txt
paste -s -d',' file1.txt
```

### Deliverable
Show each output.

---

## Lab 5C: CSV Lab with `cut` and `paste`

### Setup
Run the generator:

```bash
python3 order_generator.py
```

This should create:
- `user_emails.csv`
- `user_orders.csv`
- `user_addresses.csv`

### Objective
Practice extracting fields, merging aligned files, and filtering results.

---

### Exercise 1: Springfield Promotion List

#### Goal
Create a file containing usernames and emails for users in Springfield.

#### Steps

Extract usernames and emails:

```bash
cut -d, -f1,2 user_emails.csv > temp_emails.csv
```

Extract city column:

```bash
cut -d, -f3 user_addresses.csv > temp_city.csv
```

Merge aligned data:

```bash
paste -d, temp_emails.csv temp_city.csv > user_email_and_city.csv
```

Filter Springfield users:

```bash
grep 'Springfield' user_email_and_city.csv | cut -d, -f1,2 > springfield_users.csv
```

Clean up:

```bash
rm temp_emails.csv temp_city.csv
```

#### Deliverable
`springfield_users.csv`

---

### Exercise 2: Comprehensive User Information File

#### Goal
Create a file containing:
- username
- email
- order_id
- street
- city
- zipcode

#### Steps

Combine email and orders:

```bash
paste -d, user_emails.csv user_orders.csv > temp_user_info.csv
```

Validate alignment manually with a few lines:

```bash
head temp_user_info.csv
```

Add addresses:

```bash
paste -d, temp_user_info.csv user_addresses.csv > comprehensive_user_info.csv
```

Extract desired fields:

```bash
cut -d, -f1,2,4,6,7,8 comprehensive_user_info.csv > final_user_info.csv
```

Clean up:

```bash
rm temp_user_info.csv
```

#### One-line version

```bash
paste -d, user_emails.csv user_orders.csv user_addresses.csv | cut -d, -f1,2,4,6,7,8 > final_user_info.csv
```

#### Important note
This works only if the three files are aligned row by row.

#### Deliverable
`final_user_info.csv`

---

### Optional Extension: What if the rows are not aligned?

Before using `paste`, inspect samples:

```bash
head user_emails.csv
head user_orders.csv
head user_addresses.csv
```

If they are not aligned, you should not trust `paste`.

At that point, the concept students should learn is:

> `paste` is for row alignment, not for key matching.

A more advanced command for key matching is `join`, after sorting the files by key.

You do not need to master `join` yet, but you should understand why `paste` can fail.

---

# 6. Users, Groups, Ownership, and Permissions

This section is central to Linux security.

## 6.1 Users and Groups

Linux controls access by users and groups.

- **user**: an individual account
- **group**: a collection of users sharing permissions
- **root**: superuser with maximum privileges

## 6.2 Important Attributes

- **UID**: user ID
- **GID**: group ID
- **home directory**: user’s personal workspace

## 6.3 Commands for User and Group Management

### Users

```bash
sudo useradd -m username
sudo userdel username
sudo usermod -aG groupname username
sudo passwd username
```

### Groups

```bash
sudo groupadd dev_team
sudo groupdel dev_team
```

### Inspection

```bash
id username
groups username
getent passwd
getent group
last
```

## 6.4 Ownership

Every file and directory has:
- an owner user
- an owner group

View with:

```bash
ls -l
```

Change with:

```bash
sudo chown newowner file.txt
sudo chgrp newgroup file.txt
sudo chown newowner:newgroup file.txt
```

## 6.5 Permission Categories

Permissions are defined for:
- **u** = user / owner
- **g** = group
- **o** = others

## 6.6 Permission Types

### For files
- `r` read contents
- `w` modify contents
- `x` execute file as a program

### For directories
- `r` list names in directory
- `w` create/delete/rename entries in directory
- `x` enter/traverse the directory

That last point is often missed:

> On directories, execute means traversal, not execution like a program.

## 6.7 Reading `ls -l`

Example:

```text
-rwxr-x---
```

Breakdown:
- first character: file type (`-` file, `d` directory)
- next 3: owner permissions
- next 3: group permissions
- last 3: others permissions

So:
- owner = `rwx`
- group = `r-x`
- others = `---`

## 6.8 Changing Permissions with `chmod`

### Symbolic form

```bash
chmod u+x script.sh
chmod g+w report.txt
chmod o-r secret.txt
chmod u=rwx,g=rx,o= file.txt
```

### Numeric form

Each permission has a value:
- `r = 4`
- `w = 2`
- `x = 1`

Examples:
- `7 = rwx`
- `6 = rw-`
- `5 = r-x`
- `4 = r--`

So:

```bash
chmod 755 script.sh
chmod 644 notes.txt
chmod 700 private.sh
```

## 6.9 A Very Important Classroom Clarification

Students often mix up these two ideas:

### Case A

```bash
./hello.py
```

This requires:
- execute permission on the file
- a valid shebang line like `#!/usr/bin/env python3`

### Case B

```bash
python3 hello.py
```

This does **not** require the script file itself to be executable in the same way. Python reads the file as data.

So if you want to test **execute permission on the script**, use `./hello.py`, not `python3 hello.py`.

Also, path access can fail even when the file permission looks correct if the user cannot traverse one of the directories in the path.

That is why permission labs should avoid relying on another user’s home directory unless you explicitly manage the directory permissions.

---

## Lab 6A: Create Users and a Group

> Only do this lab if you have `sudo` access.

### Objective
Create a team group and two users.

### Steps

```bash
sudo groupadd dev_team
sudo useradd -m dev_alex
sudo useradd -m dev_bob
sudo passwd dev_alex
sudo passwd dev_bob
sudo usermod -aG dev_team dev_alex
```

Verify:

```bash
id dev_alex
id dev_bob
groups dev_alex
groups dev_bob
```

### Deliverable
Show group membership and user IDs.

---

## Lab 6B: Correct Permission Lab Using a Shared Group Directory

This version is more reliable than placing the file inside `/home/dev_alex`, because home-directory traversal can confuse the experiment.

### Objective
Show how ownership, group membership, directory permissions, and execute permission interact.

### Step 1: Create shared directory

```bash
sudo mkdir -p /tmp/dev_team_lab
sudo chown dev_alex:dev_team /tmp/dev_team_lab
sudo chmod 2770 /tmp/dev_team_lab
```

Explanation:
- owner = `dev_alex`
- group = `dev_team`
- directory mode `2770` means group-owned shared directory
- the leading `2` sets the setgid bit so new files inherit the group

### Step 2: Create executable script as `dev_alex`

Switch user:

```bash
su - dev_alex
cd /tmp/dev_team_lab
nano hello.py
```

Put this inside:

```python
#!/usr/bin/env python3
print("Hello, dev_team!")
```

Save, then:

```bash
chmod 750 hello.py
ls -l hello.py
exit
```

### Step 3: Test as `dev_bob` before adding to the group

```bash
su - dev_bob
cd /tmp/dev_team_lab
./hello.py
```

Expected result:
- permission denied

Why?
- file owner is not `dev_bob`
- `dev_bob` is not yet in `dev_team`
- others have no permission

Exit:

```bash
exit
```

### Step 4: Add `dev_bob` to the group

```bash
sudo usermod -aG dev_team dev_bob
```

Important: group membership often updates only in a new login session.

Now start a fresh session as `dev_bob`:

```bash
su - dev_bob
cd /tmp/dev_team_lab
id
./hello.py
```

Expected result:
- script runs successfully

### What this lab actually proves

- ownership matters
- group membership matters
- directory traversal permission matters
- execute permission on the script matters when using `./hello.py`

### Deliverable
Show:
- `ls -ld /tmp/dev_team_lab`
- `ls -l /tmp/dev_team_lab/hello.py`
- failed run before group membership
- successful run after group membership

---

## Lab 6C: Reading Permissions with `ls -l` and `stat`

### Objective
Practice interpreting permission strings.

### Steps

```bash
touch sample.txt
chmod 640 sample.txt
ls -l sample.txt
stat sample.txt
```

Questions students should answer:
1. Who can read it?
2. Who can write it?
3. Can others access it?

### Deliverable
Write a short explanation of `640` and the `ls -l` output.

---

# 7. `umask`

`umask` controls default permissions for newly created files and directories.

## 7.1 Default Creation Permissions

The system begins from these defaults:

- files: `666` (`rw-rw-rw-`)
- directories: `777` (`rwxrwxrwx`)

Then `umask` removes permissions.

## 7.2 Examples

### `umask 0022`

- new files become `644`
- new directories become `755`

### `umask 0002`

- new files become `664`
- new directories become `775`

### `umask 0077`

- new files become `600`
- new directories become `700`

This is much more private.

## 7.3 Intuition

Think of `umask` as a mask that blocks permissions from being granted by default.

It does **not** add permission.
It removes permission from the default template.

## 7.4 Optional Bitwise View

For students who want deeper understanding:

Example for a file with `umask 0002`:

```text
Default file perms: 666 = 110 110 110
Umask:              002 = 000 000 010
NOT umask:                111 111 101
AND result:               110 110 100 = 664
```

You do not need to compute this every day, but it explains why `umask` works the way it does.

---

## Lab 7A: Observe Default `umask`

### Steps

```bash
mkdir umask_lab
cd umask_lab
umask
touch file1
mkdir dir1
ls -l
```

Record the permission bits for `file1` and `dir1`.

### Deliverable
State:
- current `umask`
- permissions for `file1`
- permissions for `dir1`

---

## Lab 7B: Change `umask` and Compare Results

### Steps

```bash
umask 0022
touch file2
mkdir dir2

umask 0077
touch file3
mkdir dir3

ls -l
```

### Questions
1. Why do files and directories differ?
2. Which `umask` is more private?
3. Why is execute often missing on new files?

### Important answer for question 3
Regular text files usually do not need execute permission by default, so new files start from `666`, not `777`.

### Deliverable
A comparison table like this:

| item  | permissions |
|-------|-------------|
| file2 | ... |
| dir2  | ... |
| file3 | ... |
| dir3  | ... |

---

# 8. Optional Extension: “Everything Is a File” and Sockets

This is optional, but conceptually powerful.

Linux often models many things through the file-descriptor interface.

That includes:
- regular files
- pipes
- terminals
- sockets

## 8.1 Why This Idea Matters

If many kinds of input/output can be treated similarly, then the operating system can provide a unified programming model.

That is why the same big ideas show up again and again:
- open
- read
- write
- close

## 8.2 What Is a Socket?

A socket is a communication endpoint.

Two main common types:
- **UNIX domain sockets** for local machine communication
- **Internet sockets** for network communication

Common operations:
- `socket()` create endpoint
- `bind()` attach address
- `listen()` wait for clients
- `accept()` accept client
- `connect()` connect to server
- `send()` / `recv()` exchange data
- `close()` close connection

## 8.3 Server Workflow vs Client Workflow

### Server

1. create socket
2. bind address
3. listen
4. accept client
5. send/receive
6. close

### Client

1. create socket
2. connect to server
3. send/receive
4. close

## 8.4 Tiny Example

### `server.py`

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 65432))
server.listen()
print("Server listening on localhost:65432")

conn, addr = server.accept()
print("Connected by", addr)
conn.sendall(b"Hello from server!")
data = conn.recv(1024)
print("Client said:", data.decode())
conn.close()
server.close()
```

### `client.py`

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 65432))
msg = client.recv(1024)
print(msg.decode())
client.sendall(b"Hello from client!")
client.close()
```

## 8.5 What This Teaches

- networking is still input/output
- sockets are handled through descriptors
- Linux applies one broad model to many resources

---

## Lab 8A: Simple Local Socket Demo

### Terminal 1

```bash
python3 server.py
```

### Terminal 2

```bash
python3 client.py
```

### Deliverable
Show:
- server terminal output
- client terminal output

---

# 9. Summary Cheat Sheet

## Navigation

```bash
pwd
ls -la
cd ..
mkdir -p project/src
touch file.txt
cp a.txt b.txt
mv old.txt new.txt
rm file.txt
find . -name "*.txt"
```

## Text

```bash
cat file.txt
cat -n file.txt
echo "hello"
wc -l file.txt
sort names.txt
grep "ERROR" log.txt
head -n 5 file.txt
tail -n 5 file.txt
```

## Pipes and redirection

```bash
command > out.txt
command >> out.txt
command < in.txt
command 2> err.txt
command > all.txt 2>&1
grep "ERROR" log.txt | wc -l
```

## `cut` and `paste`

```bash
cut -d, -f2 data.txt
cut -d, -f1,3 data.txt
paste file1.txt file2.txt
paste -d, file1.txt file2.txt
paste - - < file3.txt
paste -s -d',' file1.txt
```

## Users and permissions

```bash
id
groups
ls -l
stat file.txt
chmod 755 script.sh
chmod 644 notes.txt
sudo chown user:group file.txt
sudo chgrp dev_team file.txt
umask
umask 0077
```

---

# 10. Final Advice to Students

1. Do not memorize commands as isolated words. Ask what problem each command solves.
2. Check your current directory often with `pwd`.
3. Inspect before changing: `ls`, `head`, `tail`, `cat`, `stat`.
4. Be especially careful with `rm`, permissions, and system-wide config files.
5. When something fails, ask:
   - is the path correct?
   - am I in the right directory?
   - do I have permission?
   - is the data aligned or am I assuming too much?
6. Linux becomes powerful when you combine small commands with intention.

