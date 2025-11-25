import sys, os, subprocess
from shell_builtins import commands


def main():

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = sys.stdin.readline().strip().split()

        command = user_input[0]
        args = user_input[1:]

        if command in commands:
            commands[command](args)

        else:
            paths = os.environ.get("PATH").split(":")
            for i in paths:
                filename = f"{i}/{command}"
                if os.path.isfile(filename) and os.access(filename, os.X_OK):
                    subprocess.run(user_input)
                    break
            else:
                sys.stdout.write(f"{command}: command not found\n")







if __name__ == "__main__":
    main()
