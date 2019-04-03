#!/usr/bin/env python3
from os import environ, chdir
from os.path import abspath, exists, join
from subprocess import call, CalledProcessError


def print_env(command):
    """
    prints the values of the specified environment VARIABLE(s).
    If no VARIABLE is specified, print name and value pairs for them all.
    @param command : input from user (list)
    @return None
    """
    if len(command) <= 1:
        for x, y in environ.items():
            print("{}={}".format(x, y))
        return
    for x in command[1:]:
        try:
            print(environ[x])
        except KeyError:
            pass


def export(command):
    """
    create an environment variable
    @param command : input from user (list)
    @return None
    """
    if len(command) == 1:
        return
    for var in command[1:]:
        try:
            var = var.split('=')
            environ[var[0]] = var[1]
        except IndexError:
            environ[var[0]] = ""


def unset(keys):
    """
    delete an environment variable
    @param command : input from user (list)
    @return None
    """
    if len(keys) == 1:
        return
    for x in keys[1:]:
        try:
            del environ[x]
        except KeyError:
            pass


def cd(command):
    """
    change directory working
    @param command : input from user (list)
    @return None
    """
    # change directory working become home
    if len(command) == 1:
        if environ.get('HOME'):
            chdir(environ['HOME'])
        else:
            print("intek-sh: cd: HOME not set")
        return
    # change directory working
    try:
        chdir(abspath(command[1]))
    except FileNotFoundError:
        print("intek-sh: cd: {}: No such file or directory".format(command[1]))


def execute_shell(command):
    """
    execute commands of shell (ls, pwd, ...)
    @param command : input from user (list)
    @return None
    """
    # execute shell script
    if command[0].startswith("./"):
        execute_command(command)
        return
    # execute commands of shell
    try:
        list_path = environ['PATH'].split(':')
    except KeyError:
        print("intek-sh: {}: command not found".format(command[0]))
        return
    for x in list_path:
        if exists(join(x, command[0])):
            execute_command(command)
            return
    print("intek-sh: {}: command not found".format(command[0]))


def execute_command(command):
    """
    execute shell script
    @param command : input from user (list)
    @return None
    """
    try:
        print(call(command))
    except PermissionError:
        print("intek-sh: {}: Permission denied".format(command[0]))
    except FileNotFoundError:
        print("intek-sh: {}: command not found".format(command[0]))
    except OSError:
        print("intek-sh: {}: cannot execute binary file".format(command[0]))
    except CalledProcessError:
        pass


def exit(command):
    """
    exit bash
    @param command : input from user (list)
    @return None
    """
    print('exit')
    try:
        int(command[1])
    except IndexError:
        pass
    except ValueError:
        print("intek-sh: exit:")
    quit()


def main():
    """
    handle main
    """
    while True:
        try:
            command = input("intek-sh$ ").split()
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
