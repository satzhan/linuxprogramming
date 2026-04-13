# Simple Git Collaboration Lab Using Git's HTTP Server

## Objective
Set up a bare Git repository, serve it using Git's built-in HTTP capabilities, and collaborate with a teammate.

## Prerequisites
- Two Ubuntu machines (or VMs) on the same network
- Git installed on both machines
- Basic knowledge of Git commands

## Participants
- Person A: Repository Owner
- Person B: Collaborator

## Steps

### Person A: Set Up the Repository and Git HTTP Server

1. Create a bare repository:
   ```bash
   mkdir /tmp/project.git
   cd /tmp/project.git
   git init --bare
   ```

2. Start Git's HTTP server:
   ```bash
   git daemon --reuseaddr --base-path=/tmp --export-all --enable=receive-pack --verbose &
   ```

   This command:
   - `--reuseaddr`: Allows reusing the address if the server is restarted
   - `--base-path=/tmp`: Sets the base path for repositories
   - `--export-all`: Makes all repositories in the base path available
   - `--enable=receive-pack`: Allows pushing (by default, only fetching is allowed)
   - `--verbose`: Provides detailed output for debugging

3. Find and share your IP address:
   ```bash
   ip addr show
   ```

### Person B: Clone and Make Changes

1. Clone the repository:
   ```bash
   git clone git://[Person A's IP]/project.git
   cd project
   ```

2. Make a change:
   ```bash
   echo "Hello, Git!" > README.md
   git add README.md
   git commit -m "Add README"
   ```

3. Push the changes:
   ```bash
   git push origin main
   ```

### Person A: Verify Changes

1. Clone the repository to a new location:
   ```bash
   git clone /tmp/project.git /tmp/project-verify
   cd /tmp/project-verify
   cat README.md
   ```

## Conclusion

This lab demonstrated how to set up a simple Git collaboration environment using Git's built-in HTTP server capabilities. You've learned how to create a bare repository, serve it using `git daemon`, and enable basic push access without the need for a separate web server.

