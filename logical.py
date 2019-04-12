from quoting import remove_backslash


def split_command(string):
    quote_char = ('"', "'")
    quote = True
    string = remove_backslash(string)
    for index, char in enumerate(string):
        if char in quote_char:
            quote = not quote
        if char == "&" and quote:
            if char != string[-1] and string[index+1] == '&':
                return string[:index], '&&', string
            return string[:index], '&', string
        if char == "|" and quote:
            if string[index+1] == '|':
                return string[:index], "||", string
    return string, '', string


def handle_logical(command_str):
    temp_str, logical, command_str = split_command(command_str)
    command_str = command_str.replace(temp_str + logical, '')
    return temp_str, command_str, logical