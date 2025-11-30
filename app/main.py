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

def pwd_command(args):
    print(os.getcwd())

def cd_command(args):
    dir_path = args[0]
    print(dir_path)
    if os.path.exists(dir_path):
        os.chdir(dir_path)
    else:
        print(f"cd: {dir_path}: No such file or directory")

commands = {
    "exit" : exit_command,
    "echo": echo_command,
    "type": type_command,
    "pwd": pwd_command,
    "cd": cd_command
}

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
