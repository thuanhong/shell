from subprocess import run, PIPE


def backquote(command_str, pos, open_char, close_char):
    """
    handling backquote
    @param command_str : string contain command need execute
    @param pos : the position start of string need check (to get string from a index satisfy)
    @param open_char : the character begin, "$(" or "`"
    @param close_char : the character end, ")" or "`"
    @return string after replace (if possible)
    """
    exe_command = command_str[pos:].partition(open_char)[-1].partition(close_char)[0]
    try:
        if not exe_command:
            raise ValueError()
        process_obj = run(exe_command, stdout=PIPE)
    except ValueError:
        command_str = command_str.replace(open_char + exe_command + close_char, '')
    except Exception as e:
        print("bash: {}: command not found".format(exe_command))
        command_str = command_str.replace(open_char + exe_command + close_char, '')
    else:
        command_str = command_str[:pos] +\
                    command_str[pos:].replace(open_char + exe_command + close_char, process_obj.stdout[:-1].decode())
    return command_str