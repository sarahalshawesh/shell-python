import sys, os

def exit_command():
    exit(0)

def echo_command(input):
    print(input[5:])

def type_command(input, commands):
    command = input.split()[1]
    if command in commands:
        print(f"{command} is a shell builtin")
    elif command not in commands:
        path = os.environ.get("PATH")
        if path:
            split_path = path.split(":")
            print(split_path)
            
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
        command, *args = user_input.split()
        if command in commands:
            commands[command](*args)
        else:
            sys.stdout.write(f"{user_input}: command not found\n")







if __name__ == "__main__":
    main()
