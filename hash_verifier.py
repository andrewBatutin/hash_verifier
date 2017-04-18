#!/usr/bin/python
from sys import  argv
import hashlib
import ntpath

files = argv

def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

def parse_hash_file(hash_file):
    f = open(hash_file)
    items = map(lambda  x: x.split('='), f.readlines())
    res = {k[7:-1]: v[:-1] for k, v in items}
    return res

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def check_hashes(hashes, files):
    acc = []
    for file in files:
        real_name = path_leaf(file)
        if real_name not in hashes.keys():
            acc.append(real_name)
            continue
        hash = hashes[real_name]
        if check_hash_for_file(hash, real_name) == False:
            acc.append(real_name)
            continue
    if len(acc) == 0:
        return "All certificates are valid"
    else:
        return "Certificates invalid :%s" % (', '.join(acc))

def check_hash_for_file(hash, file):
    real_hash = sha256_checksum(file)
    if real_hash in hash:
        return True
    else:
        return False


hashes = parse_hash_file(files[1])
print (check_hashes(hashes, files[2:]))