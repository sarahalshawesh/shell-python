import sys, os, subprocess, shlex, readline, rlcompleter
from pathlib import Path


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
        dirs = os.environ.get("PATH").split(":")
        for dir in dirs:
            path = Path(dir) / command
            if Path.isfile() and os.access(path, os.X_OK):
                subprocess.run(command)
                break
            else:
                sys.stdout.write(f"{command}: command not found\n")


def pwd_command(args):
    return Path.getcwd()

def cd_command(args):
    home_path = Path.home()
    if not args:
        os.chdir(home_path)
        return
    else:
        dir_path = args[0]
        if dir_path == "~":
            os.chdir(home_path)
        elif Path.is_dir(dir_path):
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

    if command in commands and output is not None:
        builtin_redirect(file_path, redirect, output)
    if actions:
        subprocess_redirect(file_path, redirect, actions)

def ensure_dir(file_path):
    dir_path = Path(file_path).name
    if dir_path:
        Path.mkdir(parents=True, exist_ok=True)

def get_mode(redirect):
    return "a" if ">>" in redirect else "w"

def builtin_redirect(file_path, redirect, output):  
    mode = get_mode(redirect)
    ensure_dir(file_path)
    p = Path(file_path)
    with p.open(mode=mode, newLine='\n'):
        if redirect.startswith("2"):
            print(output)
            pass
        else:
            p.write_text(output)
    # with open(file_path, mode) as file:
    #     if redirect.startswith("2"):
    #         print(output)
    #         pass
    #     else:
    #         file.write(str(output) + '\n')

def subprocess_redirect(file_path, redirect, actions):
    mode = get_mode(redirect)
    ensure_dir(file_path)
    with open(file_path, mode) as file:
        if not actions:
            return
        if redirect.startswith("2"):
            subprocess.run(actions, stderr=file)
        else:
            subprocess.run(actions, stdout=file)

def parse_redirect(user_input):
    redirect_options = ['2>>', '1>>', '>>', '2>', '1>', '>']
    redirect = next((redirect for redirect in redirect_options if redirect in user_input), None)
    redirect_index = user_input.index(redirect) if redirect else None
    file_path = user_input[redirect_index + 1] if redirect else None
    return redirect, redirect_index, file_path

def shell_completer(text, state):
   command_options = [cmd for cmd in commands if cmd.startswith(text)]
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
        redirect, redirect_index, file_path = parse_redirect(user_input)

        if command in commands: 
            if redirect:
                try:
                    output = commands[command](user_input[1:redirect_index])
                    redirect_helper(file_path, redirect, command, output)
                except Exception as e:
                    redirect_helper(file_path, redirect, command, output=e)
            else:
                result = commands[command](args)
                if result is not None:
                    print(result)
                
        elif redirect:
            actions = user_input[:redirect_index]
            redirect_helper(file_path, redirect, command, output=None, actions=actions)

        else:
            dirs = os.environ.get("PATH").split(":")
            for dir in dirs:
                path = Path(dir) / command
                if Path.isfile() and os.access(path, os.X_OK):
                    subprocess.run(user_input)
                    break
                else:
                    print(f"{command}: command not found\n")

        








if __name__ == "__main__":
    main()
