# Local Git Lab: Writing and Revising an Essay on Problem Solving

## Purpose of This Lab

This lab teaches Git through a writing project instead of a programming project.

You will write a short essay about why problem solving is valuable. The essay will not be finished in one step. You will create a first draft, revise it, try alternate versions, merge ideas, create a conflict, fix the conflict, and inspect the history.

The point is not to write a perfect essay. The point is to see Git as a tool for controlled thinking:

- A file changes over time.
- A commit saves a meaningful version.
- A branch lets you try an idea without damaging the main version.
- A merge combines useful ideas.
- A conflict happens when two versions change the same place in incompatible ways.
- The log shows the story of your work.

This is a **local Git lab only**. There are no remote repositories, no GitHub, no push, no pull, and no fetch.

---

## What You Will Practice

By the end of this lab, you should be able to:

1. Create a local Git repository.
2. Track a Markdown essay file.
3. Use `git status` to understand the working directory and staging area.
4. Use `git add` and `git commit` to save versions.
5. Use `git diff` and `git diff --staged` to inspect changes.
6. Create and switch branches with `git switch`.
7. Merge branches back into `main`.
8. Create and resolve a merge conflict.
9. Use `git log --oneline --graph --decorate --all` to understand project history.
10. Use local tags to mark major essay drafts.

---

## Mental Model

Think of Git as a notebook that remembers the important versions of your work.

| Writing idea | Git idea |
|---|---|
| The essay file you are editing | Working directory |
| Choosing which edits are ready to save | Staging area / index |
| Saving a meaningful version | Commit |
| Trying a different version of a paragraph | Branch |
| Combining a useful alternate version | Merge |
| Two drafts changed the same sentence differently | Merge conflict |
| Looking at the history of your thinking | Git log |

A commit should not mean “I typed something.” A commit should mean “this version now has a meaningful improvement.”

---

## Prerequisites

You need:

- A Linux terminal, macOS terminal, WSL, or any terminal with Git installed.
- A text editor such as `nano`, VS Code, Vim, or another editor.
- Basic command-line comfort.

Check Git:

```bash
git --version
```

If Git is installed, you should see a version number.

---

# Part 1: Create the Essay Project

## Step 1. Create a folder

```bash
mkdir problem_solving_essay_lab
cd problem_solving_essay_lab
```

## Step 2. Initialize a local Git repository

```bash
git init
git branch -M main
```

This creates a hidden `.git` folder. That folder stores the local Git history.

Check the repository:

```bash
git status
```

You should see that you are on branch `main` and there are no commits yet.

## Step 3. Configure your name and email for this repository only

This avoids changing global settings on a shared lab machine.

```bash
git config user.name "Student Writer"
git config user.email "student@example.com"
```

Verify:

```bash
git config user.name
git config user.email
```

---

# Part 2: First Draft

## Step 4. Create the essay file

Create a file named `essay.md`:

```bash
cat > essay.md <<'TEXT'
# Why Problem Solving Is Good

Problem solving is useful because life often gives people situations that are confusing. A person may not know what to do at first, but a problem can be made smaller by looking at what is known, what is unknown, and what can be tried next.

Problem solving is also good because it builds confidence. When people solve problems, they learn that confusion does not always mean failure. Sometimes confusion is just the beginning of understanding.

Problem solving helps people work with others. A group can compare ideas, test different approaches, and notice mistakes that one person may miss alone.

In conclusion, problem solving is good because it helps people think clearly, grow stronger, and work better with others.
TEXT
```

Read the file:

```bash
cat essay.md
```

## Step 5. Check Git status

```bash
git status
```

Git should show `essay.md` as an untracked file.

Untracked means Git sees the file, but the file is not part of the saved project history yet.

## Step 6. Stage the file

```bash
git add essay.md
```

Check status again:

```bash
git status
```

The file should now be staged.

## Step 7. Commit the first draft

```bash
git commit -m "Add first draft of problem solving essay"
```

Check the log:

```bash
git log --oneline
```

You should see one commit.

## Step 8. Mark the first draft with a local tag

```bash
git tag draft-v1
```

Check tags:

```bash
git tag
```

A tag is a name attached to a commit. Here, `draft-v1` means “this commit is the first complete draft.”

---

# Part 3: Revise the Main Draft

Now you will improve the essay directly on `main`.

## Step 9. Rewrite the introduction

Replace the first body paragraph with a stronger version.

Open the file:

```bash
nano essay.md
```

Change this paragraph:

```text
Problem solving is useful because life often gives people situations that are confusing. A person may not know what to do at first, but a problem can be made smaller by looking at what is known, what is unknown, and what can be tried next.
```

To this:

```text
Problem solving is useful because it turns confusion into a process. A difficult situation may feel like a wall at first, but careful thinking can turn that wall into smaller steps: define the problem, list what is known, notice what is missing, and try one reasonable move.
```

Save and exit.

## Step 10. Inspect the unstaged change

```bash
git diff
```

`git diff` shows changes that exist in the working directory but have not been staged yet.

## Step 11. Stage and inspect the staged change

```bash
git add essay.md
git diff --staged
```

`git diff --staged` shows what will be included in the next commit.

## Step 12. Commit the revised introduction

```bash
git commit -m "Revise introduction to define problem solving as a process"
```

Check the history:

```bash
git log --oneline
```

---

# Part 4: Try an Alternate Example on a Branch

Now you will try a new idea without changing `main` directly.

## Step 13. Create a branch for adding an example

```bash
git switch -c example-story
```

You are now on a new branch named `example-story`.

Check:

```bash
git branch
```

The branch with `*` is the current branch.

## Step 14. Add an example paragraph

Open the file:

```bash
nano essay.md
```

After the confidence paragraph, add this paragraph:

```text
For example, a student who fails to understand a command-line error can treat the error as information instead of as a dead end. The student can read the message, identify the command that failed, test one small change, and compare the result. In this way, the problem becomes a path for learning.
```

Save and exit.

## Step 15. Review, stage, and commit

```bash
git diff
git add essay.md
git commit -m "Add student example about learning from command-line errors"
```

## Step 16. Return to main

```bash
git switch main
```

View the essay:

```bash
cat essay.md
```

Notice that the example paragraph is not visible on `main` yet. It exists on the `example-story` branch.

## Step 17. Merge the example branch into main

```bash
git merge example-story
```

View the result:

```bash
cat essay.md
```

Check the graph:

```bash
git log --oneline --graph --decorate --all
```

---

# Part 5: Try a Counterargument Branch

A stronger essay usually does not only praise an idea. It also handles a possible objection.

## Step 18. Create a branch for a counterargument

```bash
git switch -c counterargument
```

## Step 19. Add a counterargument paragraph

Open the file:

```bash
nano essay.md
```

Before the conclusion paragraph, add this paragraph:

```text
Problem solving is not always comfortable. It can be slow, and it can reveal that a first idea was wrong. However, this discomfort is part of its value. A person who can revise an idea is less trapped by pride and more able to find what actually works.
```

Save and exit.

## Step 20. Commit the counterargument

```bash
git diff
git add essay.md
git commit -m "Add counterargument about discomfort and revision"
```

## Step 21. Switch back and merge

```bash
git switch main
git merge counterargument
```

Check the essay and the log:

```bash
cat essay.md
git log --oneline --graph --decorate --all
```

## Step 22. Tag the second draft

```bash
git tag draft-v2
```

Check the tags:

```bash
git tag
```

---

# Part 6: Practice Repetition with Small Polishing Commits

Now you will make small, meaningful revisions. This part is intentionally repetitive because Git is learned by doing the cycle many times:

```text
edit → diff → add → commit → log
```

## Step 23. Polish the confidence paragraph

Open the file:

```bash
nano essay.md
```

Find this paragraph:

```text
Problem solving is also good because it builds confidence. When people solve problems, they learn that confusion does not always mean failure. Sometimes confusion is just the beginning of understanding.
```

Replace it with:

```text
Problem solving also builds confidence. When people solve problems, they learn that confusion does not automatically mean failure. Sometimes confusion is the first signal that the mind has found something worth understanding.
```

Then run:

```bash
git diff
git add essay.md
git commit -m "Polish confidence paragraph"
```

## Step 24. Polish the teamwork paragraph

Open the file:

```bash
nano essay.md
```

Find this paragraph:

```text
Problem solving helps people work with others. A group can compare ideas, test different approaches, and notice mistakes that one person may miss alone.
```

Replace it with:

```text
Problem solving also improves teamwork. A group can compare ideas, test different approaches, divide the work, and notice mistakes that one person may miss alone.
```

Then run:

```bash
git diff
git add essay.md
git commit -m "Polish teamwork paragraph"
```

## Step 25. Polish the conclusion

Open the file:

```bash
nano essay.md
```

Find this paragraph:

```text
In conclusion, problem solving is good because it helps people think clearly, grow stronger, and work better with others.
```

Replace it with:

```text
In conclusion, problem solving is good because it gives people a way to move through uncertainty. It helps them think clearly, grow through revision, and work better with others.
```

Then run:

```bash
git diff
git add essay.md
git commit -m "Polish conclusion around uncertainty"
```

## Step 26. View the history

```bash
git log --oneline --graph --decorate --all
```

At this point, your history should show several commits. The essay has changed gradually, and Git has preserved the story.

---

# Part 7: Create a Merge Conflict on Purpose

A conflict is not Git failing. A conflict means Git needs a human decision.

You will create two branches that both change the same introduction paragraph differently.

## Step 27. Create a branch with a philosophical opening

Make sure you are on `main`:

```bash
git switch main
```

Create a new branch:

```bash
git switch -c philosophical-opening
```

Open `essay.md`:

```bash
nano essay.md
```

Replace the first body paragraph with this version:

```text
Problem solving is valuable because it teaches people how to live with uncertainty. Instead of demanding an immediate answer, a good problem solver learns to pause, observe the situation, and make the next thoughtful move.
```

Save and commit:

```bash
git diff
git add essay.md
git commit -m "Try philosophical opening"
```

## Step 28. Create a different opening on main

Switch back to `main`:

```bash
git switch main
```

Open `essay.md`:

```bash
nano essay.md
```

Replace the first body paragraph with this different version:

```text
Problem solving is valuable because it turns messy situations into workable questions. Instead of being stuck with a vague feeling that something is wrong, a person can name the issue, separate facts from guesses, and choose a small test.
```

Save and commit:

```bash
git diff
git add essay.md
git commit -m "Try practical opening on main"
```

## Step 29. Merge the philosophical branch into main

```bash
git merge philosophical-opening
```

Git should report a conflict in `essay.md`.

Check status:

```bash
git status
```

Open the file:

```bash
nano essay.md
```

You should see conflict markers similar to this:

```text
<<<<<<< HEAD
version from current branch
=======
version from branch being merged
>>>>>>> philosophical-opening
```

These markers mean:

- `HEAD` is the version from your current branch, `main`.
- The bottom section is the version from `philosophical-opening`.
- Git cannot choose automatically because both versions changed the same place.

## Step 30. Resolve the conflict

Replace the entire conflict block with this combined paragraph:

```text
Problem solving is valuable because it turns uncertainty into workable questions. A messy situation may first feel like a wall, but a person can pause, name the issue, separate facts from guesses, and choose one small test. This does not remove difficulty, but it gives the mind a direction.
```

Make sure you remove all conflict markers:

```text
<<<<<<<
=======
>>>>>>>
```

Save and exit.

## Step 31. Finish the merge

```bash
git status
git add essay.md
git commit -m "Resolve opening conflict by combining practical and philosophical versions"
```

Check the graph:

```bash
git log --oneline --graph --decorate --all
```

This graph should now show that two lines of work came together.

---

# Part 8: Recover from an Unwanted Edit

Sometimes you make a change and decide you do not want it.

## Step 32. Make a bad change on purpose

```bash
echo "This sentence is random and does not belong in the essay." >> essay.md
```

Check the file:

```bash
tail -n 5 essay.md
```

Check status and diff:

```bash
git status
git diff
```

## Step 33. Discard the unwanted unstaged change

```bash
git restore essay.md
```

Check that the random sentence is gone:

```bash
tail -n 5 essay.md
git status
```

`git restore essay.md` returns the file to the last committed version. Use it carefully: it discards unstaged changes.

---

# Part 9: Use a Local Branch for Final Revision

Now create one final branch to improve the essay title and final wording.

## Step 34. Create a final polish branch

```bash
git switch -c final-polish
```

## Step 35. Improve the title

Open the file:

```bash
nano essay.md
```

Change the title:

```text
# Why Problem Solving Is Good
```

To:

```text
# Why Problem Solving Helps People Grow
```

Save and commit:

```bash
git diff
git add essay.md
git commit -m "Improve essay title"
```

## Step 36. Add one final sentence to the conclusion

Open the file:

```bash
nano essay.md
```

At the end of the conclusion paragraph, add this sentence:

```text
The habit of solving problems is therefore not only a school skill; it is a life skill.
```

Save and commit:

```bash
git diff
git add essay.md
git commit -m "Add final sentence about problem solving as a life skill"
```

## Step 37. Merge final polish into main

```bash
git switch main
git merge final-polish
```

Tag the final draft:

```bash
git tag final-draft
```

---

# Part 10: Final Inspection

## Step 38. View the final essay

```bash
cat essay.md
```

## Step 39. View all commits visually

```bash
git log --oneline --graph --decorate --all
```

## Step 40. View all tags

```bash
git tag
```

## Step 41. Compare first draft and final draft

```bash
git diff draft-v1 final-draft
```

This shows how much the essay changed from the first saved draft to the final saved draft.

## Step 42. Compare second draft and final draft

```bash
git diff draft-v2 final-draft
```

This shows how much changed after the essay already had examples and a counterargument.

---

# Expected Final Essay

Your exact wording may differ if you made your own edits, but the final essay should look similar to this:

```markdown
# Why Problem Solving Helps People Grow

Problem solving is valuable because it turns uncertainty into workable questions. A messy situation may first feel like a wall, but a person can pause, name the issue, separate facts from guesses, and choose one small test. This does not remove difficulty, but it gives the mind a direction.

Problem solving also builds confidence. When people solve problems, they learn that confusion does not automatically mean failure. Sometimes confusion is the first signal that the mind has found something worth understanding.

For example, a student who fails to understand a command-line error can treat the error as information instead of as a dead end. The student can read the message, identify the command that failed, test one small change, and compare the result. In this way, the problem becomes a path for learning.

Problem solving also improves teamwork. A group can compare ideas, test different approaches, divide the work, and notice mistakes that one person may miss alone.

Problem solving is not always comfortable. It can be slow, and it can reveal that a first idea was wrong. However, this discomfort is part of its value. A person who can revise an idea is less trapped by pride and more able to find what actually works.

In conclusion, problem solving is good because it gives people a way to move through uncertainty. It helps them think clearly, grow through revision, and work better with others. The habit of solving problems is therefore not only a school skill; it is a life skill.
```

---

# Deliverables

Submit evidence that you completed the lab. The exact number of screenshots is up to you, but your submission should show the following:

1. The final contents of `essay.md`.
2. The output of:

   ```bash
   git log --oneline --graph --decorate --all
   ```

3. The output of:

   ```bash
   git tag
   ```

4. Evidence that you resolved the merge conflict. This can be shown by the merge commit in the log and the final combined opening paragraph in `essay.md`.
5. A short written reflection answering:
   - What does a commit represent in a writing project?
   - Why might a branch be useful when revising an essay?
   - What did the merge conflict mean, and how did you decide how to resolve it?

---

# Command Summary

```bash
# Create project
mkdir problem_solving_essay_lab
cd problem_solving_essay_lab
git init
git branch -M main

# Local identity for this repository
git config user.name "Student Writer"
git config user.email "student@example.com"

# Inspect state
git status
git log --oneline
git log --oneline --graph --decorate --all

# Save versions
git add essay.md
git commit -m "message"

# Compare changes
git diff
git diff --staged
git diff draft-v1 final-draft

# Branching
git switch -c branch-name
git switch main
git branch

# Merging
git merge branch-name

# Tags
git tag draft-v1
git tag draft-v2
git tag final-draft
git tag

# Restore unwanted unstaged change
git restore essay.md
```

---

# Local Git Only: Commands Not Used in This Lab

This lab intentionally does not use:

```bash
git clone
git remote
git push
git pull
git fetch
```

Those commands are for working with remote repositories. This lab focuses only on local version control.

---

# Closing Idea

A first draft is rarely the final answer. Good writing usually moves through attempts, mistakes, revisions, and recombinations. Git gives that process structure. It lets you try ideas without losing earlier work, and it lets you inspect how your thinking changed over time.
