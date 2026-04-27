# The Linux Artisan: A Hands-On Guide to Stream Editing

Welcome to the workshop. Mastering a Linux environment is not about memorizing commands; it is about building accurate mental models of how information flows. Once you understand the flow, you gain the autonomy to shape it.

This guide is entirely self-contained. We will start with a foundational concept, immediately build a sandbox to test it, and then work through progressively complex, real-world problems. 

Our approach relies on four steps for every challenge:
1. Understand the exact nature of the problem.
2. Devise a logical plan before touching the keyboard.
3. Execute the plan.
4. Look back and dissect why it worked.

---

## Part 1: The Mental Model

Imagine a traditional text editor (like Notepad or Nano) as a drawing board. You lay the entire document flat, look at it, move your pen to a specific spot, and change something. This is static editing.

`sed` (Stream Editor) is different. Imagine an assembly line. 
The text is a continuous stream of products moving swiftly down the conveyor belt. You stand next to the belt with a set of strict, pre-programmed instructions. As each line of text zooms past, you inspect it. If it matches your criteria, you instantly apply a modification (a stamp, a cut, a replacement) and let it continue down the line to the output bin. 

Because `sed` never loads the entire file into memory at once, it can process gigabytes of data in seconds. 

---

## Part 2: Constructing Your Sandbox

Experience is the only true teacher. Before we discuss theory, let us build the materials we will manipulate. 

Open your terminal and paste the following commands. This will generate three files (`app.py`, `server.conf`, and `system.log`) in your current directory. These are yours to break and rebuild.

```bash
# 1. Create a Python script
cat << 'EOF' > app.py
def init_system():
    print("DEBUG: System starting...")
    # TODO: Load environment variables
    db_connect()
    # TODO: Verify cache
    print("DEBUG: System initialized.")

def db_connect():
    connection_string = "jdbc:mysql://localhost:3306"
    print("DEBUG: Connecting to DB")
EOF

# 2. Create a Configuration file
cat << 'EOF' > server.conf
[network]
port=8080
host=127.0.0.1
protocol=http

[database]
# The primary database URL
url=http://localhost:5432
user=admin
EOF

# 3. Create a Log file
cat << 'EOF' > system.log
[2026-04-27 10:00:01] INFO  System booted successfully.
[2026-04-27 10:05:12] WARN  High memory usage detected.
[2026-04-27 10:10:45] ERROR Failed to connect to database.
[2026-04-27 10:12:00] INFO  Retrying connection...
[2026-04-27 10:12:05] ERROR Connection timeout.
EOF
```

---

## Part 3: The Core Toolkit

The anatomy of a `sed` command is: `sed [OPTIONS] 'instruction' target_file`

The `instruction` tells our assembly line worker what to do.
* **`s/old/new/` (Substitute):** Find 'old', replace with 'new'.
* **`g` (Global flag):** Apply the substitution to *every* match on the line, not just the first one.
* **`p` (Print):** Explicitly output the line.
* **`d` (Delete):** Drop the line from the assembly line; do not output it.
* **`a` (Append):** Add a new line of text *after* the current line.

**Crucial Options:**
* **`-n` (Quiet mode):** By default, `sed` outputs everything that passes down the assembly line. `-n` turns off this automatic output, forcing `sed` to only output what you explicitly tell it to (usually paired with `p`).
* **`-i` (In-place):** Saves the output permanently to the original file instead of printing it to your screen.

---

## Part 4: The Missions

We will now apply our tools to the sandbox. 

### Mission 1: The Broad Stroke
**1. Understand:** You are preparing `app.py` for a production release. You must change all `DEBUG:` tags to `INFO:`.
**2. Plan:** We require a basic substitution instruction. We want it applied globally across the file.
**3. Execute:**
```bash
sed 's/DEBUG:/INFO:/g' app.py
```
**4. Look Back:** The text flowed through. Everywhere `sed` saw `DEBUG:`, it stamped `INFO:`. Because we did not use `-i`, your original `app.py` remains unchanged. You are simply viewing the modified stream on your screen.

### Mission 2: Escaping the Slash
**1. Understand:** In `server.conf`, update the database URL from `http://localhost:5432` to `http://prod-db.internal:5432`.
**2. Plan:** We need substitution, but our target string contains forward slashes (`/`). If we use the standard `s/old/new/`, `sed` will interpret the slashes in `http://` as the end of the instruction and crash. We must change the delimiter.
**3. Execute:**
```bash
sed 's#http://localhost:5432#[http://prod-db.internal:5432](http://prod-db.internal:5432)#g' server.conf
```
**4. Look Back:** `sed` is flexible. The character immediately following the `s` becomes the delimiter. By using `#`, we safely encapsulated the slashes within our search string.

### Mission 3: Signal Extraction
**1. Understand:** You are investigating an outage. You only want to see the `ERROR` lines in `system.log`.
**2. Plan:** The default behavior of printing everything is useless here. We must silence the default output (`-n`), search for the pattern `ERROR`, and explicitly print (`p`) only those lines.
**3. Execute:**
```bash
sed -n '/ERROR/p' system.log
```
**4. Look Back:** The stream is quieted. The instruction `/ERROR/` identifies the target, and `p` reveals it. This is how you extract needles from haystacks.

### Mission 4: Precision Surgery (Contextual Addressing)
**1. Understand:** Look at `server.conf`. There is a `host=127.0.0.1` under `[network]`. Imagine there were other `host=` lines in the file, but you *only* want to change the network host to `0.0.0.0`.
**2. Plan:** We cannot just do `s/127.0.0.1/0.0.0.0/` because it might change the wrong line. We must give `sed` an *address*. We tell it: "Find the line containing `host=`, and *then* perform the substitution."
**3. Execute:**
```bash
sed '/host=/ s/127.0.0.1/0.0.0.0/' server.conf
```
**4. Look Back:** The assembly worker inspects the line. Does it contain `host=`? If yes, it applies the substitution logic. If no, it passes the line along untouched. 

### Mission 5: The Architect (Structural Changes)
**1. Understand:** You need to add a new configuration parameter, `timeout=30`, immediately after the `protocol=http` line in `server.conf`.
**2. Plan:** We are not substituting text; we are injecting it. We will search for the specific line, then use the Append (`a`) command.
**3. Execute:**
```bash
sed '/protocol=http/a timeout=30' server.conf
```
**4. Look Back:** The `/protocol=http/` acts as the trigger. When the worker sees this line, it passes it through, and immediately manufactures a new line `timeout=30` right behind it on the assembly belt.

### Mission 6: The Transmuter (Advanced Pattern Capture)
**1. Understand:** In `app.py`, you want to standardize your function definitions. You want to change `def init_system():` to `def system_init():`, but you want a rule that works for *any* two words separated by an underscore.
**2. Plan:** We must use Regular Expressions to capture the two words into temporary variables, then swap their order in the output.
**3. Execute:**
```bash
sed -E 's/def ([a-z]+)_([a-z]+)\(\):/def \2_\1():/g' app.py
```
**4. Look Back:** * `-E` enables extended regular expressions (making syntax cleaner).
* `([a-z]+)` captures a sequence of letters and stores it in memory. We do this twice.
* In the replacement string, `\1` recalls the first captured word (`init`), and `\2` recalls the second (`system`). We output them in reverse order: `\2_\1`. 

---

## Part 5: Independent Practice

You have seen how the concepts connect to execution. True competence requires independent experimentation. Use your sandbox to solve these challenges:

1.  **The Cleaner:** Write a command that removes all lines starting with `#` from `app.py` and `server.conf`. (Hint: Use the delete `d` command with a line-start `^` regex).
2.  **The Time Traveler:** Write a single command that extracts only the timestamps (e.g., `2026-04-27 10:00:01`) from `system.log`, discarding the rest of the text on the line. 
3.  **The Commitment:** Once you are confident in your solution for The Cleaner, apply it using the `-i` flag to permanently alter your sandbox files. Use `cat app.py` to verify the comments are gone forever.

The system will do exactly what you tell it to do. If it breaks, observe the output, adjust your mental model, refine your plan, and try again.
