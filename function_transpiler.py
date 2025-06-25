import re

# Pattern for function definitions
FUNC_DEF_PATTERN = r'^(int|bool|char|float|string|dyn)\s+(\w+)\((.*)\)\s*{'

def transpile_function(line):
    """
    Transpiles function-related constructs (definitions and return statements).
    Returns None if the line is not a function-related construct.
    """
    # Function definitions
    match = re.match(FUNC_DEF_PATTERN, line)
    if match:
        return_type, func_name, param_list = match.groups()
        # Handle empty parameter list
        if not param_list.strip():
            return f'def {func_name}():'
        # Split parameters and extract variable names
        params = []
        for param in param_list.split(','):
            param = param.strip()
            if not param:
                continue
            # Match parameter format: optional type followed by name
            param_match = re.match(r'^(?:(int|bool|char|float|string|dyn)\s+)?(\w+)$', param)
            if param_match:
                _, var_name = param_match.groups()
                params.append(var_name)
            else:
                # Fallback: use the whole parameter
                params.append(param)
        py_param_list = ', '.join(params)
        return f'def {func_name}({py_param_list}):'

    # Return statements
    if line.startswith("ret "):
        return "return " + line[4:]

    # Closing brace (function end)
    if line == "}":
        return ""

    return None