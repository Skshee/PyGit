import os
import json
import hashlib
import zlib

GIT_DIR = ".git"
OBJECTS_DIR = os.path.join(GIT_DIR, "objects")
INDEX_FILE = os.path.join(GIT_DIR, "index.json")
HEAD_FILE = os.path.join(GIT_DIR, "HEAD")
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