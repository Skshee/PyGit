import argparse, collections, difflib, enum, hashlib, operator, os, stat
import struct, sys, time, urllib.request, zlib


IndexEntry = collections.namedtuple('IndexEntry', [
    'ctime_s', 'ctime_n', 'mtime_s', 'mtime_n', 'dev', 'ino', 'mode', 'uid',
    'gid', 'size', 'sha1', 'flags', 'path',
])


class ObjectType(enum.Enum):
    commit = 1
    tree = 2
    blob = 3

def read_file(path):
    """Read contents of file at given path as bytes."""
    with open(path, 'rb') as f: 
        return f.read()

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

def commit_tree(tree_sha, message, parent=None):
    commit = f'tree {tree_sha}\n'
    if parent:
        commit += f'parent {parent}\n'
    commit += f'author XYZ <XYZ@example.com> {int(time.time())} +0000\n' # Author's details with UNIX timestam
    commit += f'committer XYZ <XYZ@example.com> {int(time.time())} +0000\n\n' # Commiter's details with UNIX timestam
    commit += f'{message}\n' # Commit message entered by user
    return hash_object(commit.encode(), 'commit')






