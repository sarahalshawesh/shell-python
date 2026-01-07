import sys, os, subprocess, shlex, readline, rlcompleter


def exit_command(args):
    sys.exit(0)

def echo_command(args):
    if args is not None:
        print(" ".join(args))

def type_command(args):
    
    command = args[0]
    if command in commands:
        return f"{command} is a shell builtin"
        
    if command not in commands:
        paths = os.environ.get("PATH").split(":")
        for i in paths:
            filename = f"{i}/{command}"
            if os.path.isfile(filename) and os.access(filename, os.X_OK):
                return f"{command} is {filename}" 
        return f"{command}: not found"

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

def redirect_helper(file_path, output, redirect):
    mode = "a" if ">>" in redirect else "w"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if output is not None:
        with open(file_path, mode) as file:
            file.write(str(output) + '\n')


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

        redirect_options = ['2>>', '1>>', '>>', '2>', '1>', '>']
        redirect = next((redirect for redirect in redirect_options if redirect in user_input), None)

        if command in commands and not redirect:
            result = commands[command](args)
            if result is not None:
                print(result)
        
        elif command in commands and redirect in user_input:
            try:
                redirect_index = user_input.index(redirect)
                file_path = user_input[redirect_index + 1]
                output = commands[command](user_input[1:redirect_index])
                redirect_helper(file_path, output, redirect)
            except Exception as e:
                redirect_helper(file_path, e, redirect)
                

        elif redirect:

            redirect_index = user_input.index(redirect)
            file_path = user_input[redirect_index + 1]
            actions = user_input[:redirect_index]
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if redirect == '2>':
                with open(file_path, 'w') as file:
                    subprocess.run(actions, stderr=file)
            elif redirect == '>>':
                with open(file_path, 'a') as file:
                    subprocess.run(actions, stdout=file)
            elif redirect == '2>>':
                with open(file_path, 'a') as file:
                    subprocess.run(actions, stderr=file)
            else:
                with open(file_path, 'w') as file:
                    subprocess.run(actions, stdout=file)

        else:
            paths = os.environ.get("PATH").split(":")
            for j in paths:
                filename = f"{j}/{command}"
                if os.path.isfile(filename) and os.access(filename, os.X_OK):
                    subprocess.run(user_input)
                    break
            else:
                sys.stdout.write(f"{command}: command not found\n")








if __name__ == "__main__":
    main()
