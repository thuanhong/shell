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
                    elif char == '$' and not process:
                        