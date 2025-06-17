import os
import json
import hashlib
import zlib
import argparse

def read_file(path):
    with open(path, "rb") as f:
        return f.read()

GIT_DIR = ".git"
OBJECTS_DIR = os.path.join(GIT_DIR, "objects")
INDEX_FILE = os.path.join(GIT_DIR, "index.json")    # Tracks what is changed
HEAD_FILE = os.path.join(GIT_DIR, "HEAD")           # Points to the current branch or commit
MASTER_REF = os.path.join(GIT_DIR, "refs", "heads", "master")

def init_repo():
    os.makedirs(OBJECTS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(MASTER_REF), exist_ok=True)

    # Create an empty JSON index
    with open(INDEX_FILE, "w") as f:
        json.dump({}, f)

    # Set HEAD to point to master
    with open(HEAD_FILE, "w") as f:
        f.write("ref: refs/heads/master\n")

    # Empty master ref (no commits yet)
    with open(MASTER_REF, "w") as f:
        f.write("")

    print("Initialized empty Git repository in .git/")

def hash_object(data, obj_type, write=True):
    header = f'{obj_type} {len(data)}'.encode()  # Every git object has a header like 'blob 23', 'commit 45' etc
    full_data = header + b'\x00' + data          # header + null byte + actual content (null byte acts as a delimiter between header and actual data)

    sha1 = hashlib.sha1(full_data).hexdigest()  # Using the imported hashlib library's for sha1 encoding and storing it in hexadecimal
    if write:
        path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])  # Converts raw SHA-1 to actual filepath (One can also use pathlib library instead of os.path)
        os.makedirs(os.path.dirname(path), exist_ok=True) # Ensures that the directory exists
        with open(path, 'wb') as f:
            f.write(zlib.compress(full_data))   # Stores objects in zlib compressed format
    return sha1

def read_index():
    if not os.path.exists(INDEX_FILE):
        return {}  # empty index
    with open(INDEX_FILE, "r") as f:
        return json.load(f)

def write_index(index):
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)


def add_command(file_paths):
    # reads the .git/index.json file - Stores currently committed data
    index = read_index() 

    # Process each file and check if it's valid
    for path in file_paths:
        if not os.path.isfile(path):
            print(f"warning: {path} is not a file, skipping")
            continue

        with open(path, "rb") as f:
            data = f.read()

        # Create a Git-style object and store it
        oid = hash_object(data, "blob")  

        # Stage the file in an index
        index[path] = {
            "oid": oid,
            "mode": "100644",  # 100-regular file, 644 - WRR (WRITE,READ,READ) permissions
        }

        print(f"added: {path}")

    write_index(index)

def get_author_info():
    name = os.getenv("GIT_AUTHOR_NAME", "Suvan")
    email = os.getenv("GIT_AUTHOR_EMAIL", "suvan@example.com")
    return f"{name} <{email}>"

def write_tree():
    index = read_index()
    entries = []

    # index is a Python dictionary with file paths as keys, and their metadata (SHA1 hash(oid) and mode) as values.
    for path, meta in index.items():
        entries.append({
            "mode": meta["mode"],
            "path": path,
            "oid": meta["oid"],
        })

    tree_data = json.dumps(entries, indent=2).encode()
    # Converts the list of tree entries into a formatted JSON string and encode it as bytes, since Git objects (like trees) are stored in binary format
    return hash_object(tree_data, "tree")

def commit_command(message):
    tree_oid = write_tree() # Returns SHA-1 hash of tree object

    # Read HEAD to get current branch ref
    with open(HEAD_FILE) as f:
        ref = os.path.join(GIT_DIR, f.read().strip().split(" ")[-1])  # Gets 'refs/heads/master' - ref is the full path to the branch file
    
    parent = None
    if os.path.exists(ref):         # Checks if there is an existing commit in the current branch
        with open(ref) as f:
            parent = f.read().strip() or None

    author = get_author_info()      # Git also stores timestamp but for now I'm skipping it. Just returns name and email

    commit_lines = []
    commit_lines.append(f"tree {tree_oid}")
    if parent:
        commit_lines.append(f"parent {parent}")
    commit_lines.append(f"author {author}")
    commit_lines.append("")
    commit_lines.append(message)

    commit_data = "\n".join(commit_lines).encode()   # Joins all commit fields into a single string, encodes it as bytes.
    commit_oid = hash_object(commit_data, "commit") # Saves commit object in .git/objects/ and gets SHA-1 hash

    # Update branch ref
    with open(ref, "w") as f:
        f.write(commit_oid)     # Updates current branch to point to new commit now

    print(f"Committed to branch '{ref.split('/')[-1]}' with OID {commit_oid[:7]}: {message}")

def load_index():
    if not os.path.exists(INDEX_FILE):
        return {}
    with open(INDEX_FILE, "r") as f:
        return json.load(f)
    
def list_files():
    for root, _, files in os.walk("."):
        for file in files:
            if root.startswith(f"./{GIT_DIR}"):
                continue  # Skips .git directory
            yield os.path.relpath(os.path.join(root, file), ".")

def status():
    index = load_index()
    staged = []
    modified = []
    untracked = []

    for path in list_files():
        data = read_file(path)
        sha1 = hash_object(data, "blob", write=False)

        if path not in index:
            untracked.append(path)
        elif index[path] != sha1:
            modified.append(path)
        else:
            staged.append(path)  # Clean files that are already staged

    print("=== Staged ===")
    for path in staged:
        print(path)

    print("\n=== Modified ===")
    for path in modified:
        print(path)

    print("\n=== Untracked ===")
    for path in untracked:
        print(path)

# Wrapper function to add colour to the files based on their status. Follows ANSI codes
def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m" # Ex - "\033[32mThis is green\033[0m"

def status():
    index = load_index()
    staged = []
    modified = []
    untracked = []

    for path in list_files():
        data = read_file(path)
        sha1 = hash_object(data, "blob", write=False)

        if path not in index:
            untracked.append(path)
        elif index[path] != sha1:
            modified.append(path)
        else:
            staged.append(path)

    # Headers
    print(colored("📋 Staged Files:", "36"))
    for path in staged:
        print(colored(f"  ✅ {path}", "32"))

    print(colored("\n📋 Modified Files:", "36"))
    for path in modified:
        print(colored(f"  🛠️  {path}", "31"))

    print(colored("\n📋 Untracked Files:", "36"))
    for path in untracked:
        print(colored(f"  🆕 {path}", "33"))


def main():
    parser = argparse.ArgumentParser(description="A minimal Git implementation in Python")
    subparsers = parser.add_subparsers(dest="command")

    # git init
    subparsers.add_parser("init")

    # git add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("files", nargs="+")

    # git commit
    commit_parser = subparsers.add_parser("commit")
    commit_parser.add_argument("message")

    #git status
    subparsers.add_parser("status", help="Show file changes")

    args = parser.parse_args()

    if args.command == "init":
        init_repo()
    elif args.command == "add":
        add_command(args.files)
    elif args.command == "commit":
        commit_command(args.message)
    elif args.command == "status":
        status()  # ✅ THIS LINE WAS MISSING
    else:
        print("Unknown command.")

if __name__ == "__main__":
    main()


