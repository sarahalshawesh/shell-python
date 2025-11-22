import sys


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = sys.stdin.readline().strip()
        sys.stdout.write(f"{user_input}: command not found\n")
        if user_input.contains("exit"):
            sys.exit()


if __name__ == "__main__":
    main()
