# Systems & Streams: A Guide to the Linux Environment and `sed`

To master a system, you must first understand its fundamental mechanisms. Operating in a Linux environment is not about memorizing a dictionary of commands; it is about building an accurate mental model of how data flows. Once you understand the physical reality of the environment, you gain the autonomy to shape it to your exact will.

This manual will rebuild your understanding of text processing from first principles. We will construct a complex sandbox, break down the internal execution cycle of the stream editor, and tackle layered, real-world systems problems by observing data and deducing logical solutions.

---

## Part 1: First Principles of the Linux Environment

Before manipulating streams, you must understand what a stream is. In Linux, an elegant, fundamental philosophy dictates the architecture: *Everything is a file*. 

A text document is a file. Your keyboard is a file. Your monitor is a file. A network socket is a file. Because everything shares this common interface, data can flow between them seamlessly. 

When you launch a process, the operating system automatically opens three primary data streams, known as File Descriptors (FDs):
* **Standard Input (`stdin`, FD 0):** Where the process listens for data (usually the keyboard).
* **Standard Output (`stdout`, FD 1):** Where the process sends successful results (usually the terminal screen).
* **Standard Error (`stderr`, FD 2):** Where the process sends error diagnostics (also the terminal screen, but kept logically separate from stdout).

The pipe `|` is the connective tissue of this environment. It physically connects the `stdout` of one process directly into the `stdin` of another, allowing you to chain small, single-purpose tools into complex data pipelines.

---

## Part 2: Constructing the Laboratory

We need a sandbox of realistic files to experiment on. Open your terminal and paste this entire block exactly as it is written. This will generate four files representing a typical backend system.

```bash
# 1. Create a C source file
cat << 'EOF' > server.c
#include <stdio.h>
#include <stdlib.h>

void initialize_buffer() {
    // DEBUG: Allocating memory
    char *buffer = (char *)malloc(1024);
    if (buffer == NULL) {
        printf("ERROR: Memory allocation failed.\n");
        exit(1);
    }
    // TODO: Implement safety checks
}
EOF

# 2. Create a Configuration file
cat << 'EOF' > config.ini
[database]
uri=tcp://localhost:5432
user=admin
password=secure_pass_123

[network]
# Listen on all interfaces
bind_address=127.0.0.1
port=8080
EOF

# 3. Create a System Log
cat << 'EOF' > auth.log LOGIN_SUCCESS user=root ip=192.168.1.50 LOGIN_FAILED user=admin ip=10.0.0.5 LOGIN_FAILED user=unknown ip=10.0.0.5 SYSTEM_RESTART LOGIN_SUCCESS user=sajan ip=192.168.1.100
EOF

# 4. Create a Data Roster
cat << 'EOF' > roster.csv
ID,LastName,FirstName,Department
101,Smith,John,Engineering
102,Sitmukhambetov,Sajan,Computer Science
103,Doe,Jane,Physics
EOF
```

---

## Part 3: The Internal Mechanics of `sed`

Most users treat `sed` (Stream Editor) as a simple find-and-replace tool. `sed` is actually a Turing-complete text processing engine. 

To use it effectively, we have to look at how it handles memory. `sed` does not load a file into RAM all at once; it processes an infinite stream using two internal buffers: The **Pattern Space** (the workbench) and the **Hold Space** (the clipboard).

**The Standard Execution Cycle:**
1.  **Read:** `sed` reads exactly one line from `stdin` and places it into the Pattern Space.
2.  **Execute:** `sed` checks its list of provided instructions. If a line matches the conditions, the instruction modifies the Pattern Space.
3.  **Output:** `sed` automatically prints the final contents of the Pattern Space to `stdout` (unless the `-n` flag is used to suppress this).
4.  **Flush:** The Pattern Space is wiped clean.
5.  **Loop:** The cycle repeats for the next line.

**The Core Operations:**
* `s/old/new/` : **Substitute**. Replaces text in the Pattern Space.
* `p` : **Print**. Explicitly prints the current Pattern Space.
* `d` : **Delete**. Instantly wipes the Pattern Space and aborts the current cycle, moving to the next line.
* `a\` : **Append**. Queues text to be written to `stdout` *after* the Pattern Space is printed.
* `i\` : **Insert**. Queues text to be written to `stdout` *before* the Pattern Space is printed.

---

## Part 4: Applied Operations

Let's put the engine to work. We'll start by auditing our system for security threats. We want to extract all IP addresses that triggered a `LOGIN_FAILED` event from `auth.log`. 

Looking at the log, the data is chronological. We don't need every line, so our first move is to suppress the default output (`-n`). We only care about lines containing `LOGIN_FAILED`. Once we isolate those, we need to strip away everything leading up to the IP address.

```bash
sed -n '/LOGIN_FAILED/ s/.*ip=//p' auth.log
```

Here, `/LOGIN_FAILED/` acts as an address; `sed` only runs the substitution if this matches. The `s/.*ip=//` command replaces everything from the start of the line up to `ip=` with nothing. Finally, `p` prints our modified workbench. You should see `10.0.0.5` outputted twice.

Next, consider a backend migration. In `config.ini`, we need to change the database URI from `tcp://localhost:5432` to `tls://db.internal:5432`. However, we must ensure we *only* touch the database block. Also, our target text contains forward slashes, which usually break the standard `s/old/new/` syntax.

To handle the slashes, we can swap the default delimiter for a hash `#`. To restrict where the change happens, we can provide `sed` with a range address based on the file's headers.

```bash
sed '/\[database\]/,/\[network\]/ s#tcp://localhost:5432#tls://db.internal:5432#' config.ini
```

The range `/\[database\]/,/\[network\]/` creates an execution window. `sed` activates the substitution rule when it sees `[database]` and deactivates it when it hits `[network]`. 

Sometimes, data is structurally sound but formatted incorrectly for our needs. Our legacy `roster.csv` stores names as "LastName,FirstName". If a new system requires "FirstName LastName" (dropping the comma), simple string matching won't work because the names vary. We have to match the structural pattern.

Using Extended Regular Expressions (`-E`), we can capture the structural elements into temporary memory blocks using parentheses, and then reassemble them using backreferences (`\1`, `\2`).

```bash
sed -E 's/([A-Za-z]+),([A-Za-z]+)/\2 \1/' roster.csv
```

The first `([A-Za-z]+)` captures the last name as `\1`, and the second captures the first name as `\2`. The replacement string `\2 \1` neatly swaps their positions and inserts a space instead of a comma.

Up to this point, we have only modified data within a single line. To move data *across* lines, we must engage the **Hold Space**. Think of it as a clipboard where we can tuck data away for later.
* `h`: Copy Pattern Space to Hold Space.
* `H`: Append Pattern Space to Hold Space.
* `G`: Append Hold Space to Pattern Space.

In `server.c`, the includes for `<stdio.h>` and `<stdlib.h>` are physically in the wrong order. To swap them, we need to read the first line, hide it on the clipboard, print the second line, and then retrieve the first line.

```bash
sed '/stdio\.h/ { h; d; }; /stdlib\.h/ G' server.c
```

When `sed` hits the `stdio.h` line, it copies it to the clipboard (`h`), then deletes the Pattern Space (`d`) so it doesn't print, immediately starting the next cycle. When it hits the `stdlib.h` line, it appends the clipboard to the Pattern Space (`G`). When the cycle finishes, `stdlib.h` prints, followed immediately by `stdio.h`.

---

## Part 5: Independent Exploration

You now possess the logical components necessary to architect complex text transformations. Try to deduce the solutions for these scenarios without looking for external answers. Rely on the execution cycle.

**1. The Code Sweeper**
Create a single command that removes all comments (lines starting with `//`) AND removes all empty lines from `server.c`. 
*Hint: You can chain multiple commands by separating them with a semicolon `;` or passing multiple `-e` flags.*

**2. Dynamic Injection**
Locate the `bind_address=127.0.0.1` line in `config.ini`. Using the `a\` (append) command, inject a new line dynamically that says `max_connections=500` immediately following the bind address.

**3. The Sentinel**
Parse `auth.log`. For any line containing `LOGIN_SUCCESS`, replace the word `SUCCESS` with `GRANTED` and append the phrase `[AUDITED]` to the very end of the line. 
*Hint: The `$` character in regex represents the end of the line.*

**4. Permanent Architecture**
Once you have formulated a command you are confident in, execute it using the `-i` flag. This will bypass `stdout` and permanently rewrite the file in place. Verify the structural changes by reading the file with `cat`.
