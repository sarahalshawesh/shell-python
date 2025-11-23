import sys


def main():

    def exit_command(input):
        if input.startswith("type exit"):
            print("exit is a shell builtin")
        else:
            exit(0)
        return

    def echo(input):
        if input.startswith("type echo"):
            print("echo is a shell builtin")
        else:
            print(user_input[5:])
        return
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = sys.stdin.readline().strip()
        

        if "exit" in user_input:
            exit_command(user_input)
        elif "echo" in user_input:
            echo(user_input) 
        else:
            sys.stdout.write(f"{user_input}: command not found\n")







if __name__ == "__main__":
    main()
