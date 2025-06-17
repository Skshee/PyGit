# Chapter 2 - Hashing And Writing Git Objects

`Blobs` - In git, the contents of files are stored in objects called blobs, binary large objects. A blob doesn’t register its creation date, its name, or anything but its contents.

`Tree` - Equivalent of a directory in Git

`Commit` - In git, a snapshot is a commit. A commit object includes a pointer to the main tree (the root directory), as well as other meta-data such as the committer, a commit message and the commit time.

Internally, Git stores each object in a compressed and uniquely hashed format using SHA-1(160 bits or 40 hexadecimal chars).

NOTE : **Blobs and trees that have the same data will have the same SHA-1 hash values.**

## <u> Hash_Object() Function</u> :

### 🎯 Purpose:
Implement the logic for storing files as blobs in your .pygit/objects directory and return their SHA-1 hash (just like Git does).:
This function creates a Git object (blob, tree, or commit), stores it in `.git/objects/`, and returns its SHA-1 hash.

<hr>

So here we first get the header append to the actual data and find out the SHA-1 hash for that data.

`.git/objects` is the main storage area in Git for all object files

Each object is stored as:
- `Folder`: First 2 characters of SHA-1

- `File`: Remaining 38 characters

So for example if our SHA-1 value is : sha-1 = `"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"`
                                Then : Path = `".git/objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391"`
                        
As you can see the first 2 hexadecimal characters i.e "e6" is our subdirectory and the remaining hexadecimal values are used as the filename.

## <u> Commit_Tree() Function </u> :

### 🎯 Purpose:
This builds and saves a commit object that refers to a tree and (optionally) a parent commit.

<hr>

A commit points to a tree and stores:

- Tree SHA1

- Parent SHA1 (For all commits except the very first)

- Author and Committer info

- Message

Git stores author and committer info with UNIX timestamps and adds the user-written commit message



