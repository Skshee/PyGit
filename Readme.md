# PyGit – A Minimal Git Implementation in Python

**PyGit** is a lightweight and educational version-control system that mimics core Git functionality in Python.
It is inspired by Ben Hoyt's pygit (https://benhoyt.com/writings/pygit/) but I've used JSON based encoding instead of the actual Binary Git files, therefore it's not completely mimicing Git.  

-> This version is better suited for beginners and those looking to understand Git internals without the complexity of full Git plumbing.

`This project is not a complete Git replacement, nor is it intended for production use.`

For Simplicity and better understanding of how and why the code was implemented the way it is, I have broken down the steps and the logic into different chapters.

---

## 📦 Features

| Command          | Description                                                               |
|------------------|---------------------------------------------------------------------------|
| `init`           | Initializes a new Git-like repository                                     |
| `add`            | Stages files by hashing them into `.git/objects/` and tracking them      |
| `commit`         | Creates a tree and commit object and updates the branch reference        |
| `status`         | Shows staged, modified, and untracked files with color-coded output      |
| `sync-github`    | *(Optional)* Uses native Git to sync files to GitHub for convenience     |

---

## 🛠️ Setup

> Requires **Python 3.7+** and optionally **Git CLI** for `sync-github`.

Clone or copy the project files:

```bash
git clone https://github.com/Skshee/PyGit
cd PyGit
```

## 🚀 Usage 

### Initialize Repository

``` bash
python PyGit.py init
```

Creates the .git/ directory and essential files like index.json, HEAD, and refs/.

### Stage Files

``` bash
python PyGit.py add file1.txt file2.py
```

Files are hashed, compressed, and stored as Git-style blobs. Their metadata is recorded in a custom `index.json`.

### Commit Changes

``` bash
python PyGit.py commit "Your Commit Message"
```

Generates:

A tree object (representing file structure)

A commit object with metadata and message

Updates the current branch reference (`refs/heads/master`)

### View File Status

``` bash
python PyGit.py status
```

Displays:
- <font color="green">Staged</font>
- <font color="red">Modified</font>
- <font color="yellow">Untracked</font>

Color-coded using ANSI escape codes(in the respective colours as above).

###  Sync to GitHub (Optional Convenience Command)

``` bash
python PyGit.py sync-github https://github.com/your-username/your-repo
```

`⚠️ Note`: This does not push your PyGit commits or trees. It uses real Git underneath for convenience only.

You can ignore this command entirely if you are only interested in learning Git internals.

I avoided implementing a true push because it would require building Git’s binary packfile format and speaking Git’s complex network protocol — far beyond the scope of a minimal, educational project.

## 🧠 How It Works :
`Objects`: Files are hashed using SHA-1 and stored in .git/objects/, compressed with zlib.

`Index`: A simplified index.json tracks file paths and object IDs.

`Trees & Commits`: Stored as structured JSON or plain text, hashed into Git-style objects.

`HEAD & Refs`: Point to current branch (master) and the latest commit SHA.

## 📈 Future Improvements:

- `Full push/pull support` - Implement Git's Push and Pull by implementing proper raw binary Git objects

- `Implement log or show` - To view commit history

- `Support Branching` - Allow creating and switching between multiple branches by updating HEAD

## 📋 References : 

https://benhoyt.com/writings/pygit/

https://www.freecodecamp.org/news/git-internals-objects-branches-create-repo/

https://www.geeksforgeeks.org/git/git-internals/

https://www.youtube.com/playlist?list=PL9lx0DXCC4BNUby5H58y6s2TQVLadV8v7

https://www.youtube.com/watch?v=MVWzn5EIdIY







