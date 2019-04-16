from os import environ, chdir, getcwd
from os.path import abspath, exists, join
from subprocess import call, CalledProcessError


def print_env(command): 
    """
    prints the values of the specified environment VARIABLE(s).
    If no VARIABLE is specified, print name and value pairs for them all.
    @param command : input from user (list)
    @return None
    """
    exit_code = 0
    if len(command) <= 1:
        for x, y in environ.items():
            print("{}={}".format(x, y))
        return exit_code
    for x in command[1:]:
        try:
            print(environ[x])
        except KeyError:
            exit_code = 1
            pass
    return exit_code


def export(command):
    """
    create an environment variable
    @param command : input from user (list)
    @return None
    """
    if len(command) == 1:
        return 0
    for var in command[1:]:
        try:
            var = var.split('=')
            environ[var[0]] = var[1]
        except IndexError:
            environ[var[0]] = ""
    return 0


def unset(keys):
    """
    delete an environment variable
    @param command : input from user (list)
    @return None
    """
    exit_code = 0
    if len(keys) == 1:
        return exit_code
    for x in keys[1:]:
        try:
            del environ[x]
        except KeyError:
            exit_code = 1
            pass
    return exit_code


def cd(command):
    """
    change directory working
    @param command : input from user (list)
    @return None
    """
    # change directory working become home
    oldpwd = getcwd()
    if len(command) == 1:
        if environ.get('HOME'):
            try:
                chdir(environ['HOME'])
            except FileNotFoundError:
                print("bash: cd: {}: No such file or directory".format(environ['HOME']))
                return 1
            else:
                environ['OLDPWD'] = oldpwd
                environ['PWD'] = getcwd()
                return 0
        else:
            print("bash: cd: HOME not set")
        return 1
    # change directory working
    try:
        chdir(abspath(command[1]))
    except FileNotFoundError:
        print("bash: cd: {}: No such file or directory".format(command[1]))
        return 1
    else:
        environ['OLDPWD'] = oldpwd
        environ['PWD'] = getcwd()
        return 0


def execute_shell(command):
    """
    execute commands of shell (ls, pwd, ...)
    @param command : input from user (list)
    @return None
    """
    # execute shell script
    if command[0].startswith("./"):
        return execute_command(command)
    # execute commands of shell
    try:
        list_path = environ['PATH'].split(':')
    except KeyError:
        print("bash: {}: command not found".format(command[0]))
        return 127
    for x in list_path:
        if exists(join(x, command[0])):
            return execute_command(command)
    print("bash: {}: command not found".format(command[0]))
    return 127


def execute_command(command):
    """
    execute shell script
    @param command : input from user (list)
    @return None
    """
    try:
        exit_code = call(command)
    except PermissionError:
        print("bash: {}: Permission denied".format(command[0]))
        return 126
    except FileNotFoundError:
        print("bash: {}: command not found".format(command[0]))
        return 127
    except OSError:
        print("bash: {}: cannot execute binary file".format(command[0]))
        return 126
    except CalledProcessError:
        return 1
    return exit_code

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
        print("bash: exit:")
    quit()