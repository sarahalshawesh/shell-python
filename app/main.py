import sys


def main():
    flag = True
    while flag:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = sys.stdin.readline().strip()
        sys.stdout.write(f"{user_input}: command not found\n")
        if "exit" in user_input:
            sys.exit()
            flag = False




if __name__ == "__main__":
    main()
