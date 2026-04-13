1) Create a New Branch: 
Start by creating a new branch based off the current branch (assumed to be git_cloned):

```
git checkout -b new_branch
```

This command switches you to a new branch called new_branch.

2) Do Some Work: Next, you modify or create files. In your example, you're adding text to file1. If file1 doesn't already exist, this command will create it.
```
echo 'cloned new_branch commit' >> file1
```

3) Stage Changes: Before committing, you need to stage any new files or changes. Since git commit -am only stages modified (not new) files, you should use git add if file1 is new or if you want to ensure all changes including new files are staged:
```
git add file1
```

4) Commit the Changes: Now commit your changes with a message.

```
git commit -m 'cloned new_branch commit'
```

If you're sure file1 was already tracked and you haven't added any new files, you could use your original command with -am to stage modifications and commit:

```
git commit -am 'cloned new_branch commit'
```

5) Push the Branch to the Remote Repository: 
Finally, push your new branch along with the commits to the remote repository:
```
git push origin new_branch
```
This command uploads your local new_branch to the remote repository (typically named origin), making it available for others to see and collaborate on.


By following these steps, you ensure that your local changes are properly committed and then pushed to the remote repository under the correct branch.

Delete Branch

To delete a local branch in Git, you can use the git branch command with the -d or -D flag. 
Here's how you can do it:

Example
Let's say you have a branch named new_feature that you want to delete:

Safe Delete:
```
git branch -d new_feature
```
Force Delete:
```
git branch -D new_feature
```

Additional Notes
Make sure you are not currently on the branch you are trying to delete. If you are, switch to another branch first:
```
git switch main
```
or
```
git checkout main
```
Always double-check that you no longer need the branch or that its changes have been safely merged into another branch before deleting it, especially when using the force delete option.


To delete remote branch
```
$ git push origin :new_branch
```

