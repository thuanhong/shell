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


# def handle_quoting(command_list):
#     for index, command in enumerate(command_list):
        