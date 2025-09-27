import sys
import os
import subprocess


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
            if (args == "exit") or (args == "type") or (args == "echo") or (args == "pwd"):
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
            if os.path.isdir(args[1]):
                WORKING_DIR = args[1]
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
