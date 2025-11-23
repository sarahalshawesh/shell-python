import sys

commands = {
    "exit" : exit(0),
    "echo" : print(user_input[5:]),
    "type echo": print("echo is a shell builtin")
    }

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = sys.stdin.readline().strip()
        command = user_input[0]
        if command in commands:
            commands.command
        else:
            sys.stdout.write(f"{user_input}: command not found\n")







if __name__ == "__main__":
    main()
