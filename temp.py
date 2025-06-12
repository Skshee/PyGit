import os
import hashlib
import json
import zlib

GIT_DIR = ".git"
OBJECTS_DIR = os.path.join(GIT_DIR, "objects")
INDEX_FILE = os.path.join(GIT_DIR, "index.json")

def read_file(path):
    with open(path, 'rb') as f:
        return f.read()

def write_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def hash_object(data, obj_type="blob", write=True):
    header = f"{obj_type} {len(data)}".encode()
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        dir_path = os.path.join(OBJECTS_DIR, sha1[:2])
        file_path = os.path.join(dir_path, sha1[2:])
        os.makedirs(dir_path, exist_ok=True)
        write_file(file_path, zlib.compress(full_data))
    return sha1

def read_index():
    if not os.path.exists(INDEX_FILE):
        return {}
    try:
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: Could not read index. Starting fresh.")
        return {}

def write_index(index):
    os.makedirs(GIT_DIR, exist_ok=True)
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)

def git_add(paths):
    index = read_index()
    for path in paths:
        data = read_file(path)
        sha1 = hash_object(data)
        index[path] = sha1
        print(f"Staged {path}: {sha1}")
    write_index(index)
