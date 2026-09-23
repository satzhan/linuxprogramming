# Lab: Users, Groups, Permissions, umask and sudo

dev_alex writes a small Python script. The team he's on, dev_team, should be able to run it. dev_bob isn't on the team yet, so he shouldn't. Later bob gets promoted, and at the very end a brand-new account gets the right to use sudo, then loses it again.

Along the way you'll create users and groups, hand a file over to a team, watch Linux say no (and later yes), find out what umask does to new files, and give someone administrator rights. Everything gets cleaned up at the end.

The reference page, *Who gets in*, explains the reasoning behind each step. This lab is the hands-on part. Keep both open.

---

## Before you start

**Where to do this.** Any Linux machine where your account can use `sudo`: your GitHub Codespace, a departmental VM, Ubuntu under WSL, or a virtual machine of your own. A Codespace is ideal, because it's disposable. Everything here was tested on Ubuntu 24.04. Please don't do this lab on a server other people rely on.

**How to read the commands.** A line starting with `$` is something you type (leave out the `$` itself). Lines without it are what the computer prints back.

```
$ whoami
codespace
```

Your output will differ in the details: user IDs, group IDs, dates, file sizes, sometimes a default value. What should match is the shape. Where a difference is likely, the lab says so.

**Your home base.** Type `whoami` now and remember the answer. That's your own account, the one allowed to use sudo, and every `sudo` command in this lab is typed from there. You'll switch into other users a lot. Whenever the lab says *back at home base*, type `exit` until `whoami` prints your own name again. Most prompts show the current user too, something like `dev_alex@...:~$`.

**The optional parts.** Anything marked **Try another way** or **Experiment** is optional. The main path works without them. Most of the surprises live in the experiments, though, so do the ones you have time for.

**If something says it already exists**, you've probably run part of this lab before. Go to [Cleanup](#cleanup), run it, and start again.

**Order.** Part 2 needs the users from Part 1. Parts 3 and 4 stand on their own and can be done in any order.

---

## Part 1: Users and groups

### Step 1.1 Look around before changing anything

```
$ whoami
$ id
$ tail -n 3 /etc/passwd
```

`id` shows your user ID, your primary group, and every other group you belong to. You may or may not see `sudo` in that list; some systems grant sudo rights another way. `tail` prints the last three accounts on the system, one per line, with fields separated by colons. New accounts get added at the bottom, so this is where yours will show up.

### Step 1.2 Create the team group

```
$ sudo groupadd dev_team
$ grep dev_team /etc/group
dev_team:x:1002:
```

Four fields: the name, an unused password field (`x`), the group ID, and the member list. The list is empty because nobody has joined yet. Your group ID may be a different number.

> **Try another way.** `getent group dev_team` prints the same line. `getent` asks the system's account lookup instead of reading the file directly, which matters on machines that also get accounts from a network directory.

### Step 1.3 Create dev_alex

```
$ sudo useradd -m -s /bin/bash dev_alex
```

No output means it worked. `-m` makes a home directory, `/home/dev_alex`. `-s /bin/bash` gives him the bash shell. Leave `-s` off and Ubuntu gives the account `/bin/sh`, which works but has no tab completion and no arrow-key history.

```
$ ls -ld /home/dev_alex
drwxr-x--- 2 dev_alex dev_alex 4096 Sep 23 16:33 /home/dev_alex
```

Keep that `drwxr-x---` in mind. It matters in Part 2.

> **Try another way.** On Ubuntu and Debian, `sudo adduser dev_alex` does this step and the next one together. It asks for a password and a few optional details (press Enter to skip those), and it sets bash automatically. You may notice it also adds him to a group called `users`, which is harmless. If you go this way, skip Step 1.4.

### Step 1.4 Give dev_alex a password

```
$ sudo passwd dev_alex
New password:
Retype new password:
passwd: password updated successfully
```

Nothing shows while you type. Not a letter, not a dot. Pick something you'll remember for the next hour; the account won't outlive the lab. If you get a `BAD PASSWORD` warning, it's advice. Because you're using sudo, the password is normally accepted anyway.

### Step 1.5 Put dev_alex on the team

```
$ id dev_alex
uid=1001(dev_alex) gid=1003(dev_alex) groups=1003(dev_alex)
$ sudo usermod -aG dev_team dev_alex
$ id dev_alex
uid=1001(dev_alex) gid=1003(dev_alex) groups=1003(dev_alex),1002(dev_team)
$ groups dev_alex
dev_alex : dev_alex dev_team
```

Notice that dev_alex already belonged to a group before you did anything: a group called `dev_alex`, with him as its only member. That's his *primary* group, created for him automatically. `dev_team` is a *supplementary* group, an extra membership.

The `-a` in `-aG` means *append*. Without it, `-G` throws away his whole list of extra groups and replaces it with what you typed. Step 1.8 lets you watch that happen.

> **Try another way.** `sudo gpasswd -a dev_alex dev_team` does the same thing. So does `sudo adduser dev_alex dev_team` on Ubuntu and Debian. Both can only add, never replace, which makes them hard to get wrong.

### Step 1.6 Read the account files

```
$ grep dev_alex /etc/passwd
dev_alex:x:1001:1003::/home/dev_alex:/bin/bash
$ grep dev_team /etc/group
dev_team:x:1002:dev_alex
```

The passwd line has seven fields: name, `x`, user ID, primary group ID, a comment (empty here, which is why you see `::`), home directory, and login shell. The group line now lists dev_alex as a member.

That `x` in the passwd line means "the password is kept somewhere else".

> **Experiment.** Look for the password yourself:
>
> ```
> $ cat /etc/shadow
> cat: /etc/shadow: Permission denied
> $ sudo grep dev_alex /etc/shadow
> ```
>
> The first fails because only root may read `/etc/shadow`. The second shows a long scrambled string, the hashed password. The scrambling only works in one direction: when dev_alex logs in, the system scrambles what he typed the same way and compares the two results.

### Step 1.7 Become dev_alex, then come back

```
$ su - dev_alex
Password:
$ whoami
dev_alex
$ pwd
/home/dev_alex
$ exit
logout
$ whoami
```

The last `whoami` should print your own name again. `su` asks for **dev_alex's** password, the one you set in Step 1.4, not yours. The dash gives you a proper login as him, in his home directory with his shell. `exit` takes you back to home base.

If `su` says `su: Authentication failure`, the password didn't match. Set a new one with `sudo passwd dev_alex`, or use the way below.

> **Try another way.** `sudo -iu dev_alex` gives you the same login without knowing his password. It asks for yours instead (in a Codespace it usually doesn't ask at all). Leave with `exit`, as always.

### Step 1.8 Experiment: forget the `-a`

```
$ sudo groupadd scratch
$ sudo usermod -G scratch dev_alex
$ id dev_alex
uid=1001(dev_alex) gid=1003(dev_alex) groups=1003(dev_alex),1004(scratch)
```

dev_team is gone. `-G` without `-a` replaced his list instead of adding to it. Put things right:

```
$ sudo usermod -aG dev_team dev_alex
$ sudo gpasswd -d dev_alex scratch
Removing user dev_alex from group scratch
$ sudo groupdel scratch
$ id dev_alex
uid=1001(dev_alex) gid=1003(dev_alex) groups=1003(dev_alex),1002(dev_team)
```

**Before moving on:** `id dev_alex` must show `dev_team`. Part 2 depends on it.

---

## Part 2: Permissions

### Step 2.1 Create dev_bob, not on the team

```
$ sudo useradd -m -s /bin/bash dev_bob
$ sudo passwd dev_bob
$ id dev_bob
uid=1002(dev_bob) gid=1004(dev_bob) groups=1004(dev_bob)
```

Only his own private group. As far as dev_team is concerned, bob is a stranger.

### Step 2.2 Why the script won't live in alex's home

Look at alex's home directory again:

```
$ ls -ld /home/dev_alex
drwxr-x--- 2 dev_alex dev_alex 4096 Sep 23 16:33 /home/dev_alex
```

Read the last three characters, `---`. They're for everyone who isn't alex and isn't in the group `dev_alex`. No `r`, so they can't list what's inside. No `x`, so they can't pass through it at all. To reach any file you need `x` on every directory along its path, and only then do the file's own permissions matter. A path is a hallway of doors, and this door is locked.

Joining dev_team wouldn't help bob here either. This directory's group is `dev_alex`, not `dev_team`.

If yours shows `drwxr-xr-x`, your system uses an older default. The rest of the lab works the same either way, because the script is going somewhere else.

### Step 2.3 Make a shared folder for the team

```
$ sudo mkdir -p /srv/devteam
$ sudo chown dev_alex:dev_team /srv/devteam
$ sudo chmod 775 /srv/devteam
$ ls -ld /srv/devteam
drwxrwxr-x 2 dev_alex dev_team 4096 Sep 23 16:33 /srv/devteam
```

Reading that string: the owner (alex) and the group (dev_team) can list, add, remove and enter. Everyone else can walk in and read the names, nothing more. `/srv` is the traditional spot for data a machine serves up, so a team folder fits there.

> **Try another way.** `sudo chmod u=rwx,g=rwx,o=rx /srv/devteam` sets exactly the same permissions using letters instead of digits.

### Step 2.4 As dev_alex, write the script

```
$ su - dev_alex
$ cd /srv/devteam
$ nano hello.py
```

Type these two lines:

```python
#!/usr/bin/env python3
print("Hello, dev_team!")
```

Save with `Ctrl+O` then `Enter`, and leave with `Ctrl+X`. Check it:

```
$ cat hello.py
#!/usr/bin/env python3
print("Hello, dev_team!")
```

The first line is called a *shebang*. It tells Linux which program should run the file when someone runs the file directly. Step 2.7 shows when that matters.

> **Try another way (no editor).** Type this exactly. Everything between the two `EOF` lines goes into the file:
>
> ```
> $ cat > hello.py << 'EOF'
> #!/usr/bin/env python3
> print("Hello, dev_team!")
> EOF
> ```
>
> Use this if `nano` isn't installed. dev_alex can't install it himself: he has no sudo rights. If you prefer `vim`, that works too.

### Step 2.5 Look at what you made

```
$ ls -l hello.py
-rw-r--r-- 1 dev_alex dev_alex 49 Sep 23 16:33 hello.py
```

Two things to notice. The group is `dev_alex`, not `dev_team`, because new files belong to their creator's primary group. And nobody has `x`: new files never start out executable (Part 3 explains why). You might see `-rw-rw-r--` instead, which just means a different umask, also covered in Part 3. The size may be off by a byte or two depending on how you typed it.

### Step 2.6 Hand the file to the team

```
$ chgrp dev_team hello.py
$ chmod 770 hello.py
$ ls -l hello.py
-rwxrwx--- 1 dev_alex dev_team 49 Sep 23 16:33 hello.py
```

No `sudo` here, on purpose. dev_alex doesn't have sudo rights, and he doesn't need them: the owner of a file may switch its group to any group he belongs to. Only giving a file to a different *owner* needs root.

`770` is three digits for three audiences. `7` is `rwx` for the owner, `7` is `rwx` for the group, `0` is nothing for everyone else. (r counts 4, w counts 2, x counts 1, added up per audience.)

> **Try another way.** All of these land in the same place:
>
> ```
> $ chown :dev_team hello.py          # instead of chgrp
> $ chmod u=rwx,g=rwx,o= hello.py     # letters instead of 770
> $ chmod ug+x,g+w,o-r hello.py       # small changes starting from rw-r--r--
> ```
>
> And for the full picture, run `stat hello.py` and find the line starting with `Access:`. It shows both notations side by side, `(0770/-rwxrwx---)`.

### Step 2.7 Run it, two ways

```
$ python3 hello.py
Hello, dev_team!
$ ./hello.py
Hello, dev_team!
```

Same output, different mechanics. In the first, you run `python3`, and python3 reads hello.py like any text file, so the file only needs `r`. In the second, you run the file itself, which needs `x` on the file plus the shebang line to say which interpreter to use.

### Step 2.8 Experiment: take the `x` away

```
$ chmod 660 hello.py
$ python3 hello.py
Hello, dev_team!
$ ./hello.py
-bash: ./hello.py: Permission denied
$ chmod 770 hello.py
```

Reading was still allowed, so python3 didn't care. Only running the file directly needed `x`. The last line puts it back to 770; make sure you ran it.

### Step 2.9 Experiment: the owner who locked himself out

Still as dev_alex:

```
$ chmod 070 hello.py
$ ls -l hello.py
----rwx--- 1 dev_alex dev_team 49 Sep 23 16:33 hello.py
$ cat hello.py
cat: hello.py: Permission denied
```

alex is in dev_team, and the group has `rwx`, so why the refusal? Linux applies exactly one of the three triplets to you, checking in a fixed order: owner first, then group, then everyone else. alex is the owner, so the owner triplet, `---`, is his answer, and the group triplet is never consulted. He can still fix it, because the owner can always `chmod` his own file:

```
$ chmod 770 hello.py
```

Now leave, back to home base:

```
$ exit
```

### Step 2.10 dev_bob tries, and fails

```
$ su - dev_bob
$ ls -l /srv/devteam
total 4
-rwxrwx--- 1 dev_alex dev_team 49 Sep 23 16:33 hello.py
$ python3 /srv/devteam/hello.py
python3: can't open file '/srv/devteam/hello.py': [Errno 13] Permission denied
$ cat /srv/devteam/hello.py
cat: /srv/devteam/hello.py: Permission denied
$ ls /home/dev_alex
ls: cannot open directory '/home/dev_alex': Permission denied
$ exit
```

bob can see that the file exists, because the folder gives everyone `r` and `x`. But he's not the owner and not in dev_team, so the file's last triplet applies to him, and it's `---`. And alex's home is closed to him completely, as Step 2.2 predicted.

### Step 2.11 Promote dev_bob

Back at home base:

```
$ sudo usermod -aG dev_team dev_bob
$ groups dev_bob
dev_bob : dev_bob dev_team
```

### Step 2.12 dev_bob tries again

```
$ su - dev_bob
$ id
uid=1002(dev_bob) gid=1004(dev_bob) groups=1004(dev_bob),1002(dev_team)
$ python3 /srv/devteam/hello.py
Hello, dev_team!
$ /srv/devteam/hello.py
Hello, dev_team!
$ exit
```

This worked because you logged in as bob *after* the change. Group memberships are read once, at login, and every program started in that session inherits them. A shell that was already open keeps its old list until it logs out.

> **Experiment: the stale session.** This one needs two terminals. In a Codespace or VS Code, open a second one with the **+** button in the terminal panel. Call them A and B.
>
> 1. In **B**: `su - dev_bob`, then `id`. dev_team is listed.
> 2. In **A** (home base): `sudo gpasswd -d dev_bob dev_team`.
> 3. In **B**: `id` again, then `python3 /srv/devteam/hello.py`. He's still in the team, and the script still runs.
> 4. In **B**: `exit`, then `su - dev_bob` again, then `id` and `python3 /srv/devteam/hello.py`. Now dev_team is gone and he's refused.
> 5. In **A**: put him back with `sudo usermod -aG dev_team dev_bob`. In **B**: `exit`.
>
> The lesson cuts both ways. Adding someone to a group doesn't take effect until they log in again, and neither does removing them. On a real server, taking access away properly also means ending their open sessions.

### Step 2.13 Experiment: who gets to delete

As alex, make a file that's read-only for everyone:

```
$ su - dev_alex
$ echo "please don't delete me" > /srv/devteam/notes.txt
$ chmod 444 /srv/devteam/notes.txt
$ ls -l /srv/devteam/notes.txt
-r--r--r-- 1 dev_alex dev_alex 23 Sep 23 16:33 /srv/devteam/notes.txt
$ exit
```

Now bob, who's on the team, so the folder lets him write:

```
$ su - dev_bob
$ rm /srv/devteam/notes.txt
rm: remove write-protected regular file '/srv/devteam/notes.txt'? y
$ ls /srv/devteam
hello.py
$ exit
```

bob couldn't have changed a single character inside notes.txt, and yet he deleted it. Deleting a file means removing its name from the folder's list of names, which is a change to the *folder*, not to the file. The folder gives dev_team `w`, so bob wins. The question `rm` asked is rm being polite; the system had already agreed.

The fix is the *sticky bit*, the `t` you can see at the end of `/tmp`'s permissions:

```
$ ls -ld /tmp
drwxrwxrwt 6 root root 4096 Sep 23 16:32 /tmp
$ sudo chmod +t /srv/devteam
$ ls -ld /srv/devteam
drwxrwxr-t 2 dev_alex dev_team 4096 Sep 23 16:33 /srv/devteam
```

Repeat the first block of this step (as alex, create notes.txt and make it 444). Then:

```
$ su - dev_bob
$ rm -f /srv/devteam/notes.txt
rm: cannot remove '/srv/devteam/notes.txt': Operation not permitted
$ exit
```

In a sticky folder you can delete only files you own (the folder's owner can still delete anything). That's how `/tmp` lets everyone write without letting everyone erase each other's work.

### Step 2.14 Experiment: stop needing chgrp

Every new file in `/srv/devteam` starts out in its creator's primary group, so somebody has to `chgrp` it each time. The *setgid* bit on a folder changes that: new files inside take the folder's group automatically.

```
$ sudo chmod g+s /srv/devteam
$ ls -ld /srv/devteam
drwxrwsr-t 2 dev_alex dev_team 4096 Sep 23 16:33 /srv/devteam
$ su - dev_alex
$ touch /srv/devteam/new.py
$ ls -l /srv/devteam/new.py
-rw-r--r-- 1 dev_alex dev_team 0 Sep 23 16:33 /srv/devteam/new.py
$ exit
```

Group `dev_team`, no chgrp. The `s` sitting where the group's `x` would be is the setgid bit. (If you skipped Step 2.13, you'll see `x` instead of `t` at the very end.)

---

## Part 3: umask

Do this part at home base. It doesn't need anything from Parts 1 or 2.

### Step 3.1 Set up and look

```
$ mkdir ~/umask_lab
$ cd ~/umask_lab
$ umask
0022
$ umask -S
u=rwx,g=rx,o=rx
```

Yours might say `0002`. Both are common defaults. `umask` shows which permission bits get *removed* from new files. `umask -S` shows the other side: which letters are still allowed through.

### Step 3.2 Make something with the default

```
$ touch file_default
$ mkdir dir_default
$ ls -l
total 4
drwxr-xr-x 2 you you 4096 Sep 23 16:33 dir_default
-rw-r--r-- 1 you you    0 Sep 23 16:33 file_default
```

(You'll see your own name where it says `you`.)

Programs ask for `666` on new files and `777` on new directories. umask removes bits from that request, like painter's tape over some of the slots: `666` with 022 taped over is `644`, and `777` becomes `755`. Tape can keep paint off but never add any, which is why files don't get `x` when they're created. Nobody asked for it, and umask can't put it there.

### Step 3.3 Try several values

One at a time, repeating this pattern with different numbers:

```
$ umask 077
$ touch file_077
$ mkdir dir_077
$ ls -ld file_077 dir_077
```

Do it for `022`, `002`, `027`, `007`, `077` and `033`.

> **Try another way: all at once with a loop.**
>
> ```
> $ for m in 022 002 027 007 077 033; do umask $m; touch file_$m; mkdir dir_$m; done
> $ ls -l
> ```
>
> The loop sets each umask in turn and creates one file and one directory under each.

Either way, you should end up with this:

```
total 28
drwxrwxr-x 2 you you 4096 Sep 23 16:33 dir_002
drwxrwx--- 2 you you 4096 Sep 23 16:33 dir_007
drwxr-xr-x 2 you you 4096 Sep 23 16:33 dir_022
drwxr-x--- 2 you you 4096 Sep 23 16:33 dir_027
drwxr--r-- 2 you you 4096 Sep 23 16:33 dir_033
drwx------ 2 you you 4096 Sep 23 16:33 dir_077
drwxr-xr-x 2 you you 4096 Sep 23 16:33 dir_default
-rw-rw-r-- 1 you you    0 Sep 23 16:33 file_002
-rw-rw---- 1 you you    0 Sep 23 16:33 file_007
-rw-r--r-- 1 you you    0 Sep 23 16:33 file_022
-rw-r----- 1 you you    0 Sep 23 16:33 file_027
-rw-r--r-- 1 you you    0 Sep 23 16:33 file_033
-rw------- 1 you you    0 Sep 23 16:33 file_077
-rw-r--r-- 1 you you    0 Sep 23 16:33 file_default
```

Line each one up against its umask and find which letters went missing.

**Important:** your shell now has whatever umask you set last (033, if you used the loop). Put it back before continuing:

```
$ umask 0022
```

(Use the value Step 3.1 showed, if it was different.)

### Step 3.4 The subtraction trap

You may have been doing subtraction in your head: 666 − 022 = 644. It works for the usual values, so it's a natural guess. Now look at `file_033`. Subtraction predicts 666 − 033 = 633, which would be `rw--wx-wx`.

```
$ ls -l file_033
-rw-r--r-- 1 you you 0 Sep 23 16:33 file_033
```

644, not 633. umask doesn't subtract. It removes the listed bits if they're there and ignores them if they aren't. 033 says "no `w`, no `x`" for the group and for others. The file never asked for `x`, so that part of the mask had nothing to remove, and nothing gets "borrowed" from the neighbouring bits the way it does in subtraction.

Look at `dir_033` while you're here: `drwxr--r--`. Others may list the names inside (`r`) but can't enter (no `x`). An odd combination, and one reason nobody uses 033.

### Step 3.5 umask never touches existing files

```
$ umask 077
$ ls -l file_default
-rw-r--r-- 1 you you 0 Sep 23 16:33 file_default
$ umask 0022
```

Still 644. umask shapes only files created after it's set. For files that already exist, use `chmod`.

### Step 3.6 Experiment: make it stick

A umask typed at the prompt lasts until that terminal closes. To make it permanent for an account, add it to the account's `~/.bashrc`. Practise on dev_alex, since he gets deleted at the end anyway (skip this if you didn't do Part 1):

```
$ su - dev_alex
$ echo 'umask 027' >> ~/.bashrc
$ exit
$ su - dev_alex
$ umask
0027
$ exit
```

`>>` adds a line to the end of the file. A single `>` would replace the whole file with that one line, so check which one you typed, every time.

---

## Part 4: sudo

This part doesn't need anything from the earlier parts. Start at home base.

### Step 4.1 What are you allowed to do?

```
$ sudo -l
```

The last lines list what your account may run as root. In a Codespace you'll probably see `(ALL) NOPASSWD: ALL`: everything, no password needed. Elsewhere it's often `(ALL : ALL) ALL`, which means everything, after you type your password.

### Step 4.2 Create newuser

```
$ sudo useradd -m -s /bin/bash newuser
$ sudo passwd newuser
$ id newuser
uid=1003(newuser) gid=1005(newuser) groups=1005(newuser)
```

### Step 4.3 newuser tries sudo, and is refused

```
$ su - newuser
$ sudo ls -la /root
[sudo] password for newuser:
newuser is not in the sudoers file.
$ exit
```

sudo asks for **newuser's own** password, not root's, and then checks the rules and says no. Older versions of sudo add "This incident will be reported." The refusal does get logged.

### Step 4.4 Find the rule that matters

```
$ sudo grep '^%sudo' /etc/sudoers
%sudo	ALL=(ALL:ALL) ALL
```

Left to right: members of the group `sudo` (the `%` means "group"), on any machine, may act as any user and any group, and run any command. So on Ubuntu, joining the `sudo` group is all it takes.

If there's no `%sudo` line, your system probably uses a group called `wheel` (Fedora and RHEL do). Use `wheel` wherever this lab says `sudo` as a group name.

> **Try another way.** `sudo cat /etc/sudoers` shows the whole file. `sudo visudo` opens it in an editor, and it's the only safe way to *change* it, because it checks your syntax before saving. A typo saved straight into this file can break sudo for everyone. Today, just look. To leave without saving: in nano, press `Ctrl+X` (and `N` if it asks about saving); if it opens in vi instead, type `:q!` and press `Enter`.

### Step 4.5 Promote newuser

```
$ sudo usermod -aG sudo newuser
$ groups newuser
newuser : newuser sudo
```

> **Try another way.** `sudo gpasswd -a newuser sudo`, or on Ubuntu and Debian, `sudo adduser newuser sudo`.

### Step 4.6 newuser tries again

A fresh login, so the new group counts:

```
$ su - newuser
$ sudo ls -la /root
[sudo] password for newuser:
total 24
drwx------  4 root root 4096 Apr 18 18:13 .
drwxr-xr-x 22 root root 4096 Sep 23 16:32 ..
-rw-r--r--  1 root root 3106 Apr 22  2024 .bashrc
-rw-r--r--  1 root root  161 Apr 22  2024 .profile
...
$ sudo whoami
root
$ sudo -l
...
User newuser may run the following commands on ...:
    (ALL : ALL) ALL
```

The exact files in `/root` will differ on your machine.

Why `ls -la` and not plain `ls`? Root's home usually contains only hidden files, so `sudo ls /root` often prints nothing at all. That silence isn't an error.

Notice that `sudo whoami` didn't ask for the password again. sudo remembers you for a while (15 minutes by default). Make it forget and watch the prompt come back:

```
$ sudo -k
$ sudo whoami
[sudo] password for newuser:
root
$ exit
```

### Step 4.7 Experiment: take it away

Back at home base:

```
$ sudo gpasswd -d newuser sudo
Removing user newuser from group sudo
$ su - newuser
$ sudo -l
[sudo] password for newuser:
Sorry, user newuser may not run sudo on <your machine's name>.
$ exit
```

---

## Cleanup

Make sure nobody from this lab is still logged in anywhere: type `exit` in every terminal until `whoami` shows your own name, and close any extra terminals you opened for Step 2.12. Then:

```
$ whoami
$ sudo rm -r /srv/devteam
$ sudo userdel -r dev_alex
userdel: dev_alex mail spool (/var/mail/dev_alex) not found
$ sudo userdel -r dev_bob
userdel: dev_bob mail spool (/var/mail/dev_bob) not found
$ sudo userdel -r newuser
userdel: newuser mail spool (/var/mail/newuser) not found
$ sudo groupdel dev_team
$ rm -r ~/umask_lab
```

The mail spool messages are harmless. `userdel -r` tried to tidy up a mailbox that never existed. `-r` is what removes each home directory; without it the accounts would vanish and their files would stay behind.

Skip any line for something you didn't create. If you changed your umask and this is still the same terminal, run `umask 0022` too (or just close the terminal).

Check that it's all gone:

```
$ id dev_alex
id: 'dev_alex': no such user
$ getent group dev_team
$ ls /home
```

`getent` prints nothing when the group doesn't exist, and `/home` should no longer contain `dev_alex`, `dev_bob` or `newuser`.

---

## If something goes wrong

| You see | Likely reason | What to do |
|---|---|---|
| `useradd: user 'dev_alex' already exists` (or a group that already exists) | Leftovers from an earlier attempt | Run [Cleanup](#cleanup), then start over |
| `su: Authentication failure` | Wrong password for that user | `sudo passwd dev_alex` to set a new one, or use `sudo -iu dev_alex` |
| `dev_alex is not in the sudoers file` | You typed a `sudo` command while switched into a lab user | `exit` back to home base and try again |
| `Permission denied` where you expected success | Wrong user, a login from before a group change, or a locked directory on the path | Check `whoami`; log out and `su -` in again; run `ls -ld` on each directory along the path |
| `userdel: user dev_bob is currently used by process 1234` | Some terminal is still logged in as bob | `exit` everywhere and retry; as a last resort, `sudo pkill -u dev_bob` |
| A bare `$` prompt with no tab completion | The account was created without `-s /bin/bash` | `sudo usermod -s /bin/bash dev_alex`, then log in again |
| `nano: command not found` | nano isn't installed | Use the `cat > hello.py << 'EOF'` method from Step 2.4 |
| `groupdel: cannot remove the primary group of user ...` | A user still has that group as primary | Delete the user first, then the group |
