# Chapter 4 - Implementing Git Commit

- Git stores the snapshot of files in a commit as a tree object. Each entry looks like: `<mode> <filename>\0<20-byte SHA1 binary>`

## <u>Write_Tree()</u> function:

### 🎯 Purpose:

- Takes the current staging area (i.e., the **index**)
- Turns it into a tree object (a Git representation of the directory state)
- Stores it in the .git/objects folder using its SHA-1 hash.

## Steps

- `Load the Index` : Reads the staged files from `.git/index.json`
- `Build Tree entries` : For each file, collect its mode, path, and SHA-1 hash into a list.
- `Encode as JSON bytes` : Convert the list into a JSON-formatted byte string.
- `Store the tree object` : Save the byte string as a Git "tree" object and return its SHA-1 hash.

