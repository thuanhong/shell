#!/usr/bin/env python3
from built_ins import *


def path():
    try:
        if exists(environ['HOME']):
            current_path = getcwd()[len(environ['HOME']):]
        else:
            current_path = getcwd()
    except KeyError:
        current_path = getcwd()
    log = '\033[1m{}\033[0m'.format('hthuan@intek-sh')
    log = '\033[32m{}\033[0m'.format(log)
    current_path = '\033[31m{}\033[0m'.format(":-" + current_path + "$ ")
    return log + current_path


def main():
    """
    handle main
    """
    while True:
        try:
            command = input(path()).split()
            if command[0] == 'printenv':
                print_env(command)
            elif command[0] == 'export':
                export(command)
            elif command[0] == 'unset':
                unset(command)
            elif command[0] == 'cd':
                cd(command)
            elif command[0] == 'exit':
                exit(command)
            else:
                execute_shell(command)
        except IndexError:
            pass
        except KeyboardInterrupt:
            print('')


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        pass