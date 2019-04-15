import shlex

def remove_backslash(string):
    quote_tuple = ('"', "'")
    quote = True
    output = ""
    go_on = False
    for index, char in enumerate(string):
        if go_on:
            go_on = False
            continue
        if char in quote_tuple:
            quote = not quote
        elif char == '\\' and quote:
            if string[index+1] in ['(', ')', '&', '|']:
                go_on = True
            continue
        output += char
    return output


def add_input(command_full_str):
    while True:
        try:
            lex = shlex.shlex(command_full_str, posix=True)
            lex.whitespace_split = True
            lex.quotes += '`'
            list(lex)
            return command_full_str
        except ValueError:
            add_content = input('> ')
            command_full_str += add_content