import sys


def main():
    sys.stdout.write("$ ")
    sys.stdout.flush()
    user_input = sys.stdin.readline().strip()
    sys.stdout.write(f"{user_input}: command not found\n")
    pass


if __name__ == "__main__":
    main()
