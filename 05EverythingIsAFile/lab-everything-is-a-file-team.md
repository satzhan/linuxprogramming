# Everything Is a File, Together: A Team Lab

## Why do this with someone else

In the solo lab you were the only person on your machine. You made a named pipe, and you were the writer and the reader. You started a chat server, and you were the client too. That's a good way to see how the pieces work, but it hides what makes them interesting. A pipe, a socket, a terminal, a shared folder: these are the places where two programs meet, and on a real Linux machine the two programs very often belong to two different people.

As soon as two people share a machine, a second question sits next to "how does this work?", and that question is "who is allowed to use it?" Linux answers it the same way for nearly everything: with the owner, group and other permission bits from the users-and-permissions lab. In this lab you'll watch that one answer apply in turn to a terminal, a text file, a link, a running program, a pipe and a socket.

So this lab needs two of you. (Three works too; look for the boxes marked **If you're three**.) Every part is built so neither person can finish it alone. One of you sets something up, the other has to find it, read it or connect to it, and the information has to travel through the machine to get there.

---

## Before you start

**One machine, two people.** You'll both work on one person's Azure Lab VM. That person is the **Host**, and the other person is the **Guest**. The Host creates an account for the Guest on the Host's VM. From then on each of you logs in from your own computer, as yourself: one machine, two users, two terminals. Pick who will be Host for this lab, and switch next time.

**What you need:**

- Each person at their own computer, with a terminal you normally use to reach your VM.
- The Host's VM running (start it from the Azure Lab Services page as usual). The Host should stay logged in for the whole lab.
- The Host's connection command, the one that looks like `ssh -p 5037 student@lab-xxxxxxxx.eastus.cloudapp.azure.com`. The Guest will use the same address and port with their own name. Never give your partner your password; the Guest gets an account of their own.

**Send it through the machine.** You'll be sitting near each other, and talking is fine, especially for planning. But whenever a step asks one of you to pass something to the other (a secret word, an inode number, a message), send it through the channel that part is about, or through the team logbook you'll build in Part 0. The logbook is how you show it happened.

**How to read the commands.** A line starting with `$` is something you type; leave out the `$`. A label above each block says who types it:

**Host:**

```
$ whoami
student
```

**Guest:**

```
$ whoami
maria
```

The examples use `student` for the Host (that's the account Azure gives every lab VM) and `maria` for the Guest. Use your Guest's real first name, in lowercase, everywhere this lab writes `maria`. Terminal numbers, process IDs, inode numbers and times will differ on your machine; the shape should match.

**Tested on** Ubuntu 24.04, with a Host and a Guest logged in over SSH as separate users. On a different Ubuntu version, a few messages may be worded differently. Where that's likely, the lab says so.

**Parts.** Part 0 sets up the team and must come first. After that, each part stands alone and makes its own folder under `/srv/team`, so you can do them in any order. Where a part has a leading role, swap and repeat it if you have time, so both of you do both sides.

| Part | Topic | Who leads |
|---|---|---|
| 0 | Set up the team machine | Host, then Guest |
| 1 | Your terminal is a file with an owner | both |
| 2 | Mystery files and inode hide-and-seek | both |
| 3 | Links between two people | Host sets up, Guest watches |
| 4 | Your partner's program, seen through `/proc` | Host runs, Guest investigates, then swap |
| 5 | A pipe between two people | both |
| 6 | A chat room that knows who's talking | Guest runs it, everyone joins |

**The optional boxes.** Anything marked **Experiment** is optional; the main path works without it, though most of the surprises live there. **If you're three** boxes give a third person a real job in that part, not just a seat.

**Predict first.** Before you press Enter on a step marked *predict*, each of you says what you think will happen. Two people guessing differently is the best possible start.

**What to hand in** (one per team): your team logbook and your reflection answers. Details are at the end, in [What to hand in](#what-to-hand-in).

---

## Part 0: Set up the team machine

The Host creates an account for the Guest, a group called `team` with both of you in it, and a folder that belongs to that group. Then the Guest logs in and builds the team logbook. Everything here comes from the users-and-permissions lab. The difference is that this time a real person is on the other end.

### Step 0.1 Host: make the group and the Guest's account

Log in to your VM as usual, then:

**Host:**

```
$ sudo groupadd team
$ sudo useradd -m -s /bin/bash -G team maria
$ sudo passwd maria
New password:
Retype new password:
passwd: password updated successfully
$ sudo usermod -aG team student
```

One line at a time:

- `groupadd team` creates the group.
- `useradd -m -s /bin/bash -G team maria` creates the account. `-m` makes a home folder, `-s /bin/bash` gives it the usual shell (without it, Ubuntu hands out a plainer one), and `-G team` puts the new user in `team`.
- `passwd maria` sets a temporary password. Nothing shows while you type. Tell the Guest this one password out loud; they'll change it the moment they log in.
- `usermod -aG team student` adds you, the Host, to the group too. The `-a` (append) matters. Without it, `-G` *replaces* your list of groups instead of adding one, and you'd lose `sudo`.

Don't add the Guest to the `sudo` group. Several parts of this lab depend on the Guest being an ordinary user, and anyone with `sudo` can step around every permission you're about to test.

While you have `sudo` handy, make sure `nc` is installed, since the Guest can't install anything:

**Host:**

```
$ sudo apt install -y netcat-openbsd
```

### Step 0.2 Host: a folder that belongs to the team

**Host:**

```
$ sudo mkdir /srv/team
$ sudo chgrp team /srv/team
$ sudo chmod 2770 /srv/team
$ ls -ld /srv/team
drwxrws--- 2 root team 4096 Oct  5 11:30 /srv/team
```

`/srv` is the standard place for data a machine serves to other people, which makes it a natural home for a shared folder. Read the permissions in three groups of three: the owner, root, has `rwx`; the group `team` has `rws`; everyone else has nothing.

The `s` where the group's `x` would be comes from the `2` at the front of `2770`. On a directory it's called *setgid*, and it means "anything created in here belongs to this folder's group". Without it, a file the Guest makes would belong to the Guest's own group, `maria`, and you couldn't touch it. With it, everything inside `/srv/team` belongs to `team` automatically.

### Step 0.3 Host: someone who isn't on the team

Several parts need an outsider to test against. Make a user with no password, so nobody can log in as them:

**Host:**

```
$ sudo useradd -m visitor
$ sudo -u visitor ls /srv/team
ls: cannot open directory '/srv/team': Permission denied
```

`sudo -u visitor` runs one command as `visitor`. Only the Host can do this, because only the Host has `sudo`. Whenever this lab says "try it as the visitor", that's the Host's job. (`sudo` will sometimes ask for a password: it's the Host's own password it wants.)

### Step 0.4 Host: predict, then log in again

*Predict:* you just added yourself to `team`, and `team` has full access to `/srv/team`. Will this work?

**Host:**

```
$ touch /srv/team/hello
touch: cannot touch '/srv/team/hello': Permission denied
$ id
uid=30035(student) gid=30036(student) groups=30036(student),27(sudo)
```

`team` isn't in the list. Your groups are read once, when you log in, and every program you start copies that list from the shell that started it. This shell started before you joined `team`. Log out and connect again:

**Host:**

```
$ exit
```

Reconnect with your usual `ssh` command, then:

**Host:**

```
$ id
uid=30035(student) gid=30036(student) groups=30036(student),27(sudo),30037(team)
$ touch /srv/team/hello
$ ls -l /srv/team
total 0
-rw-rw-r-- 1 student team 0 Oct  5 11:30 hello
$ rm /srv/team/hello
```

The file belongs to group `team`, even though your own group is `student`. That's setgid at work. Your numbers will differ.

### Step 0.5 Guest: log in as yourself

Use the Host's connection command, with your own name in place of `student`:

**Guest:**

```
$ ssh -p 5037 maria@lab-xxxxxxxx.eastus.cloudapp.azure.com
```

The port number picks the Host's VM; the name picks who you are on it. If `ssh` asks whether you're sure you want to continue connecting, type `yes`: it hasn't seen this VM before. Type the temporary password, then change it straight away:

**Guest:**

```
$ passwd
Changing password for maria.
Current password:
New password:
Retype new password:
passwd: password updated successfully
$ id
uid=30036(maria) gid=30038(maria) groups=30038(maria),30037(team)
```

### Step 0.6 Both: check your umask

**Both:**

```
$ umask
0002
```

`0002` means new files you create are writable by your group, so your partner can change them. If you see `0022` instead, files you make will be read-only for your partner, and later parts will fail with `Permission denied` in confusing places. Fix it now and for future logins:

```
$ umask 002
$ echo 'umask 002' >> ~/.bashrc
```

### Step 0.7 Guest: build the team logbook

The logbook is one text file, `/srv/team/logbook.txt`, that you both add lines to. A small program signs each line with who wrote it, from which terminal, and when. Nobody types their own name; the program asks the system who you are.

**Guest:**

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

**Guest:**

```
$ chmod +x /srv/team/log
$ ls -l /srv/team
total 4
-rwxrwxr-x 1 maria team 744 Oct  5 11:31 log
```

The first line, `#!/usr/bin/env python3`, tells Linux which program should run this file, so it can be started by name without typing `python3` first. `os.getuid()` is the number the kernel knows you by, and `pwd.getpwuid` turns that number into your name by looking it up in `/etc/passwd`, which is, of course, a file.

### Step 0.8 Both: a short name, and the first entries

So you can type `log` instead of `/srv/team/log`:

**Both:**

```
$ echo 'alias log=/srv/team/log' >> ~/.bashrc
$ source ~/.bashrc
```

Now see who's on the machine, and sign the book:

**Host:**

```
$ who
maria    pts/1        2026-10-05 11:31
student  pts/3        2026-10-05 11:31
$ log 'Host here, setup done'
logged as student
```

(`who` also prints where each login came from, at the end of each line.)

**Guest:**

```
$ log "Guest here, I can see the Host's entry"
logged as maria
$ cat /srv/team/logbook.txt
11:31:18  student  pts/3  Host here, setup done
11:31:18  maria    pts/1  Guest here, I can see the Host's entry
```

Two people, one file, every line signed by the system. From here on, whenever a step says **Log it**, add a line like this. The times come from the VM's clock, which may be set to a different time zone from yours.

`log` isn't tamper-proof: anyone in the team could edit the file with `nano`. It's an honest record as long as you use it honestly, and that's all it needs to be.

> **If you're three.** The Host repeats Step 0.1 for the second Guest (`sudo useradd -m -s /bin/bash -G team jose`, then `sudo passwd jose`). Both Guests log in with the Host's address and port and their own names, and each does Steps 0.6 and 0.8. In the rest of the lab, "Guest" means either of them unless a box says otherwise.

---

## Part 1: Your terminal is a file with an owner

In the solo lab, `tty` showed that your terminal is a file like `/dev/pts/0`, and writing into that file made text appear on your screen. With two people logged in, there are two of those files, and each one has an owner.

### Step 1.1 Find each other

**Both:**

```
$ tty
```

The Guest sees something like `/dev/pts/1`, the Host something like `/dev/pts/3`. The Host doesn't need to ask which one belongs to the Guest; the earlier `who` already said so. Now look at all of them:

**Host:**

```
$ ls -l /dev/pts
total 0
crw------- 1 root    root 136, 0 Oct  5 11:31 0
crw--w---- 1 maria   tty  136, 1 Oct  5 11:31 1
crw------- 1 root    root 136, 2 Oct  5 11:31 2
crw--w---- 1 student tty  136, 3 Oct  5 11:31 3
c--------- 1 root    root   5, 2 Oct  5 11:06 ptmx
```

Every login gets its own terminal file, owned by whoever logged in on it. (The ones owned by root belong to the system itself. `ptmx` is the device that hands out new terminals.)

### Step 1.2 Host: knock

*Predict:* will this put text on the Guest's screen? Use the Guest's number.

**Host:**

```
$ echo "knock knock" > /dev/pts/1
-bash: /dev/pts/1: Permission denied
```

Read the line for terminal `1` again: `crw--w---- 1 maria tty`. The owner, `maria`, may read and write. The group, `tty`, may write. Everyone else may do nothing. You're not `maria` and you're not in group `tty`, so you're "everyone else".

> **About `write`.** Linux has an old command made for exactly this job: `write maria` sends a message to a user's terminal. Try it. On current Ubuntu you'll most likely get `write: effective gid does not match group of /dev/pts/3`. In 2024 a security bug (nicknamed WallEscape) showed that `write` and its cousin `wall` could be used to put fake text on other people's screens, and Ubuntu's fix took away the special group permission those commands used to reach other terminals. Underneath, `write` was only ever doing what you just tried: opening someone's terminal file and writing into it. On an older system it may still work.

### Step 1.3 Guest: open the door to your team

**Guest:**

```
$ chgrp team $(tty)
$ ls -l $(tty)
crw--w---- 1 maria team 136, 1 Oct  5 11:32 /dev/pts/1
```

`$(tty)` gets replaced by the output of `tty`, which is your terminal's path. You own your terminal, so you can hand it to any group you belong to. The group still has write permission; it's just a different group now.

**Host:**

```
$ echo "knock knock" > /dev/pts/1
```

On the Guest's screen:

```
knock knock
```

**Log it.** Guest: `log "the Host's knock arrived on my terminal"`

### Step 1.4 Host: try it as the visitor

**Host:**

```
$ sudo -u visitor sh -c 'echo "visitor here" > /dev/pts/1'
sh: 1: cannot create /dev/pts/1: Permission denied
```

The visitor isn't in `team`, so the door is still shut for them.

Why the `sh -c '...'`? The `>` is handled by the shell *before* the command runs. In `sudo -u visitor echo hi > /dev/pts/1`, your own shell would open the terminal file as you, and only `echo` would run as the visitor. `sh -c` starts a whole new shell as the visitor, so the visitor is the one doing the opening.

### Step 1.5 Guest: close the door

**Guest:**

```
$ chmod g-w $(tty)
$ ls -l $(tty)
crw------- 1 maria team 136, 1 Oct  5 11:32 /dev/pts/1
```

Now the Host knocks again. *Predict* first, then try it.

Then swap roles: the Host opens their door with `chgrp team $(tty)`, the Guest knocks with `echo ... > /dev/pts/3` (the Host's number), the Host logs what arrived, and the Host closes the door again.

None of this is permanent. Your terminal file is created fresh each time you log in, with the default permissions.

> **Experiment: what `mesg` really does.** `mesg` is the classic on/off switch for "may other people write to my terminal?". Run `mesg n`, then `ls -l $(tty)`: it's `chmod g-w` under another name. Now turn it back on:
>
> ```
> $ mesg y
> $ ls -l $(tty)
> crw--w--w- 1 maria team 136, 1 Oct  5 11:32 /dev/pts/1
> ```
>
> On current Ubuntu, `mesg y` also turns on write permission for *others* (another side effect of the 2024 fix). Ask the Host to try the visitor's knock now. Then close the gap with `chmod o-w $(tty)`. A convenience command can do more than its name suggests, and `ls -l` tells you what it really did.

> **Experiment: the Host's master key.** Guest, close your door (`chmod g-w $(tty)`). Host:
>
> ```
> $ echo "root does not need to knock" | sudo tee /dev/pts/1 > /dev/null
> ```
>
> It arrives anyway: root ignores permission bits. (`sudo tee` rather than `sudo echo ... >` for the same reason as `sh -c` above: here `tee`, running as root, is the program that opens the terminal file.) The Guest can't return the favor without `sudo`, which is exactly why the Guest doesn't get it.

> **If you're three.** Guest 1 wants to let Guest 2 write to them, but not the Host. Try it with `chgrp` and `chmod`. You'll find you can't: a file has one owner and one group, and the Host and Guest 2 are both in `team`. Linux does have a finer tool, access control lists, which can name individual users (`setfacl -m u:jose:w somefile`; the Host may need `sudo apt install acl`). They work on ordinary files. Try one on your terminal, though, and you'll get `setfacl: /dev/pts/1: Operation not supported`. Not every kind of file supports every feature.

---

## Part 2: Mystery files and inode hide-and-seek

A name is only a label in a directory. What a file *is*, and which file it is, lives in its inode. This part turns both ideas into games.

### Step 2.1 Set up

**Either of you:**

```
$ mkdir -p /srv/team/part2/mystery
```

### Step 2.2 Guest: make four things with misleading names

**Guest:**

```
$ cd /srv/team/part2/mystery
$ mkdir photo.jpg
$ mkfifo notes.txt
$ ln -s /etc/hostname music.mp3
$ python3 -c "import socket; socket.socket(socket.AF_UNIX).bind('readme')"
```

A directory called `photo.jpg`, a named pipe called `notes.txt`, a symbolic link called `music.mp3` and a socket called `readme`. Don't tell the Host which is which.

### Step 2.3 Host: identify them without asking

Start with only the names:

**Host:**

```
$ cd /srv/team/part2/mystery
$ ls
music.mp3  notes.txt  photo.jpg  readme
```

The names are lying, on purpose. Now ask the system:

**Host:**

```
$ ls -l
total 4
lrwxrwxrwx 1 maria team   13 Oct  5 11:32 music.mp3 -> /etc/hostname
prw-rw-r-- 1 maria team    0 Oct  5 11:32 notes.txt
drwxrwsr-x 2 maria team 4096 Oct  5 11:32 photo.jpg
srwxrwxr-x 1 maria team    0 Oct  5 11:32 readme
$ file *
music.mp3: symbolic link to /etc/hostname
notes.txt: fifo (named pipe)
photo.jpg: setgid, directory
readme:    socket
```

The first letter in `ls -l` gives each one away: `l`, `p`, `d`, `s`. Notice also that all four belong to group `team`, and `file` calls the directory "setgid": it inherited the bit from the folder it was made in, so the rule from Step 0.2 keeps applying all the way down.

**Log it.** Host: write down what each one really is, like `log "photo.jpg is a directory, notes.txt is a named pipe, ..."`

> **Experiment: what does `cat` do to each one?** Have Ctrl+C ready.
>
> ```
> $ cat photo.jpg
> cat: photo.jpg: Is a directory
> $ cat readme
> cat: readme: No such device or address
> $ cat notes.txt
> ```
>
> The last one just sits there: a named pipe waits for someone to write into it (Part 5). Press Ctrl+C. Then try `cat music.mp3`, which follows the link and prints the VM's name. Opening a file you haven't identified can hang, which is a good reason to look before you `cat`.

If you have time, swap: the Host makes four new mystery files and the Guest identifies them.

### Step 2.4 Hide and seek, round 1: the Host hides

The Host hides a file and tells the Guest only one thing about it: its inode number. Use your own secret word and your own hiding place.

**Host:**

```
$ cd /srv/team/part2
$ echo 'the secret word is: pineapple' > treasure.txt
$ ls -i treasure.txt
894513 treasure.txt
$ log "hid something. its inode is 894513"
$ mkdir -p attic/box/sock
$ mv treasure.txt attic/box/sock/laundry.txt
```

New name, new folder. The Guest reads the logbook and goes looking:

**Guest:**

```
$ tail -3 /srv/team/logbook.txt
$ find /srv/team -inum 894513
/srv/team/part2/attic/box/sock/laundry.txt
$ cat /srv/team/part2/attic/box/sock/laundry.txt
the secret word is: pineapple
$ log "found it: pineapple"
```

The name changed completely and the inode number didn't. Moving a file within one filesystem only changes directory entries, so the inode, and its number, stay exactly where they were.

### Step 2.5 Round 2: the Guest hides, maybe sneakily

The Guest makes a new treasure and logs its inode number. Then the Guest secretly picks one of two ways to hide it: `mv` like the Host did, or this:

**Guest:**

```
$ mkdir -p shed && cp treasure.txt shed/rake.txt && rm treasure.txt
```

The file still ends up in a new place under a new name. *Predict*, Host: if the Guest chose this way, what will `find` say?

**Host:**

```
$ find /srv/team -inum 894517
$
```

Nothing. `cp` made a brand-new inode with a new number, and `rm` removed the only name of the old one, so the old one is gone. The Host can still find the treasure by what's *in* it:

**Host:**

```
$ grep -rl 'secret word' /srv/team/part2
/srv/team/part2/shed/rake.txt
/srv/team/part2/attic/box/sock/laundry.txt
```

**Log it.** Host: which way did the Guest hide it, and how can you tell?

One surprise from testing this lab: right after the Guest's `rm`, the very next file anyone created got the freed number, 894517. An inode number belongs to a file only while that file exists. If `find -inum` ever turns up a file with the wrong contents, the number was recycled.

> **If you're three: the Keeper.** Right after the hider logs the inode number, and before hiding, the third person makes a second name for the treasure:
>
> ```
> $ ln /srv/team/part2/treasure.txt /srv/team/part2/keeper.txt
> ```
>
> Now the hider uses `cp` and `rm`. This time `find -inum` *does* find something: `keeper.txt`, still holding the original. `rm` removed one name, but the inode had two, so it lived on. Then predict what `ls -li keeper.txt` shows for the link count, and check.

---

## Part 3: Links between two people

A hard link is a second name for the same inode. A symbolic link is a little file holding a path, like a sticky note. With two people, both kinds behave in ways that are easy to miss when you're alone.

### Step 3.1 Host: some shared settings

**Host:**

```
$ mkdir -p /srv/team/part3 && cd /srv/team/part3
$ echo '{"color": "blue", "size": 3}' > settings.json
$ ls -l settings.json
-rw-rw-r-- 1 student team 29 Oct  5 11:33 settings.json
```

### Step 3.2 Guest: a second name, in your own home

**Guest:**

```
$ ln /srv/team/part3/settings.json ~/my_settings.json
$ ls -li ~/my_settings.json /srv/team/part3/settings.json
894523 -rw-rw-r-- 2 student team 29 Oct  5 11:33 /home/maria/my_settings.json
894523 -rw-rw-r-- 2 student team 29 Oct  5 11:33 /srv/team/part3/settings.json
```

Same inode, link count 2, owned by `student`. The Host's file now has a name inside the Guest's home folder, a place the Host can't even look into:

**Host:**

```
$ ls -l settings.json
-rw-rw-r-- 2 student team 29 Oct  5 11:33 settings.json
$ ls ~maria
ls: cannot open directory '/home/maria': Permission denied
$ find / -samefile /srv/team/part3/settings.json 2>/dev/null
/srv/team/part3/settings.json
```

(The `find` searches the whole disk, so give it a few seconds.) The link count says there are two names. `find` only finds one, because it can only search where the Host is allowed to look. A hard link doesn't record where its other names are.

### Step 3.3 Host: change the settings, two ways

**Host:**

```
$ echo '{"color": "green", "size": 3}' > settings.json
```

**Guest:**

```
$ cat ~/my_settings.json
{"color": "green", "size": 3}
```

Same file, so of course the Guest sees it. Now the Host edits with `sed -i`:

**Host:**

```
$ sed -i 's/green/red/' settings.json
$ cat settings.json
{"color": "red", "size": 3}
```

*Predict*, Guest: what does your copy say now?

**Guest:**

```
$ cat ~/my_settings.json
{"color": "green", "size": 3}
$ ls -li ~/my_settings.json /srv/team/part3/settings.json
894523 -rw-rw-r-- 1 student team 30 Oct  5 11:33 /home/maria/my_settings.json
894524 -rw-rw-r-- 1 student team 28 Oct  5 11:33 /srv/team/part3/settings.json
```

Two inodes now, each with one name. `sed -i` doesn't edit a file in place. It writes a new file and renames it over the old name, so the Host's name moved to a new inode and the Guest's name stayed with the old one. Nobody got an error. On your own machine this was a curiosity; between two people it's a real trap, because the Guest has no way of knowing their copy has gone stale unless someone tells them.

**Log it.** Guest: what your copy says now, and why.

### Step 3.4 A link into a private place

**Host:**

```
$ echo 'dear diary: I love tacos' > ~/diary.txt
$ ls -ld ~
drwxr-x--- 3 student student 4096 Oct  5 11:33 /home/student
```

**Guest:**

```
$ ln -s /home/student/diary.txt /srv/team/part3/diary-link
$ ls -l /srv/team/part3/diary-link
lrwxrwxrwx 1 maria team 23 Oct  5 11:33 /srv/team/part3/diary-link -> /home/student/diary.txt
$ cat /srv/team/part3/diary-link
cat: /srv/team/part3/diary-link: Permission denied
```

**Host:**

```
$ cat /srv/team/part3/diary-link
dear diary: I love tacos
```

The same link, two readers, two results. `ln -s` didn't check anything; it wrote down a path. Whoever follows the link walks that path with their own permissions, and the Host's home folder (`drwxr-x---`) lets nobody else in. A symlink can point anywhere; it can't take anyone anywhere they couldn't already go.

### Step 3.5 A live switch

Plenty of servers run whatever is in a folder called `current`, which is a symlink to the release in use. Switching versions means switching the link. Here, the Host deploys and the Guest is the user who notices.

**Host:**

```
$ mkdir -p releases/v1 releases/v2
$ echo 'version 1' > releases/v1/app.txt
$ echo 'version 2' > releases/v2/app.txt
$ ln -s releases/v1 current
```

The Guest starts watching. This loop reads the file through the link once a second:

**Guest:**

```
$ while true; do cat /srv/team/part3/current/app.txt; sleep 1; done
version 1
version 1
version 1
```

Leave it running. The Host switches:

**Host:**

```
$ ln -sfn releases/v2 current
$ log "switched current to v2"
```

On the Guest's screen, within a second:

```
version 1
version 2
version 2
```

Press Ctrl+C to stop the loop, then **log it**: the time you saw the change. Compare with the Host's entry.

The Guest's loop was never restarted, and nobody told it anything. Each `cat` follows the link afresh, so the moment the link changed, every new read went to v2.

> **Experiment: a shell that stays behind.** Guest, step *into* the release through the link:
>
> ```
> $ cd /srv/team/part3/current
> $ cat app.txt
> version 2
> ```
>
> Host, switch back: `ln -sfn releases/v1 current`. Guest, *predict*, then:
>
> ```
> $ cat app.txt
> version 2
> $ pwd -P
> /srv/team/part3/releases/v1
> $ ls -l /proc/$$/cwd
> lrwxrwxrwx 1 maria maria 0 Oct  5 11:33 /proc/1961/cwd -> /srv/team/part3/releases/v2
> ```
>
> When you `cd`'d, the shell followed the link once and settled into the real folder, `v2`. Switching the link doesn't move you. `pwd -P` gets it wrong: it re-reads the link and reports where the link points *now*. `/proc/$$/cwd` asks the kernel where your shell actually is. Real deployments run into this: a program that started inside the old release keeps running the old release until it's restarted.

> **Experiment: a hard link the kernel refuses.** Host:
>
> ```
> $ echo 'mine' > locked.txt
> $ chmod 644 locked.txt
> ```
>
> Guest:
>
> ```
> $ cat /srv/team/part3/locked.txt
> mine
> $ ln /srv/team/part3/locked.txt ~/grab.txt
> ln: failed to create hard link '/home/maria/grab.txt' => '/srv/team/part3/locked.txt': Operation not permitted
> ```
>
> The Guest can read the file but can't give it another name. Ubuntu switches on a rule (`cat /proc/sys/fs/protected_hardlinks` prints `1`) that only lets you hard link files you own or can write to. It exists because planting a hard link to someone else's file in the right place used to be a way to trick privileged programs into changing that file.

> **If you're three.** One Guest runs the watching loop while the other does the "shell that stays behind" experiment at the same time. When the Host switches, one of you sees the change and the other doesn't. Log both.

---

## Part 4: Your partner's program, seen through `/proc`

`/proc` has a folder for every running program. With two people on the machine, some of what's in those folders is open to everyone, and some isn't. The Host runs a program with a secret; the Guest finds out as much about it as possible without asking.

### Step 4.1 Host: run a program with a secret

The Host creates this in their home folder, where the Guest can't read it:

**Host:**

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

**Host:**

```
$ python3 ~/mystery.py library
Mystery program running. Press Ctrl+C to stop it.
```

Leave it running.

### Step 4.2 Guest: investigate

Work through these in order, and keep notes on what worked and what didn't.

**Is it running, and what's its number?**

**Guest:**

```
$ pgrep -u student -a python3
2020 python3 /home/student/mystery.py library
```

`-u student` limits the search to the Host's programs, and `-a` shows the whole command line. You already have the secret word. **Log it** right away.

**How long has it been running?**

```
$ ps -o pid,user,etime,args -p 2020
  PID USER         ELAPSED COMMAND
 2020 student        00:02 python3 /home/student/mystery.py library
```

**Where do `ps` and `pgrep` get the command line?** From a file, naturally:

```
$ tr '\0' ' ' < /proc/2020/cmdline; echo
python3 /home/student/mystery.py library
```

Inside `cmdline` the words are separated by zero bytes, which aren't printable; `tr` turns them into spaces so you can read them. (Try `cat /proc/2020/cmdline`: depending on your terminal, the words either run together or come out with odd gaps.)

**What state is it in, and how much memory is it using?**

```
$ grep -E '^(Name|State|Uid|VmRSS)' /proc/2020/status
Name:	python3
State:	S (sleeping)
Uid:	30035	30035	30035	30035
VmRSS:	    8752 kB
```

**Which folder is it running in? Which files does it have open? What are its settings?**

```
$ ls -l /proc/2020/cwd
ls: cannot read symbolic link '/proc/2020/cwd': Permission denied
lrwxrwxrwx 1 student student 0 Oct  5 11:33 /proc/2020/cwd
$ ls /proc/2020/fd
ls: cannot open directory '/proc/2020/fd': Permission denied
$ cat /proc/2020/environ
cat: /proc/2020/environ: Permission denied
```

**Can you read the program itself?**

```
$ cat ~student/mystery.py
cat: /home/student/mystery.py: Permission denied
```

**Log it.** Two short lists: what you could learn about the Host's program, and what was closed to you.

The pattern: anyone can see *that* a program runs, who owns it, how it was started and how busy it is. Only the owner can see *inside* it: its open files, its working folder, its environment. The command line is on the public side, which has a practical lesson: never type a password as part of a command (some database tools allow `-pSECRET`, for example). While that command runs, every user on the machine can read it from `/proc`.

### Step 4.3 Host: the private side

Open a second connection to your VM (same `ssh` command, new terminal window), so the mystery program can keep running in the first one.

**Host** (second terminal):

```
$ ls -l /proc/2020/fd
total 0
lrwx------ 1 student student 64 Oct  5 11:33 0 -> /dev/pts/3
lrwx------ 1 student student 64 Oct  5 11:33 1 -> /dev/pts/3
lrwx------ 1 student student 64 Oct  5 11:33 2 -> /dev/pts/3
lr-x------ 1 student student 64 Oct  5 11:33 3 -> '/home/student/note.txt (deleted)'
```

Descriptor 3 is a file with no name left. The program wrote a note, kept it open and deleted it, just like `ghost.py` in the solo lab. The note still exists as long as the program holds it, and the owner can copy it out through `/proc`. Rescue it into the team folder so the Guest can read it:

**Host:**

```
$ mkdir -p /srv/team/part4
$ cp /proc/2020/fd/3 /srv/team/part4/rescued.txt
```

**Guest:**

```
$ cat /srv/team/part4/rescued.txt
The note says: meet at the library.
```

**Log it.** Guest: the rescued note. Then the Host stops the mystery program with Ctrl+C in the first terminal.

### Step 4.4 Swap

The Guest creates their own `~/mystery.py` (the same code; the Host's copy is out of reach) and runs it with a new secret word. The Host investigates with the same commands, using `-u maria` instead of `-u student`.

Do it twice. First without `sudo`: the Host meets the same walls the Guest did. Then put `sudo` in front of the commands that failed, such as `sudo ls -l /proc/<pid>/fd`. Everything opens. Then the Guest tries to return the favor:

**Guest:**

```
$ sudo ls /proc/2020/fd
[sudo] password for maria:
maria is not in the sudoers file.
```

(Older versions of `sudo` add "This incident will be reported.") **Log** both results.

> **If you're three.** Two investigators split the questions in Step 4.2, then compare notes in the logbook. Did either of you find a way past a `Permission denied` without `sudo`?

---

## Part 5: A pipe between two people

A named pipe has a name in a folder, so any program that can reach the folder can find it. Put it in `/srv/team` and two people can pass text through it.

### Step 5.1 Host: two pipes, one each way

**Host:**

```
$ mkdir -p /srv/team/part5 && cd /srv/team/part5
$ mkfifo to_host to_guest
$ ls -l
total 0
prw-rw-r-- 1 student team 0 Oct  5 11:34 to_guest
prw-rw-r-- 1 student team 0 Oct  5 11:34 to_host
$ sudo -u visitor cat /srv/team/part5/to_guest
cat: /srv/team/part5/to_guest: Permission denied
```

The visitor can't even reach the pipe: `/srv/team` itself keeps them out.

### Step 5.2 One way

The Guest listens:

**Guest:**

```
$ cat /srv/team/part5/to_guest
```

It sits and waits. The Host writes:

**Host:**

```
$ cat > /srv/team/part5/to_guest
```

Type a few lines, pressing Enter after each. They show up on the Guest's screen as you go:

```
hello through a named pipe
second line
```

Then the Host presses Ctrl+D. The Guest's `cat` ends too: when the last writer closes the pipe, the reader gets end-of-file.

### Step 5.3 Both ways, one terminal each

**Host:**

```
$ cat /srv/team/part5/to_host & cat > /srv/team/part5/to_guest
```

**Guest:**

```
$ cat /srv/team/part5/to_guest & cat > /srv/team/part5/to_host
```

Each of you runs two programs at once. The `&` starts a reader in the background, listening on the pipe that comes *to* you. The second `cat` is the writer, sending what you type into the pipe that goes *to* your partner. Start typing. After the Host types one line and the Guest answers, the Host's screen looks like this:

```
$ cat /srv/team/part5/to_host & cat > /srv/team/part5/to_guest
[1] 2114
hi guest, can you hear me?
loud and clear
```

`[1] 2114` is the shell reporting the background job and its process ID. The first message is what the Host typed; the second arrived through `to_host`. When you're done, both press Ctrl+D.

> **Experiment: two writers, no readers.** Both of you run *only* the writer half: the Host `cat > /srv/team/part5/to_guest`, the Guest `cat > /srv/team/part5/to_host`. Type something. Nothing arrives, ever. Opening a pipe for writing waits until someone opens it for reading, and here both of you are waiting at a door for the other to come through. Press Ctrl+C. That's why the `&` reader matters.

### Step 5.4 The Python version, with names

Either of you creates this file in the shared folder:

```
$ nano /srv/team/part5/fifochat.py
```

```python
# fifochat.py: a two-way chat over two named pipes.
# Usage:  python3 fifochat.py <pipe to read from> <pipe to write to>
import os
import pwd
import sys
from threading import Thread

inbox, outbox = sys.argv[1], sys.argv[2]
me = pwd.getpwuid(os.getuid()).pw_name


def listen():
    with open(inbox) as pipe:                 # waits until the other side opens it for writing
        for line in pipe:                     # one line per message
            print(line, end="", flush=True)
    print("(the other side closed the pipe)")


Thread(target=listen, daemon=True).start()   # read in the background...

with open(outbox, "w") as pipe:               # ...while we wait to open the other pipe for writing
    print(f"Connected as {me}. Type a line and press Enter. Ctrl+D to leave.")
    for line in sys.stdin:                    # every line you type
        pipe.write(f"{me}: {line}")           # goes into the pipe, signed with your name
        pipe.flush()
```

Same idea as the shell version: a thread does the listening, the main program does the writing. Each of you names the pipe to read from first, then the pipe to write to:

**Host:**

```
$ python3 /srv/team/part5/fifochat.py /srv/team/part5/to_host /srv/team/part5/to_guest
Connected as student. Type a line and press Enter. Ctrl+D to leave.
```

**Guest:**

```
$ python3 /srv/team/part5/fifochat.py /srv/team/part5/to_guest /srv/team/part5/to_host
Connected as maria. Type a line and press Enter. Ctrl+D to leave.
```

Chat for a bit. On the Host's screen:

```
maria: hola from the guest side
the host says hi back
```

When one of you presses Ctrl+D, the other sees `(the other side closed the pipe)`.

**Log it.** Each of you copies one line you received into the logbook.

> **If you're three: one pipe, two voices.** The Host reads `cat /srv/team/part5/to_host`, and *both* Guests run `cat > /srv/team/part5/to_host` at the same time. Take turns typing. The Host sees one stream with both voices in it:
>
> ```
> maria: hello
> jose: hi too
> maria: bye
> ```
>
> Lines stay whole, because Linux never splits a single write of up to 4096 bytes into a pipe. Then one Guest presses Ctrl+D. The Host's `cat` keeps going, because a reader only gets end-of-file when the *last* writer leaves. Check by typing from the other Guest.

---

## Part 6: A chat room that knows who's talking

The solo lab's chat server used a TCP socket, reached by an address and a port number. With two people on the machine, it matters who can connect, and whether the server can tell who connected. TCP and Unix sockets answer those questions very differently.

### Step 6.1 TCP with `nc`

**Host:**

```
$ nc -l 5007
```

**Guest:**

```
$ nc localhost 5007
```

Type in either window and press Enter; it shows up in the other. Leave it connected. The Host opens a second connection to the VM and looks at the network table:

**Host** (second terminal):

```
$ ss -tnp | grep 5007
ESTAB 0      0          127.0.0.1:50812     127.0.0.1:5007
ESTAB 0      0          127.0.0.1:5007      127.0.0.1:50812 users:(("nc",pid=2208,fd=4))
```

Two lines, one for each end of the connection. The Host's end shows which program owns it. The Guest's end shows nothing in that column: Linux tells you the connection exists, but not whose program is on the other side. The Guest gets the mirror image if they run the same command.

The Guest presses Ctrl+C. The Host's `nc` ends too, since `nc -l` serves one connection and quits.

### Step 6.2 TCP doesn't ask who's calling

**Host:**

```
$ nc -l 5007
```

**Host** (second terminal):

```
$ sudo -u visitor nc localhost 5007
visitor sneaking in
```

The visitor's message appears in the first terminal. A port number has no owner and no permission bits: any user on the machine can connect to it. And all the listening side learns is an address and a port number like `127.0.0.1:50812`, not who's typing. Press Ctrl+C in both.

### Step 6.3 Guest: open a room

A Unix socket is a file, so it has an owner, a group and permissions. And because both ends are on the same machine, the kernel knows which user is on each end, and will tell the server if asked.

**Guest:**

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

- `caller_name` is the new idea. `SO_PEERCRED` asks the kernel for the *credentials of the peer*: the process ID, user ID and group ID of whoever is on the other end. The room never asks anyone their name, and nobody can type a fake one.
- Each caller gets their own thread (`serve`), so several people can be in the room at once. `say_to_all` sends a line to everyone, and the `lock` makes sure two threads never change the member list at the same moment.
- Each connection gets two file objects: `incoming` to read lines from, the same way you'd loop over a text file, and `outgoing` for the room to write to.
- `os.chmod(ADDRESS, 0o660)` sets the socket file's permissions: owner and group may connect, everyone else may not.

Run it:

**Guest:**

```
$ python3 /srv/team/part6/team_room.py
Room open at /srv/team/part6/room.sock. Press Ctrl+C to close it.
```

Leave it running. The Guest opens a second connection to the VM to join their own room. Then both of you join:

**Host** and **Guest** (second terminal):

```
$ nc -U /srv/team/part6/room.sock
```

`-U` tells `nc` the address is a Unix socket file. Say something. After the Host and then the Guest have each sent one line, the Host's screen shows:

```
$ nc -U /srv/team/part6/room.sock
* student joined
* maria joined
hello room, this is the host
student: hello room, this is the host
maria: hi host! guest here
```

Your own line appears twice: once as you type it, and once when the room sends it back to everyone with your name on it. Meanwhile the room's own terminal shows every line too. Look at the socket file and at the logbook:

**Guest** (second terminal; leave `nc` with Ctrl+C first):

```
$ ls -l /srv/team/part6/room.sock
srw-rw---- 1 maria team 0 Oct  5 11:35 /srv/team/part6/room.sock
$ tail -2 /srv/team/logbook.txt
11:35:30  student  room   hello room, this is the host
11:35:30  maria    room   hi host! guest here
```

The room signed those lines itself, with names it got from the kernel.

### Step 6.4 Who may come in

**Host:**

```
$ sudo -u visitor nc -U /srv/team/part6/room.sock
nc: /srv/team/part6/room.sock: Permission denied
```

The same visitor walked straight into the TCP chat in Step 6.2. Now the Guest, who owns the socket file, takes write permission away from the group:

**Guest** (second terminal):

```
$ chmod 640 /srv/team/part6/room.sock
$ ls -l /srv/team/part6/room.sock
srw-r----- 1 maria team 0 Oct  5 11:35 /srv/team/part6/room.sock
```

If the Host is still in the room, send a line now. It still gets through: permissions are checked when you connect, and anyone already inside stays inside. Now leave with Ctrl+C.

*Predict*, Host: the group can still read the file. Can you get back in?

**Host:**

```
$ nc -U /srv/team/part6/room.sock
nc: /srv/team/part6/room.sock: Permission denied
```

Connecting to a Unix socket counts as *writing* to it, so the group needs `w`. The Guest puts it back with `chmod 660 /srv/team/part6/room.sock`, and the Host can join again.

Here's everything Part 6 found, side by side:

| Who tries to connect | TCP port 5007 | `room.sock` with `rw-rw----` | `room.sock` with `rw-r-----` |
|---|---|---|---|
| Host (in `team`) | connected | connected | Permission denied |
| visitor (not in `team`) | connected | Permission denied | Permission denied |
| Does the server learn the caller's name? | no, only a port number | yes, from the kernel | |

**Log it.** One line each: what surprised you most in this table.

### Step 6.5 Close the room

The Guest presses Ctrl+C in the room's terminal:

```
^C
Room closed.
```

The program removes `room.sock` on the way out (check with `ls /srv/team/part6`). A socket file is a name in a folder, and names stay until someone removes them.

> **Experiment: the barber with one chair.** Copy the room to a new file, `cp team_room.py one_chair.py`, and in the copy replace the line
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
> Run `one_chair.py` instead of the room. The Host joins and chats. Then the Guest joins from a second terminal and types something. *Predict* what the Guest sees. Answer: nothing at all, not even "joined". The Guest's connection was accepted by the kernel and is waiting in line, but the program is busy with the Host and won't call `accept()` again until the Host leaves. When the Host presses Ctrl+C, the Guest suddenly gets "joined", followed by the line they typed while waiting. Nothing was lost; it sat in the kernel's buffer the whole time. That's why the real room gives each caller a thread.

> **Experiment: across machines.** Everything in this lab happened on one VM. A Unix socket can only ever work that way: it's a file on one machine's disk. TCP can cross machines, which is why the internet runs on it, and it's also why TCP can't tell the server who's calling: the other end could be any computer anywhere. Proving who you are across a network takes passwords or keys, which is what SSH has been doing for you every time you log in. If your class has found that lab VMs can reach each other, try Step 6.1 between two VMs: run `hostname -I` on the Host's VM and give that address to `nc` on the other VM, instead of `localhost`.

> **If you're three.** The room was made for three. Everyone joins at once. Then try the barber with one chair: the third person waits in line behind the second.

---

## Reflection

Split the questions between you, and put the name of whoever wrote each answer next to it. Short answers are fine. Where a question asks "why", point to something you saw in the lab.

1. In Part 0, the Host was added to `team` but still got `Permission denied` until logging in again. Why?
2. In Part 1, what exactly did `chgrp team $(tty)` change, and why could the visitor still not write to the terminal? What does `mesg n` really do?
3. In Part 2, the treasure could be found by its inode number after `mv`, but not after `cp` followed by `rm`. Explain this using names and inodes.
4. In Part 3, after the Host ran `sed -i`, the Guest's copy kept the old settings and nobody saw an error. Who owns `/home/maria/my_settings.json` now, and why might that surprise the Host later?
5. In Part 3, the same symlink worked for the Host and failed for the Guest. What decides whether following a link works?
6. In Part 4, list what one user could and couldn't learn about another user's running program. Why is it a bad idea to type a password as part of a command?
7. In Part 5, why does the two-way chat need the `&`? What happened without it?
8. In Part 6, anyone could connect to the TCP port, but only the team could enter the room. Name two things the Unix socket gave you that TCP didn't.
9. Describe one moment in this lab where you couldn't have finished a step without your partner.

---

## What to hand in

One submission per team:

1. **Your logbook.** Print it with `cat /srv/team/logbook.txt` and copy everything into your submission. Or copy the file to your own computer with `scp`. Run this on your own computer, not on the VM, using the Host's address and port and your own name:

   ```
   $ scp -P 5037 maria@lab-xxxxxxxx.eastus.cloudapp.azure.com:/srv/team/logbook.txt .
   ```

   Note the capital `-P` for the port: `scp` spells it differently from `ssh`.
2. **Your reflection answers**, each marked with the name of whoever wrote it.

---

## Cleanup

Remove what this lab made, but keep the team itself: the accounts, the `team` group, `/srv/team` and the `log` tool are meant to be reused in later team labs.

**Host:**

```
$ rm -rf /srv/team/part2 /srv/team/part3 /srv/team/part4 /srv/team/part5 /srv/team/part6
$ rm -f ~/diary.txt ~/mystery.py
$ mv /srv/team/logbook.txt /srv/team/logbook-lab05.txt
```

The Host can delete files the Guest made because deleting is decided by the *folder's* permissions, and the team has write permission on these folders. Renaming the logbook means the next lab starts a fresh one.

**Guest:**

```
$ rm -f ~/my_settings.json ~/mystery.py ~/grab.txt
```

If any program from this lab is still running in some terminal, press Ctrl+C there.

**At the end of the semester**, when your team is done for good, the Guest logs out and the Host removes everything:

```
$ sudo userdel -r maria
$ sudo userdel -r visitor
$ sudo rm -rf /srv/team
$ sudo groupdel team
```

`userdel -r` also deletes the user's home folder. It refuses while that user is still logged in (`user maria is currently used by process ...`). A warning that the user's `mail spool` was `not found` is harmless: these accounts never got any mail.

---

## Troubleshooting

| What you see | Likely cause | What to do |
|---|---|---|
| `Permission denied` in `/srv/team` right after setup | Group membership is read at login (Step 0.4) | Log out and connect again, then check `id` |
| Guest can't log in | Wrong name, wrong port, or a typo in the temporary password | Use the Host's address and port with the Guest's name; the Host can reset it with `sudo passwd maria` |
| `log: command not found` | The alias isn't loaded in this terminal | `source ~/.bashrc`, or type the full `/srv/team/log` |
| `/srv/team/log: Permission denied` | The script isn't executable | `chmod +x /srv/team/log` (whoever created it) |
| Your partner can't change a file you made | Your `umask` is `0022` (Step 0.6) | `chmod g+w thefile` now, and `umask 002` for next time |
| `-bash: !great: event not found`, or an old command shows up inside your log line | Inside double quotes, bash treats `!` as "something from your history"; `!!` means "the last command" | Use single quotes: `log 'wow!great'` |
| `write: effective gid does not match group of ...` | Ubuntu's 2024 security fix (Step 1.2) | Write to the terminal file directly, as Part 1 does |
| A command just sits there | A named pipe waiting for its other end (Parts 2 and 5) | Open the other end, or press Ctrl+C |
| `pgrep` prints nothing | The program isn't running, or it's a different user | Check the user name after `-u`, and that the program is still running |
| `nc: ... room.sock: Permission denied` | Not in `team`, the socket isn't group-writable, or you haven't logged in again since joining `team` | `ls -l` the socket file, and run `id` |
| `nc: ... room.sock: No such file or directory` or `Connection refused` | The room isn't running | Start `team_room.py` first |
| `sudo` asks for a password | That's normal | It wants the Host's own password |
| The VM stops in the middle of the lab | Your lab's automatic shutdown settings, or the Host's quota ran out | Restart it from the Azure Lab Services page; the Host should stay logged in |

---

## Quick reference: who got in?

| Thing | What decides access | Teammate | Visitor | Root |
|---|---|---|---|---|
| `/srv/team` and everything in it | the folder: `drwxrws---`, group `team` | yes | no | yes |
| Your terminal, `/dev/pts/N` | your terminal file; you choose with `chgrp` and `chmod` | only if you let them | no | yes |
| Your home folder | `drwxr-x---` | no | no | yes |
| A running program's command line and status | readable by everyone | yes | yes | yes |
| A running program's open files and working folder | owner only | no | no | yes |
| A named pipe in `/srv/team` | the folder, then the pipe's own permissions | yes | no | yes |
| A TCP port | nothing at all | yes | yes | yes |
| A Unix socket file | the folder, then the socket's own permissions (connecting needs `w`) | yes, with `rw-rw----` | no | yes |
