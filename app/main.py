import sys

commands = {
    "exit" : exit(0),
    "echo": echo(input),
    "type": type(input)
}

def echo(input):
    print(input[5:])

def type(input, commands):
    for command in commands:
        if command in commands:
            print(f"{command}is a shell builtin")
        else: 
            print(f"{command}: command not found\n")

def main():

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = sys.stdin.readline().strip()
        command = user_input.split()[0]

        if command in commands:
            commands[command]()
        else:
            sys.stdout.write(f"{user_input}: command not found\n")







if __name__ == "__main__":
    main()
