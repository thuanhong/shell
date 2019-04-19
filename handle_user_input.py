from globbing import globbing
from path_expandsion import param_expansion, titde_expansion


def convert_command_str(command_str, environ, exit_code):
    quote = False
    # quoting " '
    if command_str.startswith('"') or command_str.startswith("'"):
        if command_str.startswith('"'):
            quote = True
            command_str = command_str[1:-1]
        else:
            return command_str[1:-1]
    # parameter expandsion
    if '$' in command_str:
        command_str = param_expansion(command_str, exit_code)
    
    # titde expandsion
    if command_str.startswith('~') and not quote:
        command_str = titde_expansion(command_str, environ)

    return command_str


def handle_user_input(command):
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
                elif char == '"':
                    quote_double = not quote_double
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
