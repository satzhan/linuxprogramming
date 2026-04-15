# Simple Linux Labs: VFS, Copy-on-Write, and Journaling

## Purpose

These three labs are small, terminal-driven exercises meant to **teach the core idea** behind:

1. **VFS** — one common interface, many possible file-system backends
2. **Copy-on-Write (CoW)** — delay the real copy until a write happens
3. **Journaling** — record intended changes first so recovery is possible after a crash

These are **teaching labs**, not real kernel or production file-system implementations. The point is to make the idea visible with commands you can run safely in a temporary directory.

---

## Before You Start

Use a temporary workspace in your home directory:

```bash
mkdir -p ~/linux_fs_labs
cd ~/linux_fs_labs
```

Check that Python is available:

```bash
python3 --version
```

---

# Lab 1 — VFS Idea Lab

## Goal

Understand the basic VFS idea:

- user programs use the **same kinds of operations** (`open`, `read`, `write`, `close`)
- the **backend implementation** may differ
- the interface looks uniform from the outside

In real Linux, the kernel's VFS layer gives a common interface to different file systems. In this toy lab, we simulate that idea by switching one active path between two different backends.

## Big Picture

Think of VFS like a **universal electrical outlet adapter**:

- you plug into the same front side
- behind the wall, the actual wiring may differ

Here, the **same path** will point to different backends.

## Commands

### Step 1: Create the lab area

```bash
cd ~/linux_fs_labs
mkdir -p vfs_lab/{ext4_fs,xfs_fs}
cd vfs_lab
```

### Step 2: Create similar files in both backends

```bash
echo "This file lives in the ext4-like backend." > ext4_fs/notes.txt
echo "This file lives in the xfs-like backend." > xfs_fs/notes.txt
```

### Step 3: Point a common path to one backend

```bash
ln -sfn ext4_fs active_fs
```

### Step 4: Use the same commands through the common path

```bash
ls active_fs
cat active_fs/notes.txt
echo "Appended through the common interface." >> active_fs/notes.txt
cat active_fs/notes.txt
```

### Step 5: Switch the common path to the other backend

```bash
ln -sfn xfs_fs active_fs
```

### Step 6: Run the same commands again

```bash
ls active_fs
cat active_fs/notes.txt
echo "A different backend, same interface idea." >> active_fs/notes.txt
cat active_fs/notes.txt
```

### Step 7: Compare the two backend files directly

```bash
echo "--- ext4-like backend ---"
cat ext4_fs/notes.txt

echo "--- xfs-like backend ---"
cat xfs_fs/notes.txt
```

## What You Should Notice

- You kept using the **same path**: `active_fs/notes.txt`
- But the actual file changed depending on which backend `active_fs` pointed to
- That mirrors the core idea of VFS: **same style of operations, different underlying implementation**

## Optional Extra Check

Look at the symlink itself:

```bash
ls -l active_fs
```

## Reflection Questions

1. What stayed the same when you switched backends?
2. What changed?
3. In real Linux, what would be handled by the VFS layer, and what would be handled by the specific file system?

## Cleanup

```bash
cd ~/linux_fs_labs
rm -rf vfs_lab
```

---

# Lab 2 — Copy-on-Write Idea Lab

## Goal

Understand the CoW idea:

- at first, the new object can share the original data logically
- when the first write happens, that is when the copy becomes necessary
- the original stays unchanged

In real systems, CoW is used in places like snapshots and memory management. In this lab, we use a tiny Python model that behaves like a lazy overlay: reads come from the original until a write happens.

## Big Picture

Think of CoW like a **transparent sheet on top of a book page**:

- at first, both readers see the same page
- once you mark something on the sheet, only your view changes
- the original page remains untouched

## Commands

### Step 1: Create the lab area

```bash
cd ~/linux_fs_labs
mkdir -p cow_lab
cd cow_lab
```

### Step 2: Create the demo script

```bash
cat > cow_demo.py <<'PY'
class CowList:
    def __init__(self, original_list):
        self.original_list = original_list
        self.modified_indices = {}

    def __getitem__(self, index):
        if index in self.modified_indices:
            return self.modified_indices[index]
        return self.original_list[index]

    def __setitem__(self, index, value):
        self.modified_indices[index] = value

    def __str__(self):
        final_list = []
        for i in range(len(self.original_list)):
            if i in self.modified_indices:
                final_list.append(self.modified_indices[i])
            else:
                final_list.append(self.original_list[i])
        return str(final_list)

original_list = [1, 2, 3, 4, 5]
cow_list = CowList(original_list)

print("Original list at start:      ", original_list)
print("CoW list before modification:", cow_list)

cow_list[2] = 99

print("CoW list after write:        ", cow_list)
print("Original list after write:   ", original_list)
PY
```

### Step 3: Run the script

```bash
python3 cow_demo.py
```

## Expected Output Pattern

You should see something like:

```text
Original list at start:       [1, 2, 3, 4, 5]
CoW list before modification: [1, 2, 3, 4, 5]
CoW list after write:         [1, 2, 99, 4, 5]
Original list after write:    [1, 2, 3, 4, 5]
```

## What You Should Notice

- Before writing, the CoW object behaves like the original
- The first write creates a separate modified view
- The original data remains unchanged

That is the teaching core of CoW: **do not copy immediately; copy when modification actually requires separation**.

## Optional Contrast: Ordinary Copy

Now compare it with a normal file copy:

```bash
echo -e "1\n2\n3\n4\n5" > original.txt
cp original.txt plain_copy.txt
sed -i '3s/.*/99/' plain_copy.txt

echo "--- original.txt ---"
cat original.txt

echo "--- plain_copy.txt ---"
cat plain_copy.txt
```

### Why This Contrast Matters

A regular `cp` makes a full copy right away. The CoW idea tries to avoid that immediate cost unless a write forces the separation.

## Reflection Questions

1. What part of the data stayed shared conceptually before the write?
2. Why can CoW save memory or work?
3. Why can CoW become more expensive once many writes happen?

## Cleanup

```bash
cd ~/linux_fs_labs
rm -rf cow_lab
```

---

# Lab 3 — Journaling Idea Lab

## Goal

Understand the journaling idea:

- before applying a change, record the intended change in a journal
- if a crash happens, replay or recover from that journal
- the file system can return to a consistent state

In real journaling file systems, this is much more complex and often focuses on metadata. Here we use a tiny teaching model.

## Big Picture

Think of journaling like a **pilot checklist or a transaction notebook**:

- write down what you are about to do
- perform it
- if something goes wrong, the notebook helps you recover

## Commands

### Step 1: Create the lab area

```bash
cd ~/linux_fs_labs
mkdir -p journaling_lab
cd journaling_lab
```

### Step 2: Create the demo script

```bash
cat > journaling_demo.py <<'PY'
class JournalingFileSystem:
    def __init__(self):
        self.file_system = {}
        self.journal = []

    def write(self, filename, data):
        self.journal.append(("write", filename, data))
        self.file_system[filename] = data

    def delete(self, filename):
        self.journal.append(("delete", filename))

    def crash_recovery(self):
        self.file_system = {}
        for operation, filename, *args in self.journal:
            if operation == "write":
                self.file_system[filename] = args[0]
            elif operation == "delete":
                self.file_system.pop(filename, None)

    def display(self, label):
        print(f"\n--- {label} ---")
        print(f"File system: {self.file_system}")
        print(f"Journal:     {self.journal}")

fs = JournalingFileSystem()
fs.write("file1.txt", "Hello, World!")
fs.write("file2.txt", "Hello, Journaling!")
fs.delete("file1.txt")
fs.display("State before crash")

print("\nSimulating crash...\n")
fs.crash_recovery()
fs.display("State after recovery")
PY
```

### Step 3: Run the script

```bash
python3 journaling_demo.py
```

## What You Should Notice

- The journal records operations first
- After the simulated crash, recovery rebuilds the file-system state from the journal
- The delete operation is preserved because it was written into the journal

## Expected Final State Idea

After recovery, `file2.txt` should still exist, while `file1.txt` should be gone.

## Optional Extension

Open the script and comment out the line below:

```python
self.journal.append(("delete", filename))
```

Then run it again:

```bash
python3 journaling_demo.py
```

### What This Teaches

If you fail to record an intended operation in the journal, recovery cannot reliably reconstruct the correct state.

## Reflection Questions

1. Why log the operation before recovery matters?
2. What could go wrong if the system crashes in the middle of changes?
3. Why do real file systems usually journal metadata more carefully than this toy model shows?

## Cleanup

```bash
cd ~/linux_fs_labs
rm -rf journaling_lab
```

---

# Wrap-Up

## Core Contrast

### VFS

The main idea is **uniform access**.

- same style of operations
- different backend implementations

### Copy-on-Write

The main idea is **delay the copy until the first write**.

- efficient when copies are frequent but modifications are rare
- can become more expensive with many writes

### Journaling

The main idea is **record intended changes so recovery is possible**.

- helps preserve consistency after crashes
- does not mean the file system never fails; it means recovery is more controlled

## Suggested Teaching Sequence

If you teach these in order, the progression is natural:

1. **VFS** — how Linux presents one interface over many file systems
2. **CoW** — one strategy for managing updates safely and efficiently
3. **Journaling** — another strategy for preserving consistency during updates

## Final Cleanup

If you want to remove everything from these labs:

```bash
rm -rf ~/linux_fs_labs
```
