# Git Basic File Commands

## git add

Adds files to the staging area (index) and prepares them for commit.

**Usage:**
```bash
git add <file(s)>
```

**Options:**
- `-i`: Interactive mode for choosing files to stage
- `-u`: Update only files already known to Git

**Example:**
```bash
git add myfile.txt
git add -i
git add -u
```

## git rm

Removes files from both the working directory and the index.

**Usage:**
```bash
git rm <file>
```

**Options:**
- `--cached`: Remove only from the index, not the working directory

**Example:**
```bash
git rm oldfile.txt
git rm --cached stagedfile.txt
```

## git mv

Renames a file in both the working directory and the index.

**Usage:**
```bash
git mv <old-file> <new-file>
```

**Example:**
```bash
git mv oldname.txt newname.txt
```

## git ls-files

Shows information about files in the index and working tree.

**Usage:**
```bash
git ls-files [options]
```

**Options:**
- `--others`: Show untracked files
- `--exclude-standard`: Use standard ignore rules

**Example:**
```bash
git ls-files --others --exclude-standard
```

## Effects of Commands on Different Areas

| Command   | Source Files       | Index               | Commit Chain | References |
|-----------|---------------------|---------------------|--------------|------------|
| git add   | Unchanged           | Updated with new file | Unchanged    | Unchanged  |
| git rm    | File removed        | File removed         | Unchanged    | Unchanged  |
| git mv    | File moved/renamed  | Updates file name/location | Unchanged | Unchanged |

**Note:** Changes are not committed until you run `git commit`.

