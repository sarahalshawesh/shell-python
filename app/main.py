import sys, os, subprocess, shlex


def exit_command(args):
    sys.exit(0)

def echo_command(args):
    return " ".join(args)

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

def main():

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        lines = sys.stdin.readline()
        user_input = shlex.split(lines)
        command, args = user_input[0], user_input[1:]

        redirect = None
        if '>' in user_input:
            redirect = '>'
        elif '1>' in user_input:
            redirect = '1>'
        elif '2>' in user_input:
            redirect = '2>'
        elif '2>>' in user_input:
            redirect = '2>>'
        elif '1>>' in user_input or '>>' in user_input:
            redirect = '>>'
        
        

        if command in commands and not redirect in user_input:
            result = commands[command](args)
            if result is not None:
                print(result)

        elif command in commands and redirect in user_input:
            i = user_input.index(redirect)
            file_path = user_input[i + 1]
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            try:
                output = commands[command](user_input[1:i])
                if redirect == '2>':
                    print(output)
                    with open(file_path, 'w') as file:
                        pass
                elif redirect == '>>':
                    with open(file_path, 'a') as file:
                        file.write(str(output) + '\n')
                else:
                    with open(file_path, 'w') as file:
                        file.write(str(output) + '\n')
            except Exception as e:
                if redirect == '2>':
                    with open(file_path, 'w') as file:
                        file.write(str(e) + '\n')
                else:
                    with open(file_path, 'a') as file:
                        file.write(str(e) + '\n')


        else:
            if redirect:
                i = user_input.index(redirect)
                file_path = user_input[i + 1]
                actions = user_input[:i]
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                if redirect == '2>':
                    with open(file_path, 'w') as file:
                        subprocess.run(actions, stderr=file)
                elif redirect == '>>':
                    with open(file_path, 'a') as file:
                        subprocess.run(actions, stdout=file)
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
