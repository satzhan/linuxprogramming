# Everything Is a File, Together: A Team Lab

## Why do this with other people

In the solo lab you were the only person on your machine. You made a named pipe, and you were both the writer and the reader. You started a chat server, and you were the client too. That's a fine way to see how the pieces work, but it hides what makes them interesting. A terminal, a shared folder, a pipe, a socket: these are the places where two programs meet, and on a real Linux machine those two programs very often belong to two different people.

As soon as several people share a machine, a second question sits next to "how does this work?", and that question is "who is allowed to use it?" Linux answers it the same way for nearly everything: with the owner, group and other permission bits from the users-and-permissions lab. In this lab you'll watch that one answer apply in turn to a terminal, a text file, a link, a running program, a pipe and a socket.

So this lab needs three of you. Every part is built so nobody can finish it alone. Someone sets something up, someone else has to find it, read it or connect to it, and the information has to travel through the machine to get there. And because each of you has your own VM, each of you will be the person who runs the machine for part of the lab, and a guest on your teammates' machines for the rest.

---

## Before you start

**Three people, three VMs.** Each of you has your own Azure Lab VM, and you log in to it as `student`. In Part 0, each of you turns your own VM into a team machine by creating accounts for your two teammates. When Part 0 is done, every VM has all three of you on it:

- On your own VM you are `student`, and you are the **Host**: the one with `sudo`, who runs the machine.
- On each teammate's VM you are a **Guest**, with an account named after you.

**The example team.** The examples follow a team of three: Ana, Ben and Cruz. Their Guest accounts are `ana`, `ben` and `cruz`. Decide now which of you is A, B and C, and from then on follow the lines for the person with your letter: A follows Ana's lines, B follows Ben's, C follows Cruz's. Use your own first names, in lowercase, wherever the examples say `ana`, `ben` or `cruz`.

**Who hosts what.** Part 0 happens on all three VMs. After that, each part is played on one VM, and its owner is the Host for that part:

| Part | Topic | Played on | Host | Guests |
|---|---|---|---|---|
| 0 | Make every VM a team machine | all three | each owner | the other two |
| 1 | Your terminal is a file with an owner | A's VM | Ana | Ben, Cruz |
| 2 | Mystery files and inode hide-and-seek | B's VM | Ben | Ana, Cruz |
| 3 | Links between three people | C's VM | Cruz | Ana, Ben |
| 4 | Someone else's program, seen through `/proc` | A's VM | Ana | Ben, Cruz |
| 5 | Pipes between three people | B's VM | Ben | Ana, Cruz |
| 6 | A chat room that knows who's talking | C's VM | Cruz | Ana, Ben |
| Cleanup | Take your VM apart again | all three | each owner | |

Everyone hosts two parts and is a Guest in four. Once Part 0 is done on a VM, the parts played there stand alone, so you can do them in any order. If you have time, replay a part on a different VM with the roles moved around.

**Your team's connection details.** The lab address is usually the same for the whole class; the port number is what picks the VM. Fill in a table like this before you start, with your real ports and names:

| VM owner | Owner connects with | Teammates connect with |
|---|---|---|
| Ana | `ssh -p 5037 student@lab-xxxxxxxx.eastus.cloudapp.azure.com` | `ssh -p 5037 ben@...`, `ssh -p 5037 cruz@...` |
| Ben | `ssh -p 5041 student@lab-xxxxxxxx.eastus.cloudapp.azure.com` | `ssh -p 5041 ana@...`, `ssh -p 5041 cruz@...` |
| Cruz | `ssh -p 5052 student@lab-xxxxxxxx.eastus.cloudapp.azure.com` | `ssh -p 5052 ana@...`, `ssh -p 5052 ben@...` |

Never give anyone your `student` password. Teammates get accounts of their own.

**Lots of terminal windows.** You'll be logged in to several VMs at once, and some steps need two windows on the same VM. Name or arrange your windows so you always know which VM, and which account, each one is. When in doubt, `whoami` and `hostname` tell you.

**Send it through the machine.** You'll be sitting near each other, and talking is fine, especially for planning. But whenever a step asks one of you to pass something on (a secret word, an inode number, a message), send it through the channel that part is about, or through the team logbook you'll build in Part 0. The logbook is how you show it happened.

**How to read the commands.** A line starting with `$` is something you type; leave out the `$`. A label above each block says who types it, and the part's opening line says which VM you're on:

**Ana (Host):**

```
$ whoami
student
```

**Ben:**

```
$ whoami
ben
```

Terminal numbers, process IDs, inode numbers and times will differ on your VM; the shape should match. The machine used for testing was called `vm`, so where an example says `student@vm`, yours will show your VM's name, something like `student@labPTIHOQ`. Where `who` prints an address at the end of a line, the examples leave it out.

**Tested on** Ubuntu 20.04.6, the same release the lab VMs use, with three people logged in over SSH as separate users. A few things on 20.04 behave differently from newer Ubuntu releases, and the lab points them out where they matter.

**The optional boxes.** Anything marked **Experiment** is optional. The main path works without it, though many of the surprises live there.

**Predict first.** Before you press Enter on a step marked *predict*, each of you says what you think will happen. Three different guesses is the best possible start.

> **Team of two?** Do Part 0 on both VMs, and play Parts 3 and 6 on whichever VM you like. When a step has lines for two Guests, the one Guest does them. Skip Step 1.7, which needs two Guests, and in round 3 of hide-and-seek let the Host be the Keeper.

---

## Part 0: Make every VM a team machine

**On all three VMs.** The examples show Ana's VM: Ana is the Host (`student`), and Ben and Cruz are Guests.

Each of you does Steps 0.1 to 0.6 on your own VM, at the same time. Then everyone logs in to everyone else's VM for Steps 0.7 to 0.11. Everything here comes from the users-and-permissions lab. The difference is that this time real people are on the other end.

### Step 0.1 Host: look around first

Earlier labs may have left accounts, groups and folders behind on your VM. Find them before you build anything new.

**Ana (Host):**

```
$ awk -F: '$3 >= 1000 && $3 < 60000 {print $1}' /etc/passwd
student
dev_alex
dev_bob
visitor
$ ls -l /home
total 16
drwxr-xr-x 2 dev_alex dev_alex 4096 Oct  7 12:10 dev_alex
drwxr-xr-x 2 dev_bob  dev_bob  4096 Oct  7 12:10 dev_bob
drwxr-xr-x 3 student  student  4096 Oct  7 12:10 student
drwxr-xr-x 2 visitor  visitor  4096 Oct  7 12:10 visitor
$ getent group team
$ ls -ld /srv/team
ls: cannot access '/srv/team': No such file or directory
$ who
student  pts/1        Oct  7 12:11
```

The first command reads `/etc/passwd`, the list of every account on the machine, and prints the names of accounts whose user number (the third field) is between 1000 and 60000. Accounts below 1000 belong to the system itself: programs like the SSH server and the mail system run under them. Human accounts start at 1000. `student` is 1000, because Azure created it first.

So this VM has three leftovers from earlier labs: `dev_alex`, `dev_bob` and `visitor`. There's no `team` group and no `/srv/team` yet. Yours may show different names, or none.

### Step 0.2 Host: clear the stage

Remove everything from earlier labs that this lab doesn't need. For each leftover account:

**Ana (Host):**

```
$ sudo pkill -u dev_alex
$ sudo userdel -r dev_alex
userdel: dev_alex mail spool (/var/mail/dev_alex) not found
$ sudo pkill -u dev_bob
$ sudo userdel -r dev_bob
userdel: dev_bob mail spool (/var/mail/dev_bob) not found
$ sudo pkill -u visitor
$ sudo userdel -r visitor
userdel: visitor mail spool (/var/mail/visitor) not found
$ ls /home
student
```

- `pkill -u dev_alex` ends every program running as that user, which also logs them out if they're still connected. If nothing was running, it prints nothing.
- `userdel -r` deletes the account, its home folder (`-r`), and its private group of the same name.
- The `mail spool ... not found` warning is harmless. It means the account never received any mail.

If a `team` group or a `/srv/team` folder is left over from an earlier team, remove those too:

```
$ sudo rm -rf /srv/team
$ sudo groupdel team
groupdel: group 'team' does not exist
```

`rm -rf` prints nothing either way. `groupdel` complains only if there was no `team` group to remove, which is fine.

> **Never delete `student`.** It's the only way into your own VM. `userdel` refuses while you're logged in as `student` (`user student is currently used by process ...`), but don't count on that. Read each `userdel` line before you press Enter. The Cleanup section at the end of the lab goes through all of this again, more slowly.

### Step 0.3 Host: a group and two accounts

**Ana (Host):**

```
$ sudo groupadd team
$ sudo useradd -m -s /bin/bash -G team ben
$ sudo passwd ben
New password:
Retype new password:
passwd: password updated successfully
$ sudo useradd -m -s /bin/bash -G team cruz
$ sudo passwd cruz
New password:
Retype new password:
passwd: password updated successfully
$ sudo usermod -aG team student
$ getent group team
team:x:1001:ben,cruz,student
```

One line at a time:

- `groupadd team` creates the group.
- `useradd -m -s /bin/bash -G team ben` creates the account. `-m` makes a home folder, `-s /bin/bash` gives it the usual shell (without it, Ubuntu hands out a plainer one), and `-G team` puts the new user in `team`.
- `passwd ben` sets a temporary password. Nothing shows while you type. Tell your teammate this one password out loud; they'll change it the moment they log in.
- `usermod -aG team student` adds you, the Host, to the group too. The `-a` (append) matters. Without it, `-G` *replaces* your list of groups instead of adding one, and you'd lose `sudo`.
- `getent group team` shows the group's line from `/etc/group`: its name, its number (1001), and its members.

If a command says `group 'team' already exists` or `user 'ben' already exists`, Step 0.2 missed something. Either keep it and move on, or remove it and run the line again.

Don't put your teammates in the `sudo` group. Several parts of this lab depend on Guests being ordinary users, and anyone with `sudo` can step around every permission you're about to test.

### Step 0.4 Host: a folder that belongs to the team

**Ana (Host):**

```
$ sudo mkdir /srv/team
$ sudo chgrp team /srv/team
$ sudo chmod 2770 /srv/team
$ ls -ld /srv/team
drwxrws--- 2 root team 4096 Oct  7 12:11 /srv/team
```

`/srv` is the standard place for data a machine serves to other people, which makes it a natural home for a shared folder. Read the permissions in three groups of three: the owner, root, has `rwx`; the group `team` has `rws`; everyone else has nothing.

The `s` where the group's `x` would be comes from the `2` at the front of `2770`. On a directory it's called *setgid*, and it means "anything created in here belongs to this folder's group". Without it, a file Ben makes would belong to Ben's own private group, `ben`, and Cruz couldn't change it. With it, everything inside `/srv/team` belongs to `team` automatically.

### Step 0.5 Host: someone who isn't on the team

Several parts need an outsider to test against. Make a user with no password, so nobody can log in as them:

**Ana (Host):**

```
$ sudo useradd -m visitor
$ sudo -u visitor ls /srv/team
ls: cannot open directory '/srv/team': Permission denied
```

`sudo -u visitor` runs one command as `visitor`. Only the Host can do this, because only the Host has `sudo`. Whenever this lab says "try it as the visitor", it's the Host's job. (When `sudo` asks for a password, it wants the Host's own `student` password.)

### Step 0.6 Host: predict, then log in again

*Predict:* you just added yourself to `team`, and `team` has full access to `/srv/team`. Will this work?

**Ana (Host):**

```
$ touch /srv/team/hello
touch: cannot touch '/srv/team/hello': Permission denied
$ id
uid=1000(student) gid=1000(student) groups=1000(student),27(sudo)
```

`team` isn't in the list. (Your list may be longer; Azure puts `student` in a few more groups.) Your groups are read once, when you log in, and every program you start copies that list from the shell that started it. This shell started before you joined `team`. Log out and connect again:

**Ana (Host):**

```
$ exit
```

Reconnect with your usual `ssh` command, then:

**Ana (Host):**

```
$ id
uid=1000(student) gid=1000(student) groups=1000(student),27(sudo),1001(team)
$ touch /srv/team/hello
$ ls -l /srv/team
total 0
-rw-rw-r-- 1 student team 0 Oct  7 12:11 hello
$ rm /srv/team/hello
```

The file belongs to group `team`, even though your own group is `student`. That's setgid at work.

### Step 0.7 Everyone: log in to your teammates' VMs

Each of you now has two new accounts waiting, one on each teammate's VM. Open a new terminal window for each and connect with that VM's port and your own name. Ben, connecting to Ana's VM:

**Ben:**

```
$ ssh -p 5037 ben@lab-xxxxxxxx.eastus.cloudapp.azure.com
```

If `ssh` asks whether you're sure you want to continue connecting, type `yes`: it hasn't seen this VM's port before. Type the temporary password, then change it straight away:

**Ben** (on Ana's VM):

```
$ passwd
Changing password for ben.
Current password:
New password:
Retype new password:
passwd: password updated successfully
$ id
uid=1001(ben) gid=1002(ben) groups=1002(ben),1001(team)
```

Do the same on your other teammate's VM. When everyone is done, each of you has three windows open: one on your own VM as `student`, and one on each teammate's VM under your own name.

### Step 0.8 Everyone: who can see into your home folder?

*Predict:* can Ben read a file in Ana's home folder? Can Cruz look into Ben's?

**Ana (Host):**

```
$ ls -ld /home/*
drwxr-xr-x 3 ben     ben     4096 Oct  7 12:11 /home/ben
drwxr-xr-x 3 cruz    cruz    4096 Oct  7 12:11 /home/cruz
drwxr-xr-x 3 student student 4096 Oct  7 12:10 /home/student
drwxr-xr-x 2 visitor visitor 4096 Oct  7 12:11 /home/visitor
$ echo 'my private notes' > ~/notes.txt
```

**Ben:**

```
$ cat ~student/notes.txt
my private notes
```

**Cruz:**

```
$ ls -a ~ben
.  ..  .bash_logout  .bashrc  .cache  .profile
```

(`~student` is short for "the home folder of `student`". If you already locked `student` in an earlier lab, Ben's `cat` fails right away; Cruz's look into `~ben` still works, because new accounts start open.) Look at the last three letters of each home folder's permissions: `r-x`. That's what everyone else gets, so anyone on the machine can walk into any home folder and read whatever isn't locked separately. On Ubuntu 20.04, `useradd` makes home folders this way, and so did whoever created `student`. Starting with Ubuntu 21.04, new home folders are private by default (`drwxr-x---`), so on a newer system this step would have failed for Ben and Cruz. Your privacy here depended on a default you never chose.

Fix it. Each person runs this once, on this VM:

**Everyone:**

```
$ chmod 750 ~
```

Now try again:

**Ana (Host):**

```
$ ls -ld /home/*
drwxr-x--- 3 ben     ben     4096 Oct  7 12:11 /home/ben
drwxr-x--- 3 cruz    cruz    4096 Oct  7 12:11 /home/cruz
drwxr-x--- 3 student student 4096 Oct  7 12:11 /home/student
drwxr-xr-x 2 visitor visitor 4096 Oct  7 12:11 /home/visitor
$ ls ~ben
ls: cannot open directory '/home/ben': Permission denied
$ sudo ls ~ben
$ rm ~/notes.txt
```

**Ben:**

```
$ cat ~student/notes.txt
cat: /home/student/notes.txt: Permission denied
```

`750` means: the owner can do everything, the owner's private group can look in (and only the owner is in it), and everyone else gets nothing. The `visitor` folder is still open, which doesn't matter since nobody can log in as `visitor`. And `sudo ls ~ben` still works, because root ignores permission bits. `ls` printed nothing because Ben's folder has only hidden files.

**Do this on every VM.** On each of the three VMs, all three accounts run `chmod 750 ~`: you lock `student` on your own VM, and your own home on each teammate's VM. Later parts (3.4 and 4.2) assume every home folder is locked.

> **Experiment: change the default.** The Host can make every account created from now on private, so nobody has to remember the `chmod`:
>
> ```
> $ echo 'HOME_MODE 0750' | sudo tee -a /etc/login.defs
> HOME_MODE 0750
> $ sudo useradd -m testprivate
> $ ls -ld /home/testprivate
> drwxr-x--- 2 testprivate testprivate 4096 Oct  7 12:18 /home/testprivate
> $ sudo userdel -r testprivate
> ```
>
> `/etc/login.defs` is the settings file `useradd` reads for its defaults, and `HOME_MODE` is the line newer Ubuntu releases ship with. It only affects accounts created after the change; existing folders keep their permissions. (`sudo tee -a` appends to a file as root, because `sudo echo ... >> file` would open the file as you.)

### Step 0.9 Everyone: check your umask

**Everyone:**

```
$ umask
0002
```

`0002` means new files you create are writable by their group, so your teammates can change files you make in `/srv/team`. That's the lab VMs' default. If anyone sees `0022`, files they make will be read-only for the rest of the team, and later parts will fail with `Permission denied` in confusing places. Fix it now and for future logins:

```
$ umask 002
$ echo 'umask 002' >> ~/.bashrc
```

### Step 0.10 One Guest: build the team logbook

The logbook is one text file, `/srv/team/logbook.txt`, that everyone on the VM adds lines to. A small program signs each line with who wrote it, from which terminal, and when. Nobody types their own name; the program asks the system who you are.

On each VM, the Guest whose letter comes after the Host's builds it: Ben builds it on Ana's VM, Cruz on Ben's VM, and Ana on Cruz's VM.

**Ben** (on Ana's VM):

```
$ nano /srv/team/log
```

Paste this in, save with Ctrl+O and Enter, and leave with Ctrl+X:

```python
#!/usr/bin/env python3
# log: add one signed line to the team logbook.
# Usage:  log "what happened"
import datetime
import os
import pwd
import sys

BOOK = "/srv/team/logbook.txt"

who = pwd.getpwuid(os.getuid()).pw_name         # your login name, looked up from your user ID
try:
    where = os.ttyname(0).replace("/dev/", "")   # the terminal you typed this in, like pts/1
except OSError:
    where = "-"                                   # input came from a pipe, not a terminal
when = datetime.datetime.now().strftime("%H:%M:%S")
message = " ".join(sys.argv[1:])

if not message:
    sys.exit('usage: log "what happened"')

with open(BOOK, "a") as book:
    book.write(f"{when}  {who:<8} {where:<6} {message}\n")
print(f"logged as {who}")
```

Then make it runnable as a command:

**Ben:**

```
$ chmod +x /srv/team/log
$ ls -l /srv/team
total 4
-rwxrwxr-x 1 ben team 744 Oct  7 12:11 log
```

The first line, `#!/usr/bin/env python3`, tells Linux which program should run this file, so it can be started by name without typing `python3` first. `os.getuid()` is the number the kernel knows you by, and `pwd.getpwuid` turns that number into your name by looking it up in `/etc/passwd`, which is, of course, a file.

### Step 0.11 Everyone: a short name, and the first entries

So you can type `log` instead of `/srv/team/log`, each account runs this once on this VM:

**Everyone:**

```
$ echo 'alias log=/srv/team/log' >> ~/.bashrc
$ source ~/.bashrc
```

Now see who's on the machine, and sign the book:

**Ana (Host):**

```
$ who
student  pts/2        Oct  7 12:11
ben      pts/3        Oct  7 12:11
cruz     pts/5        Oct  7 12:11
$ log 'Ana here (Host), setup done on my VM'
logged as student
```

**Ben:**

```
$ log 'Ben here, logged in as ben'
logged as ben
```

**Cruz:**

```
$ log 'Cruz here, logged in as cruz'
logged as cruz
$ cat /srv/team/logbook.txt
12:11:55  student  pts/2  Ana here (Host), setup done on my VM
12:11:55  ben      pts/3  Ben here, logged in as ben
12:11:55  cruz     pts/5  Cruz here, logged in as cruz
```

Three people, one file, every line signed by the system. Notice that Ana signs as `student`: on her own VM, that's who the kernel says she is. From here on, whenever a step says **Log it**, add a line like this on the VM you're playing on. The times come from the VM's clock, which may be set to a different time zone from yours.

`log` isn't tamper-proof: anyone in the team could edit the file with `nano`. It's an honest record as long as you use it honestly, and that's all it needs to be.

### Part 0 checklist

Before moving on, check each of the three VMs:

- `getent group team` lists all three accounts.
- `ls -ld /home/*` shows `drwxr-x---` for `student` and both Guests.
- `log` works for all three of you, and the logbook has a line from each.

---

## Part 1: Your terminal is a file with an owner

**On A's VM.** Ana is the Host (`student`); Ben and Cruz are Guests.

In the solo lab, `tty` showed that your terminal is a file like `/dev/pts/0`, and writing into that file made text appear on your screen. With three people logged in, there are three of those files, and each one has an owner.

### Step 1.1 Find each other

**Everyone:**

```
$ tty
```

Ana sees `/dev/pts/1`, Ben `/dev/pts/3`, Cruz `/dev/pts/5`. Nobody needs to ask which terminal belongs to whom; `who` already knows:

**Ana (Host):**

```
$ who
student  pts/1        Oct  7 12:18
ben      pts/3        Oct  7 12:18
cruz     pts/5        Oct  7 12:18
$ ls -l /dev/pts
total 0
crw------- 1 root    root 136, 0 Oct  7 12:18 0
crw--w---- 1 student tty  136, 1 Oct  7 12:18 1
crw------- 1 root    root 136, 2 Oct  7 12:18 2
crw--w---- 1 ben     tty  136, 3 Oct  7 12:18 3
crw------- 1 root    root 136, 4 Oct  7 12:18 4
crw--w---- 1 cruz    tty  136, 5 Oct  7 12:18 5
c--------- 1 root    root   5, 2 Oct  7 11:50 ptmx
```

Every login gets its own terminal file, owned by whoever logged in on it. (The ones owned by root belong to the system itself, and `ptmx` is the device that hands out new terminals.)

### Step 1.2 Ana: knock on Ben's terminal

*Predict:* will this put text on Ben's screen?

**Ana (Host):**

```
$ echo "knock knock" > /dev/pts/3
-bash: /dev/pts/3: Permission denied
```

Read the line for terminal `3` again: `crw--w---- 1 ben tty`. The owner, `ben`, may read and write. The group, `tty`, may write. Everyone else may do nothing. Ana isn't `ben` and isn't in group `tty`, so she's "everyone else".

### Step 1.3 A program with a borrowed badge

Linux has an old command made for exactly this job. `write ben` sends a message to Ben's terminal; type lines, then Ctrl+D to finish:

**Ana (Host):**

```
$ write ben
Hi Ben, it's Ana. Can you read this?
```

(Press Ctrl+D after the line.) On Ben's screen:

```
Message from student@vm on pts/1 at 12:18 ...
Hi Ben, it's Ana. Can you read this?
EOF
```

Cruz can do it in one line, by piping the message in:

**Cruz:**

```
$ echo 'Ben, Cruz here, me too' | write ben
```

So `echo` was refused, but `write` got through. Why? Look at the program itself. `/usr/bin/write` is a symlink, so follow it first:

**Ana (Host):**

```
$ readlink -f /usr/bin/write
/usr/bin/bsd-write
$ ls -l /usr/bin/bsd-write
-rwxr-sr-x 1 root tty 14488 Mar 30  2020 /usr/bin/bsd-write
```

The `s` in the group position, together with the group `tty`, makes this a *setgid* program: whoever runs it gets group `tty` added to their badge for as long as it runs. Terminals let group `tty` write, so `write` gets in where Ana's own shell couldn't. Linux lends a badge to the program, not to the person. `write` only does one careful thing with it, and it checks first whether the receiver has said they're willing.

### Step 1.4 Ben: do not disturb

**Ben:**

```
$ mesg n
$ ls -l $(tty)
crw------- 1 ben tty 136, 3 Oct  7 12:18 /dev/pts/3
```

`$(tty)` gets replaced by the output of `tty`, your terminal's path. `mesg n` took away the group's write permission. Now:

**Ana (Host):**

```
$ echo 'still there?' | write ben
write: ben has messages disabled
```

**Cruz:**

```
$ echo 'hello?' | write ben
write: ben has messages disabled
```

*Predict*, before Ben turns messages back on: which permissions will `mesg y` give back?

**Ben:**

```
$ mesg y
$ ls -l $(tty)
crw--w--w- 1 ben tty 136, 3 Oct  7 12:18 /dev/pts/3
```

Group *and* others. On these lab VMs, `mesg y` opens your terminal to everyone on the machine, not just to `write`. Ana can show what that means:

**Ana (Host):**

```
$ sudo -u visitor sh -c 'echo "visitor here" > /dev/pts/3'
```

On Ben's screen:

```
visitor here
```

The visitor isn't a teammate and doesn't need `write`. Ben closes the gap:

**Ben:**

```
$ chmod o-w $(tty)
$ ls -l $(tty)
crw--w---- 1 ben tty 136, 3 Oct  7 12:18 /dev/pts/3
```

Why `sh -c '...'`? The `>` is handled by the shell *before* the command runs. In `sudo -u visitor echo hi > /dev/pts/3`, Ana's own shell would open the terminal file as Ana, and only `echo` would run as the visitor. `sh -c` starts a whole new shell as the visitor, so the visitor is the one doing the opening.

A convenience command can do more than its name suggests, and `ls -l` tells you what it really did.

### Step 1.5 Ben: open the door to the team

**Ben:**

```
$ chgrp team $(tty)
$ ls -l $(tty)
crw--w---- 1 ben team 136, 3 Oct  7 12:18 /dev/pts/3
```

Ben owns his terminal, so he can hand it to any group he belongs to. The group still has write permission; it's just a different group now. Both teammates can knock directly:

**Ana (Host):**

```
$ echo "knock knock, from Ana" > /dev/pts/3
```

**Cruz:**

```
$ echo "knock knock, from Cruz" > /dev/pts/3
```

**Ana (Host):**

```
$ sudo -u visitor sh -c 'echo "visitor here" > /dev/pts/3'
sh: 1: cannot create /dev/pts/3: Permission denied
```

On Ben's screen:

```
knock knock, from Ana
knock knock, from Cruz
```

**Log it.** Ben: `log "knocks from Ana and Cruz arrived, the visitor's didn't"`

### Step 1.6 Ana: a message for everyone

`wall` ("write all") sends one message to every logged-in terminal. *Predict*: right now Ben's terminal is open to `team` and Cruz's is still the default (`crw--w---- cruz tty`). Who gets this?

**Ana (Host):**

```
$ wall 'Ana here: can everyone see this?'

Broadcast message from student@vm (pts/1) (Wed Oct  7 12:18:24 2026):

Ana here: can everyone see this?
```

Ana sees it, and so does Ben. Cruz sees nothing at all. Look at the program:

**Ana (Host):**

```
$ ls -l /usr/bin/wall
-rwxr-xr-x 1 root root 35048 Apr  9  2024 /usr/bin/wall
```

No `s`, and the date is April 2024. That month a security bug (nicknamed WallEscape) showed that `wall` could be used to put fake text on other people's screens, and Ubuntu's fix took away its borrowed `tty` badge. So `wall` now reaches only the terminals Ana could write to herself: her own, and Ben's, because she's in `team`. `write` on 20.04 is a different program (`bsd-write`), and it kept its badge.

Now Cruz turns messages off, and Ana tries again as root:

**Cruz:**

```
$ mesg n
```

**Ana (Host):**

```
$ sudo wall 'Ana again, this time with sudo'
```

All three of you see it, Cruz included. Root ignores permission bits. Cruz turns messages back on, and closes the gap from Step 1.4:

**Cruz:**

```
$ mesg y
$ chmod o-w $(tty)
$ ls -l $(tty)
crw--w---- 1 cruz tty 136, 5 Oct  7 12:18 /dev/pts/5
```

### Step 1.7 Ben and Cruz: a private line

Ben wants Cruz to be able to knock, but not Ana. `team` won't do it, because Ana is in `team` too. A file has exactly one owner and one group, so the way to pick particular people is a group with exactly those people in it. Making groups takes `sudo`, so the Host makes it, even though it's meant to keep her out:

**Ana (Host):**

```
$ sudo groupadd bc
$ sudo usermod -aG bc ben
$ sudo usermod -aG bc cruz
$ getent group bc
bc:x:1005:ben,cruz
```

*Predict*, Ben: you're in `bc` now. Can you hand your terminal to it?

**Ben:**

```
$ chgrp bc $(tty)
chgrp: changing group of '/dev/pts/3': Operation not permitted
$ id
uid=1001(ben) gid=1002(ben) groups=1002(ben),1001(team)
```

The badge again: Ben's groups were read when he logged in, before `bc` existed. Logging out would give him a new badge, but also a new terminal. `newgrp` starts a new shell with a fresh badge, in the same terminal:

**Ben:**

```
$ newgrp bc
$ id
uid=1001(ben) gid=1005(bc) groups=1005(bc),1001(team),1002(ben)
$ chgrp bc $(tty)
$ ls -l $(tty)
crw--w---- 1 ben bc 136, 3 Oct  7 12:18 /dev/pts/3
```

Now Cruz knocks. *Predict* first.

**Cruz:**

```
$ echo "Cruz on the private line" > /dev/pts/3
-bash: /dev/pts/3: Permission denied
$ newgrp bc
$ echo "Cruz on the private line" > /dev/pts/3
```

Cruz needed a fresh badge too. Now Ana:

**Ana (Host):**

```
$ echo "Ana, trying the private line" > /dev/pts/3
-bash: /dev/pts/3: Permission denied
$ echo "Ana with the master key" | sudo tee /dev/pts/3 > /dev/null
```

On Ben's screen:

```
Cruz on the private line
Ana with the master key
```

The group kept Ana out, until she used `sudo`. (`sudo tee` rather than `sudo echo ... >`, for the same reason as `sh -c` in Step 1.4: here `tee`, running as root, is the program that opens the terminal file.) This is why Guests don't get `sudo`: anyone with it can step around every lock in this lab.

**Log it.** Ben and Cruz: one line each about what the private line let through and what it didn't.

Clean up the private line. Ben and Cruz each leave the `newgrp` shell, and Ana deletes the group:

**Ben and Cruz:**

```
$ exit
```

**Ana (Host):**

```
$ sudo groupdel bc
```

**Ben:**

```
$ ls -l $(tty)
crw--w---- 1 ben 1005 136, 3 Oct  7 12:18 /dev/pts/3
```

Ben's terminal now belongs to group `1005`: a number with no name, because the group is gone. It's harmless, and the terminal disappears when Ben logs out. The Cleanup section shows why leftover numbers like this can matter.

### Step 1.8 Rotate

Do Steps 1.2 to 1.5 twice more, so everyone gets knocked on: once with Cruz as the receiver, and once with Ana. To reach Ana with `write`, use her account name on this VM:

**Ben:**

```
$ echo 'hi Ana' | write student
```

On Ana's screen:

```
Message from ben@vm on pts/3 at 12:18 ...
hi Ana
EOF
```

None of these terminal settings are permanent. A terminal file is created fresh each time someone logs in, with the default permissions.

> **Experiment: lists that name people.** Linux has a finer tool than groups: access control lists, which name individual users (`setfacl -m u:cruz:w somefile`). Try one on your terminal and you'll get `Operation not supported`: the terminal filesystem doesn't support them. On an ordinary file in `/srv/team` they work, if the `acl` package is installed (the Host can add it with `sudo apt install acl`). Not every kind of file supports every feature.

---

## Part 2: Mystery files and inode hide-and-seek

**On B's VM.** Ben is the Host (`student`); Ana and Cruz are Guests.

A name is only a label in a directory. What a file *is*, and which file it is, lives in its inode. This part turns both ideas into games.

### Step 2.1 Set up

**Ben (Host):**

```
$ mkdir -p /srv/team/part2/mystery
$ ls -ld /srv/team/part2
drwxrwsr-x 3 student team 4096 Oct  7 12:14 /srv/team/part2
```

Check for `rwx` in the group's place and the `s`. Without them, the Guests will get `Permission denied` in this part. If they're missing, Ben's umask isn't `0002` (Step 0.9); fix the folder with `chmod -R g+w /srv/team/part2`.

### Step 2.2 Ana: four things with misleading names

**Ana:**

```
$ cd /srv/team/part2/mystery
$ mkdir photo.jpg
$ mkfifo notes.txt
$ ln -s /etc/hostname music.mp3
$ python3 -c "import socket; socket.socket(socket.AF_UNIX).bind('readme')"
```

A directory called `photo.jpg`, a named pipe called `notes.txt`, a symbolic link called `music.mp3`, and a socket called `readme`. Don't tell the others which is which.

### Step 2.3 Cruz and Ben: identify them without asking

Cruz starts with only the names:

**Cruz:**

```
$ cd /srv/team/part2/mystery
$ ls
music.mp3  notes.txt  photo.jpg  readme
```

The names are lying, on purpose. Now ask the system:

**Cruz:**

```
$ ls -l
total 4
lrwxrwxrwx 1 ana team   13 Oct  7 12:14 music.mp3 -> /etc/hostname
prw-rw-r-- 1 ana team    0 Oct  7 12:14 notes.txt
drwxrwsr-x 2 ana team 4096 Oct  7 12:14 photo.jpg
srwxrwxr-x 1 ana team    0 Oct  7 12:14 readme
```

The first letter gives each one away: `l`, `p`, `d`, `s`. Ben gets a second opinion from two other tools:

**Ben (Host):**

```
$ cd /srv/team/part2/mystery
$ file *
music.mp3: symbolic link to /etc/hostname
notes.txt: fifo (named pipe)
photo.jpg: setgid, directory
readme:    socket
$ stat -c '%-10n %F' *
music.mp3  symbolic link
notes.txt  fifo
photo.jpg  directory
readme     socket
```

All four belong to group `team`, and `file` calls the directory "setgid": it inherited the bit from the folder it was made in, so the rule from Step 0.4 applies all the way down.

**Log it.** Cruz and Ben: each of you logs what the four really are.

> **Experiment: what does `cat` do to each one?** Have Ctrl+C ready.
>
> ```
> $ cat photo.jpg
> cat: photo.jpg: Is a directory
> $ cat readme
> cat: readme: No such device or address
> $ cat music.mp3
> vm
> $ cat notes.txt
> ```
>
> The link leads to `/etc/hostname`, so it prints the VM's name. The last one just sits there: a named pipe waits for someone to write into it (Part 5). Press Ctrl+C. Opening a file you haven't identified can hang, which is a good reason to look before you `cat`.

### Step 2.4 Hide and seek, round 1: Ben hides, Ana and Cruz race

Ben hides a file and tells the others only one thing about it: its inode number. Use your own secret word and your own hiding place.

**Ben (Host):**

```
$ cd /srv/team/part2
$ echo 'the secret word is: pineapple' > treasure.txt
$ ls -i treasure.txt
926134 treasure.txt
$ log "round 1: hid something. its inode is 926134"
logged as student
$ mkdir -p attic/box/sock
$ mv treasure.txt attic/box/sock/laundry.txt
```

New name, new folder. Ana and Cruz read the logbook and race:

**Ana:**

```
$ tail -1 /srv/team/logbook.txt
12:14:54  student  pts/1  round 1: hid something. its inode is 926134
$ find /srv/team -inum 926134
/srv/team/part2/attic/box/sock/laundry.txt
```

**Cruz:**

```
$ find /srv/team -inum 926134
/srv/team/part2/attic/box/sock/laundry.txt
$ cat /srv/team/part2/attic/box/sock/laundry.txt
the secret word is: pineapple
```

**Log it.** Whoever found it first logs the secret word.

The name changed completely and the inode number didn't. Moving a file within one filesystem only changes directory entries, so the inode, and its number, stay exactly where they were.

### Step 2.5 Round 2: Ana hides, maybe sneakily

Ana makes a new treasure, with her own secret word, and logs its number:

**Ana:**

```
$ cd /srv/team/part2
$ echo 'the secret word is: mango' > treasure.txt
$ ls -i treasure.txt
926267 treasure.txt
$ log "round 2: hid something. its inode is 926267"
logged as ana
```

Then Ana secretly picks one of two ways to hide it.

**Way A**, a move, like Ben's:

```
$ mkdir -p shed
$ mv treasure.txt shed/rake.txt
```

**Way B**, a copy, then delete the original:

```
$ mkdir -p shed
$ cp treasure.txt shed/rake.txt
$ rm treasure.txt
```

Either way, the file ends up at `shed/rake.txt`. *Predict*, Ben and Cruz: if Ana chose Way B, what will `find` say?

**Ben (Host):**

```
$ find /srv/team -inum 926267
$
```

**Cruz:**

```
$ find /srv/team -inum 926267
$
```

Nothing, for both. `cp` made a brand-new inode with a new number, and `rm` removed the only name of the old one, so the old one is gone. The treasure can still be found by what's *in* it:

**Ben (Host):**

```
$ grep -rl 'secret word' /srv/team/part2
/srv/team/part2/shed/rake.txt
/srv/team/part2/attic/box/sock/laundry.txt
```

**Log it.** Ben and Cruz: which way did Ana hide it, and how can you tell?

### Step 2.6 Round 3: Cruz hides, Ana keeps

This time Cruz uses Way B on purpose, and Ana plays the Keeper. First Cruz makes a treasure and logs its number:

**Cruz:**

```
$ cd /srv/team/part2
$ echo 'the secret word is: guava' > treasure.txt
$ ls -i treasure.txt
926267 treasure.txt
$ log "round 3: hid something. its inode is 926267"
logged as cruz
```

Look at the number: it's the one Ana's treasure had in round 2. Ana's old inode was freed when she ran `rm`, and the next file anyone created got its number. An inode number belongs to a file only while that file exists. If `find -inum` ever turns up a file with the wrong contents, the number was recycled.

Before Cruz hides it, Ana quietly gives the treasure a second name:

**Ana:**

```
$ ln /srv/team/part2/treasure.txt /srv/team/part2/keeper.txt
$ ls -li /srv/team/part2/keeper.txt
926267 -rw-rw-r-- 2 cruz team 26 Oct  7 12:14 /srv/team/part2/keeper.txt
```

Same inode, link count 2. Now Cruz hides it with Way B:

**Cruz:**

```
$ mkdir -p cellar
$ cp treasure.txt cellar/jar.txt
$ rm treasure.txt
```

*Predict*, Ben: round 2 found nothing with `find -inum`. What about now?

**Ben (Host):**

```
$ find /srv/team -inum 926267
/srv/team/part2/keeper.txt
$ ls -li /srv/team/part2/keeper.txt
926267 -rw-rw-r-- 1 cruz team 26 Oct  7 12:14 /srv/team/part2/keeper.txt
$ cat /srv/team/part2/keeper.txt
the secret word is: guava
```

`rm` removed one name, but the inode had two, so it lived on, still holding the original. The link count dropped from 2 to 1.

**Log it.** Ben: what you found, and why the Keeper's name survived.

---

## Part 3: Links between three people

**On C's VM.** Cruz is the Host (`student`); Ana and Ben are Guests.

A hard link is a second name for the same inode. A symbolic link is a little file holding a path, like a sticky note. With several people, both kinds behave in ways that are easy to miss when you're alone.

### Step 3.1 Cruz: some shared settings

**Cruz (Host):**

```
$ mkdir -p /srv/team/part3
$ cd /srv/team/part3
$ echo '{"color": "blue", "size": 3}' > settings.json
$ ls -l settings.json
-rw-rw-r-- 1 student team 29 Oct  7 12:16 settings.json
```

### Step 3.2 Ana and Ben: a name each, in your own homes

**Ana:**

```
$ ln /srv/team/part3/settings.json ~/my_settings.json
```

**Ben:**

```
$ ln /srv/team/part3/settings.json ~/my_settings.json
$ ls -li ~/my_settings.json /srv/team/part3/settings.json
926280 -rw-rw-r-- 3 student team 29 Oct  7 12:16 /home/ben/my_settings.json
926280 -rw-rw-r-- 3 student team 29 Oct  7 12:16 /srv/team/part3/settings.json
```

One inode, link count 3, owned by `student`. Cruz's file now has names inside Ana's and Ben's home folders, places Cruz can't even look into:

**Cruz (Host):**

```
$ ls -li settings.json
926280 -rw-rw-r-- 3 student team 29 Oct  7 12:16 settings.json
$ ls ~ana ~ben
ls: cannot open directory '/home/ana': Permission denied
ls: cannot open directory '/home/ben': Permission denied
$ find / -samefile /srv/team/part3/settings.json 2>/dev/null
/srv/team/part3/settings.json
$ sudo find / -xdev -samefile /srv/team/part3/settings.json 2>/dev/null
/home/ben/my_settings.json
/home/ana/my_settings.json
/srv/team/part3/settings.json
```

(The `find` commands search the whole disk, so give them a few seconds. `2>/dev/null` throws away the many "Permission denied" complaints.) The link count says there are three names. Plain `find` finds only one, because it can only search where Cruz is allowed to look. With `sudo` it finds all three. A hard link doesn't record where its other names are; the only way to find them is to search, and you can only search where you're allowed.

### Step 3.3 Cruz: change the settings, two ways

**Cruz (Host):**

```
$ echo '{"color": "green", "size": 3}' > settings.json
```

**Ana:**

```
$ cat ~/my_settings.json
{"color": "green", "size": 3}
```

**Ben:**

```
$ cat ~/my_settings.json
{"color": "green", "size": 3}
```

Same file, so of course both see it. Now Cruz edits with `sed -i`:

**Cruz (Host):**

```
$ sed -i 's/green/red/' settings.json
$ cat settings.json
{"color": "red", "size": 3}
```

*Predict*, Ana: what does your copy say now?

**Ana:**

```
$ cat ~/my_settings.json
{"color": "green", "size": 3}
$ ls -li ~/my_settings.json /srv/team/part3/settings.json
926280 -rw-rw-r-- 2 student team 30 Oct  7 12:16 /home/ana/my_settings.json
926281 -rw-rw-r-- 1 student team 28 Oct  7 12:16 /srv/team/part3/settings.json
```

Two inodes now. `sed -i` doesn't edit a file in place. It writes a new file and renames it over the old name, so Cruz's name moved to a new inode (926281, link count 1). Ana's and Ben's names stayed with the old one, which now has a link count of 2. Nobody got an error.

*Predict*, Ben: Ana is about to change her copy. Will you see it?

**Ana:**

```
$ echo '{"color": "purple", "size": 3}' > ~/my_settings.json
```

**Ben:**

```
$ cat ~/my_settings.json
{"color": "purple", "size": 3}
```

**Cruz (Host):**

```
$ cat settings.json
{"color": "red", "size": 3}
```

The team has split in two. Ana and Ben share one file and stay in sync with each other; Cruz is on her own with another. And the Guests' copy still belongs to `student`, even though it lives in their homes. On your own machine this was a curiosity. With three people it's a real trap: nobody can tell from their own copy that it has drifted.

**Log it.** Each of you: what your copy says now, and which teammate it agrees with.

### Step 3.4 A link into a private place

**Cruz (Host):**

```
$ echo 'dear diary: I love tacos' > ~/diary.txt
$ ls -ld ~
drwxr-x--- 3 student student 4096 Oct  7 12:16 /home/student
```

**Ana:**

```
$ ln -s /home/student/diary.txt /srv/team/part3/diary-link
$ ls -l /srv/team/part3/diary-link
lrwxrwxrwx 1 ana team 23 Oct  7 12:16 /srv/team/part3/diary-link -> /home/student/diary.txt
$ cat /srv/team/part3/diary-link
cat: /srv/team/part3/diary-link: Permission denied
```

**Ben:**

```
$ cat /srv/team/part3/diary-link
cat: /srv/team/part3/diary-link: Permission denied
```

**Cruz (Host):**

```
$ cat /srv/team/part3/diary-link
dear diary: I love tacos
```

The same link, three readers, two results. `ln -s` didn't check anything; it wrote down a path. Whoever follows the link walks that path with their own permissions, and Cruz's home folder, locked in Step 0.8, lets nobody else in. A symlink can point anywhere; it can't take anyone anywhere they couldn't already go. (If Ana or Ben *can* read the diary, Cruz skipped `chmod 750 ~` on this VM.)

> **Experiment: a folder you can walk through but not look into.** For a directory, `r` means "list the names" and `x` means "pass through". Cruz gives everyone else pass-through only:
>
> ```
> $ chmod 751 ~
> $ ls -ld ~ ~/diary.txt
> drwxr-x--x 3 student student 4096 Oct  7 12:16 /home/student
> -rw-rw-r-- 1 student student   25 Oct  7 12:16 /home/student/diary.txt
> ```
>
> Ana tries both again:
>
> ```
> $ cat /srv/team/part3/diary-link
> dear diary: I love tacos
> $ ls ~student
> ls: cannot open directory '/home/student': Permission denied
> ```
>
> Ana can reach a file whose name she already knows, but can't list the folder to discover any names. Then Cruz tries it as the visitor: `sudo -u visitor cat /home/student/diary.txt` prints the diary too. `x` for others means *everyone*, and the diary itself is readable by everyone (`-rw-rw-r--`). Hiding a name isn't the same as locking a file. Cruz puts it back with `chmod 750 ~`.

### Step 3.5 A live switch, seen two ways

Plenty of servers run whatever is in a folder called `current`, which is a symlink to the release in use. Switching versions means switching the link. Here Cruz deploys, and the two Guests are users who notice in different ways.

**Cruz (Host):**

```
$ mkdir -p releases/v1 releases/v2
$ echo 'version 1' > releases/v1/app.txt
$ echo 'version 2' > releases/v2/app.txt
$ ln -s releases/v1 current
```

Ben steps *into* the release, through the link:

**Ben:**

```
$ cd /srv/team/part3/current
$ cat app.txt
version 1
```

Ana starts watching. This loop reads the file through the link once a second:

**Ana:**

```
$ while true; do cat /srv/team/part3/current/app.txt; sleep 1; done
version 1
version 1
version 1
```

Leave it running. Cruz switches:

**Cruz (Host):**

```
$ ln -sfn releases/v2 current
$ log "switched current to v2"
logged as student
```

On Ana's screen, within a second:

```
version 1
version 2
version 2
```

Ana presses Ctrl+C. *Predict*, Ben: what will `cat app.txt` print in your shell?

**Ben:**

```
$ cat app.txt
version 1
$ pwd -P
/srv/team/part3/releases/v2
$ ls -l /proc/$$/cwd
lrwxrwxrwx 1 ben ben 0 Oct  7 12:16 /proc/26375/cwd -> /srv/team/part3/releases/v1
$ cat /srv/team/part3/current/app.txt
version 2
```

Ana's loop was never restarted, and nobody told it anything. Each `cat` follows the link afresh, so the moment the link changed, every new read went to v2. Ben's shell stayed behind. When he ran `cd`, the shell followed the link once and settled into the real folder, `v1`; switching the link doesn't move him. `pwd -P` gets this wrong: it re-reads the link and reports where the link points *now*. `/proc/$$/cwd` asks the kernel where Ben's shell actually is. Real deployments run into the same thing: a program that started inside the old release keeps running the old release until it's restarted.

**Log it.** Ana: the time you saw the change. Ben: what your shell still shows. Compare with Cruz's entry.

> **Experiment: a hard link the kernel refuses.** Cruz:
>
> ```
> $ echo 'mine' > locked.txt
> $ chmod 644 locked.txt
> ```
>
> Ben:
>
> ```
> $ cat /srv/team/part3/locked.txt
> mine
> $ ln /srv/team/part3/locked.txt ~/grab.txt
> ln: failed to create hard link '/home/ben/grab.txt' => '/srv/team/part3/locked.txt': Operation not permitted
> ```
>
> Ben can read the file but can't give it another name, while in Step 3.2 he could. The difference: `settings.json` was group-writable, and `locked.txt` isn't. Ubuntu switches on a rule that only lets you hard link files you own or can write to. Only root can read the setting on the lab VMs:
>
> ```
> $ sudo sysctl fs.protected_hardlinks
> fs.protected_hardlinks = 1
> ```
>
> The rule exists because planting a hard link to someone else's file in the right place used to be a way to trick privileged programs into changing that file.

---

## Part 4: Someone else's program, seen through `/proc`

**On A's VM.** Ana is the Host (`student`); Ben and Cruz are Guests.

`/proc` has a folder for every running program. With several people on the machine, some of what's in those folders is open to everyone, and some isn't. Ana runs a program with a secret; Ben and Cruz find out as much about it as they can without asking.

### Step 4.1 Ana: run a program with a secret

Ana creates this in her home folder, which the Guests can't read:

**Ana (Host):**

```
$ nano ~/mystery.py
```

```python
# mystery.py: a program with a secret. Run it as:  python3 ~/mystery.py <your secret word>
import os
import sys
import time

secret = sys.argv[1] if len(sys.argv) > 1 else "nothing"
note = os.path.expanduser("~/note.txt")

with open(note, "w") as f:
    f.write(f"The note says: meet at the {secret}.\n")

held = open(note)            # keep the note open...
os.remove(note)              # ...and delete its only name

print("Mystery program running. Press Ctrl+C to stop it.")
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("\nStopped.")
```

Pick a secret word (a place works well), don't say it, and run:

**Ana (Host):**

```
$ python3 ~/mystery.py library
Mystery program running. Press Ctrl+C to stop it.
```

Leave it running.

### Step 4.2 Ben and Cruz: investigate

Split the questions: Ben takes the first three, Cruz the rest. Keep notes on what worked and what didn't, then compare.

**Ben:** Is it running, and what's its number?

```
$ pgrep -u student -a python3
25513 python3 /home/student/mystery.py library
```

`-u student` limits the search to the Host's programs, and `-a` shows the whole command line. That already gives away the secret word. **Log it** right away.

**Ben:** How long has it been running?

```
$ ps -o pid,user,etime,args -p 25513
  PID USER         ELAPSED COMMAND
25513 student        00:01 python3 /home/student/mystery.py library
```

**Ben:** Where do `ps` and `pgrep` get the command line? From a file, naturally:

```
$ tr '\0' ' ' < /proc/25513/cmdline; echo
python3 /home/student/mystery.py library
```

Inside `cmdline` the words are separated by zero bytes, which aren't printable; `tr` turns them into spaces. (Try `cat /proc/25513/cmdline`: depending on your terminal, the words either run together or come out with odd gaps.)

**Cruz:** What state is it in, and how much memory is it using?

```
$ grep -E '^(Name|State|Uid|VmRSS)' /proc/25513/status
Name:	python3
State:	S (sleeping)
Uid:	1000	1000	1000	1000
VmRSS:	    8556 kB
```

**Cruz:** Which folder is it running in? Which files does it have open? What are its settings?

```
$ ls -l /proc/25513/cwd
ls: cannot read symbolic link '/proc/25513/cwd': Permission denied
lrwxrwxrwx 1 student student 0 Oct  7 12:13 /proc/25513/cwd
$ ls /proc/25513/fd
ls: cannot open directory '/proc/25513/fd': Permission denied
$ cat /proc/25513/environ
cat: /proc/25513/environ: Permission denied
```

**Cruz:** Can you read the program itself?

```
$ cat ~student/mystery.py
cat: /home/student/mystery.py: Permission denied
```

**Log it.** Ben and Cruz: two short lists between you. What you could learn about Ana's program, and what was closed to you.

The pattern: anyone can see *that* a program runs, who owns it, how it was started and how busy it is. Only the owner can see *inside* it: its open files, its working folder, its environment. The command line is on the public side, which has a practical lesson: never type a password as part of a command (some database tools allow `-pSECRET`, for example). While that command runs, every user on the machine can read it from `/proc`.

### Step 4.3 Ana: the private side

Ana opens a second connection to her VM (the same `ssh` command, in a new window), so the mystery program keeps running in the first.

**Ana (Host)**, second window:

```
$ ls -l /proc/25513/fd
total 0
lrwx------ 1 student student 64 Oct  7 12:13 0 -> /dev/pts/1
lrwx------ 1 student student 64 Oct  7 12:13 1 -> /dev/pts/1
lrwx------ 1 student student 64 Oct  7 12:13 2 -> /dev/pts/1
lr-x------ 1 student student 64 Oct  7 12:13 3 -> '/home/student/note.txt (deleted)'
```

Descriptor 3 is a file with no name left. The program wrote a note, kept it open and deleted it, just like `ghost.py` in the solo lab. The note still exists as long as the program holds it, and its owner can copy it out through `/proc`. Ana rescues it into the team folder:

**Ana (Host):**

```
$ mkdir -p /srv/team/part4
$ cp /proc/25513/fd/3 /srv/team/part4/rescued.txt
```

**Ben:**

```
$ cat /srv/team/part4/rescued.txt
The note says: meet at the library.
```

**Log it.** Ben: the rescued note. Then Ana stops the mystery program with Ctrl+C in the first window:

```
^C
Stopped.
```

### Step 4.4 Swap: Ben's secret

Ben creates his own `~/mystery.py` with the same code (Ana's copy is out of reach) and runs it with a new secret word:

**Ben:**

```
$ python3 ~/mystery.py bakery
Mystery program running. Press Ctrl+C to stop it.
```

Now Cruz investigates a fellow Guest, and Ana investigates as the Host. Cruz first:

**Cruz:**

```
$ pgrep -u ben -a python3
25548 python3 /home/ben/mystery.py bakery
$ ls /proc/25548/fd
ls: cannot open directory '/proc/25548/fd': Permission denied
$ cat ~ben/mystery.py
cat: /home/ben/mystery.py: Permission denied
```

The same walls. Two Guests are no closer to each other than to the Host. Ana tries without `sudo`, then with it:

**Ana (Host):**

```
$ ls /proc/25548/fd
ls: cannot open directory '/proc/25548/fd': Permission denied
$ sudo ls -l /proc/25548/fd
total 0
lrwx------ 1 ben ben 64 Oct  7 12:13 0 -> /dev/pts/3
lrwx------ 1 ben ben 64 Oct  7 12:13 1 -> /dev/pts/3
lrwx------ 1 ben ben 64 Oct  7 12:13 2 -> /dev/pts/3
lr-x------ 1 ben ben 64 Oct  7 12:13 3 -> '/home/ben/note.txt (deleted)'
$ sudo cat /proc/25548/fd/3
The note says: meet at the bakery.
```

Everything opens. Cruz tries to do the same:

**Cruz:**

```
$ sudo ls /proc/25548/fd
[sudo] password for cruz:
cruz is not in the sudoers file.  This incident will be reported.
```

("Reported" means a line in the system's log files, which the Host can read.) Ben stops his program with Ctrl+C.

**Log it.** Each of you: one line on what `sudo` changed.

---

## Part 5: Pipes between three people

**On B's VM.** Ben is the Host (`student`); Ana and Cruz are Guests.

A named pipe has a name in a folder, so any program that can reach the folder can find it. Put pipes in `/srv/team` and the three of you can pass text through them.

### Step 5.1 Ben: one pipe per person

Each pipe is someone's inbox, named after the account that reads it:

**Ben (Host):**

```
$ mkdir -p /srv/team/part5
$ cd /srv/team/part5
$ mkfifo to_student to_ana to_cruz
$ ls -l
total 0
prw-rw-r-- 1 student team 0 Oct  7 12:15 to_ana
prw-rw-r-- 1 student team 0 Oct  7 12:15 to_cruz
prw-rw-r-- 1 student team 0 Oct  7 12:15 to_student
$ sudo -u visitor cat /srv/team/part5/to_ana
cat: /srv/team/part5/to_ana: Permission denied
```

Ben's inbox is `to_student`, because on his own VM that's who he is. The visitor can't even reach the pipes: `/srv/team` itself keeps them out.

### Step 5.2 One way

Ana listens on her inbox:

**Ana:**

```
$ cat /srv/team/part5/to_ana
```

It sits and waits. Cruz writes into it:

**Cruz:**

```
$ cat > /srv/team/part5/to_ana
```

Cruz types a few lines, pressing Enter after each. They show up on Ana's screen as Cruz goes:

```
hi Ana, it's Cruz
this went through a pipe on Ben's VM
```

Then Cruz presses Ctrl+D. Ana's `cat` ends too: when the last writer closes the pipe, the reader gets end-of-file. Check the size afterwards with `ls -l`: still 0. The bytes went through the kernel, never the disk.

### Step 5.3 One pipe, two voices

Ben listens on his inbox:

**Ben (Host):**

```
$ cat /srv/team/part5/to_student
```

*Both* Guests write into it at once:

**Ana:**

```
$ cat > /srv/team/part5/to_student
```

**Cruz:**

```
$ cat > /srv/team/part5/to_student
```

Take turns typing, and start each line with your name so Ben can tell you apart. Ben sees one stream with both voices in it:

```
ana: hello Ben
cruz: hi from me too
ana: gotta go
```

Lines stay whole, because Linux never splits a single write of up to 4096 bytes into a pipe. *Predict*: Ana presses Ctrl+D. Does Ben's `cat` end?

It doesn't. A reader only gets end-of-file when the *last* writer leaves. Cruz types one more line, and it still arrives:

```
cruz: still here
```

Then Cruz presses Ctrl+D, and Ben's `cat` ends.

> **Experiment: everyone writing, nobody reading.** All three of you run *only* a writer, each into someone else's inbox: Ana `cat > /srv/team/part5/to_cruz`, Cruz `cat > /srv/team/part5/to_student`, Ben `cat > /srv/team/part5/to_ana`. Type something. Nothing arrives, ever. Opening a pipe for writing waits until someone opens it for reading, and here all three of you are waiting at a door for someone else to come through. Press Ctrl+C. That's why a chat program has to start reading first.

### Step 5.4 A group chat made of pipes

Ben creates this file in the shared folder:

**Ben (Host):**

```
$ nano /srv/team/part5/fifochat.py
```

```python
# fifochat.py: a group chat over named pipes.
# Each person reads from their own pipe, to_<name>, and writes into everyone else's.
import glob
import os
import pwd
import sys
from threading import Thread

FOLDER = "/srv/team/part5"
me = pwd.getpwuid(os.getuid()).pw_name
inbox = f"{FOLDER}/to_{me}"
outboxes = sorted(p for p in glob.glob(f"{FOLDER}/to_*") if p != inbox)


def listen():
    with open(inbox) as pipe:                  # waits until someone opens it for writing
        for line in pipe:                      # one line per message
            print(line, end="", flush=True)
    print("(everyone else has left)")


Thread(target=listen, daemon=True).start()    # read your own pipe in the background...

print(f"Waiting for {len(outboxes)} teammates...")
pipes = {}
for path in outboxes:                          # ...while opening everyone else's for writing
    pipes[path] = open(path, "w")              # waits until that person is listening
print(f"Connected as {me}. Type a line and press Enter. Ctrl+D to leave.")

for line in sys.stdin:                         # every line you type
    for path, pipe in list(pipes.items()):
        try:
            pipe.write(f"{me}: {line}")        # goes into each teammate's pipe, signed
            pipe.flush()
        except BrokenPipeError:                # nobody is reading that pipe any more
            print(f"({os.path.basename(path)[3:]} has left)")
            del pipes[path]
            try:
                pipe.close()
            except BrokenPipeError:
                pass
```

The parts worth reading closely:

- `glob.glob(f"{FOLDER}/to_*")` finds every inbox in the folder. Your own is skipped; everyone else's becomes an outbox. Nobody has to tell the program who's on the team.
- A thread reads your own inbox in the background. It starts first, and that's what avoids the deadlock from the experiment above.
- Opening each outbox waits until its owner is listening, so the program says "Waiting..." until all three of you have started it.
- Every line you type is written into every outbox, signed with the name the system knows you by.
- When someone leaves, writing to their pipe fails with `BrokenPipeError`, because nobody is reading it any more. The program notes it and stops writing there.

All three of you start it, in any order:

**Everyone:**

```
$ python3 /srv/team/part5/fifochat.py
Waiting for 2 teammates...
Connected as ana. Type a line and press Enter. Ctrl+D to leave.
```

("Connected" appears once the last of you has started it.) Chat for a bit. After Ana, Ben and Cruz have each sent one line, Ana's screen shows:

```
hola from ana
student: ben says hi
cruz: cruz here, I see you both
```

Ben's messages arrive signed `student`: the program asked the kernel, and on this VM that's who Ben is. When Ana presses Ctrl+D, the others see nothing until they next type. Then:

```
did Ana leave?
(ana has left)
```

When both Guests have left, Ben sees `(everyone else has left)`.

**Log it.** Each of you copies one line you received into the logbook.

---

## Part 6: A chat room that knows who's talking

**On C's VM.** Cruz is the Host (`student`); Ana and Ben are Guests.

The solo lab's chat server used a TCP socket, reached by an address and a port number. With several people on the machine, it matters who can connect, and whether the server can tell who connected. TCP and Unix sockets answer those questions very differently.

### Step 6.1 TCP with `nc`, and an observer

**Cruz (Host):**

```
$ nc -l 5007
```

**Ana:**

```
$ nc localhost 5007
```

Type in either window and press Enter; it shows up in the other. Leave it connected. Ben is the observer, looking at the machine's connection table:

**Ben:**

```
$ ss -tn | grep 5007
ESTAB  0       0              127.0.0.1:54614         127.0.0.1:5007
ESTAB  0       0              127.0.0.1:5007          127.0.0.1:54614
$ ss -tnp | grep 5007
ESTAB  0       0              127.0.0.1:54614         127.0.0.1:5007
ESTAB  0       0              127.0.0.1:5007          127.0.0.1:54614
```

Two lines, one for each end of the conversation: Ana's end on port 54614, Cruz's on 5007. `-p` asks which program owns each end, and Ben gets no answer for either. Cruz opens a second window on her VM and asks the same question:

**Cruz (Host)**, second window:

```
$ ss -tnp | grep 5007
ESTAB  0       0              127.0.0.1:54614         127.0.0.1:5007
ESTAB  0       0              127.0.0.1:5007          127.0.0.1:54614   users:(("nc",pid=26533,fd=4))
```

Cruz sees her own end's program, and nothing for Ana's. Anyone can see that a connection exists; only the owner can see whose program is behind each end.

Ana presses Ctrl+C. Cruz's `nc` ends too, since `nc -l` serves one connection and quits.

### Step 6.2 TCP doesn't ask who's calling

**Cruz (Host):**

```
$ nc -l 5007
```

**Cruz (Host)**, second window:

```
$ sudo -u visitor nc localhost 5007
visitor sneaking in
```

The visitor's message appears in the first window. A port number has no owner and no permission bits: any user on the machine can connect to it. And all the listening side learns is an address and a port number like `127.0.0.1:54614`, not who's typing. Press Ctrl+C in both.

### Step 6.3 Ana: open a room

A Unix socket is a file, so it has an owner, a group and permissions. And because both ends are on the same machine, the kernel knows which user is on each end, and will tell the server if asked.

**Ana:**

```
$ mkdir -p /srv/team/part6
$ nano /srv/team/part6/team_room.py
```

```python
# team_room.py: a chat room on a Unix socket. The kernel tells the room who each caller is.
import datetime
import os
import pwd
import socket
import struct
from threading import Lock, Thread

ADDRESS = "/srv/team/part6/room.sock"
LOGBOOK = "/srv/team/logbook.txt"

members = []        # one writable stream per person currently in the room
lock = Lock()       # only one thread at a time may change the list or send to everyone


def caller_name(conn):
    """Ask the kernel which user is on the other end of this connection."""
    raw = conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
    pid, uid, gid = struct.unpack("3i", raw)      # three numbers: process, user, group
    return pwd.getpwuid(uid).pw_name


def say_to_all(text):
    print(text, end="", flush=True)               # the room's own terminal sees everything
    with lock:
        for out in members:
            try:
                out.write(text)
                out.flush()
            except OSError:
                pass                              # that person just left; skip them


def serve(conn):
    name = caller_name(conn)
    incoming = conn.makefile("r", encoding="utf-8")
    outgoing = conn.makefile("w", encoding="utf-8")
    with lock:
        members.append(outgoing)
    say_to_all(f"* {name} joined\n")
    try:
        for line in incoming:                     # read the connection like a text file
            say_to_all(f"{name}: {line}")
            with open(LOGBOOK, "a") as book:      # and keep a signed copy in the logbook
                when = datetime.datetime.now().strftime("%H:%M:%S")
                book.write(f"{when}  {name:<8} room   {line}")
    finally:
        with lock:
            members.remove(outgoing)
        say_to_all(f"* {name} left\n")
        conn.close()


if os.path.exists(ADDRESS):
    os.remove(ADDRESS)                            # a leftover socket file would block bind()

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(ADDRESS)                              # creates room.sock on disk
os.chmod(ADDRESS, 0o660)                          # owner and group may connect, nobody else
server.listen()
print(f"Room open at {ADDRESS}. Press Ctrl+C to close it.")
try:
    while True:
        conn, _ = server.accept()
        Thread(target=serve, args=(conn,), daemon=True).start()
except KeyboardInterrupt:
    print("\nRoom closed.")
finally:
    server.close()
    os.remove(ADDRESS)                            # tidy up the socket file
```

The parts worth reading closely:

- `caller_name` is the new idea. `SO_PEERCRED` asks the kernel for the *credentials of the peer*: the process number, user number and group number of whoever is on the other end. The room never asks anyone their name, and nobody can type a fake one.
- Each caller gets their own thread (`serve`), so all three of you can be in the room at once. `say_to_all` sends a line to everyone, and the `lock` makes sure two threads never change the member list at the same moment.
- Each connection gets two file objects: `incoming` to read lines from, the same way you'd loop over a text file, and `outgoing` for the room to write to.
- `os.chmod(ADDRESS, 0o660)` sets the socket file's permissions: owner and group may connect, everyone else may not.

Run it:

**Ana:**

```
$ python3 /srv/team/part6/team_room.py
Room open at /srv/team/part6/room.sock. Press Ctrl+C to close it.
```

Leave it running. Ana opens a second window on Cruz's VM to join her own room. Then all three of you join:

**Everyone** (Ana in her second window):

```
$ nc -U /srv/team/part6/room.sock
```

`-U` tells `nc` the address is a Unix socket file. Say something. After Cruz, Ben and Ana have each sent a line, Cruz's screen shows:

```
* student joined
* ben joined
* ana joined
hello room, Cruz here
student: hello room, Cruz here
ben: Ben here
ana: and Ana makes three
```

Your own line appears twice: once as you type it, and once when the room sends it back to everyone with your name on it. The room's own window shows every line too. Ana leaves the room (Ctrl+C in her second window) and looks at the socket file and the logbook:

**Ana**, second window:

```
$ ls -l /srv/team/part6/room.sock
srw-rw---- 1 ana team 0 Oct  7 12:16 /srv/team/part6/room.sock
$ tail -3 /srv/team/logbook.txt
12:16:54  student  room   hello room, Cruz here
12:16:54  ben      room   Ben here
12:16:55  ana      room   and Ana makes three
```

The room signed those lines itself, with names it got from the kernel.

### Step 6.4 Who may come in

**Cruz (Host)**, second window:

```
$ sudo -u visitor nc -U /srv/team/part6/room.sock
nc: unix connect failed: Permission denied
nc: /srv/team/part6/room.sock: Permission denied
```

The same visitor walked straight into the TCP chat in Step 6.2. Now Ana, who owns the socket file, takes write permission away from the group:

**Ana**, second window:

```
$ chmod 640 /srv/team/part6/room.sock
$ ls -l /srv/team/part6/room.sock
srw-r----- 1 ana team 0 Oct  7 12:16 /srv/team/part6/room.sock
```

Cruz and Ben are still in the room. *Predict*: can they still talk?

**Ben:**

```
am I still in after chmod?
```

It gets through, and Cruz sees it. Permissions are checked when you connect, and anyone already inside stays inside. Now Ben leaves (Ctrl+C) and tries to come back:

**Ben:**

```
$ nc -U /srv/team/part6/room.sock
nc: unix connect failed: Permission denied
nc: /srv/team/part6/room.sock: Permission denied
```

The group can still *read* the file, but connecting to a Unix socket counts as *writing* to it. Ana puts it back with `chmod 660 /srv/team/part6/room.sock`, and Ben can join again.

Here's everything Part 6 found, side by side:

| Who tries to connect | TCP port 5007 | `room.sock` with `rw-rw----` | `room.sock` with `rw-r-----` |
|---|---|---|---|
| a teammate (in `team`) | connected | connected | Permission denied (unless already inside) |
| visitor (not in `team`) | connected | Permission denied | Permission denied |
| Does the server learn the caller's name? | no, only a port number | yes, from the kernel | |

**Log it.** One line each: what surprised you most in this table.

### Step 6.5 Close the room

Everyone leaves with Ctrl+C. Then Ana presses Ctrl+C in the room's window:

```
^C
Room closed.
```

The program removes `room.sock` on the way out (check with `ls /srv/team/part6`). A socket file is a name in a folder, and names stay until someone removes them.

> **Experiment: the barber with one chair.** Ana copies the room and changes one line in the copy:
>
> ```
> $ cd /srv/team/part6
> $ cp team_room.py one_chair.py
> $ nano one_chair.py
> ```
>
> Near the bottom, replace
>
> ```python
>         Thread(target=serve, args=(conn,), daemon=True).start()
> ```
>
> with
>
> ```python
>         serve(conn)                               # one caller at a time
> ```
>
> Ana runs `python3 one_chair.py`. Cruz joins with `nc -U /srv/team/part6/room.sock` and chats. Then Ben joins and types something. *Predict* what Ben sees. Answer: nothing at all, not even "joined". Ben's connection was accepted by the kernel and is waiting in line, but the program is busy with Cruz and won't call `accept()` again until Cruz leaves. When Cruz presses Ctrl+C, Ben suddenly gets "joined", followed by the line he typed while waiting. Nothing was lost; it sat in the kernel's buffer the whole time. That's why the real room gives each caller a thread.

> **Experiment: across machines.** Everything in this lab happened on one VM at a time. A Unix socket can only ever work that way: it's a file on one machine's disk. TCP can cross machines, which is why the internet runs on it, and it's also why TCP can't tell the server who's calling: the other end could be any computer anywhere. Proving who you are across a network takes passwords or keys, which is what SSH has been doing for you every time you log in. If your class has found that lab VMs can reach each other, try Step 6.1 between two VMs: run `hostname -I` on Cruz's VM and give that address to `nc` on Ana's VM, instead of `localhost`.

---

## Reflection

Answer these on your own. Short answers are fine. Where a question asks "why", point to something you saw in the lab.

1. In Step 0.6, the Host was added to `team` but still got `Permission denied` until logging in again. In Step 1.7, Ben and Cruz used `newgrp` instead. What do the two fixes have in common?
2. In Step 0.8, your teammates could read files in your home folder until you ran `chmod 750 ~`. What decided the folder's permissions in the first place, and why would the same step behave differently on Ubuntu 22.04?
3. In Part 1, `echo` into Ben's terminal was refused but `write ben` got through. Explain the difference, and say why `wall` reached Ben but not Cruz.
4. In Part 2, the treasure could be found by its inode number after `mv`, but not after `cp` followed by `rm`, unless someone had made a hard link first. Explain all three cases using names and inodes.
5. In Part 3, after Cruz ran `sed -i`, Ana and Ben stayed in sync with each other but not with Cruz. Draw or describe which names pointed at which inodes, before and after.
6. In Part 3, the same symlink worked for Cruz and failed for Ana and Ben. What decides whether following a link works?
7. In Part 4, list what one user could and couldn't learn about another user's running program. Why is it a bad idea to type a password as part of a command?
8. In Part 5, why did the group chat need to start reading before it started writing?
9. In Part 6, anyone could connect to the TCP port, but only the team could enter the room. Name two things the Unix socket gave you that TCP didn't.
10. Describe one moment in this lab where you couldn't have finished a step without one of your teammates.

---

## Cleanup: take your VM apart

**On all three VMs, each Host on their own VM.** The examples show Ana's VM.

You'll be in a different team next time, so take everything this lab built back down: your teammates' accounts, the visitor, the team group and the team folder. Taking a machine apart cleanly is a skill of its own, and a couple of the steps below show why the order and the details matter.

### Step C.1 Save what you want

The team folder is about to be deleted. If you want the logbook, print it now and copy it somewhere:

**Ana (Host):**

```
$ cat /srv/team/logbook.txt
```

### Step C.2 Guests: leave

Each Guest types `exit` in their window on this VM. Then the Host checks who's still here:

**Ana (Host):**

```
$ who
student  pts/1        Oct  7 12:14
```

Only `student` should be left.

### Step C.3 Find what your Guests own outside their homes

`userdel -r` deletes a user's home folder, but not files they made anywhere else. Find those first:

**Ana (Host):**

```
$ sudo find / -xdev -user ben -not -path '/home/ben*' 2>/dev/null
/srv/team/log
$ sudo find / -xdev -user cruz -not -path '/home/cruz*' 2>/dev/null
```

- `-user ben` matches files owned by `ben`.
- `-not -path '/home/ben*'` skips his home folder, which `userdel -r` will take care of.
- `-xdev` stays on this disk instead of wandering into `/proc` and `/sys`.

On Ana's VM, Ben owns the `log` tool he built in Step 0.10, and Cruz owns nothing outside her home. On B's and C's VMs, the lists will be longer: the hide-and-seek files, the mystery files, the room.

### Step C.4 Remove the accounts

**Ana (Host):**

```
$ sudo pkill -u ben
$ sudo userdel -r ben
userdel: ben mail spool (/var/mail/ben) not found
$ sudo pkill -u cruz
$ sudo userdel -r cruz
userdel: cruz mail spool (/var/mail/cruz) not found
$ sudo userdel -r visitor
userdel: visitor mail spool (/var/mail/visitor) not found
```

If a Guest forgot to log out, `userdel` refuses with `user ben is currently used by process 25611`. `pkill -u ben` ends all of that user's programs, which also closes their SSH connection; on Ben's screen it shows up as `Connection to ... closed by remote host.` Then `userdel` works.

### Step C.5 Orphans

*Predict*: Ben's account is gone. Who owns the `log` file now?

**Ana (Host):**

```
$ ls -l /srv/team
total 12
-rwxrwxr-x 1    1001 team  744 Oct  7 12:11 log
-rw-rw-r-- 1 student team  171 Oct  7 12:11 logbook.txt
drwxrwsr-x 2 student team 4096 Oct  7 12:13 part4
```

`1001`, a bare number. A file's inode never stored the name `ben`, only his user number. `ls` used to translate 1001 into `ben` by looking it up in `/etc/passwd`, and that line is gone. Files like this are called orphans, and `find` can list them all:

**Ana (Host):**

```
$ sudo find / -xdev \( -nouser -o -nogroup \) 2>/dev/null
/run/sudo/ts/cruz
/srv/team/log
```

(`/run/sudo/ts/cruz` is a tiny file `sudo` made when Cruz tried it in Step 4.4. It lives in `/run`, which is emptied every time the VM restarts.)

Here's why orphans matter. *Predict*: what number will the next new account get?

**Ana (Host):**

```
$ sudo useradd -m newbie
$ id newbie
uid=1001(newbie) gid=1002(newbie) groups=1002(newbie)
$ ls -l /srv/team/log
-rwxrwxr-x 1 newbie team 744 Oct  7 12:11 /srv/team/log
$ sudo userdel -r newbie
```

`useradd` picks the next number after the highest one in use, and with Ben and Cruz gone that's 1001 again. So the next person you create inherits every file Ben left behind, without anyone handing them over. In a few weeks that could be a teammate from a different team, owning last month's files. That's why the next step deletes the team folder, and why Step 0.2 cleans up before building anything.

In everyday cleanup you'd usually delete the files first and the accounts second, so no orphans ever appear. This lab did it the other way round so you could see one.

### Step C.6 Remove the team folder and the group

**Ana (Host):**

```
$ sudo rm -rf /srv/team
$ sudo groupdel team
```

`rm -rf` deletes without asking, and there's no undo. Read the line before you press Enter: `sudo rm -rf /srv/team` and `sudo rm -rf / srv/team`, with one stray space, are very different commands.

If you made any other groups during the lab (`bc` from Step 1.7, if it wasn't deleted then), remove them too: `getent group bc`, then `sudo groupdel bc`.

### Step C.7 Tidy your own account

Your `student` account still has a few things from this lab: the `log` alias, the mystery program, the diary.

**Ana (Host):**

```
$ sed -i '/alias log=/d' ~/.bashrc
$ rm -f ~/mystery.py ~/diary.txt
```

`sed -i '/alias log=/d'` deletes every line containing `alias log=` from your `.bashrc`. Your home folder stays at `750`: leaving it private is the better default anyway.

### Step C.8 Check that it's clean

**Ana (Host):**

```
$ awk -F: '$3 >= 1000 && $3 < 60000 {print $1}' /etc/passwd
student
$ getent group team
$ ls /srv
$ id
uid=1000(student) gid=1000(student) groups=1000(student),27(sudo),1001
```

Only `student` is left, there's no `team` group, and `/srv` is empty. But `id` still lists `1001`: the group is gone, and its number is still on your badge, which was printed when you logged in. Log out and back in, and it disappears.

Next lab, with a new team, starts again at Part 0, and Step 0.2 catches anything you missed here.

> **Never delete `student`.** Every command in this section names an account, so read each one before you press Enter. If `student` is gone, the only way back into your VM is to have it reset, which wipes everything on it.

---

## Troubleshooting

| What you see | Likely cause | What to do |
|---|---|---|
| `Permission denied` in `/srv/team` right after setup | Group membership is read at login (Step 0.6) | Log out and connect again, then check `id` |
| A teammate can't log in | Wrong name, wrong port, or a typo in the temporary password | Use the Host's port with the teammate's name; the Host can reset it with `sudo passwd ben` |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` when connecting | That VM was reset since you last connected | On your own computer: `ssh-keygen -R "[lab-xxxxxxxx.eastus.cloudapp.azure.com]:5037"` with that VM's address and port, then connect again |
| `useradd: user 'ben' already exists` or `groupadd: group 'team' already exists` | Left over from an earlier lab | See Step 0.2 |
| Teammates can read your home folder | Home folders on Ubuntu 20.04 start as `drwxr-xr-x` | `chmod 750 ~` (Step 0.8) |
| `log: command not found` | The alias isn't loaded in this window | `source ~/.bashrc`, or type the full `/srv/team/log` |
| `/srv/team/log: Permission denied` | The script isn't executable | `chmod +x /srv/team/log` (whoever created it) |
| A teammate can't change a file you made | Your `umask` is `0022` (Step 0.9) | `chmod g+w thefile` now, and `umask 002` for next time |
| `-bash: !great: event not found`, or an old command shows up inside a log line | Inside double quotes, bash treats `!` as "something from your history" | Use single quotes: `log 'wow!great'` |
| `chgrp: changing group of '/dev/pts/3': Operation not permitted` | You're not in that group in this shell | `newgrp groupname`, or log out and in (Step 1.7) |
| `write: ben has messages disabled` | Ben ran `mesg n` | Ask Ben to run `mesg y` (and then `chmod o-w $(tty)`) |
| `cp: cannot stat 'treasure.txt': No such file or directory` | You're in a different folder, or skipped making the treasure | `cd /srv/team/part2`, then `ls` (Step 2.5) |
| `mkdir: cannot create directory ... Permission denied` in `/srv/team/partN` | Whoever made the folder had umask `0022` | The folder's owner runs `chmod -R g+w /srv/team/partN` |
| `cat: /proc/sys/fs/protected_hardlinks: Permission denied` | Only root may read it on the lab VMs | `sudo sysctl fs.protected_hardlinks` |
| A command just sits there | A named pipe waiting for its other end (Parts 2 and 5) | Open the other end, or press Ctrl+C |
| `fifochat.py` stays at `Waiting for 2 teammates...` | Someone hasn't started it yet | All three run it; it connects when the last one starts |
| `pgrep` prints nothing | The program isn't running, or it's a different user | Check the name after `-u`, and that the program is still running |
| `nc: unix connect failed: Permission denied` | Not in `team`, the socket isn't group-writable, or you haven't logged in again since joining `team` | `ls -l` the socket file, and run `id` |
| `nc: ... room.sock: No such file or directory` or `Connection refused` | The room isn't running | Start `team_room.py` first |
| `userdel: user ben is currently used by process ...` | Ben is still logged in, or has something running | `sudo pkill -u ben`, then `userdel` again |
| `sudo` asks for a password | That's normal | It wants the Host's own `student` password |
| The VM stops in the middle of the lab | The lab's automatic shutdown, or the owner's quota ran out | The owner restarts it from the Azure Lab Services page |

---

## Quick reference: who got in?

| Thing | What decides access | Teammate | Visitor | Root |
|---|---|---|---|---|
| `/srv/team` and everything in it | the folder: `drwxrws---`, group `team` | yes | no | yes |
| Your home folder, after `chmod 750 ~` | `drwxr-x---` | no | no | yes |
| Your terminal, `/dev/pts/N`, by default | `crw--w----`, group `tty` | only through `write` | no | yes |
| Your terminal after `chgrp team` | group `team` may write | yes | no | yes |
| Your terminal after `mesg y` | also opens it to everyone else | yes | yes | yes |
| `write` | setgid `tty`, and it checks `mesg` | yes, if you allow it | yes, if you allow it | yes |
| `wall` | not setgid since 2024: only terminals the sender could write to | some | no | everyone, with `sudo` |
| A running program's command line and status | readable by everyone | yes | yes | yes |
| A running program's open files and working folder | owner only | no | no | yes |
| A named pipe in `/srv/team` | the folder, then the pipe's own permissions | yes | no | yes |
| A TCP port | nothing at all | yes | yes | yes |
| A Unix socket file | the folder, then the socket's own permissions (connecting needs `w`) | yes, with `rw-rw----` | no | yes |
| Files left by a deleted user | the bare user number in the inode | whoever gets that number next | | yes |
