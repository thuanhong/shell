from globbing import globbing
from path_expandsion import handling_dollar, titde_expansion


def convert_command_str(command_str, environ, exit_code):
    """
    convert command become another to execute easier
    @param command_str : the string need convert
    @param environ : environment variable
    @return the string have convert
    """
    quote = False
    # check quote in string
    if command_str.startswith('"') or command_str.startswith("'"):
        if command_str.startswith('"'):
            quote = True
            command_str = command_str[1:-1]
        else:
            return command_str[1:-1]

    # parameter expandsion, backquote
    if '$' in command_str:
        command_str = handling_dollar(command_str, exit_code)

    # titde expandsion
    if command_str.startswith('~') and not quote:
        command_str = titde_expansion(command_str, environ)

    return command_str


def handle_user_input(command):
    """
    check input from user
    if input not right , display ">" in new line and continue input
    the string just input from user
    @param command : input from user
    @return a input valid
    """
    while True:
        try:
            bracket = {"{":"}", "(":")"}
            quote_single = True
            quote_double = True
            go_on = False
            closing = ''
            process = False
            for index, char in enumerate(command):
                if go_on:
                    go_on = False
                    continue
                if char == '\\':
                    go_on = True
                # check open double quoting
                elif char == '"':
                    quote_double = not quote_double
                # check open single quoting
                elif char == "'":
                    quote_single = not quote_single
                if quote_single and quote_double:
                    if not process and char == '$' and char != command[-1]\
                    and command[index+1] in bracket:
                        closing = bracket[command[index+1]]
                        process = True
                    elif char == closing:
                        process = False
            else:
                if process or not quote_double or not quote_single:
                    raise ValueError("")
        except ValueError:
            add_content = input('> ')
            command += add_content
        else:
            return command


def convert_command_list(command_list, environ, exit_code):
    """
    convert all part in command list become another to execute easier
    @param command_list : the list contain all part command
    @param environ : environment variable
    @return a list contain all part have convert
    """
    for index, ele in enumerate(command_list):
        if not any(x in ele for x in ['"', "'"]):
            command_list[index] = convert_command_str(ele, environ, exit_code)
            continue
        output = ''
        out = ''
        closing = ''
        go_on = False
        for x, y in enumerate(ele):
            if go_on:
                go_on = False
            elif y == '\\':
                go_on = True
            elif not closing:
                if y == '"':
                    closing = ('"', x)
                elif y == "'":
                    closing = ("'", x)
                else:
                    out += y
            else:
                if y == closing[0]:
                    output += convert_command_str(out, environ, exit_code) +\
                                convert_command_str(ele[closing[1]:x+1], environ, exit_code)
                    out = ''
                    closing = ''
                    
        command_list[index] = output + out
    return globbing(command_list)
