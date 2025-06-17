import os
import json
import hashlib
import zlib
import argparse
import subprocess


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
        dir_path = os.path.join(OBJECTS_DIR, sha1[:2])
        file_path = os.path.join(dir_path, sha1[2:])
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as f: 
            f.write(zlib.compress(full_data))
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
    # Read HEAD to find current branch (should be master)
    with open(HEAD_FILE) as f:
        ref_line = f.read().strip()
    assert ref_line.startswith("ref: ")
    ref_path = os.path.join(GIT_DIR, ref_line[5:])

    # Get parent commit SHA if it exists
    parent = None
    if os.path.exists(ref_path):
        with open(ref_path) as f:
            parent = f.read().strip()
        if parent == "":
            parent = None

    # ✅ Get tree SHA by building it from index
    tree_sha = write_tree()

    # Create commit object
    lines = []
    lines.append(f"tree {tree_sha}")
    if parent:
        lines.append(f"parent {parent}")
    lines.append("author Suvan <suvan@example.com> 1720000000 +0530")
    lines.append("committer Suvan <suvan@example.com> 1720000000 +0530")
    lines.append("")
    lines.append(message)

    commit_data = "\n".join(lines).encode()
    commit_sha = hash_object(commit_data, "commit")

    # Write to current branch ref
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open(ref_path, "w") as f:
        f.write(commit_sha)

    print(f"[master {commit_sha[:7]}] {message}")


def load_index():
    if not os.path.exists(INDEX_FILE):
        return {}
    with open(INDEX_FILE, "r") as f:
        return json.load(f)
    
def list_files():
    for root, _, files in os.walk("."):
        # Normalize path separators for cross-platform support
        full_path = os.path.normpath(root)
        if os.path.commonpath([GIT_DIR]) in full_path:
            continue  # Skip any .git subfolders

        for file in files:
            yield os.path.relpath(os.path.join(root, file), ".")

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
        elif index[path]["oid"] != sha1:
            modified.append(path)
        else:
            staged.append(path)

    # Output with color
    print(colored("📋 Staged Files:", "36"))
    for path in staged:
        print(colored(f"  ✅ {path}", "32"))

    print(colored("\n📋 Modified Files:", "36"))
    for path in modified:
        print(colored(f"  🛠️  {path}", "31"))

    print(colored("\n📋 Untracked Files:", "36"))
    for path in untracked:
        print(colored(f"  🆕 {path}", "33"))

def push_command(remote_url):
    try:
        # Check if this is already a Git repo
        if not os.path.exists(".git") or not os.path.isdir(".git"):
            subprocess.run(["git", "init"], check=True)
            print("🧱 Initialized native Git repo for pushing")

        # Add all current files to native Git index
        subprocess.run(["git", "add", "."], check=True)

        # Commit with a generic message (could also reuse your commit msg if stored)
        subprocess.run(["git", "commit", "-m", "Sync PyGit commit"], check=True)

        # Create master branch if not set
        subprocess.run(["git", "branch", "-M", "master"], check=True)

        # Add remote if not added
        try:
            subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
        except subprocess.CalledProcessError:
            pass  # Ignore error if remote already exists

        # Push to GitHub
        subprocess.run(["git", "push", "-u", "origin", "master"], check=True)
        print("✅ Push successful via native Git.")
    except subprocess.CalledProcessError as e:
        print("❌ Push failed:", e)


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

    # git push
    sync_parser = subparsers.add_parser("sync-github", help="Sync working directory to GitHub using native Git")
    sync_parser.add_argument("remote_url", help="Remote repository URL")


    args = parser.parse_args()

    if args.command == "init":
        init_repo()
    elif args.command == "add":
        add_command(args.files)
    elif args.command == "commit":
        commit_command(args.message)
    elif args.command == "status":
        status()  
    elif args.command == "push":
        push_command(args.remote_url)
    else:
        print("Unknown command.")

if __name__ == "__main__":
    main()


