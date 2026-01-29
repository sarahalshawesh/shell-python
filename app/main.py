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
        
    for dir in os.environ.get("PATH").split(":"):
        p = Path(dir) / command
        if p.is_file() and os.access(p, os.X_OK):
            return f"{command} is {p}"
    return f"{command}: not found"


def pwd_command(args):
    return str(Path.cwd())

def cd_command(args):
    home_path = Path.home()
    if not args:
        os.chdir(home_path)
        return
    else:
        dir_path = args[0]
        if dir_path == "~":
            os.chdir(home_path)
        elif Path(dir_path).is_dir():
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
    p = Path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)

def get_mode(redirect):
    return "a" if ">>" in redirect else "w"

def builtin_redirect(file_path, redirect, output):  
    mode = get_mode(redirect)
    ensure_dir(file_path)
    p = Path(file_path)
    with p.open(mode=mode) as file:
        if redirect.startswith("2"):
            print(output)
            return
        file.write(output + '\n')


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

def handle_builtin_cmds(user_input, file_path, redirect, command, redirect_index, args):
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

def handle_external_cmds(user_input, command):
    dirs = os.environ.get("PATH").split(":")
    for dir in dirs:
        p = Path(dir) / command
        if p.is_file() and os.access(p, os.X_OK):
            subprocess.run(user_input)
            break
    else:
        print(f"{command}: command not found")


def shell_completer(text, state):
    global tab_count, last_prefix, cached_matches, printed_list
    
    if state == 0:
        matches = []

        for cmd in commands:
            if cmd.startswith(text):
                matches.append(cmd + " ")
     
        for dir in os.environ.get("PATH").split(":"):
            paths = sorted(Path(dir).glob(f"{text}*"))
            external_commands = list(filter(lambda x: os.access(x, os.X_OK),  paths))
            for cmd in external_commands:
                matches.append(cmd.name + " ")
        
        cached_matches = sorted(matches)
        if len(cached_matches) == 1:
            return cached_matches[state] if state < 1 else None
       
        if text != last_prefix:
            tab_count = 0
            printed_list = False

        
        if len(cached_matches) > 1:
            tab_count += 1
            if tab_count == 1:
                print("\x07")
            elif tab_count == 2 and not printed_list:
                printed_list = True
                print(" ".join(cached_matches))
                print(f"$ {text}")

        last_prefix = text

    
    return cached_matches[state] if state < len(cached_matches) else None


tab_count = 0
last_prefix = ""
cached_matches = []
printed_list = False
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
            handle_builtin_cmds(user_input, file_path, redirect, command, redirect_index, args)
                
        elif redirect:
            actions = user_input[:redirect_index]
            redirect_helper(file_path, redirect, command, output=None, actions=actions)

        else:
            handle_external_cmds(user_input, command)

        








if __name__ == "__main__":
    main()
