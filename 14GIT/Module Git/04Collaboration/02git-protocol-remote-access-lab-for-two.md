# Lab for Two: Accessing a Repository Remotely with git Protocol

## Objective
Learn how to create a remote Git repository, make it accessible via the git protocol, and collaborate with another person by cloning and making changes to the repository.

## Prerequisites
- Git installed on both participants' machines
- Basic knowledge of Git commands
- Access to a terminal or command prompt on both machines
- Network connectivity between the two machines (same local network or internet access)

## Participants
- Person A: Repository Owner
- Person B: Collaborator

## Lab Steps

### Person A: Set Up the Repository

1. Create and populate a repository:
   ```bash
   mkdir git-test
   cd git-test
   git init
   echo "# Our Collaborative Project" > README.md
   git add README.md
   git commit -m "Initial commit"
   ```

2. Create a bare clone to serve as the remote:
   ```bash
   git clone --bare /path/to/git-test /tmp/our-remote-repo.git
   ```

3. Make the repository accessible:
   ```bash
   touch /tmp/our-remote-repo.git/git-daemon-export-ok
   ```

4. Start the Git daemon:
   ```bash
   git daemon --reuseaddr --base-path=/tmp --export-all &
   ```

   Note: The `--reuseaddr` option allows quick restarts of the daemon by reusing the address. The `--export-all` option allows access to all repositories in the base path without needing individual `git-daemon-export-ok` files.

5. Find out your IP address:
   - On Linux/Mac: `ifconfig` or `ip addr show`
   - On Windows: `ipconfig`

6. Share your IP address with Person B.

### Person B: Clone and Modify the Repository

1. Clone the repository:
   ```bash
   git clone git://[Person A's IP address]/our-remote-repo.git
   ```

2. Navigate to the cloned repository:
   ```bash
   cd our-remote-repo
   ```

3. Make a change:
   ```bash
   echo "This is a change made by Person B" >> README.md
   git add README.md
   git commit -m "Person B's contribution"
   ```

4. Push the change:
   ```bash
   git push origin main
   ```

### Person A: Pull Changes and Verify

1. Navigate to your original repository:
   ```bash
   cd /path/to/git-test
   ```

2. Add the remote repository:
   ```bash
   git remote add shared /tmp/our-remote-repo.git
   ```

3. Pull the changes:
   ```bash
   git pull shared main
   ```

4. Verify the changes:
   ```bash
   cat README.md
   ```

### Collaborative Exercise

1. Person A: Make a change to the README.md file, commit, and push to the shared repository.

2. Person B: Pull the changes, make another change, commit, and push.

3. Person A: Pull the latest changes and verify.

4. Both: Discuss the collaboration process and how changes were synchronized.

## Troubleshooting

1. If Person B can't clone the repository:
   - Ensure the Git daemon is running on Person A's machine
   - Check if there are any firewall issues blocking port 9418
   - Verify the IP address is correct

2. If push/pull operations fail:
   - Check if the Git daemon is still running
   - Ensure both parties have the correct remote URLs configured

## Additional Experiments

1. Try stopping and restarting the Git daemon. Notice how the `--reuseaddr` option allows for quick restarts.

2. Explore what happens if you remove the `git-daemon-export-ok` file from the repository.

3. Attempt to clone other repositories in the `/tmp` directory and observe the effect of the `--export-all` option.

## Conclusion

This lab demonstrated how two people can collaborate using Git with a custom remote repository setup. You practiced setting up a remote repository, making it accessible via the git protocol, cloning, pushing, and pulling changes. These skills form the foundation of distributed version control and collaboration in Git.

## Clean Up

After completing the lab:

1. Person A: Stop the Git daemon
   ```bash
   pkill git-daemon
   ```

2. Both: Remove the cloned repositories and test directories to free up space.

