import sys, os, subprocess

def exit_command(args):
    exit(0)

def echo_command(args):
    print(" ".join(args))

def type_command(args):
    command = args[0]
    if command in commands:
        print(f"{command} is a shell builtin")
        return
    if command not in commands:
        paths = os.environ.get("PATH").split(":")
        for i in paths:
            filename = f"{i}/{command}"
            if os.path.isfile(filename) and os.access(filename, os.X_OK):
                print(f"{command} is {filename}") 
                return
     
    print(f"{command}: not found")

commands = {
    "exit" : exit_command,
    "echo": echo_command,
    "type": type_command
}

def main():

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = sys.stdin.readline().strip()
        command = user_input.split()[0]
        args = user_input.split()[1:]

        if command in commands:
            commands[command](args)

        elif command not in commands:
            paths = os.environ.get("PATH").split(":")
            for i in paths:
                filename = f"{i}/{command}"
                if os.path.isfile(filename) and os.access(filename, os.X_OK):
                    subprocess.run([command, args[0], args[1]])
        else:
            sys.stdout.write(f"{command}: command not found\n")







if __name__ == "__main__":
    main()
