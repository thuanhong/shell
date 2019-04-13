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


