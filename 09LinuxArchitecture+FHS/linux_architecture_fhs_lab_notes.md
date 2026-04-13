# Linux Architecture, Filesystem Hierarchy, and `/proc` Observation Labs

## Overview

This document organizes the uploaded notes into one coherent handout. It moves from the big picture of Linux, to the filesystem hierarchy, and then to hands-on labs that show how Linux exposes system state through files.

The central idea tying these materials together is simple:

> Linux is organized in layers, and many parts of the system expose information through the filesystem.

That is why directories like `/proc`, `/sys`, `/dev`, `/home`, and `/var` matter so much. They are not random folders. They reflect how the system is structured and how it is used.

---

## 1. The Big Picture: Linux Architecture

Linux can be understood as a stack of layers.

### 1.1 Hardware

This is the physical machine:
- CPU
- RAM
- storage devices
- network hardware
- input/output devices

This is the bottom layer. Everything else ultimately depends on it.

### 1.2 Kernel

The kernel is the core of Linux.

Its job is to:
- manage hardware access
- schedule processes
- manage memory
- manage filesystems
- manage devices
- manage networking

A useful mental model is this: the kernel is the system manager sitting between programs and the actual machine.

### 1.3 System Libraries

System libraries provide common functionality that applications use to request system-level services.

Instead of every program talking to the kernel in a raw way, many programs rely on libraries that offer standard functions.

### 1.4 Shell

The shell is the command interpreter.

It:
- accepts commands from the user
- launches programs
- connects commands together
- handles redirection, pipes, and scripting

The shell is not the kernel. It is the interface a user commonly uses to ask the system to do work.

### 1.5 System Utilities

These are the small tools that perform specific jobs.

Examples include commands for:
- listing files
- checking memory
- viewing processes
- managing networking
- controlling users and permissions

These utilities are a big part of Linux culture: many small tools, each doing one job well.

### 1.6 Users

Users are the actors of the system.

They:
- log in
- run commands
- launch programs
- create and modify files
- operate within permission boundaries

### 1.7 User Applications

These are higher-level programs such as:
- browsers
- editors
- office software
- games
- IDEs

These applications usually rely on system libraries, utilities, and kernel services underneath.

---

## 2. Linux Filesystem Hierarchy: Why the Directory Layout Matters

The filesystem hierarchy gives Linux a predictable organization. Instead of scattering things randomly, Linux uses directories with specific purposes.

### 2.1 `/` — Root

This is the top of the filesystem.

Everything in the Linux system lives under `/`.

### 2.2 `/bin` and `/usr/bin` — User Binaries

These hold user-facing command binaries.

Examples include many commands people run directly from the shell.

Why they matter:
- they support user interaction
- they connect the shell to executable tools

### 2.3 `/sbin` and `/usr/sbin` — System Binaries

These contain administrative or system-oriented binaries.

They are more closely associated with system management tasks and are often used by the root user.

### 2.4 `/etc` — Configuration Files

This directory stores system-wide configuration.

Programs and services read files here to decide how to behave.

Think of `/etc` as “system setup instructions.”

### 2.5 `/dev` — Device Files

Linux represents devices as files.

This means hardware interfaces can appear under `/dev`, which is one of the clearest examples of the Unix idea that many system resources can be interacted with through file-like interfaces.

### 2.6 `/proc` and `/sys` — Virtual System Information

These are special virtual filesystems.

They do not behave like ordinary stored files. Instead, they expose live kernel and system information.

Examples:
- CPU information
- memory information
- process information
- device and kernel state

These directories are central to the labs later in this document.

### 2.7 `/var` — Variable Data

This stores data that changes over time, such as:
- logs
- caches
- spool files
- service-generated state

This connects to the system’s ongoing operation.

### 2.8 `/home` — User Home Directories

Each user typically has a personal space under `/home`.

This is where user files, shell configuration, and personal data are commonly stored.

### 2.9 `/lib` and `/usr/lib` — Libraries

These contain libraries used by programs in directories such as `/bin` and `/sbin`.

They support the execution of applications and system tools.

### 2.10 `/boot` — Boot Files

This contains files required for booting the system, including kernel-related boot artifacts.

### 2.11 `/tmp` — Temporary Files

Programs use `/tmp` for temporary working files.

This is important in the labs because temporary files often help demonstrate how processes interact with the filesystem while they run.

### 2.12 `/run` — Runtime State

`/run` holds runtime data since the last boot.

It reflects live system state and is closely tied to currently running services and processes.

### 2.13 `/usr/local` — Local User-Installed Software

This area is commonly used for software installed locally rather than by the system package manager.

It reflects modularity: not everything must be part of the base operating system.

---

## 3. Connecting Linux Architecture to the Filesystem Hierarchy

This is the main bridge between the first two topics.

The architecture tells us **what layers exist**.
The filesystem hierarchy shows **where those layers appear in practice**.

### 3.1 Kernel and System Files

These directories relate strongly to the kernel and core system operation:
- `/boot`
- `/lib`, `/lib64`
- `/etc`
- `/proc`
- `/sys`
- `/run`

Why:
- `/boot` supports system startup
- libraries support essential binaries
- `/etc` configures system behavior
- `/proc` and `/sys` expose the kernel’s live view of the system
- `/run` stores runtime state

### 3.2 User and Shell Interface

These directories support command execution and user interaction:
- `/bin`
- `/usr/bin`
- `/sbin`
- `/usr/sbin`

Why:
- they contain commands and utilities
- they are what the shell launches when users type commands

### 3.3 User Data and Applications

These directories reflect user space and user-installed software:
- `/home`
- `/usr/local`

Why:
- they store personal files and user-specific configuration
- they separate local user software from core system software

### 3.4 System Operation and Process Management

These directories reflect activity, state, and hardware-process interfaces:
- `/var`
- `/proc`
- `/dev`
- `/tmp`

Why:
- `/var` changes during normal operation
- `/proc` reflects process and kernel state
- `/dev` gives access to devices through files
- `/tmp` supports temporary process work

### 3.5 A Useful Summary

A good way to think about it is this:

- **Architecture** explains the roles.
- **Filesystem hierarchy** gives those roles locations.
- **Labs** let you observe those roles in action.

---

## 4. Why `/proc` Matters So Much

The labs repeatedly use `/proc` because it gives a live, file-based view into system behavior.

This is one of the strongest examples of the Unix/Linux design style:

- system information is exposed in a regular, inspectable form
- commands can read that information
- users can often inspect the same state either through a command or directly through a file

That means many commands are, in spirit, just cleaner windows into the same underlying system state.

Examples:
- `lscpu` is a cleaner view of CPU information also visible in `/proc/cpuinfo`
- `free` is a cleaner view of memory information also visible in `/proc/meminfo`

---

## 5. Lab: Observing CPU and Memory Information

This lab shows that Linux system information can often be viewed in two ways:

1. through a command designed for humans
2. through files exposed by the system

### 5.1 CPU Information

#### Human-friendly command

```bash
lscpu
```

#### Direct file-based view

```bash
cat /proc/cpuinfo
```

### 5.2 Memory Information

#### Human-friendly command

```bash
free -h
```

#### Direct file-based view

```bash
cat /proc/meminfo
```

### 5.3 Main Lesson

The main lesson is not just “how to check CPU and memory.”

The deeper lesson is this:

- Linux exposes internal system state through files
- commands are often formatted views over the same state

---

## 6. Lab: Observing Command History

This lab shifts from live system state to user-level persistent data.

### 6.1 Check Current History Size

```bash
history | wc -l
```

### 6.2 Run a Command

```bash
echo "Hello, World!"
```

### 6.3 Check History Again

```bash
history | wc -l
```

### 6.4 Inspect the History File

```bash
tail ~/.bash_history
```

### 6.5 Force Current Session History to Be Written

```bash
history -a
```

Then inspect again:

```bash
tail ~/.bash_history
```

### 6.6 Main Lesson

This lab highlights an important distinction:

- `history` shows the current shell’s in-memory/session history
- `~/.bash_history` is persistent storage written to disk

So not everything interesting in Linux is in `/proc`.

Some information is live kernel state.
Some is user data stored in normal files.

That contrast matters.

---

## 7. Lab: Observing a TCP Connection Through `/proc/net/tcp`

This lab shows that network state is also reflected through the filesystem.

### 7.1 Before the Connection

Check active connections:

```bash
netstat -tnp
# or
ss -tnp
```

Save a snapshot:

```bash
cat /proc/net/tcp > /tmp/before-connection.txt
```

### 7.2 Establish a Connection

```bash
nc example.com 80
# or
telnet example.com 80
```

### 7.3 After the Connection

Check active connections again:

```bash
netstat -tnp
# or
ss -tnp
```

Save another snapshot:

```bash
cat /proc/net/tcp > /tmp/after-connection.txt
```

Compare them:

```bash
diff /tmp/before-connection.txt /tmp/after-connection.txt
```

### 7.4 Main Lesson

Network activity is not invisible magic.

The kernel tracks it, and Linux exposes that state in a file-oriented way.

That means you can:
- observe a connection before and after it happens
- compare snapshots
- reason about networking through files

---

## 8. Lab: Observing Open File Descriptors with `file_wait.py`

This lab demonstrates a process opening a file and how that appears in `/proc/[PID]/fd`.

### 8.1 Script

```python
with open('/tmp/testfile.txt', 'w') as f:
    print("File is open. Please enter any text and press enter:")
    user_input = input()
    f.write(user_input)
    print("You've written to the file!")
```

### 8.2 Run the Script

```bash
python3 file_wait.py
```

The script opens `/tmp/testfile.txt` and waits for input. While it waits, the file remains open.

### 8.3 Find the PID

In another terminal:

```bash
ps aux | grep file_wait.py
```

### 8.4 Inspect Open File Descriptors

```bash
ls -l /proc/[PID]/fd
```

Replace `[PID]` with the real process ID.

You should see a file descriptor pointing to `/tmp/testfile.txt`.

### 8.5 Finish the Script

Go back to the original terminal, type text, and press Enter.

### 8.6 Inspect Again

```bash
ls -l /proc/[PID]/fd
```

If the process has exited, the PID directory may no longer exist. If it is still alive for some reason, the file descriptor for `/tmp/testfile.txt` should no longer be open.

### 8.7 Main Lesson

This lab shows that:
- processes have file descriptors
- open files appear in `/proc/[PID]/fd`
- process state changes are reflected live through the filesystem

This is a very concrete example of “everything is a file” in practice.

---

## 9. Lab: CPU Load Simulator and Temporary File Observation

This lab extends the previous ideas by combining:
- process execution
- CPU activity
- temporary files
- file descriptors
- logging

### 9.1 Script Purpose

The script does two things at the same time:

1. creates CPU load using worker threads
2. creates and keeps open a temporary file while the process runs

That makes it useful for observing both resource usage and open-file behavior.

### 9.2 Run the Script

```bash
python3 cpu_load_simulator.py
```

Use two terminals.

### 9.3 Find the PID

```bash
ps aux | grep cpu_load_simulator.py
```

### 9.4 Inspect Open File Descriptors

```bash
ls -l /proc/[PID]/fd
```

Look for a symlink pointing to a temporary file under `/tmp/`.

### 9.5 Read the Temporary File via the Descriptor

```bash
cat /proc/[PID]/fd/[FD_NUMBER]
```

Replace `[FD_NUMBER]` with the descriptor number corresponding to the temp file.

### 9.6 Watch Logs

Depending on the system:

```bash
tail -f /var/log/syslog
```

or

```bash
tail -f /var/log/messages
```

### 9.7 Stop the Script

Try Ctrl+C in the terminal where it is running.

If needed:

```bash
kill [PID]
```

### 9.8 Check Cleanup

```bash
ls -l /proc/[PID]/fd
```

If the process has terminated, the directory should disappear or the temporary file descriptor should no longer be present.

### 9.9 Main Lesson

This lab brings several ideas together:

- processes consume CPU
- processes can keep files open
- open files appear in `/proc/[PID]/fd`
- temporary files can exist only while a process is alive
- logs provide another lens into program behavior

---

## 10. What These Labs Are Really Trying to Teach

It is easy to get lost in commands and miss the point.

The deeper lessons across all labs are these:

### 10.1 Commands Are Often Views Into State

Commands like `lscpu`, `free`, `ss`, and `history` are not isolated magic tricks.

They are often formatted views over underlying system or user data.

### 10.2 The Filesystem Is More Than Stored Documents

In Linux, the filesystem is also a way of exposing:
- device interfaces
- process state
- kernel state
- network state
- temporary runtime state

### 10.3 `/proc` Is a Live Window

`/proc` is not just a folder of saved text files.

It is a live interface into the running system.

### 10.4 Process Behavior Leaves Traces

When a program runs, you can often observe its effects through:
- PIDs
- file descriptors
- network entries
- logs
- temporary files

That gives you a way to reason about the system from the outside.

---

## 11. Quick Concept Map

A compact way to connect everything:

- **Hardware** is the real machine.
- **Kernel** manages hardware and system resources.
- **Shell** lets the user ask the system to do work.
- **Utilities** perform focused tasks.
- **Filesystem hierarchy** gives predictable locations for system pieces.
- **`/proc` and related directories** expose live system state.
- **Labs** show that system activity becomes visible through files.

---

## 12. Suggested Lab Flow for Teaching or Review

If you want to present this material in a logical order, this sequence works well:

1. Linux architecture overview
2. Filesystem hierarchy overview
3. Connect architecture to directories
4. Show `/proc` as a live interface
5. CPU and memory observation lab
6. command history lab
7. TCP connection lab
8. file descriptor lab with `file_wait.py`
9. CPU load and temp-file lab with `cpu_load_simulator.py`

That order moves from idea → structure → observation.

---

## Appendix A: `file_wait.py`

```python
# file_wait.py
with open('/tmp/testfile.txt', 'w') as f:
    print("File is open. Please enter any text and press enter:")
    user_input = input()
    f.write(user_input)
    print("You've written to the file!")
```

---

## Appendix B: `cpu_load_simulator.py`

```python
# cpu_load_simulator.py
import threading
import time
import tempfile
import syslog

# Function to simulate CPU intensive task
def cpu_intensive_task():
    while True:
        # Perform a calculation that uses CPU resources
        [x**2 for x in range(10000)]

# Create and start multiple threads to increase CPU load
def create_load(threads=4):
    syslog.syslog(syslog.LOG_INFO, f"Simulating high CPU load with {threads} threads.")
    for _ in range(threads):
        thread = threading.Thread(target=cpu_intensive_task)
        thread.daemon = True  # allows thread to exit when main thread exits
        thread.start()

# Run the function to create CPU load
if __name__ == "__main__":
    try:
        # You can change the number of threads to increase or decrease the load
        create_load(threads=8)

        # Demonstrate creating a temporary file
        with tempfile.NamedTemporaryFile() as temp_file:
            syslog.syslog(syslog.LOG_INFO, f"Created temporary file at {temp_file.name}")
            # Keep the program running
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        syslog.syslog(syslog.LOG_INFO, "Load simulation stopped by user.")
```

---

## Closing Summary

These materials are all pointing at one unifying insight:

Linux is not just a collection of commands. It is a structured system where architecture, directories, processes, and files all connect.

Once you start seeing:
- `/proc` as a live window,
- directories as roles,
- commands as views,
- and processes as things you can observe from the outside,

Linux becomes much less mysterious and much more logical.
