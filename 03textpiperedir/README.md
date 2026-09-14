# 03 — Text manipulation, pipes, redirection, file descriptors

## [Read the guide](https://satzhan.github.io/linuxprogramming/03textpiperedir/pipes-and-redirection.html)

The guide is one page and it is meant to be read start to finish with a terminal
open next to it. Everything in it runs in this Codespace unchanged.

If the link above shows you a wall of HTML instead of a web page, you clicked the
file in the repository rather than the published version. Use the link.

## Before you start

Open this repository in a Codespace, then make the sample files:

```bash
cd 03textpiperedir
python3 setup_generator.py
```

That gives you five files to work on: a greeting, ten names, twenty numbers, a
small log, and a to-do list. They are small on purpose. The point is not the
data, it is what you can make the tools do to it.

## What the guide covers

- The seven commands: `cat`, `echo`, `wc`, `sort`, `grep`, `head`, `tail`
- Redirection: `>`, `>>`, `<`, `2>`, and the one that quietly destroys your file
- The three numbered slots every program is born with
- Pipes, and why they are not redirection even though they look similar
- What the shell actually does to make a redirection happen: fork, dup2, exec
- Inside a pipe: the buffer, blocking, and why piping into `head` returns instantly
- The same ideas in Python, using file descriptors by number
- `2>&1`, `tee`, `/dev/null`

There are boxes through the guide that ask a question before showing the answer.
Work out your answer first. Opening the box straight away costs you the only
part of it that teaches anything.

## Also in this folder

`file_descriptor.py` is the Python program used in the guide. Run it, then run
it again with its output redirected, and notice that the second time it looks
like it has frozen. The guide explains why. It has not frozen.

The `.md` and `.txt` files are the original course notes. The guide replaces
them; they are kept here as a shorter reference once you already know the
material.
