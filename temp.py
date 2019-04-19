def backquote(command_list):
    for command in command_list:
        pos = 0
        while '$' in command[pos:]:
            index = command.index('$', pos)
            if command[index-1] == '\\':
                pos = index + 1
                continue
            exe_command = command[pos:].partition('${')[-1].partition('}')[0]