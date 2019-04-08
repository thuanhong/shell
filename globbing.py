from glob import glob
from os.path import expanduser, expandvars
import os


def handle_glob(command_str):
    return ' '.join(glob(command_str))


def replace(string, old_str, new_str):
    try:
        return string.replace(old_str, new_str)
    except KeyError:
        return string


def titde_expansion(command_str, env):
    if command_str.startswith('~+/') or command_str == '~+':
        return replace(command_str, '~+', env['PWD'])
    elif command_str.startswith('~-/') or command_str == '~-':
        return replace(command_str, '~-/', env['OLDPWD'])
    elif command_str.startswith('~/') or command_str == '~':
        return replace(command_str, '~', expanduser('~'))


def param_expansion(command_str):
    output = command_str
    special_char = ['!', '@', '#', '$', '%', '^', '&', '*',
                    '(', ')', '{', '}', '?', ':', ',', '.'
                    '[', ']']
    while '${' in output:
        temp_str = output.partition('${')[-1].partition('}')[0]

        if temp_str[0].isdigit() or any(x in temp_str for x in special_char):
            print('bash: {}: bad substitution'.format(command_str))
            print(temp_str)
            return False
        else:
            temp_str = '${' + temp_str + '}'
            if expandvars(temp_str) == temp_str:
                output = output.replace(temp_str, "")
            else:
                output = output.replace(temp_str, expandvars(temp_str))

    while '$' in output:
        index = output.index('$')
        
        if output[index+1].isdigit():
            if expandvars(output[index:index+2]) == output[index:index+2]:
                output = output.replace(output[index:index+2], "")
            else:
                output = output.replace(output[index:index+2], expandvars(output[index:index+2]))
            continue
        for number, char in enumerate(output[index+1:], index+1):
            if char in special_char:
                if expandvars(output[index:number]) == output[index:number]:
                    output = output.replace(output[index:number], "")
                else:
                    output = output.replace(output[index:number], expandvars(output[index:number]))
                break
        else:
            if len(output[index:number]) != 1:
                if expandvars(output[index:number]) == output[index:number]:
                    output = output.replace(output[index:number], "")
                else:
                    output = output.replace(output[index:number], expandvars(output[index:number]))

    return output