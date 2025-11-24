import sys, os

def exit_command(args):
    exit(0)

def echo_command(args):
    print(args[5:])

def type_command(args):
    command = args.split()[0]
    if command in commands:
        print(f"{command} is a shell builtin")
    elif command not in commands:
        paths = os.environ.get("PATH").split(":")
        for i in paths:
            if os.path.isfile(f"{i}/{command}"):
                print(f"{command} is {i}")
            
    else: 
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
        command, args = user_input.split()
        if command in commands:
            commands[command](args)
        else:
            sys.stdout.write(f"{user_input}: command not found\n")







if __name__ == "__main__":
    main()
