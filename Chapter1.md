# Chapter 1 - Repository Initialization (git init)

### <u>Objects in Git</u>

Git stores data as objects—each having a type: commit, tree, or blob. 

`Blob` - A file's content

`Tree` - A directory's structure

`commit` - Current Status of your project at a specific point in time

What We Need to Create:
- `.git/` – root of all Git data

- `.git/objects/` – where blob and commit files will be stored

- `.git/index.json` – The Staging area in JSON

- `.git/HEAD` – pointer to the current branch (refs/heads/master)

- `.git/refs/heads/master` – will contain the latest commit SHA-1

