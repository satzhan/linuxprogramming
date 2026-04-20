# Linux Text Processing Module: `cut` and `paste`

## Overview

This module teaches two foundational Linux text-processing commands:

- `cut` — extract selected parts of each input line
- `paste` — combine lines side by side

These commands are small, but they are powerful building blocks for shell work, CSV-style manipulation, data cleaning, quick reporting, and scripting.

---

## Learning Goals

By the end of this module, students should be able to:

1. Explain the line-by-line model used by text-processing commands.
2. Distinguish between extracting by **field** and extracting by **character position**.
3. Use `cut` with delimiters to select meaningful columns from text data.
4. Use `paste` to combine files horizontally.
5. Explain when `paste` is safe and when it is dangerous.
6. Use `cut`, `paste`, `grep`, `sort`, and pipes together in a simple workflow.
7. Verify whether their output is actually correct instead of assuming a one-liner is correct.

---

## Prerequisites

Students should already know:

- how to open a terminal
- how to navigate directories with `cd` and list files with `ls`
- how to view files with `cat`, `less`, or `head`
- basic shell redirection with `>`
- basic piping with `|`

---

## Big Idea

Think of a text file as a stack of lines.

Each line is one record.
Inside each line, the data may be split into smaller pieces:

- by a delimiter such as `,` or `:`
- by character positions

`cut` works **within one line**.
It does not compare different lines to each other.

`paste` works **across files or input streams**, combining corresponding lines side by side.
It assumes line 1 matches line 1, line 2 matches line 2, and so on.

That assumption is the most important danger in this topic.
If the rows are not aligned, `paste` still runs — but the result may be wrong.

---

## Part 1 — The `cut` Command

## What `cut` does

`cut` extracts selected parts of each line from a file or standard input.

It is most commonly used in two modes:

- **field mode**: split a line by a delimiter and choose fields
- **character mode**: choose characters by position

### Basic syntax

```bash
cut [options] file
```

Common options:

```bash
-f LIST          select fields
-d DELIM         set the field delimiter
-c LIST          select character positions
--complement     select everything except the requested part
```

---

## Mental model for `cut`

Suppose a line is:

```text
apple,red,5
```

With `-d,`, `cut` sees this as:

```text
[apple][red][5]
```

Then:

```bash
cut -d, -f2 data.txt
```

means:

- read one line
- split it using comma
- keep field 2
- print it
- repeat for every line

---

## Example dataset for `cut`

Create this file as `data.txt`:

```text
apple,red,5
banana,yellow,6
cherry,red,20
```

### Example: extract the second field

```bash
cut -d, -f2 data.txt
```

Output:

```text
red
yellow
red
```

### Example: extract fields 1 and 3

```bash
cut -d, -f1,3 data.txt
```

Output:

```text
apple,5
banana,6
cherry,20
```

### Example: extract characters instead of fields

```bash
cut -c1-3 file1.txt
```

If `file1.txt` contains:

```text
apple
banana
cherry
```

then the output is:

```text
app
ban
che
```

This is not field extraction. This is character slicing.

---

## Field mode vs character mode

These are easy to confuse.

### Field mode

```bash
cut -d, -f2 data.txt
```

- understands structure only because you told it the delimiter
- useful for CSV-like text when fields do not contain embedded commas

### Character mode

```bash
cut -c2-5 file1.txt
```

- ignores delimiters entirely
- useful for fixed-width text

A helpful analogy:

- field mode is like cutting a loaf at the natural slice marks
- character mode is like using a ruler and cutting by exact distance

---

## Useful field lists

```bash
cut -d, -f2 file.csv        # one field
cut -d, -f1,3 file.csv      # selected fields
cut -d, -f2-4 file.csv      # range of fields
cut -d, -f1,4-6 file.csv    # mixed list
```

---

## Using `--complement`

Sometimes it is easier to say what to remove.

```bash
cut -d, --complement -f3 data.txt
```

This means: keep everything except field 3.

Output:

```text
apple,red
banana,yellow
cherry,red
```

---

## Common `cut` mistakes

### 1. Forgetting the delimiter

```bash
cut -f2 data.txt
```

Without the correct delimiter, the shell may not split the line the way you expect.
For comma-separated data, explicitly use `-d,`.

### 2. Using `cut` on true CSV with quoted commas

`cut` is simple text processing. It is not a full CSV parser.
If a field contains commas inside quotes, `cut` can break the data incorrectly.

Example of problematic CSV:

```text
alice,"New York, NY",42
```

A simple `-d,` split will treat the city as two fields.

### 3. Confusing field number with character number

```bash
cut -f2 file
```

is not the same as:

```bash
cut -c2 file
```

### 4. Assuming the output delimiter stays identical in every context

With field extraction, the selected fields are printed separated by the input delimiter.
Students often forget this and expect spaces.

---

## Part 2 — The `paste` Command

## What `paste` does

`paste` merges lines horizontally.

If two files contain:

`file1.txt`

```text
apple
banana
cherry
```

`file2.txt`

```text
red
yellow
red
```

then:

```bash
paste file1.txt file2.txt
```

produces:

```text
apple   red
banana  yellow
cherry  red
```

By default, the separator is a tab.

---

## Basic syntax

```bash
paste [options] file1 file2 ...
```

Common options:

```bash
-d LIST     use custom delimiter(s)
-s          serial mode
```

---

## Mental model for `paste`

Imagine two vertical strips of paper.

`paste` reads the first line from each strip and puts them on one row.
Then it reads the second line from each strip and puts them on the next row.

So:

- line 1 joins with line 1
- line 2 joins with line 2
- line 3 joins with line 3

This is why row alignment matters.

---

## Examples with `paste`

### Example 1: default tab-delimited merge

```bash
paste file1.txt file2.txt
```

### Example 2: use comma instead of tab

```bash
paste -d, file1.txt file2.txt
```

Output:

```text
apple,red
banana,yellow
cherry,red
```

### Example 3: reshape one file into two columns

If `file3.txt` contains:

```text
1
2
3
4
5
6
```

then:

```bash
paste - - < file3.txt
```

Output:

```text
1       2
3       4
5       6
```

Why does this work?

The two `-` entries mean: read two columns from standard input.
So the command groups the input into pairs.

### Example 4: serial mode

```bash
paste -s -d, file1.txt
```

Output:

```text
apple,banana,cherry
```

This changes the job entirely.
Instead of pasting lines in parallel, `-s` turns one file into one long line.

---

## Common `paste` mistakes

### 1. Assuming matching rows without checking

This is the biggest mistake.

If the files are:

`user_emails.csv`

```text
alice,alice@example.com
bob,bob@example.com
```

`user_orders.csv`

```text
bob,ORD002
alice,ORD001
```

then:

```bash
paste -d, user_emails.csv user_orders.csv
```

runs successfully, but produces wrong pairings.

The command is not “smart.”
It does not join by username.
It joins by row number.

### 2. Forgetting the default separator is a tab

Students often expect commas but get tabs.
Use `-d,` when you want CSV-style output.

### 3. Treating `paste` like a database join

`paste` is not SQL.
It is not `join`.
It does not match keys.
It simply glues lines together.

---

## `cut` and `paste` together

These commands are often stronger together than alone.

### Example workflow

Suppose you want names from one file and colors from another:

```bash
cut -c1-6 file1.txt > names_part.txt
paste -d, names_part.txt file2.txt
```

This pipeline style is common in shell work:

- extract
- reshape
- combine
- filter
- save

---

## Relationship to other commands

These commands are often combined with:

- `grep` — filter lines by pattern
- `sort` — reorder lines
- `uniq` — collapse duplicates after sorting
- `wc` — count lines, words, bytes
- `head` / `tail` — inspect parts of a file

Example:

```bash
cut -d, -f4 books.csv | sort | uniq
```

This extracts one column, sorts it, and finds unique values.

---

## A subtle correction students should understand

A common pattern is:

```bash
grep "Software Engineering" books.csv | cut -d, -f1,2
```

This makes sense because:

1. `grep` keeps only matching rows
2. `cut` extracts the fields you want from those rows

But this command is wrong:

```bash
cut -d, -f1,2 | grep "Software Engineering" books.csv
```

Why is it wrong?

Because the pipe sends data from `cut` into `grep`, but that `grep` command is still told to read from `books.csv` directly. That breaks the pipeline idea.

A correct pipeline version would be:

```bash
cut -d, -f1,4 books.csv | grep "Software Engineering"
```

Even then, the earlier version is usually clearer because it filters full rows first.

---

## Inspection habits before and after processing

Students should get used to checking files before trusting output.

Useful commands:

```bash
head file.csv
wc -l file.csv
cat file.csv
```

A strong workflow is:

1. inspect input
2. run transformation
3. inspect output
4. verify row count or sample rows

This is the shell version of “measure twice, cut once.”

---

## Mini Demonstration Set

Create these example files.

### `data.txt`

```text
apple,red,5
banana,yellow,6
cherry,red,20
```

### `file1.txt`

```text
apple
banana
cherry
```

### `file2.txt`

```text
red
yellow
red
```

### `file3.txt`

```text
1
2
3
4
5
6
```

### Demo commands

```bash
cut -d, -f2 data.txt
cut -d, -f1,3 data.txt
paste file1.txt file2.txt
paste -d, file1.txt file2.txt
paste - - < file3.txt
paste -s -d, file1.txt
```

---

# Lab Section

## Lab Philosophy

These labs are not just about getting a file to appear.
They are about learning to reason about text structure, assumptions, and verification.

For every lab, students should answer:

1. What is one line in this file supposed to represent?
2. What makes one field different from another?
3. Am I selecting by delimiter or by position?
4. If I combine files, how do I know the rows really match?

---

## Lab 0 — Warm-Up with Tiny Files

### Goal

Use the small example files to understand the mechanics before touching larger CSV files.

### Input files

- `data.txt`
- `file1.txt`
- `file2.txt`
- `file3.txt`

### Tasks

1. Print only the color column from `data.txt`.
2. Print only the fruit and count columns from `data.txt`.
3. Merge `file1.txt` and `file2.txt` with the default delimiter.
4. Merge `file1.txt` and `file2.txt` using commas.
5. Turn `file3.txt` into two columns.
6. Turn `file1.txt` into one comma-separated line.

### Suggested commands

```bash
cut -d, -f2 data.txt
cut -d, -f1,3 data.txt
paste file1.txt file2.txt
paste -d, file1.txt file2.txt
paste - - < file3.txt
paste -s -d, file1.txt
```

### Deliverables

Show the commands used and the resulting output for each task.

---

## Lab 1 — Extract and Target Users by City

### Scenario

You want to send a promotional email to users who live in `Springfield`.

### Generator and input files

Run:

```bash
python3 order_generator.py
```

Expected files:

- `user_emails.csv` with `username,email`
- `user_orders.csv` with `username,order_id`
- `user_addresses.csv` with `username,street,city,zipcode`

### Core idea

You do not need every field.
You only need enough structure to answer the question.

### Step-by-step version

#### Step 1: extract usernames and emails

```bash
cut -d, -f1,2 user_emails.csv > temp_emails.csv
```

#### Step 2: extract city column

```bash
cut -d, -f3 user_addresses.csv > temp_city.csv
```

#### Step 3: combine them side by side

```bash
paste -d, temp_emails.csv temp_city.csv > user_email_and_city.csv
```

#### Step 4: keep only Springfield users

```bash
grep 'Springfield' user_email_and_city.csv | cut -d, -f1,2 > springfield_users.csv
```

#### Step 5: remove temporary files

```bash
rm temp_emails.csv temp_city.csv
```

### Why this works

- `cut` extracts just the needed columns
- `paste` aligns rows side by side
- `grep` filters matching rows
- final `cut` removes the city field because it is no longer needed

### Verification checklist

Before submitting, students should verify:

```bash
head user_emails.csv
head user_addresses.csv
head springfield_users.csv
wc -l springfield_users.csv
```

### Deliverable

A file named:

```text
springfield_users.csv
```

containing usernames and emails for users in Springfield.

### Reflection questions

1. Why did we not need `user_orders.csv` in this lab?
2. What assumption did `paste` make?
3. What would go wrong if `user_addresses.csv` were in a different order?

---

## Lab 2 — Build a Comprehensive User Info File

### Scenario

You need a file containing:

- username
- email
- order_id
- street
- city
- zipcode

### Step-by-step version

#### Step 1: merge emails and orders

```bash
paste -d, user_emails.csv user_orders.csv > temp_user_info.csv
```

#### Step 2: inspect for alignment

```bash
head temp_user_info.csv
```

Students should confirm that usernames from both source files line up correctly.

#### Step 3: add address data

```bash
paste -d, temp_user_info.csv user_addresses.csv > comprehensive_user_info.csv
```

#### Step 4: keep and reorder the needed fields

```bash
cut -d, -f1,2,4,6,7,8 comprehensive_user_info.csv > final_user_info.csv
```

#### Step 5: optional cleanup

```bash
rm temp_user_info.csv
```

### One-line version

```bash
paste -d, user_emails.csv user_orders.csv user_addresses.csv | cut -d, -f1,2,4,6,7,8 > final_user_info.csv
```

### Important warning

This one-liner is only correct if the rows already align across all files.
A fast command is not the same as a safe command.

### Verification checklist

```bash
head user_emails.csv
head user_orders.csv
head user_addresses.csv
head final_user_info.csv
wc -l final_user_info.csv
```

Also spot-check a few usernames manually.

### Deliverable

A file named:

```text
final_user_info.csv
```

with this field order:

```text
username,email,order_id,street,city,zipcode
```

### Reflection questions

1. Why do the chosen field numbers become `1,2,4,6,7,8` after multiple pastes?
2. What does `paste` preserve from the source files?
3. How would you detect a row mismatch quickly?

---

## Lab 3 — Detect Why `paste` Can Fail Silently

### Scenario

Real data is messy. A command can run and still produce incorrect results.
This lab makes that visible.

### Setup

Create two files:

`users_a.csv`

```text
alice,alice@example.com
bob,bob@example.com
carol,carol@example.com
```

`users_b.csv`

```text
bob,ORD002
alice,ORD001
carol,ORD003
```

### Task 1: paste them directly

```bash
paste -d, users_a.csv users_b.csv
```

### Task 2: explain what is wrong

Students should identify that the first row combines `alice` with `bob`'s order.

### Task 3: inspect both files with line numbers

```bash
nl -ba users_a.csv
nl -ba users_b.csv
```

### Task 4: repair by sorting both files by username first

```bash
sort users_a.csv > users_a_sorted.csv
sort users_b.csv > users_b_sorted.csv
paste -d, users_a_sorted.csv users_b_sorted.csv
```

### Why this lab matters

This is the heart of the topic.
`paste` can be perfectly syntactically correct and still logically wrong.

### Deliverables

Show:

- the incorrect pasted output
- a brief explanation of why it is incorrect
- the corrected workflow after sorting

---

## Lab 4 — Build a Reusable Pipeline

### Scenario

You want a reusable shell command that produces a simple report from a CSV-like file.

### Input

Use `data.txt`:

```text
apple,red,5
banana,yellow,6
cherry,red,20
```

### Tasks

1. Extract the color column.
2. Sort it.
3. Remove duplicates.
4. Save the result into `unique_colors.txt`.

### Solution pattern

```bash
cut -d, -f2 data.txt | sort | uniq > unique_colors.txt
```

### Extension

Create `fruit_and_color.txt` with:

```bash
cut -d, -f1,2 data.txt > fruit_and_color.txt
```

Then create a serial version of the fruit names only:

```bash
cut -d, -f1 data.txt | paste -s -d, > fruits_one_line.txt
```

### Deliverables

Submit:

- `unique_colors.txt`
- `fruit_and_color.txt`
- `fruits_one_line.txt`

and the commands used to generate them.

---

## Optional Challenge Lab — Character Mode vs Field Mode

### Goal

Prove to yourself that field-based extraction and character-based extraction are different ideas.

### Input file

Create `codes.txt`:

```text
A12-ENGINE
B07-DESIGN
C33-TEST
```

### Tasks

1. Extract the first three characters from each line.
2. Extract everything after the dash using delimiter-based logic.
3. Explain why these two tasks require different mental models.

### Example solutions

```bash
cut -c1-3 codes.txt
cut -d- -f2 codes.txt
```

### Deliverable

A short written explanation plus the commands and outputs.

---

# Common Student Questions

## “Why not just use one command for everything?”

Because shell tools are often designed as small parts.
One command selects, another filters, another combines.
The power comes from composition.

## “Why does `paste` not care that the usernames mismatch?”

Because it does not understand usernames.
It only understands line position.

## “Why do we verify with `head`?”

Because a file can exist and still be wrong.
A few sampled rows often reveal structural mistakes quickly.

## “When should I use `cut` instead of `awk`?”

Use `cut` when the job is simple and the structure is regular.
Use more advanced tools when parsing rules become more complicated.

## “Can `cut` parse all CSV files?”

No.
It works best on simple delimiter-separated text.
Quoted commas and more complex CSV structure require stronger tools.

---

# Teaching Notes / Instructor Notes

## What students usually misunderstand

1. They think `paste` matches rows by key instead of by line number.
2. They confuse fields with characters.
3. They trust output files too quickly.
4. They use a one-liner before they understand the intermediate files.
5. They forget that the default `paste` delimiter is a tab.

## A good teaching order

1. start with tiny files
2. show line-by-line logic
3. show delimiter-based field extraction
4. show horizontal merging
5. show one correct workflow
6. show one workflow that looks correct but is wrong
7. make students verify output

## Strong discussion prompt

Ask:

> Which is more dangerous: a command that crashes, or a command that runs successfully but gives the wrong answer?

For this module, the second is more dangerous.

---

# Quick Reference

## `cut`

```bash
cut -d, -f2 file.csv
cut -d, -f1,3 file.csv
cut -c1-5 file.txt
cut -d, --complement -f3 file.csv
```

## `paste`

```bash
paste file1.txt file2.txt
paste -d, file1.txt file2.txt
paste - - < file3.txt
paste -s -d, file1.txt
```

## Helpful support commands

```bash
head file
wc -l file
sort file
uniq file
grep pattern file
nl -ba file
```

---

# Summary

`cut` and `paste` are simple commands with a deep lesson behind them.

- `cut` extracts structure from each line
- `paste` combines corresponding lines across files
- both are useful, but both depend on understanding the structure of the data
- the most important practical habit is verification

Students who truly understand this module are not just running commands.
They are reasoning about records, fields, assumptions, and correctness.
