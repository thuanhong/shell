#!/usr/bin/env python3
from built_ins import *
from logical import handle_logical
from handle_user_input import *
from os.path import exists
from os import getcwd, environ
from quoting import add_input
from readline import parse_and_bind
from shlex import split


def path():
    try:
        if exists(environ['HOME']):
            current_path = getcwd()[len(environ['HOME']):]
        else:
            current_path = getcwd()
    except KeyError:
        current_path = getcwd()
    log = '\033[1m{}\033[0m'.format('code@intek-sh')
    log = '\033[32m{}\033[0m'.format(log)
    current_path = '\033[31m{}\033[0m'.format(":-" + current_path + "$ ")
    return log + current_path


def main():
    """
    handle main
    """
    exit_code = 0
    while True:
        try:
            command_full = input(path())
            parse_and_bind('tab: complete')
            command_full = handle_user_input(command_full)
            while command_full != '':
                command, command_full, logical = handle_logical(command_full)
                command = convert_command(split(command, posix=False), environ, exit_code)
                if not command:
                    exit_code = 1
                    break
                if command[0] == 'printenv':
                    exit_code = print_env(command)
                elif command[0] == 'export':
                    exit_code = export(command)
                elif command[0] == 'unset':
                    exit_code = unset(command)
                elif command[0] == 'cd':
                    exit_code = cd(command)
                elif command[0] == 'exit':
                    exit(command)
                    quit()
                else:
                    exit_code = execute_shell(command)
                if '&' in logical and exit_code != 0:
                    break
                elif logical == '||' and exit_code == 0:
                    break
        except SyntaxError as syn:
            print(syn)
        except KeyboardInterrupt:
            exit_code = 130
            print('')
        except Exception as exp:
            exit_code = 1
            print('----Something was wrong----')
            print('Error : {}----'.format(exp))
            print("----Please input again, thanks----")


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        pass
