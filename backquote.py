from subprocess import run, PIPE


def backquote(command_str, pos):
    exe_command = command_str[pos:].partition('$(')[-1].partition(')')[0]
    try:
        if not exe_command:
            raise ValueError()
        process_obj = run(exe_command, stdout=PIPE, encoding='utf-8')
    except ValueError:
        command_str = command_str.replace("$("+ exe_command + ')', '')
    except Exception:
        print("bash: {}: command_str not found".format(exe_command))
        command_str = command_str.replace("$("+ exe_command + ')', '')
    else:
        command_str = command_str[:pos] +\
                    command_str[pos:].replace("$("+ exe_command + ')', process_obj.stdout[:-1])
    return command_str