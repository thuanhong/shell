from globbing import globbing
from path_expandsion import param_expansion, titde_expansion


def convert_command(command_list, environ, exit_code):
    for number, ele in enumerate(command_list):
        # parameter expandsion
        if '$' in ele:
            command_list[number] = param_expansion(ele, exit_code)
            if command_list[number] == False:
                return False
            ele = command_list[number]
        
        # titde expandsion
        if ele.startswith('~'):
            command_list[number] = titde_expansion(ele, environ)
            ele = command_list[number]
    
    return globbing(command_list)


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


