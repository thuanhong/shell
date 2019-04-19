from glob import glob


def globbing(command_list):
    globbed = []
    for arg in command_list:
        if any(x in arg for x in ['*', '?', '[', ']']):
            if glob(arg):
                globbed.extend(glob(arg))
        else:
            globbed.append(arg)
    return globbed