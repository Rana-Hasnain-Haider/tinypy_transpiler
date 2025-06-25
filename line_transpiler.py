from function_transpiler import transpile_function
from variable_transpiler import transpile_variable
from io_transpiler import transpile_io
from conditional_transpiler import transpile_conditional, replace_conditional_operators
from datastructure_transpiler import transpile_datastructure
from loop_transpiler import transpile_loop

def transpile_line(line):
    """
    Transpiles a single line by delegating to specialized transpilers.
    """
    line = line.strip()

    # Ignore empty lines and comments
    if not line or line.startswith("//"):
        return ""

    # Remove trailing semicolons
    if line.endswith(";"):
        line = line[:-1]

    # Try each specialized transpiler in order
    # Data structures should be checked before variables since they have more specific patterns
    # Loops should be checked early since they have specific patterns too
    for transpiler in [transpile_function, transpile_datastructure, transpile_loop, transpile_variable, transpile_io, transpile_conditional]:
        result = transpiler(line)
        if result is not None:
            return result

    # Apply conditional operator replacements to any remaining lines
    line = replace_conditional_operators(line)
    
    # Default fallthrough: return the processed line
    return line