import glob
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
        
a = 'sdfdsfsdsdfsf&'
def split_command(string):
    quote_char = ('"', "'")
    quote = True
    string = remove_backslash(string)
    for index, char in enumerate(string):
        if char in quote_char:
            quote = not quote
        if char == "&" and quote:
            if string[index+1] == '&':
                print(2)
                return string[:index], '&&', string
            return string[:index], '&', string
        if char == "|" and quote:
            if string[index+1] == '|':
                return string[:index], "||", string
    return string, '', string
print(split_command(a))