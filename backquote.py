from subprocess import run, PIPE


def backquote(command_list):
    for order, command in enumerate(command_list):
        pos = 0
        while '$' in command[pos:]:
            index = command.index('$', pos)
            if command[index-1] == '\\' and command[index]:
                pos = index + 1
                continue
            exe_command = command[pos:].partition('$(')[-1].partition(')')[0]
            try:
                process_obj = run(exe_command, stdout=PIPE, encoding='utf-8')
            except Exception:
                print("bash: {}: command not found".format(exe_command))
                command = command.replace("$("+ exe_command + ')', '')
            else:
                command = command[:pos] +\
                            command[pos:].replace("$("+ exe_command + ')', process_obj.stdout[:-1])
        command_list[order] = command
    return command_list