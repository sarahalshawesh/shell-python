import sys


def main():
    sys.stdout.write("$ ")
    user_input = sys.stdin.readlines()
    sys.exit(f"{user_input}: command not found")
    pass


if __name__ == "__main__":
    main()
