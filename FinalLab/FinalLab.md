# Final Project: Build Your Own Mini-`systemd` in Userspace

## Welcome, and what you'll build

In this project, you'll build your very own **daemon** — a program that runs quietly in the background and does a job — together with a **control script** that starts, stops, and checks on it, just like the real `systemctl` command on Linux.

Think of it like this:

> A real Linux daemon is a chef running a restaurant kitchen 24/7 — taking orders, handling interruptions politely, keeping a logbook, and closing up cleanly at the end of the day. You can't become head chef at a famous restaurant today, but you can absolutely open a **lemonade stand** that uses the same playbook. That's what we're doing here.

By the end of this project, you'll have:

- A **Python daemon** (`mydaemon.py`) that runs in the background, watches a folder, writes a log, and listens for signals.
- A **control script** (`mydaemonctl.py`) with commands like `start`, `stop`, `status`, `restart`, and `dump`.
- A **written reflection** explaining what you built and how it compares to the real thing.

**Total time:** about 8–12 hours, spread over the parts.
**How to work:** solo. You may use friends or AI tools for help — but you must be able to explain every line of your own code. The reflection at the end will check this.

---

## Before you start: three ground rules

1. **Follow the handout in order.** Each part builds on the previous one. Don't skip ahead.
2. **Type the code yourself.** Don't copy-paste giant blocks. Typing it out is part of how your brain learns.
3. **Run every command as you go.** If the handout says "run this," run it. Watching the output is the lesson.

---

## Setup (do this once)

Before anything else, run the setup script your instructor gave you:

```bash
bash setup.sh
```

You should see a message ending with `Next step: open the handout and begin Part 1.` and a new folder called `mydaemon/` in your current directory.

Navigate into it:

```bash
cd mydaemon
```

Check that everything is there:

```bash
ls -la
```

You should see folders named `bin`, `etc`, `var`, and `watched`, plus a `REPORT.md` file.

### Why this folder layout?

Real Linux systems organize daemon-related files in a specific way:

| Real Linux location | What it holds | Our mini-version |
|---|---|---|
| `/usr/bin/` or `/usr/local/bin/` | The program itself | `mydaemon/bin/` |
| `/etc/` | Configuration files | `mydaemon/etc/` |
| `/var/run/` | PID files (IDs of running daemons) | `mydaemon/var/run/` |
| `/var/log/` | Log files | `mydaemon/var/log/` |

Because you don't have root access in Codespaces, we've built a **miniature copy** of this structure inside your project folder. Same idea, no permissions problems.

---

## Part 1 — Your first background process

**Goal:** See the difference between a program running in the foreground, in the background, and "detached" (independent of your terminal).

**Time estimate:** 45 minutes.

### Step 1.1 — Write a very simple daemon

Open the file `bin/mydaemon.py` in your editor and type in the following code exactly:

```python
#!/usr/bin/env python3
"""
mydaemon.py - version 0.1 (Part 1)
A very simple background program that writes the time to a log file.
"""

import time
from datetime import datetime

LOG_FILE = "var/log/mydaemon.log"

def main():
    while True:
        # Open the log file in "append" mode and write one line.
        with open(LOG_FILE, "a") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] mydaemon is alive\n")
            f.flush()  # force the line to disk immediately
        time.sleep(5)

if __name__ == "__main__":
    main()
```

**What does this code do?**
It runs forever in a loop. Every 5 seconds, it opens the log file, writes the current time, and goes back to sleep. The `f.flush()` line tells Python "don't wait — write it to disk right now," so we can see log lines appear immediately.

### Step 1.2 — Run it in the foreground

From inside your `mydaemon/` folder, run:

```bash
python3 bin/mydaemon.py
```

**What you'll see:** nothing. Your terminal will just sit there, frozen.

Open a **second terminal**, go into the same `mydaemon/` folder, and watch the log file grow:

```bash
tail -f var/log/mydaemon.log
```

You should see a new line appear every 5 seconds, like this:

```
[2026-04-21 14:03:12] mydaemon is alive
[2026-04-21 14:03:17] mydaemon is alive
[2026-04-21 14:03:22] mydaemon is alive
```

**To stop watching the log**, press `Ctrl+C` in the second terminal.
**To stop the daemon**, press `Ctrl+C` in the first terminal.

> **Why did the first terminal freeze?**
> Because the program is running in the **foreground** — it owns the terminal until it finishes. Since our program never finishes (it's an infinite loop), the terminal stays frozen.

### Step 1.3 — Run it in the background

Now try adding `&` at the end of the command:

```bash
python3 bin/mydaemon.py &
```

**What you'll see:**

```
[1] 12345
```

The `[1]` is a **job number** (this is your first background job) and `12345` is the **PID** — the Process ID. Your PID will be different. Write yours down.

Your terminal is free again! You can type `ls` or `pwd` and it works normally.

Check that the daemon is still writing:

```bash
tail -f var/log/mydaemon.log
```

Press `Ctrl+C` to stop watching (but the daemon keeps running).

To stop the daemon now, use the `kill` command with your PID:

```bash
kill 12345
```

(Replace `12345` with *your* PID.)

> **Why was `&` different?**
> The `&` told the shell "run this, but don't wait for it to finish — give me my prompt back right away." The program runs in the **background** while you do other things.

### Step 1.4 — What about closing the terminal?

Here's a subtle thing: if you start a background process with `&` and then close the terminal, the process usually **dies** with the terminal. To make it truly independent, you'd use `nohup` or `setsid`.

Try this experiment (you don't have to submit anything, just observe):

1. Run: `nohup python3 bin/mydaemon.py &`
2. Note the PID.
3. Close the terminal completely.
4. Open a new terminal, go to the `mydaemon/` folder, and run: `ps -p <PID>`
5. The process is still alive! Kill it with `kill <PID>`.

> **The big idea:** A **daemon** is a program that is intentionally detached from any terminal so it can run forever in the background. In Part 2, we'll make our program properly daemon-like.

### Checkpoint 1 ✅

Before moving on, make sure you can answer these questions in your own words. You'll use these answers later in REPORT.md.

1. What is the difference between foreground and background execution?
2. What does the `&` symbol do at the end of a command?
3. What is a PID?

**Deliverable for Part 1:** the working `mydaemon.py` above, plus a screenshot (or copy-paste) of your log file showing at least 3 lines of output.

---

## Part 2 — The PID file (so the daemon knows who it is)

**Goal:** Learn how a daemon keeps track of itself using a **PID file**, and how to prevent it from being started twice.

**Time estimate:** 1 hour.

### The problem

Right now, your daemon has a PID while it's running — but how would anyone *else* (like your control script) know what that PID is? They'd have to hunt through `ps` output. That's messy.

The solution is a convention: when a daemon starts, it writes its own PID to a known file, called a **PID file**. When it shuts down, it deletes that file. Anyone who wants to talk to the daemon can just read the file to find its PID.

Real daemons put their PID files in `/var/run/`. Ours will go in `var/run/mydaemon.pid`.

### Step 2.1 — Update `mydaemon.py`

Replace the contents of `bin/mydaemon.py` with this expanded version:

```python
#!/usr/bin/env python3
"""
mydaemon.py - version 0.2 (Part 2)
Now with a PID file so other programs can find us.
"""

import os
import sys
import time
from datetime import datetime

LOG_FILE = "var/log/mydaemon.log"
PID_FILE = "var/run/mydaemon.pid"


def log(message):
    """Write one line to the log file."""
    with open(LOG_FILE, "a") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {message}\n")
        f.flush()


def is_pid_running(pid):
    """Check if a process with the given PID is currently running."""
    try:
        # Signal 0 doesn't actually send a signal -- it just checks
        # whether we could send one. A clever trick!
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # Process exists but belongs to someone else -- still "running"
        return True


def check_already_running():
    """If a PID file exists AND that process is alive, refuse to start."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            old_pid = int(f.read().strip())
        if is_pid_running(old_pid):
            print(f"Error: mydaemon is already running (PID {old_pid}).")
            print("Use 'python3 bin/mydaemonctl.py stop' first.")
            sys.exit(1)
        else:
            # Stale PID file -- the old daemon crashed without cleaning up.
            print(f"Removing stale PID file (old PID {old_pid} is dead).")
            os.remove(PID_FILE)


def write_pid_file():
    """Write our own PID to the PID file."""
    my_pid = os.getpid()
    with open(PID_FILE, "w") as f:
        f.write(str(my_pid))
    log(f"mydaemon started with PID {my_pid}")


def remove_pid_file():
    """Clean up the PID file on exit."""
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    log("mydaemon stopped cleanly")


def main():
    check_already_running()
    write_pid_file()
    try:
        while True:
            log("mydaemon is alive")
            time.sleep(5)
    finally:
        # This runs even if the program is interrupted.
        remove_pid_file()


if __name__ == "__main__":
    main()
```

### Step 2.2 — Try it out

Start the daemon:

```bash
python3 bin/mydaemon.py &
```

Check that the PID file was created:

```bash
cat var/run/mydaemon.pid
```

You should see a number. That's the same PID the shell printed when you started it.

Now try to start it **again**:

```bash
python3 bin/mydaemon.py
```

You should see:

```
Error: mydaemon is already running (PID 12345).
Use 'python3 bin/mydaemonctl.py stop' first.
```

Perfect — that's the PID file doing its job.

Stop the daemon:

```bash
kill $(cat var/run/mydaemon.pid)
```

This is a neat little trick: `$(cat var/run/mydaemon.pid)` reads the PID from the file and plugs it right into the `kill` command. Very elegant.

Check that the PID file was removed:

```bash
ls var/run/
```

It should be empty.

### Step 2.3 — The `kill -0` trick explained

The most clever line in Part 2 is inside `is_pid_running()`:

```python
os.kill(pid, 0)
```

It looks like we're killing the process with signal 0 — but **signal 0 isn't actually a signal**. It's a special case: the operating system checks whether it *could* send a signal to that PID, but doesn't send anything. If the process exists, the call succeeds. If the process doesn't exist, Python raises `ProcessLookupError`.

It's like knocking on a door without opening it: you find out if anyone's home without disturbing them.

### Checkpoint 2 ✅

1. What does `os.kill(pid, 0)` do, and why is it useful?
2. What is a "stale" PID file?
3. Where do real Linux systems keep PID files?

**Deliverable for Part 2:** the updated `mydaemon.py`, and a terminal transcript showing (a) starting the daemon, (b) the PID file contents, (c) a refused second-start attempt, (d) stopping it, (e) the PID file being gone.

---

## Part 3 — Teaching your daemon manners with signals

**Goal:** Make your daemon respond politely to signals — the way a real daemon must.

**Time estimate:** 1.5–2 hours. This is the heart of the project.

### What's a signal?

A **signal** is a tiny message the operating system can send to a running process. There's no body — just a number (or a name). When a process receives a signal, it either:

1. Does the default thing the OS defines for that signal (usually: terminate), **or**
2. Runs a special function the programmer set up — called a **signal handler** — to react in a custom way.

You've already been sending signals without knowing it:

- `Ctrl+C` sends `SIGINT` (signal 2) — "please interrupt."
- `kill 12345` sends `SIGTERM` (signal 15) — "please terminate."
- `kill -9 12345` sends `SIGKILL` (signal 9) — "die immediately, no cleanup."

Analogy: signals are like someone knocking on your office door. The default reaction might be "pack up and leave." But if you install a signal handler, it's like training yourself to say "one moment, let me save my work first."

### What we'll handle

Our daemon will catch two signals:

| Signal | What we'll do when we receive it |
|---|---|
| `SIGTERM` (15) | Shut down gracefully: clean up the PID file, write a log line, exit cleanly |
| `SIGUSR1` (10) | Write a "status dump" to the log: how long we've been running, how many log lines we've written |

`SIGKILL` (9) cannot be caught — it always kills. That's a feature, not a bug: it guarantees you can always stop a runaway process.

### Step 3.1 — Update `mydaemon.py`

Replace your `bin/mydaemon.py` with this version:

```python
#!/usr/bin/env python3
"""
mydaemon.py - version 0.3 (Part 3)
Now with signal handlers -- responds to SIGTERM and SIGUSR1.
"""

import os
import sys
import time
import signal
from datetime import datetime

LOG_FILE = "var/log/mydaemon.log"
PID_FILE = "var/run/mydaemon.pid"

# We'll use these to track information about ourselves.
start_time = None
loops_completed = 0
should_exit = False  # set to True by the SIGTERM handler


def log(message):
    with open(LOG_FILE, "a") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {message}\n")
        f.flush()


def is_pid_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def check_already_running():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            old_pid = int(f.read().strip())
        if is_pid_running(old_pid):
            print(f"Error: mydaemon is already running (PID {old_pid}).")
            sys.exit(1)
        else:
            print(f"Removing stale PID file (old PID {old_pid} is dead).")
            os.remove(PID_FILE)


def write_pid_file():
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    log(f"mydaemon started with PID {os.getpid()}")


def remove_pid_file():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    log("mydaemon stopped cleanly")


# --- Signal handlers below ---

def handle_sigterm(signum, frame):
    """Called when we receive SIGTERM. Asks the main loop to exit."""
    global should_exit
    log(f"Received SIGTERM -- will exit after current loop")
    should_exit = True


def handle_sigusr1(signum, frame):
    """Called when we receive SIGUSR1. Dumps status to the log."""
    uptime = int(time.time() - start_time)
    log(f"STATUS DUMP: uptime={uptime}s, loops_completed={loops_completed}, pid={os.getpid()}")


def install_signal_handlers():
    """Connect the signals to our handler functions."""
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGUSR1, handle_sigusr1)


def main():
    global start_time, loops_completed

    check_already_running()
    write_pid_file()
    install_signal_handlers()
    start_time = time.time()

    try:
        while not should_exit:
            log("mydaemon is alive")
            loops_completed += 1
            time.sleep(5)
    finally:
        remove_pid_file()


if __name__ == "__main__":
    main()
```

### Step 3.2 — Test SIGTERM (graceful shutdown)

Start the daemon:

```bash
python3 bin/mydaemon.py &
```

Send it SIGTERM:

```bash
kill -TERM $(cat var/run/mydaemon.pid)
```

Check the log:

```bash
tail var/log/mydaemon.log
```

You should see something like:

```
[2026-04-21 14:30:02] mydaemon started with PID 12345
[2026-04-21 14:30:02] mydaemon is alive
[2026-04-21 14:30:07] mydaemon is alive
[2026-04-21 14:30:10] Received SIGTERM -- will exit after current loop
[2026-04-21 14:30:12] mydaemon stopped cleanly
```

Notice: the daemon didn't die instantly. It logged the signal, finished what it was doing, cleaned up the PID file, and exited politely. **That's the whole point.**

### Step 3.3 — Test SIGUSR1 (status dump)

Start the daemon again:

```bash
python3 bin/mydaemon.py &
```

Wait about 20 seconds, then send it SIGUSR1:

```bash
kill -USR1 $(cat var/run/mydaemon.pid)
```

Check the log:

```bash
tail var/log/mydaemon.log
```

You should see a line like:

```
[2026-04-21 14:35:30] STATUS DUMP: uptime=22s, loops_completed=4, pid=12345
```

Send it again a minute later — the uptime and loop count will have grown.

Finally, shut it down:

```bash
kill -TERM $(cat var/run/mydaemon.pid)
```

### How signal handlers actually work (the honest explanation)

When you call `signal.signal(signal.SIGUSR1, handle_sigusr1)`, you're telling Python: "Hey, whenever this process receives SIGUSR1, interrupt whatever you're doing and run `handle_sigusr1()`."

This is genuinely a little bit magical — the operating system pauses your code mid-execution, runs your handler, and then resumes. It's like the OS taps your program on the shoulder and hands it a note.

### Checkpoint 3 ✅

1. What's the difference between SIGTERM and SIGKILL? Why can't you catch SIGKILL?
2. In our code, why do we use a `should_exit` flag instead of calling `sys.exit()` directly inside the signal handler?
3. What does `kill -USR1 <pid>` do to our daemon?

**Deliverable for Part 3:** the updated `mydaemon.py`, and a terminal transcript showing (a) the daemon starting, (b) you sending SIGUSR1 and seeing a status dump, (c) you sending SIGTERM and seeing a graceful shutdown.

---

## Part 4 — Give the daemon a real job

**Goal:** Make your daemon actually *do* something useful: watch a folder and log changes.

**Time estimate:** 45 minutes.

### The job

Your daemon will look inside `watched/` every 5 seconds and log how many files are there. If the number changes, it'll say so clearly.

This is a simple version of how real monitoring daemons work.

### Step 4.1 — Update `mydaemon.py`

Open `bin/mydaemon.py`. Find the `main()` function. We're going to change it so it does real work instead of just logging "is alive."

Find the `while not should_exit:` loop. Replace just that loop block with this:

```python
    # Track how many files we saw last time so we can detect changes.
    previous_count = -1

    try:
        while not should_exit:
            # Count files in the watched directory.
            try:
                files = os.listdir("watched")
                current_count = len(files)
            except FileNotFoundError:
                log("WARNING: watched/ folder is missing!")
                current_count = 0

            # Log differently depending on whether anything changed.
            if current_count != previous_count:
                log(f"Watched folder changed: now has {current_count} file(s)")
                previous_count = current_count
            else:
                log(f"Watched folder stable: {current_count} file(s)")

            loops_completed += 1
            time.sleep(5)
    finally:
        remove_pid_file()
```

### Step 4.2 — Test it

Start the daemon:

```bash
python3 bin/mydaemon.py &
```

In another terminal (or after a few seconds), watch the log:

```bash
tail -f var/log/mydaemon.log
```

You should see lines like:

```
[2026-04-21 14:40:00] Watched folder changed: now has 0 file(s)
[2026-04-21 14:40:05] Watched folder stable: 0 file(s)
```

Now add a file to `watched/`:

```bash
touch watched/hello.txt
```

Within 5 seconds, you should see:

```
[2026-04-21 14:40:15] Watched folder changed: now has 1 file(s)
```

Try adding more files, deleting files, etc. Each change should show up in the log.

Stop when you're done:

```bash
kill -TERM $(cat var/run/mydaemon.pid)
```

### Checkpoint 4 ✅

1. Why do we use `try / except FileNotFoundError` around `os.listdir()`?
2. How does `previous_count = -1` at the start guarantee the first check always logs as "changed"?

**Deliverable for Part 4:** the updated `mydaemon.py`, plus a log-file excerpt showing the daemon detecting at least one file being added and one being removed.

---

## Part 5 — The control script (`mydaemonctl.py`)

**Goal:** Build a nice command-line tool that makes your daemon easy to use — just like `systemctl` on real Linux.

**Time estimate:** 2 hours.

### What we're building

Your control script will support five commands:

| Command | What it does |
|---|---|
| `start` | Launches the daemon in the background |
| `stop` | Sends SIGTERM and waits for a graceful shutdown |
| `status` | Shows whether it's running, its PID, and the last 5 log lines |
| `dump` | Sends SIGUSR1 to trigger a status dump, then shows it |
| `restart` | Stop, then start |

Usage will look like:

```bash
python3 bin/mydaemonctl.py start
python3 bin/mydaemonctl.py status
python3 bin/mydaemonctl.py stop
```

### Step 5.1 — Type the control script

Open `bin/mydaemonctl.py` and type in the following:

```python
#!/usr/bin/env python3
"""
mydaemonctl.py - control script for mydaemon
Usage: python3 bin/mydaemonctl.py <start|stop|status|dump|restart>
"""

import os
import sys
import time
import signal
import subprocess

PID_FILE = "var/run/mydaemon.pid"
LOG_FILE = "var/log/mydaemon.log"
DAEMON_SCRIPT = "bin/mydaemon.py"


def is_pid_running(pid):
    """Same trick we used before."""
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def read_pid():
    """Return the PID from the PID file, or None if not running."""
    if not os.path.exists(PID_FILE):
        return None
    with open(PID_FILE, "r") as f:
        return int(f.read().strip())


def cmd_start():
    """Start the daemon in the background."""
    pid = read_pid()
    if pid and is_pid_running(pid):
        print(f"mydaemon is already running (PID {pid}).")
        return

    # Launch the daemon as a detached background process.
    # Popen with start_new_session=True makes it independent of this shell.
    subprocess.Popen(
        ["python3", DAEMON_SCRIPT],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    # Give it a moment to write its PID file.
    time.sleep(1)

    new_pid = read_pid()
    if new_pid:
        print(f"mydaemon started (PID {new_pid}).")
    else:
        print("Something went wrong -- no PID file after 1 second.")


def cmd_stop():
    """Send SIGTERM and wait for clean shutdown."""
    pid = read_pid()
    if not pid:
        print("mydaemon is not running.")
        return
    if not is_pid_running(pid):
        print(f"Stale PID file found -- removing.")
        os.remove(PID_FILE)
        return

    print(f"Sending SIGTERM to PID {pid}...")
    os.kill(pid, signal.SIGTERM)

    # Wait up to 10 seconds for the daemon to exit cleanly.
    for _ in range(10):
        time.sleep(1)
        if not is_pid_running(pid):
            print("mydaemon stopped.")
            return

    print("mydaemon did not stop within 10 seconds. You may need 'kill -9'.")


def cmd_status():
    """Show whether the daemon is running + the last few log lines."""
    pid = read_pid()
    if pid and is_pid_running(pid):
        print(f"mydaemon is RUNNING (PID {pid}).")
    elif pid:
        print(f"mydaemon is STOPPED (stale PID file with dead PID {pid}).")
    else:
        print("mydaemon is STOPPED.")

    print("\n--- Last 5 log lines ---")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        for line in lines[-5:]:
            print(line.rstrip())
    else:
        print("(no log file yet)")


def cmd_dump():
    """Trigger a status dump inside the daemon."""
    pid = read_pid()
    if not pid or not is_pid_running(pid):
        print("mydaemon is not running.")
        return
    os.kill(pid, signal.SIGUSR1)
    print(f"Sent SIGUSR1 to PID {pid}. Waiting a moment for the log to update...")
    time.sleep(1)
    # Show the last few log lines so the user can see the dump.
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    print("\n--- Last 3 log lines ---")
    for line in lines[-3:]:
        print(line.rstrip())


def cmd_restart():
    """Stop, then start."""
    cmd_stop()
    time.sleep(1)
    cmd_start()


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 bin/mydaemonctl.py <start|stop|status|dump|restart>")
        sys.exit(1)

    command = sys.argv[1]
    commands = {
        "start": cmd_start,
        "stop": cmd_stop,
        "status": cmd_status,
        "dump": cmd_dump,
        "restart": cmd_restart,
    }

    if command not in commands:
        print(f"Unknown command: {command}")
        print("Valid commands: start, stop, status, dump, restart")
        sys.exit(1)

    commands[command]()


if __name__ == "__main__":
    main()
```

### Step 5.2 — Test every command

From the `mydaemon/` folder, try each of these in order:

```bash
python3 bin/mydaemonctl.py status
```

Expected output:

```
mydaemon is STOPPED.

--- Last 5 log lines ---
(... whatever was in your log from before ...)
```

Now:

```bash
python3 bin/mydaemonctl.py start
```

Expected output:

```
mydaemon started (PID 12345).
```

Check status again:

```bash
python3 bin/mydaemonctl.py status
```

Expected:

```
mydaemon is RUNNING (PID 12345).

--- Last 5 log lines ---
[2026-04-21 15:00:01] mydaemon started with PID 12345
[2026-04-21 15:00:01] Watched folder changed: now has 0 file(s)
[2026-04-21 15:00:06] Watched folder stable: 0 file(s)
...
```

Trigger a dump:

```bash
python3 bin/mydaemonctl.py dump
```

You should see a `STATUS DUMP` line appear.

Restart it:

```bash
python3 bin/mydaemonctl.py restart
```

You'll see both a stop and a start message, and the PID will be different.

Finally, stop it:

```bash
python3 bin/mydaemonctl.py stop
```

### Bonus — peek into `/proc`

While the daemon is running, do this:

```bash
python3 bin/mydaemonctl.py start
PID=$(cat var/run/mydaemon.pid)
ls /proc/$PID/
cat /proc/$PID/status | head -20
ls /proc/$PID/fd/
```

You're looking directly into the kernel's record of your daemon! The `/proc/$PID/fd/` directory shows every file your daemon has open — you'll see the log file listed there.

This is Linux's "everything is a file" philosophy in action: information about a running process is exposed to you as if it were just files on disk.

### Checkpoint 5 ✅

1. What is `start_new_session=True` doing when we launch the daemon?
2. Why does `cmd_stop()` wait up to 10 seconds instead of returning immediately?
3. What did you see inside `/proc/<PID>/fd/`? Can you explain why?

**Deliverable for Part 5:** the complete `mydaemonctl.py`, plus a terminal transcript showing all five commands working.

---

## Part 6 — Reflection (REPORT.md)

**Goal:** Put into words what you've built. This is worth 10% of your grade — please don't skip it.

Open `REPORT.md` and fill in the following. Replace each `_____` with your own answer. Write at least 2–3 sentences per section.

```markdown
# My Daemon Project - Reflection Report

**Name:** _____________
**Date:** _____________

## Section 1: What I built (in my own words)

I built a program called mydaemon.py that _____________. It uses a special
file called a _______ file (located at _______) to remember its own process
ID, so that _____________.

My control script, mydaemonctl.py, lets a user _____________ by sending
signals to the daemon. The two signals I handle are _______ (which
_____________) and _______ (which _____________).


## Section 2: What happens step-by-step when I run `start`

When a user types `python3 bin/mydaemonctl.py start`, this is what happens
in order:

1. The control script checks _____________.
2. It then launches _____________ using subprocess.Popen with
   start_new_session=True, which means _____________.
3. The new daemon process first _____________.
4. Then it installs its signal handlers, which _____________.
5. Finally, it enters its main loop where every 5 seconds it _____________.


## Section 3: How my toy daemon is different from a real systemd service

I can think of at least three ways my daemon is simpler than a real
systemd-managed service:

1. _____________
2. _____________
3. _____________


## Section 4: One thing that surprised me

While doing this project, the thing that surprised me most was
_____________ because I didn't expect _____________.


## Section 5: If I had root access, I would...

If I had root privileges in my environment, one thing I would change about
my design is _____________, because _____________.
```

---

## Final submission checklist

Before you turn this in, tick each box:

- [ ] `bin/mydaemon.py` is the final version from Part 4 (watches the folder, handles signals)
- [ ] `bin/mydaemonctl.py` is the final version from Part 5 (all 5 commands work)
- [ ] `var/log/mydaemon.log` contains evidence of the daemon running
- [ ] `REPORT.md` is fully filled in — no `_____` blanks remaining
- [ ] I can personally explain every line of code in both Python files
- [ ] I have tested that `stop` works, `restart` works, and `status` reflects reality

**How to submit:** Upload it per your instructor's instructions.

---

## Rubric (100 points)

| Part | Points | What earns them |
|---|---|---|
| Part 1 | 10 | Background process runs; log file grows |
| Part 2 | 15 | PID file written on start, removed on clean exit; second-start is refused |
| Part 3 | 25 | Both signals handled correctly; graceful shutdown demonstrated |
| Part 4 | 20 | Daemon detects file-count changes in `watched/` |
| Part 5 | 20 | All 5 control commands work correctly |
| Part 6 | 10 | REPORT.md fully filled in with thoughtful answers |

Partial credit is given throughout. A student who turns in a clean Parts 1–3 plus a thoughtful REPORT.md still earns a solid grade — so don't panic if you get stuck late.

---

## Getting help

- Stuck on a Python error? Read the traceback out loud. The last line of a Python error usually tells you what's wrong.
- Signal-related bug? Add a `print()` inside your signal handler to check it's being called.
- Daemon won't start? Check: does `var/run/mydaemon.pid` already exist from a previous session? Delete it manually and try again.
- Log file not updating? Remember `f.flush()` — without it, Python might be buffering.

Good luck, and remember the big idea: **you're building, in miniature, the same machinery real servers use every day.** That's not nothing.

— End of handout —
