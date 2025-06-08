# Chapter 1 - Repository Initialization (Implementing git init)

### <u>Imported Modules</u> :-
File and directory operations - `os, stat`

Data encoding/decoding and compression -  `zlib, struct`

Hashing - `hashlib`

Enum representation - `enum`

CLI parsing - `argparse`

### <u>IndexEntry Tuple</u> :

Git uses an index to track staged changes such creation time, modification time etc. The tuple IndexEntry matches the structure of entries in the Git Index file

### <u>Objects in Git</u>

Git stores data as objects—each having a type: commit, tree, or blob. 

`Blob` - A file's content

`Tree` - A directory's structure

`commit` - Current Status of your project at a specific point in time

