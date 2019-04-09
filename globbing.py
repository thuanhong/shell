from os.path import expanduser, expandvars
from string import punctuation
from glob import glob


def handle_glob(command_str):
    return ' '.join(glob(command_str))


def titde_expansion(command_str, env):
    try:
        if command_str.startswith('~+/') or command_str == '~+':
            return command_str.replace('~+', env['PWD'])
        elif command_str.startswith('~-/') or command_str == '~-':
            return command_str.replace('~-', env['OLDPWD'])
        elif command_str.startswith('~/') or command_str == '~':
            return command_str.replace('~', expanduser('~'))
    except KeyError:
        return command_str


def replace_variable(string_origin, string_replace):
    if expandvars(string_replace) == string_replace:
        return string_origin.replace(string_replace, "")
    else:
        return string_origin.replace(string_replace, expandvars(string_replace))


def sub_param(string_origin):
    temp_str = string_origin.partition('${')[-1].partition('}')[0]
    if temp_str[0].isdigit() or any(x in temp_str for x in punctuation):
        return False
    else:
        temp_str = '${' + temp_str + '}'
        return replace_variable(string_origin, temp_str)


def param_expansion(command_str):
    output = command_str

    while '$' in output:
        index = output.index('$')
        if output[index+1] == '{':
            output = sub_param(output)
            if output == False:
                print('bash: {}: bad substitution'.format(command_str))
                return False
            continue
        
        if output[index+1].isdigit():
            output = replace_variable(output, output[index:index+2])
            continue

        for number, char in enumerate(output[index+1:], index+1):
            if char in punctuation:
                output = replace_variable(output, output[index:number])
                break
        else:
            if len(output[index:number]) != 1:
                output = replace_variable(output, output[index:number+1])

    return output