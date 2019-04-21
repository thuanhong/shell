from os.path import expanduser, expandvars
from backquote import backquote


def titde_expansion(command_str, env):
    """
    handle titde expansion by replace string
    @param command_str : command from user
    @param env : environment variable (os.environ)
    @return a command was replace if it contain titde, otherwise return command normal
    """
    try:
        if command_str.startswith('~+/') or command_str == '~+':
            return command_str.replace('~+', env['PWD'])
        elif command_str.startswith('~-/') or command_str == '~-':
            return command_str.replace('~-', env['OLDPWD'])
        elif command_str.startswith('~/') or command_str == '~':
            return command_str.replace('~', expanduser('~'))
    except KeyError:
        return command_str


def replace_variable(string_origin, string_replace, exit_code):
    """
    Change the variable by its own value or exit code
    @param string_origin : the string be changed content
    @param string_replace : the content need changed
    @return string have changed content
    """
    # replace string by exit code
    if string_replace in ['${?}', '$?']:
        return string_origin.replace(string_replace, str(exit_code))
    # replace string by empty
    elif expandvars(string_replace) == string_replace:
        return string_origin.replace(string_replace, "")
    # replace string by value variable
    else:
        return string_origin.replace(string_replace, expandvars(string_replace))


def param_expand_bracket(string_origin, pos, exit_code):
    """
    handle the variables with '${...}'
    @param stirng_origin : the string be changed content
    @param pos : the position start of string need check (to get string from a index satisfy)
    @return string have changed content or raise Syntax if string have special character
    """
    punctuation = '!"#$%&()*+,-./:;<=>@[\]^_`{|}~' + "'"
    # get substring between '${' and '}'
    temp_str = string_origin[pos:].partition('${')[-1].partition('}')[0]
    # check substring
    if temp_str[0].isdigit() or any(x in temp_str for x in punctuation):
        raise SyntaxError('bash: {}: bad substitution'.format(string_origin))
    else:
        temp_str = '${' + temp_str + '}'
        return replace_variable(string_origin, temp_str, exit_code)


def param_expand(command_str, index, exit_code):
    """
    handle the variables with '$...'
    @param command_str : the string be changed content
    @param index : the position start of string need check (to get string from a index satisfy)
    @return string have changed content
    """
    punctuation = '!"#$%&()*+,-./:;<=>@[\]^_`{|}~' + "'"
    # this case is : $1, $2, $9, ...
    if command_str[index+1].isdigit():
        command_str = replace_variable(command_str, command_str[index:index+2], exit_code)
        return command_str
    # replace string $...
    for number, char in enumerate(command_str[index+1:], index+1):
        if char == '?':
            command_str = replace_variable(command_str, command_str[index:number+1], exit_code)
            break
        # check special character
        if char in punctuation:
            command_str = replace_variable(command_str, command_str[index:number], exit_code)
            break
    else:
        if len(command_str[index:number]) != 1:
            command_str = replace_variable(command_str, command_str[index:number+1], exit_code)
    return command_str


def handling_dollar(command_str, exit_code):
    """
    handle parameter expandsion, backquote
    @param command_str : the string be changed content
    @param exit code : exit code of the previous execute
    @return another string of raise SyntaxError
    """
    output = command_str
    pos = 0
    while '$' in output[pos:]:
        try:
            index = output.index('$', pos)
            # if the previous character is backslash
            if output[index-1] == '\\' and index != 0:
                if output[index+1] == '(':
                    raise SyntaxError("bash: syntax error near unexpected token `(")
                pos = index + 1
            # replace string ${...} print error and eixt function if it have error
            elif output[index+1] == '{':
                output = param_expand_bracket(output, index, exit_code)
            # execute backquote (if possible)
            elif output[index+1] == '(':
                output = backquote(output, index)
            else:
                output = param_expand(output, index, exit_code)
        except IndexError:
            break
    return output