import shlex

def raise_error(command_full_str, quote_char):
    if quote_char in command_full_str:
        if command_full_str.count(quote_char) % 2 != 0:
            raise SyntaxError('--Syntax Error--\nMissing closing\nPlease input again')


def check_syntax(command_full_str):
    tup = ("'", '"', "`")
    for ele in tup:
        raise_error(command_full_str, ele)
    if '(' in command_full_str:
        if command_full_str.count('(') != command_full_str.count(')'):
            raise SyntaxError('--Syntax Error--\nMissing closing "{}"\nPlease input again'.format(')'))
    if '[' in command_full_str:
        if command_full_str.count('[') != command_full_str.count(']'):
            raise SyntaxError('--Syntax Error--\nMissing closing "{}"\nPlease input again'.format(']'))
    if '{' in command_full_str:
        if command_full_str.count('{') != command_full_str.count('}'):
            raise SyntaxError('--Syntax Error--\nMissing closing "{}"\nPlease input again'.format('}'))
    print(command_full_str)
a = 'echo dfsdfsdfsd((sfdsfsdfdsfsdfsdf}}'
try:
    check_syntax(a)
except Exception as t:
    print(t)