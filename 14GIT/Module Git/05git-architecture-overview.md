# Git Architecture Overview

## Repository Structure

1. A Git repository is essentially a database containing:
   - Complete working copy of project files
   - A copy of the repository itself
   - All information required to store, manage revisions, and show history

2. Repository contents are stored in the `.git` subdirectory tree

3. Configuration parameters in each repository include:
   - Author's name and email address
   - List of all branches (local and remote)

4. When cloning a repository:
   - Configuration information is not carried forward
   - New configuration is based on the local site

## Key Data Structures

1. **Object Store**: Contains the full contents of the project
2. **Index**: Dynamic representation of the project structure at any given time

## Object Types in the Object Store

1. **Blobs (Binary Large Objects)**:
   - Store file contents
   - Do not contain file names or metadata
   - Where most of the bytes are stored

2. **Trees**:
   - Record blob identifiers, path names, and metadata
   - Represent directory structures

3. **Commits**:
   - Created for each change in the repository
   - Contain metadata describing the change

4. **Tags**:
   - Optional, human-friendly names
   - Used to retrieve specific points in project history without using hexadecimal identifiers

## Git's Approach to Content

1. Content-centric rather than file-centric:
   - Works with contents, not file names
   - Identical content across different files/directories is stored only once

2. Content identification:
   - Each piece of content is associated with a hexadecimal string (SHA-1 hash)
   - Changes in content result in a new blob with a new identifier

3. Efficient comparisons:
   - Git compares hexadecimal identifiers, not actual file contents
   - Only compares actual content if identifiers differ

## File Management

1. New binary blobs are created for changed files
2. No need to keep copies of files at different points in time
3. File names are treated as metadata, separate from content
4. The `.git` subdirectory structure doesn't mirror the working directory structure
5. Working files can be easily restored from the `.git` directory using `git restore`

## Benefits of This Architecture

1. Faster comparisons and operations
2. Efficient storage (identical content stored only once)
3. Robust history tracking
4. Easy file restoration

This architecture underlies Git's efficiency, flexibility, and power as a version control system, enabling its distributed nature and facilitating complex operations like branching and merging.
