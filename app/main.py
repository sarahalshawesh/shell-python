import sys, os, subprocess, shlex, readline, rlcompleter


def exit_command(args):
    sys.exit(0)

def echo_command(args):
    if args is not None:
        return " ".join(args)

def type_command(args):
    
    command = args[0]
    if command in commands:
        return f"{command} is a shell builtin"
        
    if command not in commands:
        paths = os.environ.get("PATH").split(":")
        next((f"{command} is {p}/{command}" for p in paths if os.path.isfile(f"{p}/{command}") and os.access(f"{p}/{command}", os.X_OK)), f"{command}: not found")

def pwd_command(args):
    return os.getcwd()

def cd_command(args):
    home_path = os.getenv("HOME")
    if not args:
        os.chdir(home_path)
        return
    else:
        dir_path = args[0]
        if dir_path == "~":
            os.chdir(home_path)
        elif os.path.exists(dir_path):
            os.chdir(dir_path)
        else:
            return f"cd: {dir_path}: No such file or directory"

commands = {
    "exit" : exit_command,
    "echo": echo_command,
    "type": type_command,
    "pwd": pwd_command,
    "cd": cd_command
}

def redirect_helper(file_path, redirect, command, output, actions=None):

    mode = "a" if ">>" in redirect else "w"
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    if command in commands and output is not None:
        if redirect.startswith("2"):
            print(output)
            with open(file_path, mode) as file:
                pass
        else:
            with open(file_path, mode) as file:
                file.write(str(output) + '\n')
    if actions:
        with open(file_path, mode) as file:
            if redirect.startswith("2"):
                subprocess.run(actions, stderr=file)
            else:
                subprocess.run(actions, stdout=file)


def shell_completer(text, state):
   command_options = [cmd for cmd in commands if cmd.startswith(text)]
   if command_options is not None:
       return command_options[state] + " " if state < len(command_options) else None

readline.parse_and_bind("tab: complete")
readline.set_completer(shell_completer)

def main():

    while True:
        line = input("$ ")
        if not line:
            continue
        user_input = shlex.split(line)
        command, args = user_input[0], user_input[1:]

        redirect_options = ['2>>', '1>>', '>>', '2>', '1>', '>']
        redirect = next((redirect for redirect in redirect_options if redirect in user_input), None)
        redirect_index = user_input.index(redirect) if redirect else None
        file_path = user_input[redirect_index + 1] if redirect else None

        if command in commands and not redirect:
            result = commands[command](args)
            if result is not None:
                print(result)
        
        elif command in commands and redirect in user_input:
            try:
                output = commands[command](user_input[1:redirect_index])
                redirect_helper(file_path, redirect, command, output)
            except Exception as e:
                redirect_helper(file_path, redirect, command, output=e)
                

        elif redirect:
            actions = user_input[:redirect_index]
            redirect_helper(file_path, redirect, command, output=None, actions=actions)

        else:
            paths = os.environ.get("PATH").split(":")
            next((subprocess.run(user_input) for p in paths if os.path.isfile(f"{p}/{command}") and os.access(f"{p}/{command}", os.X_OK)), sys.stdout.write(f"{command}: command not found\n"))
        








if __name__ == "__main__":
    main()
