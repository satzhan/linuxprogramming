# Essential Git Commands and Usage

This guide provides an overview of essential Git commands and their usage, based on the provided documents.

## Checking Git Version

To check the version of Git installed on your system:

```
git --version
```

Example output:
```
git version 2.27.0
```

## Getting Help

To access detailed help information (man page) for any Git subcommand:

```
git help [subcommand]
```

For example:
```
git help status
```

This is equivalent to:
```
man git-status
```

## Listing Git Commands

To see a basic list of Git commands:

```
git
```

This will display a list of commonly used Git commands and their brief descriptions.

For a more comprehensive list of all available Git commands:

```
git help --all
```

## Command Structure

Git commands typically follow this structure:

```
git [global options] subcommand [subcommand options] [arguments]
```

- Global options are prefixed with `--` (e.g., `--version`, `--help`)
- Subcommands are specific Git operations (e.g., `status`, `commit`, `push`)
- Subcommand options and arguments vary depending on the specific subcommand

## Creating a New Git Repository

To create a new Git repository:

```
mkdir git-test
cd git-test
git init
```

This creates a new directory called `git-test`, changes into it, and initializes a new Git repository.

## Adding Files to the Repository

To add a new file to the repository:

```
echo some junk > somejunkfile
git add somejunkfile
```

## Checking Repository Status

To see the current status of your repository:

```
git status
```

This will show which files are staged, unstaged, or untracked.

## Configuring User Information

Set your name and email for the repository:

```
git config user.name "Your Name"
git config user.email "your_email@example.com"
```

## Viewing Changes

To see the differences between the working directory and the staging area:

```
git diff
```

## Committing Changes

To commit staged changes:

```
git commit -m "Your commit message"
```

To sign off on your commit:

```
git commit -s -m "Your commit message"
```

## Viewing Commit History

To see the commit history:

```
git log
```

## Switching to Main Branch

Many projects now use `main` instead of `master` as the default branch name. To create and switch to a `main` branch in a new repository:

```
git init
git checkout -b main
```

For existing repositories, to rename the `master` branch to `main`:

```
git branch -m master main
git push -u origin main
git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/main
```

## Notes

1. The `.git` directory contains all the version control information.
2. Changes are not fully in the repository until you commit them.
3. Signing off on commits (-s option) is important for tracking responsibility and licensing.
4. Many projects are moving from `master` to `main` as the default branch name.
5. While there are many Git commands, some are for advanced usage and are rarely used.
6. Some commands can be more efficiently invoked through shorthand combinatorial commands.
7. Graphical interfaces for Git are available, which can simplify the usage of Git for those who prefer not to use the command line interface.

Remember to consult the official Git documentation or use the `git help` command for more detailed information on specific commands and their options.
