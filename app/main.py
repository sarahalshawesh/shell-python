import sys
import os

def exit_command(input, commands):
    os.exit(0)

def echo_command(input, commands):
    print(input[5:])

def type_command(input, commands):
    command = input.split()[0]
    if command in commands:
        print(f"{command}is a shell builtin")
    else: 
        print(f"{command}: command not found\n")

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

        if command in commands:
            commands[command](user_input, commands)
        else:
            sys.stdout.write(f"{user_input}: command not found\n")







if __name__ == "__main__":
    main()
