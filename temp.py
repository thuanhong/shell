def raise_error_quotes(command_full_str, quote_char):
    if command_full_str.count(quote_char) % 2 != 0:
        raise SyntaxError('--Syntax Error--\n \
                          Missing closing "{}"\n \
                          Please input again'.format(quote_char))


def raise_error_brackets(command_full_str, open_bracket, close_bracket):
    count_open = command_full_str.count(open_bracket)
    count_close = command_full_str.count(close_bracket):
    if count_open > count_close:
        raise SyntaxError('--Syntax Error--\n \
                          Missing closing "{}"\n \
                          Please input again'.format(close_bracket))
    elif count_open < count_close:
        raise SyntaxError('')


def check_syntax(command_full_str):
    quotes_tuple = ("'", '"', "`")
    for ele in quotes_tuple:
        if ele in command_full_str:
            raise_error_quotes(command_full_str, ele)
    
    bracket_list = [["(", ")"], ["[", "]"], ["{", "}"]]
    for ele in bracket_list:
        if ele[0] in command_full_str:
            raise_error_brackets(command_full_str, ele[0], ele[1])