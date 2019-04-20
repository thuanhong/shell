import readline
import os
import sys
import re



def history(variable):
    """get the history of commands that had been used"""
    for i in range(1,readline.get_current_history_length()+1):
        print("%3d %s" % (i, readline.get_history_item(i)))


def get_file_history(file_history):
    """get the content of the file realine of history"""
    try:
        f = open(file_history, 'r')
        with f as file:
            return [line[:-1] for line in file.readlines()]
    except Exception:
        return []


def save_history_file(file_history, command_input):
    try:
        with open(file_history, 'a+') as file:
            file.write(user_input + '\n')
    except Exception:
        pass


def save_command_input(file_history, set_variables, command_input):
    if command_input:
        save_history_file(file_history, set_variables)
        set_variables['history'].append(command_input)


def print_all_history(history_content):
    tab = len(str(len(history_content)))
    for line, content in enumerate(history_content, 1):
        print('{}{}  {}'.format(
            (tab - len(str(line)) + 2) * ' ',
            line,
            content))


def print_part_history(history_content, number):
    tab = len(str(len(history_content)))
    start = len(history_content) - number
    for line, content in enumerate(history_content[start:], start + 1):
        print('{}{}  {}'.format(
            (tab - len(str(line)) + 2) * ' ',
            line,
            content))


def show_history(arguments, set_variables):
    if set_variables['history']:
        if arguments and int(arguments[0]) < len(set_variables['history']):
            print_part_history(set_variables['history'], int(arguments[0]))
        else:
            print_all_history(set_variables['history'])


def find_command_history(command_input, set_variables):
    try:
        command_input = command_input.replace('!!', set_variables['history'][-1])
    except IndexError:
        pass
    for command in findall('\!\d+', command_input):
        try:
            command_input = command_input.replace(
                command, set_variables['history'][int(command[1:]) - 1])
        except IndexError:
            continue
    return command_input

if __name__ == '__main__':
    a = input("enter : ")
    find_command_history(a.split(),  )
