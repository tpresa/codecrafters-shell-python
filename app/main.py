import sys
import os
import subprocess
import ctypes
import ctypes.util


def expanduser(path):
    """Expand ~ to home directory"""
    if path.startswith("~"):
        home = os.environ.get("HOME", "")
        if home:
            return home + path[1:]
    return path


def join(base, path):
    """Join two path components"""
    if path.startswith("/"):
        return path
    if base.endswith("/"):
        return base + path
    return base + "/" + path


def normpath(path):
    """Normalize a path by resolving . and .. components"""
    if not path:
        return "."

    is_absolute = path.startswith("/")
    parts = path.split("/")
    result = []

    for part in parts:
        if part == "" or part == ".":
            continue
        elif part == "..":
            if result and result[-1] != "..":
                result.pop()
            elif not is_absolute:
                result.append("..")
        else:
            result.append(part)

    normalized = "/".join(result)
    if is_absolute:
        return "/" + normalized if normalized else "/"
    return normalized if normalized else "."


def isdir(path):
    """Check if path is a directory using stat system call"""
    try:
        libc = ctypes.CDLL(ctypes.util.find_library("c"))

        class Stat(ctypes.Structure):
            _fields_ = [
                ("st_dev", ctypes.c_ulong),
                ("st_ino", ctypes.c_ulong),
                ("st_nlink", ctypes.c_ulong),
                ("st_mode", ctypes.c_uint),
                ("st_uid", ctypes.c_uint),
                ("st_gid", ctypes.c_uint),
                ("__pad0", ctypes.c_int),
                ("st_rdev", ctypes.c_ulong),
                ("st_size", ctypes.c_long),
                ("st_blksize", ctypes.c_long),
                ("st_blocks", ctypes.c_long),
            ]

        stat_buf = Stat()
        path_bytes = path.encode('utf-8')
        result = libc.stat(path_bytes, ctypes.byref(stat_buf))

        if result != 0:
            return False

        # S_IFDIR is 0o040000
        S_IFMT = 0o170000
        S_IFDIR = 0o040000
        return (stat_buf.st_mode & S_IFMT) == S_IFDIR
    except:
        return False


def main():

    WORKING_DIR = '/app'
    path_envvar = os.environ["PATH"]
    path_list = path_envvar.split(":")

    map = {}
    for path in path_list:
        try:
            files = os.listdir(path)
        except:
            continue
        for file in files:
            full_path = path + "/" + file
            if os.access(full_path, os.X_OK):
                map[file] = full_path
    # Wait for user input
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command.strip() == "exit 0":
            break
        elif command.strip().startswith("echo "):
            print(command.strip()[5:])
        elif command.strip().startswith("type "):
            args = command.strip()[5:]
            if (args == "exit") or (args == "type") or (args == "echo") or (args == "pwd") or (args == "cd"):
                print(args + " is a shell builtin")
            else:
                if args in map:
                    print(args + " is " + map[args])
                else:
                    print(args + ": not found")
        elif command.strip().startswith("pwd"):
            print(WORKING_DIR)
        elif command.strip().startswith("cd "):
            args = command.split(" ")
            path = args[1]

            # Expand ~ to home directory if needed
            if path.startswith("~"):
                path = expanduser(path)

            # If relative path, resolve against WORKING_DIR
            if not path.startswith("/"):
                path = join(WORKING_DIR, path)

            # Normalize the path
            path = normpath(path)

            # Check if directory exists and update WORKING_DIR
            if isdir(path):
                WORKING_DIR = path
            else:
                print("cd: " + args[1] + ": No such file or directory")

        else:            
            args = command.split(" ")

            if args[0] in map:
                # args[0] = map[args[0]]
                subprocess.run(args)
            else:
                print(f"{command}: command not found")

if __name__ == "__main__":
    main()
