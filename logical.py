def logical(command_str):
    if '&&' in command_str and '||' in command_str:
        posx = command_str.index('&&')
        posy = command_str.index('||')
        if posx > posy:
            return command_str.partition('||')
        else:
            return command_str.partition('&&')
    elif '&&' in command_str and '||' not in command_str:
        pass
        