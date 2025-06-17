# Chapter 3 - The Staging Area (git add)

The staging area or index is an intermediate place where changes are recorded before making a commit.

## Objective
Implement the logic for:

- Tracking files added to the staging area.

- Storing the staged file metadata in `.pygit/index.json`

## Steps

1. Calculate the SHA-1 hash of the file contents.
2. Store the file path and hash in `index.json`.
3. That JSON file becomes our index.

## <u>Add_Command</u> function:

### 🎯 Purpose

1. Reads the staging area (index.json).

2. Processes each given file

3. If it's valid, it constructs a blob header nd hashes it with SHA-1

<hr>

Each staged entry has these 2 features : 
- `OID` -  The object ID (SHA-1 hash) of the file content.

- `Mode` - File permissions 

Example :
``` 
{
  "hello.txt": {
    "oid": "2c26b4...",
    "mode": "100644"
  }
}
```

