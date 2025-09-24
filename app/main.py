import sys


def main():
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
            if (args == "exit") || (args == "type") || (args == "echo")
                print(args + "is a shell builtin")
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
