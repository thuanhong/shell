from os.path import expanduser, expandvars
from string import punctuation


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
    """
    Change the variable by its own value
    """
    if expandvars(string_replace) == string_replace:
        return string_origin.replace(string_replace, "")
    else:
        return string_origin.replace(string_replace, expandvars(string_replace))


def sub_param(string_origin, pos, exit_code):
    """
    handle the variables start with '${'
    """
    # get substring between '${' and '}'
    temp_str = string_origin[pos:].partition('${')[-1].partition('}')[0]
    # check substring
    if temp_str[0].isdigit() or any(x in temp_str for x in punctuation):
        raise SyntaxError('bash: {}: bad substitution'.format(string_origin))
    else:
        temp_str = '${' + temp_str + '}'
        return replace_variable(string_origin, temp_str)


def param_expansion(command_str, exit_code):
    output = command_str
    # if '$?' in output:
    #     output = output.replace('$?', str(exit_code))
    # if '$#' in output:
    #     output = output.replace('$#', '0')
    pos = 0
    while '$' in output[pos:]:
        try:
            index = output.index('$', pos)
            if output[index-1] == '\\' or output[index+1] == '(':
                pos = index + 1
                continue
            # replace string ${...} print error and eixt function if it have error
            if output[index+1] == '{':
                output = sub_param(output, pos, exit_code)
                continue

            # this case is : $1, $2, $9, ...
            if output[index+1].isdigit():
                output = replace_variable(output, output[index:index+2])
                continue

            # replace string $...
            for number, char in enumerate(output[index+1:], index+1):
                if char in punctuation:
                    output = replace_variable(output, output[index:number])
                    break
            else:
                if len(output[index:number]) != 1:
                    output = replace_variable(output, output[index:number+1])
        except IndexError:
            break
    return output