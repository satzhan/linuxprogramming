# AWK for Log Analysis: A Student Guide

## Purpose of This Lab

Software systems produce logs: small text records describing what happened inside a program. A log might tell us that a user logged in, a database connection failed, a network request was slow, or a user interface crashed.

In this lab, you will learn how to use `awk` to inspect a pseudo-log file named `application.log`. The goal is not only to learn a few commands, but to learn a way of thinking:

> A log file is a table hiding inside plain text. `awk` helps us read each line, split it into meaningful pieces, and ask questions about those pieces.

By the end, you should be able to:

- explain what AWK records and fields are;
- use field separators with `-F`;
- print selected fields from structured text;
- filter rows using patterns and conditions;
- count and rank items using AWK arrays;
- analyze a log file by log level, module, and message.

---

## Files Used in This Lab

This lab uses the following files:

```text
application.log      # the pseudo-log file to analyze
log_generator.py     # Python script that can generate a new log file
instructions.txt     # original lab task list
solutions.txt        # original solution commands
 theory_awk.txt      # short AWK theory notes
```

The main data file is `application.log`. It contains 1000 pseudo-log entries.

A typical line looks like this:

```text
[2023-09-04 01:24:03] [ERROR] [AUTH]: Failed login attempt.
```

The intended structure is:

```text
[TIMESTAMP] [LOG_LEVEL] [MODULE]: Message
```

So the line has four logical parts:

| Logical Part | Example |
|---|---|
| Timestamp | `2023-09-04 01:24:03` |
| Log level | `ERROR` |
| Module | `AUTH` |
| Message | `Failed login attempt.` |

---

## Part 1: What Is AWK?

`awk` is a text-processing language. It is especially useful when a file has repeated structure: rows, columns, fields, or predictable patterns.

A simple AWK command has this shape:

```bash
awk 'pattern { action }' file
```

The basic idea is:

```text
for each line in the file:
    if the line matches the pattern:
        perform the action
```

If you do not give a pattern, AWK applies the action to every line.

If you do not give an action, AWK prints every line that matches the pattern.

### AWK Vocabulary

| Term | Meaning | Simple analogy |
|---|---|---|
| Record | One input line | One row in a table |
| Field | One piece of a record | One column in a row |
| Field separator | The rule for splitting a line into fields | The knife used to cut the row into columns |
| Pattern | A condition for selecting lines | “Only rows where the level is ERROR” |
| Action | What AWK does to selected lines | “Print the module” or “count this item” |

### Important Built-In Variables

| Variable | Meaning |
|---|---|
| `$0` | the entire current line |
| `$1`, `$2`, `$3`, ... | the first, second, third, etc. fields |
| `NR` | current line number, starting from 1 |
| `NF` | number of fields in the current line |
| `FS` | input field separator |
| `OFS` | output field separator |

Example:

```bash
echo "apple orange" | awk '{print $2, $1}'
```

Output:

```text
orange apple
```

Why? By default, AWK splits on whitespace. So:

```text
$1 = apple
$2 = orange
```

---

## Part 2: First Commands

### Print the whole file

```bash
awk '{print}' application.log
```

This prints every line. It is similar to:

```bash
cat application.log
```

But the AWK version matters because we can soon add filters and field logic.

### Print only the first 5 lines

```bash
awk 'NR <= 5 {print}' application.log
```

Here, `NR` is the current line number.

Read it as:

> If the current line number is less than or equal to 5, print the line.

### Print line numbers with each log line

```bash
awk '{print NR, $0}' application.log
```

Here:

- `NR` prints the current line number;
- `$0` prints the full original line.

---

## Part 3: Understanding the Log Structure

The log line is not separated by commas or simple spaces. It uses brackets:

```text
[2023-09-04 01:24:03] [ERROR] [AUTH]: Failed login attempt.
```

A useful separator for this file is:

```bash
-F'] \\['
```

That means:

> Split the line whenever AWK sees `] [`.

Use this command to inspect the first line:

```bash
awk -F'] \\[' 'NR == 1 {print "field 1:", $1; print "field 2:", $2; print "field 3:", $3}' application.log
```

Example output shape:

```text
field 1: [2023-09-04 01:24:03
field 2: WARNING
field 3: AUTH]: DB nearing max capacity.
```

Notice the important detail:

```text
$1 = [timestamp
$2 = log level
$3 = module plus message
```

The module and message are still together inside `$3`:

```text
AUTH]: DB nearing max capacity.
```

That means we often need one more step to separate the module from the message.

This is the key structural observation of the lab.

---

## Part 4: Filtering Lines by Pattern

### Print all lines containing `ERROR`

```bash
awk '/ERROR/ {print}' application.log
```

This prints any line where the full line contains the text `ERROR`.

Since every error log has `[ERROR]`, this works well for basic filtering.

### Print all logs from the `DATABASE` module

A simple version is:

```bash
awk '/DATABASE/ {print}' application.log
```

This usually works, but it is not very precise. It prints any line containing the word `DATABASE` anywhere.

A better version checks the module part specifically:

```bash
awk -F'] \\[' '$3 ~ /^DATABASE\]:/ {print}' application.log
```

Read it as:

```text
Split each line on ] [.
If field 3 begins with DATABASE]:
    print the line.
```

Why use this version? Because it distinguishes:

```text
module is DATABASE
```

from:

```text
message merely mentions DATABASE
```

In real log analysis, this difference matters.

---

## Part 5: Extracting Fields

### Print all log levels

```bash
awk -F'] \\[' '{print $2}' application.log
```

This prints the log level from every line.

Example output:

```text
WARNING
ERROR
DEBUG
WARNING
ERROR
...
```

### Print unique log levels

```bash
awk -F'] \\[' '{print $2}' application.log | sort | uniq
```

Expected unique levels:

```text
DEBUG
ERROR
INFO
WARNING
```

### Count each log level

```bash
awk -F'] \\[' '{print $2}' application.log | sort | uniq -c | sort -rn
```

For the provided `application.log`, the counts are:

```text
257 ERROR
253 INFO
248 DEBUG
242 WARNING
```

The pipeline works like this:

| Command | Role |
|---|---|
| `awk -F'] \\[' '{print $2}' application.log` | extract the log level |
| `sort` | group identical levels next to each other |
| `uniq -c` | count each group |
| `sort -rn` | rank counts from largest to smallest |

Important: `uniq` only counts adjacent duplicates. That is why `sort` must come before `uniq -c`.

---

## Part 6: Separating Module and Message

Because `$3` contains both the module and the message, we can use `split()`.

Try this on the first line:

```bash
awk -F'] \\[' 'NR == 1 {split($3, parts, "\\]: "); print "module:", parts[1]; print "message:", parts[2]}' application.log
```

Output shape:

```text
module: AUTH
message: DB nearing max capacity.
```

Explanation:

```awk
split($3, parts, "\\]: ")
```

This splits `$3` at the text:

```text
]: 
```

So if `$3` is:

```text
AUTH]: DB nearing max capacity.
```

then:

```text
parts[1] = AUTH
parts[2] = DB nearing max capacity.
```

---

## Part 7: Counting with AWK Arrays

AWK arrays are useful for counting.

The pattern is:

```awk
count[key]++
```

Read it as:

> Increase the counter for this key by 1.

### Count logs per module

```bash
awk -F'] \\[' '{split($3, parts, "\\]: "); module = parts[1]; count[module]++} END {for (module in count) print count[module], module}' application.log
```

This prints module counts, but the order may look random because AWK arrays are not automatically sorted.

To rank the modules, pipe the result into `sort -rn`:

```bash
awk -F'] \\[' '{split($3, parts, "\\]: "); module = parts[1]; count[module]++} END {for (module in count) print count[module], module}' application.log | sort -rn
```

For the provided `application.log`, the result is:

```text
225 DATABASE
206 UI
196 API
191 AUTH
182 NETWORK
```

This is a common real-world log question:

> Which part of the system is producing the most logs?

That can be a clue about activity, noise, instability, or simply which module is busiest.

---

## Part 8: Combining Conditions

AWK conditions can use logical operators.

| Operator | Meaning |
|---|---|
| `==` | equals |
| `!=` | not equal |
| `~` | matches regular expression |
| `!~` | does not match regular expression |
| `&&` | AND |
| `||` | OR |

### Print only ERROR logs from AUTH

```bash
awk -F'] \\[' '$2 == "ERROR" && $3 ~ /^AUTH\]:/ {print}' application.log
```

Read it as:

```text
If field 2 is ERROR
AND field 3 begins with AUTH]:
    print the line
```

### Print only the messages for ERROR logs from AUTH

```bash
awk -F'] \\[' '$2 == "ERROR" && $3 ~ /^AUTH\]:/ {msg = $3; sub(/^[^:]+: /, "", msg); print msg}' application.log
```

The command:

```awk
sub(/^[^:]+: /, "", msg)
```

removes the module prefix from the message.

Before:

```text
AUTH]: Failed login attempt.
```

After:

```text
Failed login attempt.
```

### Print unique ERROR messages from AUTH

```bash
awk -F'] \\[' '$2 == "ERROR" && $3 ~ /^AUTH\]:/ {msg = $3; sub(/^[^:]+: /, "", msg); print msg}' application.log | sort | uniq
```

For the provided `application.log`, the unique AUTH error messages are:

```text
DB connection lost.
Failed login attempt.
Network error.
UI crashed.
```

---

## Part 9: The Main Lab Tasks

Complete each task using `awk`. You may use helper commands such as `sort`, `uniq`, `cut`, and `head`, but try to understand what each part of the pipeline contributes.

### Task 1: Identify all unique log levels

Question:

> What different log levels appear in `application.log`?

Command:

```bash
awk -F'] \\[' '{print $2}' application.log | sort | uniq
```

Expected answer:

```text
DEBUG
ERROR
INFO
WARNING
```

---

### Task 2: Extract all logs from the DATABASE module

Question:

> Which log entries came from the `DATABASE` module?

Command:

```bash
awk -F'] \\[' '$3 ~ /^DATABASE\]:/ {print}' application.log
```

To view only the first 10 matching lines:

```bash
awk -F'] \\[' '$3 ~ /^DATABASE\]:/ {print}' application.log | head
```

---

### Task 3: Determine the number of unique ERROR messages from AUTH

Question:

> Among logs where the level is `ERROR` and the module is `AUTH`, how many different messages appear?

Command:

```bash
awk -F'] \\[' '$2 == "ERROR" && $3 ~ /^AUTH\]:/ {msg = $3; sub(/^[^:]+: /, "", msg); print msg}' application.log | sort | uniq | wc -l
```

For the provided `application.log`, the answer is:

```text
4
```

To see the messages themselves:

```bash
awk -F'] \\[' '$2 == "ERROR" && $3 ~ /^AUTH\]:/ {msg = $3; sub(/^[^:]+: /, "", msg); print msg}' application.log | sort | uniq
```

Expected messages:

```text
DB connection lost.
Failed login attempt.
Network error.
UI crashed.
```

---

### Task 4: Rank modules by number of logs generated

Question:

> Which modules generated the most log entries?

Command:

```bash
awk -F'] \\[' '{split($3, parts, "\\]: "); module = parts[1]; count[module]++} END {for (module in count) print count[module], module}' application.log | sort -rn
```

For the provided `application.log`, the answer is:

```text
225 DATABASE
206 UI
196 API
191 AUTH
182 NETWORK
```

---

## Part 10: Alternative Pipeline Versions

Sometimes you will see command-line solutions that combine AWK with other tools.

### Rank modules using `awk`, `cut`, `sort`, and `uniq`

```bash
awk -F'] \\[' '{print $3}' application.log | cut -d':' -f1 | sort | uniq -c | sort -rn
```

This works by extracting field 3:

```text
AUTH]: DB nearing max capacity.
```

Then `cut -d':' -f1` keeps only the part before the colon:

```text
AUTH]
```

This version is acceptable, but the pure AWK version is more explicit because it names the pieces:

```awk
module = parts[1]
count[module]++
```

That is often easier to extend later.

---

## Part 11: Common Mistakes and How to Debug Them

### Mistake 1: Assuming the message is `$4`

With the separator:

```bash
-F'] \\['
```

this log line:

```text
[2023-09-04 01:24:03] [ERROR] [AUTH]: Failed login attempt.
```

splits into:

```text
$1 = [2023-09-04 01:24:03
$2 = ERROR
$3 = AUTH]: Failed login attempt.
```

There is no clean `$4` message field using this separator.

To get the message, split `$3` again or remove the module prefix using `sub()`.

### Mistake 2: Forgetting that `uniq` needs sorted input

This is unreliable:

```bash
awk -F'] \\[' '{print $2}' application.log | uniq -c
```

This is reliable:

```bash
awk -F'] \\[' '{print $2}' application.log | sort | uniq -c
```

Why? `uniq` only merges neighboring duplicates.

### Mistake 3: Matching too broadly

This command:

```bash
awk '/DATABASE/ {print}' application.log
```

prints every line containing `DATABASE` anywhere.

This command is more precise:

```bash
awk -F'] \\[' '$3 ~ /^DATABASE\]:/ {print}' application.log
```

It prints lines where the module itself is `DATABASE`.

### Mistake 4: Confusing shell quotes and AWK quotes

Prefer single quotes around the AWK program:

```bash
awk -F'] \\[' '{print $2}' application.log
```

Inside the AWK program, use double quotes for strings:

```bash
awk -F'] \\[' '$2 == "ERROR" {print}' application.log
```

---

## Part 12: Optional Challenge Problems

These are not required, but they are good practice.

### Challenge 1: Count ERROR logs per module

```bash
awk -F'] \\[' '$2 == "ERROR" {split($3, parts, "\\]: "); module = parts[1]; count[module]++} END {for (module in count) print count[module], module}' application.log | sort -rn
```

### Challenge 2: Count messages regardless of module

```bash
awk -F'] \\[' '{msg = $3; sub(/^[^:]+: /, "", msg); count[msg]++} END {for (msg in count) print count[msg], msg}' application.log | sort -rn
```

### Challenge 3: Show the top 5 most common messages

```bash
awk -F'] \\[' '{msg = $3; sub(/^[^:]+: /, "", msg); count[msg]++} END {for (msg in count) print count[msg], msg}' application.log | sort -rn | head -5
```

### Challenge 4: Convert the log file into CSV-like output

```bash
awk -F'] \\[' '{timestamp = $1; sub(/^\[/, "", timestamp); level = $2; split($3, parts, "\\]: "); module = parts[1]; message = parts[2]; print timestamp "," level "," module "," message}' application.log
```

Example output shape:

```text
2023-09-04 01:24:03,WARNING,AUTH,DB nearing max capacity.
```

---

## Part 13: How the Log File Was Generated

The file `log_generator.py` creates pseudo-log entries by randomly choosing:

- a log level from `INFO`, `WARNING`, `ERROR`, and `DEBUG`;
- a module from `AUTH`, `DATABASE`, `NETWORK`, `UI`, and `API`;
- a message associated with the selected log level.

The generated line format is:

```python
return f"[{timestamp}] [{log_level}] [{module}]: {message}"
```

This is why the lab data is structured enough for AWK to analyze.

To generate a fresh log file, run:

```bash
python3 log_generator.py
```

The script writes a new `application.log` file.

Important: If you regenerate the file, your exact counts may change, because the entries are chosen randomly.

---

## Part 14: Study Summary

The essential AWK pattern from this lab is:

```bash
awk -F'] \\[' 'condition {action}' application.log
```

The essential mental model is:

```text
Each line is one record.
The separator cuts each record into fields.
Fields let us ask precise questions.
Arrays let us count repeated things.
Pipelines let us sort, rank, and summarize.
```

The most important structural fact about this log file is:

```text
$2 = log level
$3 = module plus message
```

So when a task asks for the module or message, you need to split or clean `$3`.

---

## Quick Reference

| Goal | Command |
|---|---|
| Print first 5 lines | `awk 'NR <= 5 {print}' application.log` |
| Print log levels | `awk -F'] \\[' '{print $2}' application.log` |
| Unique log levels | `awk -F'] \\[' '{print $2}' application.log \| sort \| uniq` |
| Count log levels | `awk -F'] \\[' '{print $2}' application.log \| sort \| uniq -c \| sort -rn` |
| DATABASE logs | `awk -F'] \\[' '$3 ~ /^DATABASE\\]:/ {print}' application.log` |
| AUTH ERROR logs | `awk -F'] \\[' '$2 == "ERROR" && $3 ~ /^AUTH\\]:/ {print}' application.log` |
| Unique AUTH ERROR messages | `awk -F'] \\[' '$2 == "ERROR" && $3 ~ /^AUTH\\]:/ {msg = $3; sub(/^[^:]+: /, "", msg); print msg}' application.log \| sort \| uniq` |
| Rank modules | `awk -F'] \\[' '{split($3, parts, "\\\\]: "); module = parts[1]; count[module]++} END {for (module in count) print count[module], module}' application.log \| sort -rn` |

---

## Submission Checklist

Before submitting, make sure you can answer these questions:

- What is a record in AWK?
- What is a field in AWK?
- What does `-F` do?
- Why does this lab use `-F'] \\['`?
- What is stored in `$2` for this log file?
- What is stored in `$3` for this log file?
- Why do we need `sort` before `uniq -c`?
- How does `count[module]++` work?
- How would your answer change if the log format changed?

