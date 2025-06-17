# Chapter 5 - Implementing Git Status 

The status command in Git tells us:

- Which files are staged for commit.

- Which files are modified but not yet staged.

- Which files are untracked.

## Steps :

1. Load Index
2. Get working directory files
3. Compare index with working directory

I've also enhanced the code by adding `ANSI Code based color coding` for different status outputs:

- <font color="green">Green</font> - Staged
- <font color="red">Red</font> - Modified
- <font color="yellow">Yellow</font> - Untracked

## Load_Index() function:

### 🎯 Purpose:

So our index is the staging area and it's stored as `./git/index.json`. This function loads the index file to check which files are staged, which are modified and which are untracked.

Ex - index = load_index()

    Output : A dictionary like:
             {
            "file1.txt": "a1b2c3...",
            "main.py": "d4e5f6..."
             }

## List_Files function:

### 🎯 Purpose:

It recursively lists all files in your working directory, skipping everything inside `.git/`, and yields their relative paths.

Git needs to inspect all files in your project to:

- Compare them with the index (status)

- Hash their contents (add)

- Detect untracked or modified files



             
             