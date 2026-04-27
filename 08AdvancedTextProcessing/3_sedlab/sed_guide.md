# Linux Text Processing Lab: Learning `sed` by Editing Real Files

## Purpose of This Guide

This guide introduces `sed`, the Linux **stream editor**. A stream editor reads text, applies editing rules, and prints the result. It is useful when a file is too large, repetitive, or mechanical to edit by hand.

The main idea is simple:

> Instead of opening a file and manually changing text, we describe the change as a command.

For example, instead of opening a Python file and manually changing every `Debug:` message to `Info:`, we can write one command that performs the transformation for us.

---

## Learning Goals

By the end of this lab, you should be able to:

1. Explain what `sed` does.
2. Use `sed` to print selected lines.
3. Use `sed` to replace text.
4. Understand the difference between previewing output and changing a file.
5. Use a different delimiter when replacing text that contains `/` characters.
6. Use `sed` safely on source code and configuration files.
7. Check your work using commands such as `cat`, `diff`, and redirection.

---

## The Mental Model

Imagine a conveyor belt of text lines.

A file enters `sed` one line at a time:

```text
line 1  ---> sed rule ---> output line 1
line 2  ---> sed rule ---> output line 2
line 3  ---> sed rule ---> output line 3
```

`sed` does **not** usually open a full-screen editor. It does not ask you to move your cursor. It simply reads text, applies rules, and prints the result.

This is why `sed` is powerful for automation. Once a rule is correct, it can be reused on many files.

---

## Before You Start: Create a Lab Folder

Create a clean folder for this lab:

```bash
mkdir sed_lab
cd sed_lab
```

Create the starter Python file:

```bash
cat > app.py <<'PY'
def main():
    print("Debug: Starting application")
    # TODO: Implement feature X
    connect_database()
    # TODO: Implement feature Y

def connect_database():
    url = "http://localhost:8080"
    print("Debug: Connecting to database")
    # Connection logic here
PY
```

Create the starter configuration file:

```bash
cat > settings.ini <<'INI'
[database]
url = http://localhost:8080
user = admin
password = admin1234

[server]
mode = debug
port = 8080
INI
```

Check that the files were created correctly:

```bash
cat app.py
cat settings.ini
```

---

## Part 1: Basic `sed` Syntax

The general form is:

```bash
sed [OPTIONS] 'command' file
```

Examples:

```bash
sed 's/old/new/' file
sed -n '/pattern/p' file
sed '/pattern/d' file
```

The command is usually placed inside quotes because many `sed` expressions contain characters that the shell might otherwise interpret.

---

## Part 2: Substitution

The most common `sed` operation is substitution:

```bash
sed 's/pattern/replacement/' file
```

Read it as:

```text
s / thing to find / thing to replace it with /
```

Example:

```bash
sed 's/Debug:/Info:/' app.py
```

This replaces the **first** occurrence of `Debug:` on each matching line.

To replace **all occurrences on a line**, add `g` at the end:

```bash
sed 's/Debug:/Info:/g' app.py
```

The `g` means **global within each line**.

Important detail:

> Without `-i`, `sed` prints the changed version to the terminal but does not modify the original file.

This makes `sed` safe to test.

---

## Part 3: Preview First, Write Later

Run:

```bash
sed 's/Debug:/Info:/g' app.py
```

Now check the original file:

```bash
cat app.py
```

You should see that `app.py` did **not** change.

This is a useful safety rule:

> First preview the transformation. Only write to a file after the result looks correct.

There are three common workflows.

### Workflow A: Preview Only

```bash
sed 's/Debug:/Info:/g' app.py
```

This prints the modified result to the terminal.

### Workflow B: Save to a New File

```bash
sed 's/Debug:/Info:/g' app.py > app_info.py
```

This keeps `app.py` unchanged and writes the modified version to `app_info.py`.

### Workflow C: Edit In Place

```bash
sed -i 's/Debug:/Info:/g' app.py
```

This changes the original file directly.

A safer version creates a backup:

```bash
sed -i.bak 's/Debug:/Info:/g' app.py
```

After this command, you should have:

```text
app.py
app.py.bak
```

The backup file stores the original version.

---

## Part 4: Printing Only Matching Lines

Sometimes we do not want to modify text. We only want to find lines that match a pattern.

The command is:

```bash
sed -n '/pattern/p' file
```

Example:

```bash
sed -n '/TODO/p' app.py
```

Expected output:

```text
    # TODO: Implement feature X
    # TODO: Implement feature Y
```

Why does this work?

```bash
sed -n '/TODO/p' app.py
```

Breakdown:

| Piece | Meaning |
|---|---|
| `sed` | Run the stream editor |
| `-n` | Suppress automatic printing |
| `/TODO/` | Match lines containing `TODO` |
| `p` | Print matching lines |
| `app.py` | Input file |

Without `-n`, `sed` normally prints every line automatically. The `-n` option tells `sed`: “Do not print anything unless I explicitly ask you to.”

---

## Part 5: Deleting Matching Lines

To delete lines that match a pattern:

```bash
sed '/pattern/d' file
```

Example:

```bash
sed '/TODO/d' app.py
```

This prints a version of `app.py` with all `TODO` lines removed.

Again, the original file is unchanged unless you use `-i`.

To save the result to a new file:

```bash
sed '/TODO/d' app.py > app_no_todos.py
```

---

## Part 6: Replacing URLs and Choosing a Better Delimiter

The usual substitution syntax uses `/` as the delimiter:

```bash
sed 's/old/new/g' file
```

But URLs contain `/` characters:

```text
http://localhost:8080
http://production.database.com
```

If we use `/` as the delimiter, the command becomes hard to read because every URL slash must be escaped.

Messy version:

```bash
sed 's/http:\/\/localhost:8080/http:\/\/production.database.com/g' settings.ini
```

Cleaner version:

```bash
sed 's#http://localhost:8080#http://production.database.com#g' settings.ini
```

Here, `#` is used as the delimiter instead of `/`.

The structure is still the same:

```text
s # old text # new text # g
```

Now save the result to a new file:

```bash
sed 's#http://localhost:8080#http://production.database.com#g' settings.ini > settings_new.ini
```

Check the difference:

```bash
diff settings.ini settings_new.ini
```

Expected idea:

```text
url = http://localhost:8080
```

was changed to:

```text
url = http://production.database.com
```

---

## Part 7: Function Renaming

Suppose we want to rename the function:

```text
connect_database
```

to:

```text
establish_database_connection
```

A simple command is:

```bash
sed 's/connect_database/establish_database_connection/g' app.py
```

This replaces every occurrence of the text `connect_database`.

To save the result:

```bash
sed 's/connect_database/establish_database_connection/g' app.py > app_renamed.py
```

Check the result:

```bash
cat app_renamed.py
```

Expected output:

```python
def main():
    print("Debug: Starting application")
    # TODO: Implement feature X
    establish_database_connection()
    # TODO: Implement feature Y

def establish_database_connection():
    url = "http://localhost:8080"
    print("Debug: Connecting to database")
    # Connection logic here
```

### Important Warning: `sed` Is Not a Full Code Refactoring Tool

For this small file, the command works well. But in a large codebase, simple text replacement can be dangerous.

For example, if your file contained:

```python
connect_database_backup()
```

then a simple replacement would turn it into:

```python
establish_database_connection_backup()
```

That might not be what you wanted.

This is the difference:

| Tool | Strength | Weakness |
|---|---|---|
| `sed` | Fast text transformation | Does not understand Python syntax |
| IDE refactor tool | Understands code structure better | Less useful in shell pipelines |
| Manual editing | Full human judgment | Slow and error-prone for repetitive edits |

Use `sed` when the transformation is clearly textual. Be more careful when the transformation depends on programming-language meaning.

---

## Part 8: `sed` vs `grep` vs a Text Editor

These tools overlap, but they are not identical.

| Task | Good Tool |
|---|---|
| Find lines containing `TODO` | `grep` or `sed -n '/TODO/p'` |
| Replace text in a file stream | `sed` |
| Manually inspect and edit a few lines | Text editor |
| Apply the same transformation to many files | `sed`, sometimes with `find` |

A useful comparison:

```bash
grep 'TODO' app.py
sed -n '/TODO/p' app.py
```

Both can show matching lines. But `sed` can also transform text, delete lines, and write modified output.

---

## Part 9: Lab Exercises

Complete these exercises in your `sed_lab` folder.

### Exercise 1: Code Refactoring

Use `sed` to change all instances of:

```text
Debug:
```

to:

```text
Info:
```

in `app.py`.

First preview the result. Then save the result to a new file named `app_info.py`.

---

### Exercise 2: Configuration Management

Use `sed` to update `settings.ini` so that the database URL changes from:

```text
http://localhost:8080
```

to:

```text
http://production.database.com
```

Do **not** modify the original file. Save the output to:

```text
settings_new.ini
```

---

### Exercise 3: Code Analysis

Use `sed` to extract only the lines from `app.py` that contain:

```text
TODO
```

---

### Exercise 4: Function Renaming

Use `sed` to change the function name:

```text
connect_database
```

to:

```text
establish_database_connection
```

Make sure both the function definition and the function call are changed.

Save the result to:

```text
app_renamed.py
```

---

### Exercise 5: Remove TODO Lines

Create a new file called `app_clean.py` that contains the contents of `app.py` but removes all lines containing `TODO`.

---

### Exercise 6: Change Server Mode

Use `sed` to change this line in `settings.ini`:

```text
mode = debug
```

to:

```text
mode = production
```

Save the result to:

```text
settings_production.ini
```

---

### Exercise 7: Combine Two Ideas

Create a new file called `app_production.py` where:

1. `Debug:` becomes `Info:`
2. `connect_database` becomes `establish_database_connection`

Hint: `sed` can accept multiple expressions with `-e`:

```bash
sed -e 's/old/new/g' -e 's/another/replacement/g' file
```

---

## Part 10: Solution Key

### Solution 1: Code Refactoring

Preview:

```bash
sed 's/Debug:/Info:/g' app.py
```

Save to a new file:

```bash
sed 's/Debug:/Info:/g' app.py > app_info.py
```

---

### Solution 2: Configuration Management

```bash
sed 's#http://localhost:8080#http://production.database.com#g' settings.ini > settings_new.ini
```

The `#` delimiter makes the command easier to read because the pattern and replacement are URLs containing `/`.

---

### Solution 3: Code Analysis

```bash
sed -n '/TODO/p' app.py
```

The `-n` suppresses default output. The `p` prints only matching lines.

---

### Solution 4: Function Renaming

```bash
sed 's/connect_database/establish_database_connection/g' app.py > app_renamed.py
```

Check:

```bash
cat app_renamed.py
```

---

### Solution 5: Remove TODO Lines

```bash
sed '/TODO/d' app.py > app_clean.py
```

---

### Solution 6: Change Server Mode

```bash
sed 's/mode = debug/mode = production/g' settings.ini > settings_production.ini
```

---

### Solution 7: Combine Two Ideas

```bash
sed \
  -e 's/Debug:/Info:/g' \
  -e 's/connect_database/establish_database_connection/g' \
  app.py > app_production.py
```

---

## Part 11: How to Check Your Work

Use `cat` to inspect a generated file:

```bash
cat app_info.py
```

Use `diff` to compare the original and modified files:

```bash
diff app.py app_info.py
```

Use `grep` to confirm a pattern is gone:

```bash
grep 'Debug:' app_info.py
```

If nothing prints, then `Debug:` no longer appears in `app_info.py`.

Use `grep` to confirm the new pattern exists:

```bash
grep 'Info:' app_info.py
```

---

## Part 12: Common Mistakes

### Mistake 1: Expecting `sed` to Modify the File Automatically

This command does not change the original file:

```bash
sed 's/Debug:/Info:/g' app.py
```

It only prints the changed version.

To save the output:

```bash
sed 's/Debug:/Info:/g' app.py > app_info.py
```

To edit in place:

```bash
sed -i 's/Debug:/Info:/g' app.py
```

---

### Mistake 2: Forgetting `-n` When Printing Matches

This command prints every line, plus matching lines again:

```bash
sed '/TODO/p' app.py
```

This command prints only matching lines:

```bash
sed -n '/TODO/p' app.py
```

---

### Mistake 3: Fighting the `/` Delimiter with URLs

Hard-to-read version:

```bash
sed 's/http:\/\/localhost:8080/http:\/\/production.database.com/g' settings.ini
```

Cleaner version:

```bash
sed 's#http://localhost:8080#http://production.database.com#g' settings.ini
```

---

### Mistake 4: Using `sed` for Semantic Code Refactoring

`sed` sees text. It does not fully understand variables, functions, scopes, imports, or syntax trees.

For small controlled examples, `sed` is excellent. For a large software project, use `sed` carefully and verify the result with tests.

---

## Part 13: Mini Reference

| Goal | Command Pattern |
|---|---|
| Print matching lines | `sed -n '/pattern/p' file` |
| Delete matching lines | `sed '/pattern/d' file` |
| Replace first match per line | `sed 's/old/new/' file` |
| Replace all matches per line | `sed 's/old/new/g' file` |
| Save output to new file | `sed 's/old/new/g' file > new_file` |
| Edit original file | `sed -i 's/old/new/g' file` |
| Edit original file with backup | `sed -i.bak 's/old/new/g' file` |
| Use alternate delimiter | `sed 's#old/path#new/path#g' file` |
| Use multiple edits | `sed -e 's/a/b/g' -e 's/c/d/g' file` |

---

## Final Takeaway

`sed` is not just a command to memorize. It is a way of thinking about text as a stream:

1. Select the lines you care about.
2. Transform the text using a precise rule.
3. Preview before changing files.
4. Save the result only when the output is correct.

That pattern appears everywhere in Linux: logs, source code, configuration files, scripts, pipelines, and automation.
