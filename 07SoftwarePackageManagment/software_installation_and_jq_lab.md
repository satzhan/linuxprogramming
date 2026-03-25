# Linux Software Installation Flow and `jq` Lab

## Overview

This handout combines two connected ideas:

1. the **general flow of installing software from source in Linux**
2. a **worked example using `jq`**, a command-line JSON processor

The goal is to show not only *which commands to run*, but also *why those commands appear in that order*. A useful way to think about the process is:

**Get source code → extract/archive handling → configure/build → install → test → use**

---

## Part 1: The Big Picture of Installing Software from Source

When software is distributed as source code instead of as a prebuilt package, you usually move through several stages.

### 1. Get the source code

This is the step where you download the raw source files from the internet. Open-source projects often publish source code through:

- official project websites
- GitHub or GitLab releases
- source archives such as `.tar.gz` or `.tar.bz2`

Common tools for downloading:

- `wget`
- `curl`

### Why this step matters

Your computer cannot run source code directly in most cases. First, you need to obtain the project files, usually from a trusted source.

### Example commands

Using `wget`:

```bash
wget https://example.com/project.tar.gz
```

Using `curl`:

```bash
curl -LO https://example.com/project.tar.gz
```

---

### 2. Handle the archive

Developers often bundle many source files into a single compressed archive, sometimes called a **tarball**.

Common archive formats include:

- `.tar`
- `.tar.gz`
- `.tar.bz2`

The `tar` command is commonly used to:

- bundle files together
- extract bundled files

### Why this step matters

A real software project may contain many source files, folders, scripts, and documentation. Packaging them into one archive makes download and distribution easier.

### Example: extracting a tarball

```bash
tar xzf project.tar.gz
cd project
```

After extraction, you usually enter the newly created source directory.

---

### 3. Configure the build

Many source-based projects include a configuration step before compilation.

A common command is:

```bash
./configure
```

### What `./configure` does

It checks your system for:

- available compilers
- required libraries
- supported features
- installation paths

Then it prepares build instructions that match your machine.

### Why this step matters

Different Linux systems may have different libraries, compiler versions, or install locations. The configuration step adapts the build process to the current environment.

---

### 4. Compile the source code

Compilation translates human-readable source code, often written in C or C++, into machine code that your processor can execute.

A common command is:

```bash
make
```

### What `make` does

`make` reads instructions from a `Makefile` and builds the project according to those rules.

This may involve:

- compiling multiple source files
- linking them together
- generating one or more executables or libraries

### Related tool: `gcc`

At a lower level, tools such as `gcc` compile source code directly.

Example:

```bash
gcc -Wall -o hello hello.c
```

This compiles `hello.c` into an executable named `hello`.

---

### 5. Install the program

After compilation, the next step is often installation:

```bash
sudo make install
```

### What installation means here

This usually copies files into standard system locations such as:

- `/usr/local/bin`
- `/usr/local/lib`
- `/usr/local/share`

### Why this step matters

Building creates the program. Installing places it somewhere your system can find and use it like a normal command.

---

### 6. Test the installation

After installation, verify that the program works.

Typical checks include:

- asking for the version
- running a small test command
- confirming the command is in your shell path

Example:

```bash
program_name --version
```

---

## The Common Build Sequence

For many classic open-source projects, the standard workflow looks like this:

```bash
./configure
make
sudo make install
```

Think of these three lines as:

- **configure**: inspect the system and prepare
- **make**: build the software
- **make install**: copy the finished result into system directories

---

## Important Notes and Caveats

### Dependencies

Many programs rely on external libraries or tools. These are called **dependencies**.

If dependencies are missing, configuration or compilation may fail.

Examples of common build requirements:

- compiler toolchains
- `make`
- autotools
- development headers
- required libraries

---

### Official sources matter

When downloading source code, prefer:

- official documentation
- official repositories
- official release pages

This reduces the risk of downloading outdated or unsafe files.

---

### Manual installation has trade-offs

Installing from source gives control, but it also has downsides:

- uninstalling may not be simple
- upgrades are more manual
- the package manager may not track the installation

Because of this, package managers such as `apt`, `yum`, or `zypper` are often easier for routine software management.

---

## Part 2: `jq` as a Concrete Example

Now let us apply the general installation flow to a real tool: **`jq`**.

`jq` is a command-line utility for working with JSON.

It is especially useful for:

- filtering API responses
- formatting JSON for readability
- extracting specific values from nested data
- scripting around configuration files and web services

Project page:

```text
https://jqlang.github.io/jq/
```

---

## Lab Objective

By the end of this lab, you should be able to:

- download `jq` source code
- extract and build it
- install it
- verify the installation
- use it to query JSON data

---

## Prerequisites

You should have:

- basic Linux command-line familiarity
- basic understanding of JSON structure
- access to a Linux system with common build tools installed

Typical needed tools include:

- `wget` or `curl`
- `tar`
- build tools such as `make`, `gcc`, and related utilities

---

## Lab Flow

The lab follows this sequence:

1. download the `jq` source code
2. extract the archive
3. configure and build the project
4. install `jq`
5. test the installation
6. use `jq` on sample JSON data

---

## Step 1: Download the `jq` Source Code

### Using `wget`

```bash
wget https://github.com/stedolan/jq/releases/download/jq-1.6/jq-1.6.tar.gz
```

### Using `curl`

```bash
curl -LO https://github.com/stedolan/jq/releases/download/jq-1.6/jq-1.6.tar.gz
```

### What this does

Both commands download the `jq` 1.6 source archive. The difference is mainly the tool and syntax.

- `wget` is often used as a straightforward downloader
- `curl` is broader and often used in APIs and scripted HTTP requests

---

## Step 2: Extract the Source Archive

```bash
tar xzf jq-1.6.tar.gz
cd jq-1.6
```

### What this does

- `tar xzf` extracts the gzip-compressed tar archive
- `cd jq-1.6` moves into the extracted source directory

At this point, you are inside the project source tree and ready to prepare the build.

---

## Step 3: Build and Install `jq`

```bash
autoreconf -i
./configure
make
make install
```

### What each command does

#### `autoreconf -i`
Generates or refreshes the configuration scripts needed for the build system.

#### `./configure`
Checks your environment and prepares the build configuration.

#### `make`
Compiles the program.

#### `make install`
Installs the built program onto the system.

### Important note

Some systems may require additional dependencies before these commands succeed.

---

## Step 4: Test the Installation

```bash
jq --version
```

### Expected output

```text
jq-1.6
```

### Why this matters

This confirms that:

- the installation completed
- the command is available in your environment
- the installed version is the one you expected

---

## Step 5: Use `jq` on JSON Data

### Create sample JSON

```bash
echo '{"users": [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]}' > users.json
```

This creates a file named `users.json` containing a small JSON object with a `users` array.

---

### Extract the name of the first user

```bash
jq '.users[0].name' users.json
```

### Expected output

```text
"John"
```

### How to read the filter

- `.users` means “go to the `users` field”
- `[0]` means “take the first element of that array”
- `.name` means “read the `name` field”

So the filter walks through the JSON structure step by step.

---

### Filter users younger than 28 and print their names

```bash
jq '.users[] | select(.age < 28) | .name' users.json
```

### Expected output

```text
"Jane"
```

### How to read the filter

- `.users[]` means “look at each user in the array one by one”
- `select(.age < 28)` keeps only users whose age is less than 28
- `.name` prints the name field of the remaining entries

This shows why `jq` is powerful: it can both filter and transform structured data in one command.

---

## Why `jq` Is a Useful Example

This lab is valuable because it connects two skills:

1. **system-level skill**: downloading, extracting, building, and installing software
2. **data-level skill**: working with JSON from the command line

That combination appears often in real technical workflows such as:

- DevOps
- software development
- data engineering
- scripting around APIs
- handling configuration files

---

## One-Page Mental Model

When installing software from source, think in this order:

### First: get the files
Use `wget` or `curl` to download the source archive.

### Second: unpack the archive
Use `tar` to extract the contents.

### Third: prepare the build
Run configuration tools such as `autoreconf` and `./configure`.

### Fourth: compile the code
Use `make`.

### Fifth: install the result
Use `make install`.

### Sixth: verify and use it
Run a version check and test a real command.

---

## Quick Reference

### Download with `wget`

```bash
wget URL
```

### Download with `curl`

```bash
curl -LO URL
```

### Extract a `.tar.gz` archive

```bash
tar xzf file.tar.gz
```

### Standard build sequence

```bash
./configure
make
sudo make install
```

### Check installed version

```bash
program --version
```

### Example `jq` queries

```bash
jq '.users[0].name' users.json
jq '.users[] | select(.age < 28) | .name' users.json
```

---

## Final Summary

The larger lesson is not only about `jq`. It is about recognizing a repeatable Linux workflow:

- download source code
- unpack it
- build it
- install it
- confirm it works
- use the tool for a real task

`jq` is a strong example because it turns that workflow into something immediately practical: querying and transforming JSON data from the command line.
