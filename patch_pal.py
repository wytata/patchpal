#!/usr/bin/python

import subprocess
import sys
import os

ELF_HEADER_SIZE_32 = 52
PROGRAM_HEADER_SIZE_32 = 32
SECTION_HEADER_32 = 40
OFFSET = ELF_HEADER_SIZE_32 + PROGRAM_HEADER_SIZE_32 + SECTION_HEADER_32

def apply_patches(filename):
    return filename
    old_byte = b'\x7E'
    new_byte = b'\x7F'

    with open(filename, "rb") as f:
        data = f.read()

    header_data = data[:OFFSET]
    data = data[OFFSET:]
    data = data.replace(old_byte, new_byte)

    temp_filename = filename + ".tmp"

    with open(temp_filename, "wb") as f:
        f.write(header_data)
        f.write(data)

    os.chmod(temp_filename, 0o777)

def modify_and_run(filename):
    temp_filename = apply_patches(filename)

    proc = subprocess.Popen(["./" + temp_filename])
    proc.wait()

    os.remove(temp_filename)

def main():
    filename = sys.argv[1]
    print("Gave file " + filename)
    modify_and_run(filename)

if __name__ == "__main__":
    main()
