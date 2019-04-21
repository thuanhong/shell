from subprocess import run, PIPE


def backquote(command_str, pos, open, close):
    exe_command = command_str[pos:].partition(open)[-1].partition(close)[0]
    try:
        if not exe_command:
            raise ValueError()
        process_obj = run(exe_command, stdout=PIPE, encoding='utf-8')
    except ValueError:
        command_str = command_str.replace(open + exe_command + close, '')
    except Exception:
        print("bash: {}: command_str not found".format(exe_command))
        command_str = command_str.replace(open + exe_command + close, '')
    else:
        command_str = command_str[:pos] +\
                    command_str[pos:].replace(open + exe_command + close, process_obj.stdout[:-1])
    return command_str