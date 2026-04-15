# Improved Linux Labs: VFS, Copy-on-Write, and Journaling

## Purpose

These labs are small, terminal-driven exercises meant to teach three **different** ideas that students often mix together:

1. **VFS** — one common interface over different filesystem backends
2. **Copy-on-Write (CoW)** — do **not** separate data immediately; separate it when a write forces it
3. **Journaling** — record intended changes first so recovery can restore a **consistent** state after a crash

These are **teaching labs**, not kernel internals labs.  
The goal is to make the core behavior visible with safe commands in a temporary workspace.

---

## What These Labs Try to Prevent You From Misunderstanding

By the end, you should **not** walk away thinking:

- “VFS is just another filesystem.”
- “CoW is the same as a hard link.”
- “Journaling means I automatically have a backup.”

Those are the three most common bad takeaways.

---

## Before You Start

Create a clean workspace:

```bash
mkdir -p ~/linux_fs_labs_improved
cd ~/linux_fs_labs_improved
```

Check Python:

```bash
python3 --version
```

---

# Lab 1 — VFS Lab: Same Operations, Different Backends

## Goal

See that Linux lets you use the **same style of commands** on very different kinds of filesystem objects.

This lab is trying to teach:

- VFS is **not** “one more filesystem”
- VFS is the **common interface layer**
- regular files, pseudo-files, and different mounted filesystems can still be accessed through familiar operations like `ls`, `cat`, and `stat`

## Big Picture

Think of VFS like a receptionist at a large building.

You always talk to the same front desk:

- “open this”
- “read this”
- “list this”

But behind that desk, the request may go to a different office with different internal rules.

The front side stays familiar.  
The backend can differ.

---

## Step 1: Create a regular file in your lab directory

```bash
cd ~/linux_fs_labs_improved
mkdir -p vfs_lab
cd vfs_lab

echo "Hello from a regular file." > regular.txt
```

Now inspect it:

```bash
ls -l regular.txt
cat regular.txt
stat regular.txt
```

### What to notice

This is a normal file in your working directory.

---

## Step 2: Use the **same kind of commands** on a kernel-provided pseudo-file

```bash
ls -l /proc/version
cat /proc/version
stat /proc/version
```

### What to notice

You still used:

- `ls`
- `cat`
- `stat`

But `/proc/version` is not an ordinary text file sitting on disk like `regular.txt`.

From the user side, the interaction looks familiar.  
Internally, the backend is different.

That is the point.

---

## Step 3: Compare filesystem types

Run:

```bash
stat -f -c '%n -> %T' . /proc /dev/shm
```

If `/dev/shm` exists on your system, you should see different filesystem types such as:

- your current directory’s filesystem
- `proc`
- `tmpfs`

### What to notice

You are still working through the same shell and familiar file commands, but the backing filesystem types are different.

That is closer to the real VFS idea than pretending VFS itself is a mount point.

---

## Step 4: Use the same command on two different directories

```bash
ls .
ls /proc
```

Optional:

```bash
ls /dev/shm
```

### What to notice

The same command works, even though the meaning of the content is different:

- `.` lists your lab files
- `/proc` exposes kernel/process information
- `/dev/shm` is usually a memory-backed temporary filesystem

Same style of access. Different backend.

---

## Step 5: Create one more file on a different backend if available

Try:

```bash
echo "Hello from tmpfs." > /dev/shm/vfs_demo_tmpfs.txt
cat /dev/shm/vfs_demo_tmpfs.txt
stat /dev/shm/vfs_demo_tmpfs.txt
```

If `/dev/shm` is not available, skip this step.

### What to notice

Now you created and read a file on a memory-backed filesystem using familiar commands.

Again: VFS is the common way Linux lets you *treat these backends through a uniform file-style interface*.

---

## Checkpoint

At this point, pause and say the following out loud:

- VFS is **not** the same thing as ext4 or XFS.
- VFS is the layer that helps common operations look uniform.
- The command looking the same does **not** mean the backend is the same.

If you can say that clearly, this lab worked.

---

## Mini Summary

### From the outside

You used the same kinds of operations:

- list
- read
- inspect metadata

### Underneath

Linux may have routed those requests to:

- a regular on-disk filesystem
- `proc`
- `tmpfs`

That difference underneath is exactly why VFS exists.

---

## Cleanup

```bash
rm -f /dev/shm/vfs_demo_tmpfs.txt 2>/dev/null
cd ~/linux_fs_labs_improved
rm -rf vfs_lab
```

---

# Lab 2 — Copy-on-Write Lab: Why CoW Is Not the Same as a Hard Link

## Goal

Understand three different things that students often confuse:

1. **ordinary copy**
2. **hard link**
3. **Copy-on-Write idea**

This lab is designed so that the contrast itself teaches the point.

## Big Picture

Think of three cases:

- **ordinary copy**: make another notebook immediately
- **hard link**: two labels pointing to the same notebook
- **CoW**: act shared at first, but separate only when someone writes

Hard links and CoW are **not** the same thing.

---

## Step 1: Set up the lab

```bash
cd ~/linux_fs_labs_improved
mkdir -p cow_lab
cd cow_lab

printf "alpha\nbeta\ngamma\n" > original.txt
cp original.txt plain_copy.txt
ln original.txt hard_link.txt
```

Inspect all three:

```bash
ls -li original.txt plain_copy.txt hard_link.txt
```

### What to notice

- `original.txt` and `hard_link.txt` should have the **same inode number**
- `plain_copy.txt` should have a **different inode number**

That already tells you:

- hard link = same underlying file
- ordinary copy = separate file

---

## Step 2: Modify the ordinary copy

```bash
sed -i '2s/beta/BETA/' plain_copy.txt
```

Display both:

```bash
echo "--- original.txt ---"
cat original.txt

echo "--- plain_copy.txt ---"
cat plain_copy.txt
```

### What to notice

Changing `plain_copy.txt` did **not** change `original.txt`.

That is what a normal copy does: separation happens immediately.

---

## Step 3: Modify the hard link

```bash
sed -i '3s/gamma/GAMMA/' hard_link.txt
```

Display both again:

```bash
echo "--- original.txt ---"
cat original.txt

echo "--- hard_link.txt ---"
cat hard_link.txt
```

### What to notice

Both names now show the same changed content.

Why?

Because a hard link is not “copy later.”  
It is “same file, another name.”

This is exactly where many students accidentally invent a false definition of CoW.

---

## Step 4: Build a tiny CoW teaching model

Create a script:

```bash
cat > cow_demo.py <<'PY'
class CowList:
    def __init__(self, original):
        self.original = list(original)
        self.modified = {}

    def read(self, i):
        if i in self.modified:
            return self.modified[i]
        return self.original[i]

    def write(self, i, value):
        self.modified[i] = value

    def materialize(self):
        out = []
        for i in range(len(self.original)):
            if i in self.modified:
                out.append(self.modified[i])
            else:
                out.append(self.original[i])
        return out

original = ["alpha", "beta", "gamma"]
cow_view = CowList(original)

print("Original at start: ", original)
print("CoW view at start: ", cow_view.materialize())

cow_view.write(1, "BETA")

print("CoW view after write:", cow_view.materialize())
print("Original after write:", original)
PY
```

Run it:

```bash
python3 cow_demo.py
```

### What to notice

Before the write:

- the CoW view behaves like the original

After the write:

- the CoW view changes
- the original stays unchanged

This is the teaching shape of CoW:

- start by behaving shared
- separate when a write happens

---

## Step 5: Compare the three ideas directly

### Ordinary copy

- separate file immediately

### Hard link

- same file, different name

### CoW idea

- shared view first, separation when write requires it

That middle distinction is the key.

---

## Optional Extension: Try a real reflink if your filesystem supports it

Some Linux filesystems support a real reflink-style copy:

```bash
cp --reflink=always original.txt reflink_copy.txt
```

If this fails, that is fine.  
It depends on filesystem support.

If it works, inspect:

```bash
ls -li original.txt reflink_copy.txt
```

Do **not** assume success here.  
This step is optional because real CoW file copying depends on backend support.

---

## Checkpoint

You should now be able to say:

- A hard link is **not** CoW.
- A hard link is another name for the same file.
- CoW means delayed separation on write.

If that sentence is still fuzzy, re-run Step 3 and Step 4.

---

## Cleanup

```bash
cd ~/linux_fs_labs_improved
rm -rf cow_lab
```

---

# Lab 3 — Journaling Lab: Consistency, Not Magic Backup

## Goal

Understand the journaling idea:

- record the intended change first
- then apply it
- after a crash, replay the journal to rebuild a consistent state

This lab is also trying to quietly correct a bad assumption:

- journaling is about **recoverable consistency**
- journaling is **not** the same thing as “I have a backup of everything”

## Big Picture

Think of journaling like writing instructions in a notebook before doing work:

1. write down the intended action
2. do the action
3. if the machine crashes halfway, the notebook helps recovery reconstruct what was supposed to happen

That is closer to journaling than “save copies forever.”

---

## Step 1: Set up the lab

```bash
cd ~/linux_fs_labs_improved
mkdir -p journaling_lab/fs
cd journaling_lab

: > journal.log
```

The `fs/` directory will act like our toy filesystem state.  
The `journal.log` file will act like our toy journal.

---

## Step 2: Record and apply one successful write

```bash
echo "WRITE report.txt first_version" >> journal.log
echo "first_version" > fs/report.txt
```

Inspect:

```bash
echo "--- journal.log ---"
cat journal.log

echo "--- fs/report.txt ---"
cat fs/report.txt
```

### What to notice

The intent was recorded first, then the change was applied.

---

## Step 3: Simulate a crash after journaling intent but before applying the real change

Record a second intended write:

```bash
echo "WRITE todo.txt pending_task" >> journal.log
```

Now **do not** create `fs/todo.txt`.

Instead, inspect the current state:

```bash
echo "--- journal.log ---"
cat journal.log

echo "--- current fs directory ---"
ls fs
```

### What to notice

The journal says `todo.txt` should exist, but the current toy filesystem state does not yet contain it.

That is the exact kind of mismatch journaling is meant to help repair.

---

## Step 4: Simulate crash recovery by rebuilding from the journal

First, pretend the current in-memory state is unreliable by wiping the toy filesystem state:

```bash
rm -f fs/*
```

Now create a small replay script:

```bash
cat > replay_journal.sh <<'SH'
#!/usr/bin/env bash
set -e

mkdir -p fs
while read -r action name data; do
    case "$action" in
        WRITE)
            echo "$data" > "fs/$name"
            ;;
        DELETE)
            rm -f "fs/$name"
            ;;
    esac
done < journal.log
SH
```

Make it executable and run it:

```bash
chmod +x replay_journal.sh
./replay_journal.sh
```

Inspect the recovered state:

```bash
echo "--- recovered fs directory ---"
ls fs

echo "--- recovered report.txt ---"
cat fs/report.txt

echo "--- recovered todo.txt ---"
cat fs/todo.txt
```

### What to notice

Even though the second write had not yet been applied before the simulated crash, replaying the recorded intent restored a consistent result.

That is the journaling idea in miniature.

---

## Step 5: Add a delete and replay again

Record and apply a delete:

```bash
echo "DELETE report.txt" >> journal.log
rm -f fs/report.txt
```

Inspect current state:

```bash
echo "--- journal.log ---"
cat journal.log

echo "--- current fs directory ---"
ls fs
```

Now simulate another crash and recover again:

```bash
rm -f fs/*
./replay_journal.sh
```

Inspect:

```bash
echo "--- recovered fs directory after delete replay ---"
ls fs
```

Optional direct checks:

```bash
test -f fs/report.txt && echo "report exists" || echo "report missing"
test -f fs/todo.txt && echo "todo exists" || echo "todo missing"
```

### What to notice

After replay:

- `todo.txt` should exist
- `report.txt` should be missing

This does **not** mean the old contents of `report.txt` were backed up forever.  
It means recovery can reconstruct a consistent final state from the journaled operations.

That distinction matters.

---

## Step 6: Say clearly what this toy model is and is not

This toy model logs full high-level actions like:

- `WRITE report.txt first_version`
- `DELETE report.txt`

Real journaling filesystems are more complicated and often focus heavily on filesystem bookkeeping and metadata.

But the teaching shape is the same:

- record intended change
- recover by replay

---

## Checkpoint

You should now be able to say:

- Journaling helps restore a **consistent** state after a crash.
- Journaling does **not** automatically mean “every old version is saved like a backup.”
- Our toy model logs whole actions to make the idea visible.

If you can say that cleanly, this lab worked.

---

## Cleanup

```bash
cd ~/linux_fs_labs_improved
rm -rf journaling_lab
```

---

# Final Wrap-Up

## Core Contrast Table

| Topic | Main Idea | What It Is Not |
|---|---|---|
| VFS | one common interface over different filesystem backends | not “just another filesystem” |
| CoW | delay separation until a write forces it | not the same as a hard link |
| Journaling | record intended changes so crash recovery can restore consistency | not the same as automatic backup |

---

## Suggested Teaching Order

Teach them in this order:

1. **VFS** — same outside interface, different backend
2. **CoW** — different strategies for sharing and separating data
3. **Journaling** — different strategy for surviving interrupted updates

That order tends to reduce concept mixing.

---

## Remove Everything

If you want to remove the whole workspace:

```bash
rm -rf ~/linux_fs_labs_improved
```
