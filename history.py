import readline


def history(command):
    """print the line of history"""
    exit_code = 0
    if len(command) == 1:
        for i in range(1, readline.get_current_history_length()+1):
            print("%3d %s" % (i, readline.get_history_item(i)))
        return exit_code
