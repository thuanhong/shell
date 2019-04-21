def split_command(string):
    """
    divide input from user become the other commands
    The separator between elements is "&&" or "||" without backslash before its
    @param sring : input from user
    @return string need execute first, logical and the remains
    """
    bracket = {"{":"}", "(":")"}
    quote_single = True
    quote_double = True
    # the character closing
    closing = ''
    # true when the character checking in ${...} or $(...)
    process = False
    for index, char in enumerate(string):
        try:
            # character is double quoting and don't have backslash before it
            if char == '"' and string[index-1] != '\\':
                quote_double = not quote_double
            # character is single quoting and don't have backslash before it
            elif char == "'" and string[index-1] != '\\':
                quote_single = not quote_single
            # character is '$' and the next character is ( or { then turn on process 
            elif char == '$' and string[index+1] in bracket:
                process = True
                closing = bracket[string[index+1]]
            # turn off process when character is closing
            if process and char == closing:
                closing = ''
                process = False
            # when character not in quote and not process, check logical
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
    """
    take command have been divide and logical
    replace a part command
    @param command_str : input from user
    """
    temp_str, logical, command_str = split_command(command_str)
    command_str = command_str.replace(temp_str + logical, '')
    return temp_str, command_str, logical