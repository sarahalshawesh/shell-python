import sys


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = sys.stdin.readline().strip()
        if "exit" in user_input:
            exit(0)
        sys.stdout.write(f"{user_input}: command not found\n")
        




if __name__ == "__main__":
    main()
