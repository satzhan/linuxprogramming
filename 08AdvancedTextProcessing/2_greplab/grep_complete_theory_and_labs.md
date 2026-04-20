# Grep: Theory, Patterns, and Hands-On Labs

## Table of Contents
1. [What `grep` Is and Why It Matters](#what-grep-is-and-why-it-matters)
2. [How `grep` Thinks](#how-grep-thinks)
3. [Basic Command Structure](#basic-command-structure)
4. [Core Options You Will Use Often](#core-options-you-will-use-often)
5. [Regular Expression Foundations](#regular-expression-foundations)
6. [Basic vs Extended Regular Expressions](#basic-vs-extended-regular-expressions)
7. [Useful Development Workflows](#useful-development-workflows)
8. [Lab Environment and Files](#lab-environment-and-files)
9. [Lab 1: Find Print Statements in Python Files](#lab-1-find-print-statements-in-python-files)
10. [Lab 2: Identify Error Logs](#lab-2-identify-error-logs)
11. [Lab 3: Find TODO Comments](#lab-3-find-todo-comments)
12. [Lab 4: Locate `dbConnection` With Line Numbers](#lab-4-locate-dbconnection-with-line-numbers)
13. [Lab 5: Extract URLs From a Log File](#lab-5-extract-urls-from-a-log-file)
14. [Lab 6: Match Function Definitions](#lab-6-match-function-definitions)
15. [Lab 7: Use Inverted Matches to Remove Noise](#lab-7-use-inverted-matches-to-remove-noise)
16. [Lab 8: Count Matches Instead of Printing Them](#lab-8-count-matches-instead-of-printing-them)
17. [Lab 9: Build Safer Recursive Searches](#lab-9-build-safer-recursive-searches)
18. [Challenge Practice](#challenge-practice)
19. [Troubleshooting and Common Mistakes](#troubleshooting-and-common-mistakes)
20. [Quick Reference Sheet](#quick-reference-sheet)
21. [Summary](#summary)

---

## What `grep` Is and Why It Matters

`grep` is a command-line tool for searching text.

It scans files or input streams and returns lines that match a pattern. That pattern may be a simple word, a phrase, or a regular expression. In software work, `grep` is one of the fastest ways to answer questions such as:

- Where is this variable used?
- Which log lines contain errors?
- Which files still contain TODO comments?
- Which configuration lines begin with a certain prefix?
- Which lines contain URLs, IP addresses, or function names?

A useful way to think about `grep` is this:

- **Input**: one file, many files, or piped text
- **Pattern**: what to search for
- **Output**: matching lines, file names, counts, or only the matched text

`grep` is small, but it becomes powerful because text appears everywhere in computing: source code, logs, config files, shell output, CSV files, and plain-text notes.

---

## How `grep` Thinks

By default, `grep` works **line by line**.

That idea explains many beginner surprises.

For example, suppose a function definition is on one line and its `print(...)` call is on the next line. A pattern such as:

```bash
grep 'def.*print' module_0.py
```

usually does **not** match, because `grep` is not combining those two lines into one unit. It looks at one line, checks whether the pattern matches that line, then moves to the next line.

So if the real goal is “find functions that print,” the practical starting point is usually:

- search for `print(` lines,
- or search for function definitions separately,
- or inspect a few lines of context around a match.

This is one of the most important mental models in the chapter.

---

## Basic Command Structure

The usual shape is:

```bash
grep [options] 'pattern' file
```

Examples:

```bash
grep 'ERROR' app.log
grep -n 'TODO' module_0.py
grep -R --include='*.py' 'dbConnection' .
```

Pieces:

- `grep`: the program
- `[options]`: switches such as `-n`, `-i`, `-r`, or `-E`
- `'pattern'`: the text or regex to search for
- `file`: the file or directory to search

Single quotes are usually the safest habit in the shell because they prevent the shell from interpreting special characters before `grep` sees them.

---

## Core Options You Will Use Often

### `-n` — show line numbers

```bash
grep -n 'ERROR' app.log
```

Useful when the location of the match matters.

### `-i` — ignore case

```bash
grep -i 'error' app.log
```

Matches `error`, `Error`, `ERROR`, and other case variations.

### `-v` — invert the match

```bash
grep -v 'INFO' app.log
```

Returns lines that **do not** match the pattern.

### `-r` or `-R` — recursive search

```bash
grep -R 'TODO' .
```

Searches through directories and subdirectories.

### `--include='pattern'` — limit which files are searched

```bash
grep -R --include='*.py' 'TODO' .
```

Very useful in mixed projects, because it avoids matching unrelated file types.

### `-E` — use extended regular expressions

```bash
grep -E 'ERROR|WARNING' app.log
```

Needed for operators such as `+`, `?`, `|`, and grouping parentheses without backslashes.

### `-o` — print only the matched part

```bash
grep -Eo 'https?://[^ ]+' app.log
```

Without `-o`, the whole line is printed. With `-o`, only the substring that matches the pattern is printed.

### `-c` — count matches by line

```bash
grep -c '\[ERROR\]' app.log
```

Useful when the number of matches matters more than the lines themselves.

### `-w` — whole-word match

```bash
grep -w 'print' file.txt
```

Helps avoid partial matches inside larger words.

### `-H` and `-h` — force or hide file names

These matter most when searching multiple files.

---

## Regular Expression Foundations

A regular expression is a pattern language for text.

It is easiest to learn by seeing what each piece does.

### `.` dot
Matches any single character except a newline.

```bash
grep 'function.' module_0.py
```

This matches `function_0` because `_` is a single character after `function`.

### `*` star
Matches zero or more of the **preceding** thing.

```bash
grep 'a*' file.txt
```

This means “zero or more `a` characters,” not “anything.”

A common useful form is:

```bash
grep '.*pass' module_0.py
```

Here `.*` means “any number of any characters,” so this matches lines ending with or containing `pass`.

### `^` caret
Anchors the match at the **start** of a line.

```bash
grep '^import' lab_setup.py
```

Matches lines that begin with `import`.

### `$` dollar sign
Anchors the match at the **end** of a line.

```bash
grep ':$' module_0.py
```

Matches lines that end with a colon.

### `[]` character class
Matches one character from a set or range.

```bash
grep -E '[0-9]' module_0.py
grep -E '[A-Za-z_]+' module_0.py
```

Examples:

- `[aeiou]` any one vowel
- `[0-9]` any one digit
- `[A-Z]` any uppercase letter
- `[A-Za-z]` any letter
- `[^0-9]` any non-digit

### `\` backslash
Escapes a metacharacter when it should be treated literally.

```bash
grep '\[ERROR\]' app.log
```

The brackets are escaped because `[ERROR]` would otherwise be treated as a character class in regex.

---

## Basic vs Extended Regular Expressions

`grep` supports two main styles.

### Basic Regular Expressions (BRE)
This is the default form for plain `grep`.

In BRE, some characters need extra escaping if they are used as operators.

### Extended Regular Expressions (ERE)
Use `grep -E`.

ERE makes patterns more readable for many practical searches.

#### Grouping with parentheses

```bash
grep -E '(ERROR|WARNING)' app.log
```

#### Alternation with `|`

```bash
grep -E 'ERROR|WARNING' app.log
```

Matches either pattern.

#### One or more with `+`

```bash
grep -E 'function_[0-9]+' module_0.py
```

Matches names such as `function_0`, `function_12`, and so on.

#### Zero or one with `?`

```bash
grep -E 'https?' app.log
```

Matches `http` or `https`.

This is a common real-world use of `?`: the `s` is optional.

### A practical note about `egrep`

Older material may use `egrep`. Modern usage usually prefers:

```bash
grep -E
```

because it is clearer and more consistent.

---

## Useful Development Workflows

### Search code recursively, but only in Python files

```bash
grep -R -n --include='*.py' 'TODO' .
```

### Search logs for errors with line numbers

```bash
grep -n '\[ERROR\]' app.log
```

### Find only the extracted URLs, not the whole line

```bash
grep -Eo 'https?://[^ ]+' app.log
```

### Exclude noisy lines

```bash
grep -v '\[INFO\]' app.log
```

### Count how many error lines exist

```bash
grep -c '\[ERROR\]' app.log
```

### Search for whole identifiers rather than partial fragments

```bash
grep -Rw 'dbConnection' .
```

### Pipe output from another command into `grep`

```bash
ps aux | grep python
```

This is a common pattern: another command produces text, and `grep` filters it.

---

## Lab Environment and Files

The practice files for this chapter are:

- `module_0.py` through `module_4.py`
- `app.log`
- `lab_setup.py`

The `module_*.py` files simulate a small codebase. The log file simulates application output. The generator script shows how such files can be produced.

### Recommended working directory

```bash
cd /path/to/the/lab/files
ls
```

A file list similar to the following should appear:

```text
app.log
lab_setup.py
module_0.py
module_1.py
module_2.py
module_3.py
module_4.py
```

### Optional: regenerate sample files

If a fresh copy of the files is needed, a small generator script may be used. A clean version is shown below:

```python
import random

for i in range(5):
    with open(f"module_{i}.py", "w") as f:
        f.write(f"def function_{i}():\n")
        if i % 2 == 0:
            f.write("    print('This is a print statement')\n")
        else:
            f.write("    pass\n")
        f.write("\n")
        f.write("# TODO: Check this function later\n")
        f.write("dbConnection = 'Some connection string here'\n")
        f.write(f"def another_function_{i}():\n")
        f.write("    pass\n")

log_levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
urls = [
    "http://example.com/resource1",
    "https://secure-example.com/resource2",
    "http://another-example.com/page",
]

with open("app.log", "w") as f:
    for _ in range(20):
        level = random.choice(log_levels)
        if level == "ERROR":
            f.write(f"[ERROR] There was an error on module_{random.randint(0, 4)}.py\n")
        elif level == "DEBUG":
            f.write(f"[DEBUG] Accessing {random.choice(urls)}\n")
        else:
            f.write(f"[{level}] This is a log statement\n")
```

The labs below assume the current files already exist.

---

## Lab 1: Find Print Statements in Python Files

### Goal
Find Python files in the sample codebase that contain console printing.

### Why this matters
Searching for `print(...)` is useful when cleaning debugging output or tracing quick experiments left in code.

### Command

```bash
grep -R -n --include='module_*.py' 'print(' .
```

### What this command does

- `-R`: searches recursively
- `-n`: shows line numbers
- `--include='module_*.py'`: searches only the module files
- `'print('`: finds Python print calls
- `.`: starts searching from the current directory

### Expected result with the provided sample files

```text
./module_0.py:2:    print('This is a print statement')
./module_2.py:2:    print('This is a print statement')
./module_4.py:2:    print('This is a print statement')
```

### Discussion
A pattern such as `def.*print` is tempting, but it usually fails here because the function definition and the print statement are on different lines.

### Try one variation
Show one line of context before each match:

```bash
grep -R -n -B 1 --include='module_*.py' 'print(' .
```

Now the function definition line becomes visible above the `print(...)` line.

---

## Lab 2: Identify Error Logs

### Goal
Find all error entries in the application log.

### Command

```bash
grep -n '\[ERROR\]' app.log
```

### Why the brackets are escaped
Without escaping, `[ERROR]` is interpreted as a character class in regex. Escaping makes the brackets literal.

### Expected result with the provided `app.log`

```text
3:[ERROR] There was an error on module_1.py
7:[ERROR] There was an error on module_1.py
14:[ERROR] There was an error on module_2.py
15:[ERROR] There was an error on module_3.py
17:[ERROR] There was an error on module_1.py
19:[ERROR] There was an error on module_2.py
```

### Variation
Ignore case if the log style is inconsistent:

```bash
grep -ni 'error' app.log
```

---

## Lab 3: Find TODO Comments

### Goal
Locate unfinished or deferred work in the sample codebase.

### Command

```bash
grep -R -n --include='module_*.py' 'TODO' .
```

### Expected result

```text
./module_0.py:4:# TODO: Check this function later
./module_1.py:3:# TODO: Check this function later
./module_2.py:4:# TODO: Check this function later
./module_3.py:3:# TODO: Check this function later
./module_4.py:4:# TODO: Check this function later
```

### Variation
Search all Python files, including the generator script:

```bash
grep -R -n --include='*.py' 'TODO' .
```

That broader search also finds the line in `lab_setup.py` that writes the TODO comment into the generated files.

---

## Lab 4: Locate `dbConnection` With Line Numbers

### Goal
Find where the variable `dbConnection` appears.

### Command

```bash
grep -R -n --include='module_*.py' 'dbConnection' .
```

### Expected result

```text
./module_0.py:5:dbConnection = 'Some connection string here'
./module_1.py:4:dbConnection = 'Some connection string here'
./module_2.py:5:dbConnection = 'Some connection string here'
./module_3.py:4:dbConnection = 'Some connection string here'
./module_4.py:5:dbConnection = 'Some connection string here'
```

### Variation
Use a whole-word match:

```bash
grep -R -n -w --include='module_*.py' 'dbConnection' .
```

Whole-word matching becomes more useful when identifiers appear as parts of larger strings.

---

## Lab 5: Extract URLs From a Log File

### Goal
Print only the URLs appearing in the log.

### Command

```bash
grep -Eo 'https?://[^ ]+' app.log
```

### Pattern breakdown

- `http` matches the fixed prefix
- `s?` makes the `s` optional, so both `http` and `https` match
- `://` matches the literal separator
- `[^ ]+` means one or more non-space characters

### Expected result with the provided `app.log`

```text
http://example.com/resource1
```

### Important note
The generator can produce several different URLs, but the current `app.log` contains only one URL line. So the correct output for the current file is a single URL.

### Variation
Show the entire line instead of only the URL:

```bash
grep -E 'https?://' app.log
```

---

## Lab 6: Match Function Definitions

### Goal
Find function definitions in the module files.

### Command

```bash
grep -R -n -E --include='module_*.py' '^def [a-zA-Z_][a-zA-Z0-9_]*\(\):' .
```

### Pattern explanation

- `^def ` line must start with `def `
- `[a-zA-Z_]` first character of the function name
- `[a-zA-Z0-9_]*` remaining characters of the name
- `\(\):` literal `():`

### Expected result

```text
./module_0.py:1:def function_0():
./module_0.py:6:def another_function_0():
./module_1.py:1:def function_1():
./module_1.py:5:def another_function_1():
./module_2.py:1:def function_2():
./module_2.py:6:def another_function_2():
./module_3.py:1:def function_3():
./module_3.py:5:def another_function_3():
./module_4.py:1:def function_4():
./module_4.py:6:def another_function_4():
```

### Discussion
This is a good example of when `grep -E` helps. The regex is easier to read than an over-escaped basic regex.

---

## Lab 7: Use Inverted Matches to Remove Noise

### Goal
View log lines that are not simple informational messages.

### Command

```bash
grep -v '^\[INFO\]' app.log
```

### What it returns
All lines except those beginning with `[INFO]`.

### Why this matters
In real logs, the useful lines are often buried under routine status lines. Inversion is a quick first filter.

### Variation
Show only warnings and errors with one command:

```bash
grep -E '^\[(WARNING|ERROR)\]' app.log
```

---

## Lab 8: Count Matches Instead of Printing Them

### Goal
Count how many error lines exist in the log.

### Command

```bash
grep -c '\[ERROR\]' app.log
```

### Expected result for the provided log

```text
6
```

### Variation
Count TODO comments in the module files:

```bash
grep -R -c --include='module_*.py' 'TODO' .
```

This prints a count for each file.

---

## Lab 9: Build Safer Recursive Searches

Recursive search is powerful, but it can easily become too broad.

### Less precise version

```bash
grep -R 'TODO' .
```

This searches everything under the current directory.

### Safer version

```bash
grep -R -n --include='*.py' 'TODO' .
```

This is usually better because:

- it limits the search to Python files,
- it includes line numbers,
- and it avoids irrelevant matches in logs or unrelated files.

### Even narrower version for this lab set

```bash
grep -R -n --include='module_*.py' 'TODO' .
```

This version matches the specific exercise files and avoids mixing generator logic with generated output.

### Key idea
Recursive search is like using a net. The wider the net, the more it catches, including noise. File filters make the search more deliberate.

---

## Challenge Practice

These exercises extend the core labs.

### 1. Find warnings and errors only

```bash
grep -E '^\[(WARNING|ERROR)\]' app.log
```

### 2. Extract the module names mentioned in error lines

```bash
grep '\[ERROR\]' app.log | grep -Eo 'module_[0-9]+\.py'
```

### 3. Count how many times each module appears in errors

```bash
grep '\[ERROR\]' app.log | grep -Eo 'module_[0-9]+\.py' | sort | uniq -c
```

### 4. Find every line that starts with `def`

```bash
grep -R -n --include='module_*.py' '^def ' .
```

### 5. Find lines that do not contain `print`

```bash
grep -R -n -v --include='module_*.py' 'print' .
```

This prints many lines, so it is more useful as a demonstration of inversion than as a final answer.

### 6. Find all blank lines in the module files

```bash
grep -R -n --include='module_*.py' '^$' .
```

### 7. Find lines that end with a colon

```bash
grep -R -n --include='module_*.py' ':$' .
```

This can help locate Python statements such as function definitions.

---

## Troubleshooting and Common Mistakes

### 1. “Why didn’t `def.*print` find the function that prints?”
Because `grep` usually searches one line at a time. The `def` and `print(...)` are on different lines.

### 2. “Why escape `[ERROR]`?”
Because brackets have regex meaning. Without escaping, `[ERROR]` means “match one character that is E, R, or O,” which is not the same thing as the literal text `[ERROR]`.

### 3. “Why did recursive search return too much?”
Because the search included every file under the directory. Add `--include='*.py'` or a narrower file pattern.

### 4. “Why use single quotes?”
Because the shell may interpret special characters before `grep` receives them. Single quotes usually preserve the pattern exactly.

### 5. “Why did `grep -r "pattern" *.py` behave strangely?”
Because `*.py` is expanded by the shell into file names before `grep` runs, and recursive search is designed primarily for directories. A safer recursive form is:

```bash
grep -R --include='*.py' 'pattern' .
```

### 6. “Why didn’t `grep '\# TODO:'` matter?”
Because `#` is not special in a basic grep regex the way `[` or `.` is. Escaping it is unnecessary in this case. The simpler and clearer command is:

```bash
grep 'TODO' file.py
```

### 7. “Why does `grep -E 'DEBUG?'` match `DEBU` too?”
Because `?` makes the preceding character optional. So `DEBUG?` means `DEBU` followed by an optional `G`.

That is often not what is intended. For URLs, `https?` is sensible because `http` and `https` are both valid. For log levels, `DEBUG?` is usually not the right pattern.

---

## Quick Reference Sheet

### Search for a literal word

```bash
grep 'TODO' module_0.py
```

### Search recursively in Python files

```bash
grep -R --include='*.py' 'dbConnection' .
```

### Show line numbers

```bash
grep -n 'ERROR' app.log
```

### Ignore case

```bash
grep -i 'error' app.log
```

### Invert the match

```bash
grep -v '^\[INFO\]' app.log
```

### Use extended regex

```bash
grep -E 'ERROR|WARNING' app.log
```

### Print only the matching part

```bash
grep -Eo 'https?://[^ ]+' app.log
```

### Count matching lines

```bash
grep -c '\[ERROR\]' app.log
```

### Anchor at the start of a line

```bash
grep '^def ' module_0.py
```

### Anchor at the end of a line

```bash
grep ':$' module_0.py
```

### Match any digit

```bash
grep -E '[0-9]' module_0.py
```

### Match a Python-style function name after `def`

```bash
grep -E '^def [a-zA-Z_][a-zA-Z0-9_]*\(\):' module_0.py
```

---

## Summary

`grep` is one of the most practical tools for working with text in software development.

The central ideas from this chapter are:

- `grep` searches text by pattern.
- By default, it matches one line at a time.
- Recursive search becomes much better when combined with file filters.
- Line numbers, inversion, extraction, and counts are often more useful than plain matching.
- Regular expressions turn simple searches into flexible text queries.
- Good `grep` usage is less about memorizing every option and more about building the right search habit for the question at hand.

Once these ideas are comfortable, `grep` stops feeling like a command to memorize and starts feeling like a text microscope: point it at a codebase or log file, adjust the focus with options and regex, and reveal exactly the lines that matter.
