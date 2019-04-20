from quoting import remove_backslash


def split_command(string):
    bracket = {"{":"}", "(":")"}
    quote_single = True
    quote_double = True
    closing = ''
    process = False
    for index, char in enumerate(string):
        try:
            if char == '"' and string[index-1] != '\\':
                quote_double = not quote_double
            elif char == "'" and string[index-1] != '\\':
                quote_single = not quote_single
            elif char == '$' and string[index+1] in bracket:
                process = True
                closing = bracket[string[index+1]]
            if process and char == closing:
                closing = ''
                process = False
            if quote_single and quote_double and not process:
                if char == "&":
                    if char != string[-1] and string[index+1] == '&':
                        return string[:index], '&&', string
                    return string[:index], '&', string
                elif char == "|":
                    if char != string[-1] and string[index+1] == '|':
                        return string[:index], "||", string
        except IndexError:
            pass
    return string, '', string


def handle_logical(command_str):
    temp_str, logical, command_str = split_command(command_str)
    command_str = command_str.replace(temp_str + logical, '')
    return temp_str, command_str, logical