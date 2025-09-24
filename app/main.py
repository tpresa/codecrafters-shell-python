import sys
import os

def main():

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
            if (args == "exit") or (args == "type") or (args == "echo"):
                print(args + " is a shell builtin")
            else:
                if args in map:
                    print(args + " is " + map[args])
                else:
                    print(args + ": not found")
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
