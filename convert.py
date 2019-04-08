from globbing import *
from os import environ


def convert_command(command_list):
    for number, ele in enumerate(command_list[1:], 1):
        if '$' in ele:
            command_list[number] = param_expansion(ele)
        if '~' in ele:
            command_list[number] = titde_expansion(ele, environ)
        if any(x in ele for x in ['*', '?', '[', ']']):
            command_list[number] = handle_glob(ele)


