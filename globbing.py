from os.path import expanduser, expandvars
from glob import glob


def globbing(command_list):
    globbed = []
    for arg in command_list:
        if any(x in arg for x in ['*', '?', '[', ']']):
            globbed.extend(glob(arg))
        else:
            globbed.append(arg)
    return globbed