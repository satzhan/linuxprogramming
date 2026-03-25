# Linux Tools and Archiving Notes

## Overview

These notes organize several common Linux command-line tools into a logical flow. The main idea is this:

- **`wget` and `curl`** help you download or transfer data.
- **`tar` and `zip`** help you package files together, and sometimes compress them.
- **`gcc`** helps you compile source code into an executable program.

Together, these tools form a practical workflow in Linux: you may **download source code**, **extract an archive**, and then **compile the program**.

---

## 1. `wget`

### What it is

`wget` is a non-interactive downloader for Linux. It retrieves files from the internet using protocols such as:

- HTTP
- HTTPS
- FTP

It is commonly used when you want to download files directly from the command line.

### Basic syntax

```bash
wget [options] [URL]
```

### Common options

- `-c` — continue a partially downloaded file
- `-O [filename]` — save the download using a custom filename

### Example: download a source archive

```bash
wget https://www.nano-editor.org/dist/v5/nano-5.0.tar.xz
```

This downloads the Nano text editor source code archive into your current directory.

### When `wget` is especially useful

`wget` is often preferred when the main goal is simply:

- downloading files
- resuming interrupted downloads
- downloading multiple files from a list
- doing straightforward, scriptable file retrieval

---

## 2. `curl`

### What it is

`curl` is a command-line tool used to transfer data to or from a server. It supports many protocols and is more flexible than `wget` for general network communication.

It is commonly used not only for downloading files, but also for:

- sending headers
- making API requests
- testing web endpoints
- acting like a lightweight REST client

### Basic syntax

```bash
curl [options] [URL]
```

### Common options

- `-o [filename]` — save output to a file with a chosen name
- `-O` — save output using the remote file’s original name
- `-u [user:password]` — authenticate using credentials
- `-H "Header: value"` — send a custom header
- `-X METHOD` — specify an HTTP method such as `GET` or `POST`

### Example: save a webpage to a file

```bash
curl -o google.html http://www.google.com
```

This fetches the HTML from Google’s homepage and saves it into a file named `google.html`.

If you open that file in a text editor, you will see the raw HTML source that a browser uses to render the page.

### A practical caution

If you use tools like `curl` to access websites programmatically, it is important to respect legal and ethical boundaries. Websites may publish access rules in `robots.txt`, and some services restrict automated access.

---

## 3. `tar`

### What it is

`tar` is used to create, maintain, and extract archives in the tar format.

A tar archive usually **bundles files together**. Compression may be added separately, such as with gzip or bzip2.

### Basic syntax

```bash
tar [options] [archive-file] [files or directories]
```

### Common options

- `-c` — create an archive
- `-x` — extract an archive
- `-v` — verbose mode, showing progress in the terminal
- `-f` — specify the archive filename

### Example: create and extract a tar archive

```bash
mkdir example_dir
echo "This is a test file" > example_dir/test.txt
tar -cvf example_tarball.tar example_dir
mkdir extract_here
tar -xvf example_tarball.tar -C extract_here
```

This example:

1. creates a directory
2. creates a test file inside it
3. archives that directory into a `.tar` file
4. extracts it into another location

### Why `tar` matters on Linux

One major strength of `tar` is that it preserves important Unix metadata such as:

- file permissions
- ownership
- timestamps
- read-only status (if set through permissions)

That is one reason `tar` is widely used for:

- backups
- software source distribution
- Linux/Unix system packaging

---

## 4. `gcc`

### What it is

`gcc` is a compiler commonly used for C and C++ programs. It can compile source files and link them into an executable.

### Basic syntax

```bash
gcc [options] [source files] [object files] [-Ldir] -llibname [-o outfile]
```

### Common options

- `-o [filename]` — name of the output executable
- `-Wall` — enable common warning messages

### Example: compile and run a simple C program

```bash
echo '#include<stdio.h>\n int main(){ printf("Hello, World!\\n"); return 0; }' > hello.c
gcc -Wall -o hello hello.c
./hello
```

This creates a C source file, compiles it, and runs the resulting executable.

---

## 5. `tar` vs `zip`

Both `tar` and `zip` are used to package files, but they are not identical.

### Main difference

- **`tar`** is designed to archive files and preserve Unix metadata very well.
- **`zip`** is often more convenient for cross-platform sharing, especially between Linux, Windows, and macOS.

### Metadata preservation

`tar` is generally better at preserving:

- permissions
- ownership
- timestamps
- other Unix-style metadata

When files are extracted from a tar archive, they typically retain the permissions they had when they were archived.

`zip`, by contrast, does not preserve file metadata as comprehensively by default. It may store some basic permission information, but not with the same Unix-focused completeness as `tar`.

### Practical interpretation

Use **`tar`** when:

- you care about Linux file permissions
- you are making backups
- you are distributing source code or software on Unix-like systems

Use **`zip`** when:

- you want broad compatibility
- you are sharing files across different operating systems
- exact Linux metadata preservation is not the top priority

---

## 6. Side-by-side: archiving with `tar` and `zip`

### Create an archive

#### `tar`

```bash
tar -cvf archive_name.tar /path/to/directory_or_file
```

Explanation:

- `c` creates an archive
- `v` shows verbose output
- `f` lets you specify the archive filename

#### `zip`

```bash
zip -r archive_name.zip /path/to/directory_or_file
```

Explanation:

- `-r` recursively includes files inside directories

---

## 7. Archive and compress files

### `tar` with gzip compression

Creates a `.tar.gz` archive:

```bash
tar -czvf archive_name.tar.gz /path/to/directory_or_file
```

Explanation:

- `z` applies gzip compression

### `tar` with bzip2 compression

Creates a `.tar.bz2` archive:

```bash
tar -cjvf archive_name.tar.bz2 /path/to/directory_or_file
```

Explanation:

- `j` applies bzip2 compression

### `zip`

Compression is already built into zip:

```bash
zip -r archive_name.zip /path/to/directory_or_file
```

---

## 8. Extract files

### `tar`

```bash
tar -xvf archive_name.tar -C /path/to/destination_directory
```

Explanation:

- `x` extracts the archive
- `C` specifies where to extract it

### `zip`

```bash
unzip archive_name.zip -d /path/to/destination_directory
```

Explanation:

- `-d` specifies the destination directory

---

## 9. `wget` vs `curl`

Both `wget` and `curl` can download files from the internet, but they have different strengths.

### A simple comparison

- **`wget`** is usually more download-focused.
- **`curl`** is usually more transfer- and request-focused.

You can think of it this way:

- `wget` behaves more like a file retriever
- `curl` behaves more like a general network communication tool

---

## 10. Side-by-side: `wget` and `curl`

### Download a single file

#### `wget`

```bash
wget http://example.com/file.iso
```

This downloads `file.iso` from the given URL.

#### `curl`

```bash
curl -O http://example.com/file.iso
```

The `-O` option tells `curl` to save the file using the remote filename.

---

### Download and save using a different filename

#### `wget`

```bash
wget -O custom_name.iso http://example.com/file.iso
```

#### `curl`

```bash
curl -o custom_name.iso http://example.com/file.iso
```

Notice the difference:

- `wget` uses uppercase `-O`
- `curl` uses lowercase `-o`

That small detail is easy to mix up.

---

### Download multiple files from a list

#### `wget`

```bash
wget -i urls.txt
```

This reads URLs from `urls.txt`, one per line.

#### `curl`

```bash
xargs -n 1 curl -O < urls.txt
```

`curl` does not natively read a list of URLs in the same way, so a helper tool like `xargs` is often used.

---

### Resume a broken download

#### `wget`

```bash
wget -c http://example.com/file.iso
```

The `-c` option continues a partially downloaded file.

#### `curl`

```bash
curl -C - -O http://example.com/file.iso
```

The `-C -` option tells `curl` to resume automatically from the point where the download stopped.

---

### Send request headers

#### `wget`

```bash
wget --header="Header-Name: value" http://example.com
```

#### `curl`

```bash
curl -H "Header-Name: value" http://example.com
```

Both tools can send custom headers, but `curl` is generally the more common choice for API and HTTP request work.

---

## 11. API example: why `curl` is often preferred

A good way to see the difference between `wget` and `curl` is to look at a simple API request.

### Using `wget`

```bash
wget -qO- --header='accept: application/json' 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
```

Explanation:

- `-q` = quiet mode
- `O-` = write output to standard output instead of a file
- `--header='accept: application/json'` = request JSON data

This works, but it feels a bit less natural because `wget` is mainly designed as a downloader.

### Using `curl`

```bash
curl -X 'GET' \
  'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd' \
  -H 'accept: application/json'
```

Explanation:

- `-X 'GET'` specifies the HTTP method
- `-H 'accept: application/json'` requests JSON in the response

This is one reason `curl` is often preferred for APIs: it maps more naturally onto HTTP-style communication.

---

## 12. A practical Linux workflow

Here is a realistic sequence where these tools fit together:

### Step 1: Download source code

```bash
wget https://www.nano-editor.org/dist/v5/nano-5.0.tar.xz
```

### Step 2: Extract the archive

```bash
tar -xvf nano-5.0.tar.xz
```

### Step 3: Compile source code

For a very simple C program, you might do:

```bash
gcc -Wall -o hello hello.c
```

This illustrates a common Linux pattern:

- use a network tool to fetch files
- use an archive tool to unpack them
- use a compiler to build software

---

## 13. Summary table

| Tool | Main purpose | Best known for |
|---|---|---|
| `wget` | Downloading files | simple file retrieval, resuming downloads |
| `curl` | Data transfer and HTTP/API interaction | flexible requests, headers, APIs |
| `tar` | Archiving files | preserving Linux metadata and permissions |
| `zip` | Archiving and compressing files | cross-platform sharing |
| `gcc` | Compiling programs | building C/C++ code |

---

## 14. Final takeaways

- Use **`wget`** when the job is mainly “download this file.”
- Use **`curl`** when the job is more about “communicate with a server” or “make a request.”
- Use **`tar`** when preserving Linux file metadata matters.
- Use **`zip`** when cross-platform compatibility matters more.
- Use **`gcc`** when you need to compile source code into an executable.

All of these tools are foundational because they each solve a common Linux task:

- fetching
- transferring
- packaging
- extracting
- building

That is why they often appear together in Linux labs and software workflows.
