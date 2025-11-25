def exit_command(args):
    exit(0)

def echo_command(args):
    print(" ".join(args))

def type_command(args):
    command = args[0]
    if command in commands:
        print(f"{command} is a shell builtin")
        return
    if command not in commands:
        paths = os.environ.get("PATH").split(":")
        for i in paths:
            filename = f"{i}/{command}"
            if os.path.isfile(filename) and os.access(filename, os.X_OK):
                print(f"{command} is {filename}") 
                return
     
    print(f"{command}: not found")

commands = {
    "exit" : exit_command,
    "echo": echo_command,
    "type": type_command
}