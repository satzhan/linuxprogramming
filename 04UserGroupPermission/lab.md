# Linux access lab

Users, groups, file permissions, umask, and sudo

Work through this lab in order. You will create two developers, give them access to a small project, change that access, and then give a separate practice account administrative access. Every exercise includes the commands you need and what to look for. Optional variations give you another way to do the same job or a small change to investigate.

The companion `linux-access-reference.html` explains the commands and permission rules. Nothing needs to be submitted or screenshotted.

## Before you begin

Use your own disposable Ubuntu environment, such as a course VM or an Ubuntu Codespace where your normal account can use `sudo`. These instructions use Bash, GNU command-line tools, and Ubuntu's usual `sudo` group policy. A Mac terminal by itself is not this environment. On a shared course server, use only the environment assigned for this lab.

You need `sudo`, `python3`, and the account tools already installed. From your normal terminal, run:

```bash
cat /etc/os-release
whoami
id
command -v sudo python3 useradd usermod groupadd
sudo -v
```

`sudo -v` checks that your account can authenticate to sudo; it may ask for **your normal account's password**. Some course environments do not ask for a password. If a required command is missing or sudo is denied, use the course's prepared environment before continuing.

Check for old lab accounts and files:

```bash
getent passwd dev_alex dev_bob newuser
getent group dev_team dev_review
ls -ld /srv/access-lab /home/dev_alex /home/dev_bob /home/newuser
```

For a fresh lab, these accounts, groups, and paths should not exist. No output from `getent` and “No such file or directory” from `ls` are expected here. If something already exists, establish whether it is yours before changing it. Use a fresh environment if you cannot tell. Do not repeat account creation over an existing setup.

### Keep track of which account is typing

| Label used below | Where to run the commands |
| --- | --- |
| **Admin terminal** | Your original terminal, under your normal account with sudo access. |
| **Alex shell** | A shell opened with `sudo -iu dev_alex`. |
| **Bob shell** | A shell opened with `sudo -iu dev_bob`. |
| **Newuser shell** | A shell opened with `sudo -iu newuser`. |

Keep the admin terminal open. Use a second terminal for the practice accounts. Type `exit` to leave a practice shell before entering another. If you lose track, run `whoami`; do not keep nesting shells.

The command blocks have no `$` prompt, so you can copy them directly. Run them one block at a time. Successful commands such as `chmod` often print nothing. UIDs, GIDs, timestamps, and exact error wording will vary; compare the names, permission bits, and allow/deny result.

## Part 1 — Users and groups

### 1. Create the team and its two developers

**Admin terminal:**

```bash
sudo groupadd dev_team
sudo useradd -m -U -s /bin/bash dev_alex
sudo useradd -m -U -s /bin/bash dev_bob
sudo usermod -aG dev_team dev_alex
```

`-m` creates a home directory. `-U` creates a private primary group with the user's name. `-s /bin/bash` gives the account a Bash shell. Bob has his private group, but is not yet a member of `dev_team`.

Inspect the result:

```bash
id dev_alex
id dev_bob
getent passwd dev_alex
getent group dev_team
ls -ld /home/dev_alex /home/dev_bob
```

**Look for:** Alex belongs to `dev_team`; Bob does not. Both home directories exist. Their initial permissions depend on the machine's account-creation settings.

Optional alternative for inspection:

```bash
groups dev_alex
groups dev_bob
```

`getent passwd` and `getent group` without a name list all entries available through the system's configured account databases.

### 2. Enter a developer's shell

**Second terminal, starting under your normal account:**

```bash
sudo -iu dev_alex
whoami
pwd
id
```

**Look for:** `whoami` prints `dev_alex`, `pwd` prints `/home/dev_alex`, and `id` includes `dev_team`. Leave the shell:

```bash
exit
```

**Optional password route.** The lab uses `sudo -iu` so you do not need developer passwords. To practice `su` instead, set Alex's password from the admin terminal:

```bash
sudo passwd dev_alex
```

Then, from your normal non-root account:

```bash
su - dev_alex
whoami
exit
```

`su - dev_alex` normally asks for **Alex's password**. `sudo -iu dev_alex` uses the invoking account's sudo authorization. Password typing normally produces no visible characters.

### 3. Prepare a project directory

**Admin terminal:**

```bash
sudo mkdir /srv/access-lab
sudo chown dev_alex:dev_team /srv/access-lab
sudo chmod 755 /srv/access-lab
ls -ld /srv/access-lab
stat -c '%A %a %U %G %n' /srv/access-lab
```

The `stat` result should be:

```text
drwxr-xr-x 755 dev_alex dev_team /srv/access-lab
```

This folder starts searchable by everyone so our first test can isolate the file's permissions. Later you will restrict the folder too. Using a dedicated project directory also avoids depending on whether Alex's home directory is private.

## Part 2 — Files, directories, and access

### 4. Create a small Python program

Open an **Alex shell** from your normal account in the second terminal:

```bash
sudo -iu dev_alex
cd /srv/access-lab
```

Choose **one** method to create the file.

**Option A: paste this complete block.** `PY` on the last line must be alone.

```bash
cat > hello.py <<'PY'
#!/usr/bin/env python3
print("Hello, dev_team!")
PY
```

**Option B: use an editor.** If `nano` is installed, run `nano hello.py`, type the two lines below, then press Ctrl+O, Enter, and Ctrl+X.

```python
#!/usr/bin/env python3
print("Hello, dev_team!")
```

Still as **Alex**, set the file's group and permissions:

```bash
chgrp dev_team hello.py
chmod 750 hello.py
stat -c '%A %a %U %G %n' hello.py
./hello.py
```

**Expected:**

```text
-rwxr-x--- 750 dev_alex dev_team hello.py
Hello, dev_team!
```

Alex owns the file and belongs to `dev_team`, so Alex can use `chgrp` here without sudo. The first line of the file, called a *shebang*, tells Linux which interpreter to use when you run `./hello.py`.

### 5. Give Bob access through the group

In the **Alex shell**, return to your normal account:

```bash
exit
```

Open a **Bob shell**:

```bash
sudo -iu dev_bob
id
/srv/access-lab/hello.py
```

**Expected:** permission denied. Bob can traverse the folder, but the file gives “others” no access. Leave this Bob shell open.

In the **admin terminal**:

```bash
sudo usermod -aG dev_team dev_bob
id dev_bob
```

The account database now lists Bob in `dev_team`. In the **already-open Bob shell**, try:

```bash
id
/srv/access-lab/hello.py
```

**Expected:** the old shell still lacks the group and execution still fails. An existing process keeps its group list; changing the account record does not rewrite it.

Leave that shell and open a fresh one:

```bash
exit
sudo -iu dev_bob
id
/srv/access-lab/hello.py
```

Now `id` should include `dev_team`, and the program should print `Hello, dev_team!`.

```bash
exit
```

### 6. Separate reading a script from executing it

Open an **Alex shell**:

```bash
sudo -iu dev_alex
cd /srv/access-lab
chmod 640 hello.py
ls -l hello.py
```

Run these **separately**:

```bash
./hello.py
```

```bash
python3 hello.py
```

The first is denied because the script has no execute permission. The second prints the greeting because Python is the program being executed; Python reads `hello.py` as input.

Restore the file using **either** form:

```bash
chmod 750 hello.py
```

Or:

```bash
chmod u=rwx,g=rx,o= hello.py
```

Both give the same ordinary permission bits. A numeric mode sets the whole `rwx` pattern. Symbolic forms can set it or change just part of it.

### 7. Add and remove one permission

Still in the **Alex shell**:

```bash
chmod g+w hello.py
stat -c '%a %A' hello.py
chmod g-w hello.py
stat -c '%a %A' hello.py
```

The two results should be `770 -rwxrwx---` and `750 -rwxr-x---`.

Optional variation: temporarily use `chmod 700 hello.py`. Bob will lose access even though he still belongs to `dev_team`. Restore `chmod 750 hello.py` afterward.

### 8. A readable file can be behind an inaccessible folder

Still as **Alex**:

```bash
chmod 750 /srv/access-lab
```

In the **admin terminal**, run this one command as Bob:

```bash
sudo -u dev_bob /srv/access-lab/hello.py
```

It should work. `sudo -u dev_bob` here launches a command under Bob's account; it does not give that command root's file access.

Back in the **Alex shell**:

```bash
chmod g-x /srv/access-lab
ls -ld /srv/access-lab
```

The directory is now `740`, or `drwxr-----`. In the **admin terminal**:

```bash
sudo -u dev_bob cat /srv/access-lab/hello.py
```

**Expected:** permission denied even though the file itself still grants the group read access. Bob needs search permission, `x`, on every directory along the path.

Restore the directory in the **Alex shell**:

```bash
chmod g+x /srv/access-lab
```

Repeat Bob's `cat` command from the admin terminal. It should now print the source code.

### 9. Walk through a directory without listing its names

Still in the **Alex shell**:

```bash
chmod 710 /srv/access-lab
```

In the **admin terminal**, run these separately:

```bash
sudo -u dev_bob ls /srv/access-lab
```

```bash
sudo -u dev_bob cat /srv/access-lab/hello.py
```

Listing is denied, but reading the known filename works. Directory `r` lets Bob list names. Directory `x` lets Bob look up a name he already knows, subject to the file's own permissions.

In the **Alex shell**, restore the folder:

```bash
chmod 750 /srv/access-lab
```

### 10. Editing and deleting use different permissions

Still as **Alex**, create a disposable subdirectory and file:

```bash
mkdir /srv/access-lab/delete-test
chgrp dev_team /srv/access-lab/delete-test
chmod 770 /srv/access-lab/delete-test
printf 'This copy is disposable.\n' > /srv/access-lab/delete-test/note.txt
chmod 444 /srv/access-lab/delete-test/note.txt
```

In the **admin terminal**, open a Bob shell:

```bash
sudo -iu dev_bob
```

As **Bob**, try appending to the file:

```bash
printf 'An extra line.\n' >> /srv/access-lab/delete-test/note.txt
```

**Expected:** permission denied. Now delete this disposable file:

```bash
rm -f /srv/access-lab/delete-test/note.txt
ls -l /srv/access-lab/delete-test
exit
```

Deletion succeeds because Bob has write and search permission on the containing directory. The `-f` suppresses the read-only-file confirmation; it does not override Linux permissions. This example uses an ordinary directory with no extra access rules.

In the **Alex shell**:

```bash
rmdir /srv/access-lab/delete-test
```

### 11. Change group and owner

Still as **Alex**:

```bash
printf 'An ownership practice file.\n' > /srv/access-lab/owner-demo.txt
chgrp dev_team /srv/access-lab/owner-demo.txt
chmod 640 /srv/access-lab/owner-demo.txt
```

In the **admin terminal**:

```bash
sudo chown dev_bob:dev_team /srv/access-lab/owner-demo.txt
stat -c '%A %a %U %G %n' /srv/access-lab/owner-demo.txt
sudo chown dev_alex:dev_team /srv/access-lab/owner-demo.txt
```

The first `chown` makes Bob the owner. The second restores Alex. On Linux, transferring ownership to another user normally needs administrative privilege; group write access alone does not let someone change the file's mode or ownership.

## Part 3 — Permissions at creation time

### 12. Compare four umasks

Continue in the **Alex shell**. Start with a new directory; if `umask_lab` already exists from an earlier attempt, choose a new name and use it consistently below.

```bash
mkdir /home/dev_alex/umask_lab
cd /home/dev_alex/umask_lab
lab_mask=$(umask)
umask
```

`lab_mask` saves the current value so you can restore it. Now create fresh files and directories:

```bash
umask 022
touch file_022
mkdir dir_022
stat -c '%a %A %n' file_022 dir_022
```

```bash
umask 027
touch file_027
mkdir dir_027
stat -c '%a %A %n' file_027 dir_027
```

```bash
umask 077
touch file_077
mkdir dir_077
stat -c '%a %A %n' file_077 dir_077
```

```bash
umask 002
touch file_002
mkdir dir_002
stat -c '%a %A %n' file_002 dir_002
```

**Expected ordinary permissions:**

| Mask | New file | New directory |
| --- | --- | --- |
| `022` | `644`, `rw-r--r--` | `755`, `rwxr-xr-x` |
| `027` | `640`, `rw-r-----` | `750`, `rwxr-x---` |
| `077` | `600`, `rw-------` | `700`, `rwx------` |
| `002` | `664`, `rw-rw-r--` | `775`, `rwxrwxr-x` |

Use `ls -ld dir_027` to inspect a directory itself. `ls -l dir_027` normally lists its contents.

### 13. Change the mask; check an old file

Still as **Alex** in `umask_lab`:

```bash
umask 077
touch file_002
stat -c '%a %A %n' file_002
touch made_after_077
stat -c '%a %A %n' made_after_077
```

`file_002` stays `664`; touching an existing file changes timestamps, not its permissions. The new file is `600`.

Change the existing file deliberately:

```bash
chmod 600 file_002
stat -c '%a %A %n' file_002
```

Use `umask` for the starting permissions of future creations; use `chmod` for an existing file.

### 14. See why subtraction gives the wrong answer

Still as **Alex**:

```bash
umask 033
touch file_033
mkdir dir_033
stat -c '%a %A %n' file_033 dir_033
```

**Expected:** the file is `644`, and the directory is `744`.

The group and others mask digit `3` blocks `w` and `x`. A normal newly created file starts with a request for `rw-`; removing `w` and `x` leaves `r--`. There was no execute permission to remove. Arithmetic subtraction would produce the wrong file mode.

Restore the shell's original mask:

```bash
umask "$lab_mask"
umask
```

These changes belong to this shell and the programs it launches. They do not change the umask of your already-open admin terminal.

### 15. Optional: use a temporary mask for one group of commands

Still in the **Alex shell**, run:

```bash
umask
(
    umask 077
    touch temporary_mask_file
    stat -c '%a %A %n' temporary_mask_file
)
umask
```

The file should be `600`, while the outer shell's mask before and after is the same. Parentheses run the enclosed commands in a subshell, so its mask change stays there.

Finish the Alex session:

```bash
exit
```

## Part 4 — Sudo and administration

### 16. Create a separate practice administrator

**Admin terminal:**

```bash
sudo useradd -m -U -s /bin/bash newuser
sudo passwd newuser
id newuser
getent group sudo
```

Set a password you can type again during this lab. Do not reuse an important personal password. `newuser` initially has no `sudo` group membership.

In the **second terminal**, starting as your normal account:

```bash
sudo -iu newuser
whoami
sudo -k
sudo whoami
```

**Expected on a standard Ubuntu setup:** sudo denies the request because newuser has not been granted access. If it asks for a password, enter **newuser's password**. If it already prints `root`, this machine has another matching policy; consult the instructor before using it for the grant/revoke comparison.

```bash
exit
```

### 17. Grant access, then inspect what was granted

**Admin terminal:**

```bash
sudo usermod -aG sudo newuser
id newuser
sudo -l -U newuser
```

On standard Ubuntu, the `sudo` group is authorized by a rule similar to:

```text
%sudo ALL=(ALL:ALL) ALL
```

This grants broad administrative access. The group name alone does not grant it: the policy must contain a matching rule. If `sudo -l -U newuser` still says the account is not allowed, ask the instructor to check the environment's policy. Do not paste new rules into an unfamiliar machine.

Open a **fresh Newuser shell** in the second terminal:

```bash
sudo -iu newuser
whoami
sudo -k
sudo whoami
whoami
sudo -l
```

The three identity commands should show:

```text
newuser
root
newuser
```

`sudo whoami` runs that command as root. It does not permanently turn this shell into root. Password prompts can be cached or disabled by policy; absence of a prompt is not a reliable access test.

```bash
exit
```

### 18. Inspect sudo's configuration without editing it

**Admin terminal:**

```bash
sudo visudo -c
sudo -l
```

`visudo -c` checks sudoers configuration syntax; it does not open an editor or grant permissions. Expect a “parsed OK” message for each checked file. `sudo -l` lists the permissions available to your current account.

For an authorized policy edit, administrators use `sudo visudo`, which checks syntax before accepting an edit. This lab needs no policy-file edits.

### 19. Remove the practice account's sudo membership

Make sure the Newuser shell has exited. In the **admin terminal**:

```bash
sudo gpasswd -d newuser sudo
id newuser
```

Open a **fresh Newuser shell** in the second terminal:

```bash
sudo -iu newuser
sudo -k
sudo whoami
exit
```

**Expected:** denied again, provided the sudo-group rule was newuser's only grant. Old shells can retain old groups, so removing a database membership is not a way to terminate existing privileged sessions.

## Extra practice — Choose what you want to revisit

### A. See what forgetting `-a` does

Use only Bob, the disposable practice account. Close any Bob shells first. In the **admin terminal**:

```bash
sudo groupadd dev_review
sudo usermod -aG dev_review dev_bob
id dev_bob
```

Bob should now have both `dev_team` and `dev_review` as supplementary groups. The next command deliberately leaves out `-a`:

```bash
sudo usermod -G dev_team dev_bob
id dev_bob
```

Bob loses `dev_review`: `-G` replaces the supplementary group list. His primary group remains. Repair the list:

```bash
sudo usermod -aG dev_review dev_bob
id dev_bob
```

Use `-aG` when adding a group to an existing list. Never perform this experiment on your own administrative account.

### B. Try three small repairs

For each row, run the setup in the **admin terminal**, run the failing check, apply the repair, and repeat the check. Each row restores a usable state before the next row.

| Setup | Check | Repair |
| --- | --- | --- |
| `sudo chmod 700 /srv/access-lab/hello.py` | `sudo -u dev_bob /srv/access-lab/hello.py` | `sudo chmod 750 /srv/access-lab/hello.py` |
| `sudo chmod 740 /srv/access-lab` | `sudo -u dev_bob cat /srv/access-lab/hello.py` | `sudo chmod 750 /srv/access-lab` |
| `sudo chgrp root /srv/access-lab/hello.py` | `sudo -u dev_bob /srv/access-lab/hello.py` | `sudo chgrp dev_team /srv/access-lab/hello.py` |

Useful inspection commands:

```bash
id dev_bob
ls -ld /srv /srv/access-lab
ls -l /srv/access-lab/hello.py
stat -c '%A %a %U %G %n' /srv/access-lab/hello.py
```

### C. Look at login records and your own command history

From your normal account:

```bash
last -n 5
history 10
```

If your environment has no `last` command or no login database, skip it. Containers often have little or no login history. `last` shows recorded logins; `history` shows your current Bash session's command list. The file `~/.bash_history` may not include recent commands until the shell saves them.

An administrator can often read another user's saved history, but should do so only for an authorized purpose. History is incomplete and can contain secrets; it is not a complete audit record.

## Cleanup — Only after finishing all parts

Close every Alex, Bob, and Newuser shell with `exit`. Keep your original admin terminal. The following removes the practice project, the three accounts, and their home directories; keep anything you want before running it. Remove only resources you created for this lab.

**Admin terminal:**

```bash
sudo rm -r -- /srv/access-lab
sudo userdel -r dev_alex
sudo userdel -r dev_bob
sudo userdel -r newuser
sudo groupdel dev_team
```

If you completed extra practice A, also run:

```bash
sudo groupdel dev_review
```

Ubuntu may automatically remove each user's private group. Inspect before removing any that remain:

```bash
getent group dev_alex dev_bob newuser
```

For each of those groups still present, remove it only if it is the private group created by this lab, is empty, and is not another account's primary group:

```bash
sudo groupdel dev_alex
sudo groupdel dev_bob
sudo groupdel newuser
```

Run only the applicable commands. “Group does not exist” means it was already removed. Do not remove the system's `sudo` group. A `userdel` warning about a missing mail spool can be harmless; an error about running processes means a practice session may still be open.

Verify:

```bash
getent passwd dev_alex dev_bob newuser
getent group dev_team
ls -ld /srv/access-lab /home/dev_alex /home/dev_bob /home/newuser
```

Expect no account or team-group entries, and missing-path messages.

## When a result differs

| What you see | What to check |
| --- | --- |
| Account or group already exists | You may be resuming an old lab. Do not recreate it blindly. |
| Alex is “not in the sudoers file” | Return to your original admin terminal for administrative steps. Alex does not need sudo for files Alex owns. |
| Bob's account lists `dev_team`, but an open Bob shell does not | Exit that shell and start `sudo -iu dev_bob` again. |
| A script is readable but `./hello.py` fails | Check file `x`, directory `x`, and the shebang. Also confirm Python is installed. |
| File bits look right, but access fails | Inspect every parent directory with `ls -ld`. Test as the intended user. |
| `ls -l` shows `+` after the permission bits | Extra access control lists may apply. These exercises assume ordinary permissions without additional ACLs; use a clean lab directory or ask the instructor. |
| `umask` seems to have no effect | Use a new filename, and create it in the same shell where you set the mask. |
| Root can do something a learner cannot | That is why the access checks run as Alex, Bob, or Newuser. |
| Direct execution fails despite correct bits | A `noexec` mount or another security policy can block it. Use the prepared course environment; do not change mount or security policy for this exercise. |

For local help, try `man chmod`, `man usermod`, `man sudo`, or Bash's `help umask`. Press `q` to leave a manual page. Some minimal images do not install the manual pages.

Technical references: [Linux usermod manual](https://man7.org/linux/man-pages/man8/usermod.8.html), [Linux umask manual](https://man7.org/linux/man-pages/man2/umask.2.html), [path lookup](https://man7.org/linux/man-pages/man7/path_resolution.7.html), and [sudoers manual](https://man7.org/linux/man-pages/man5/sudoers.5.html). The lab is adapted from the supplied course guides, with permission checks and account transitions made explicit.
