import re

def transpile_variable(line):
    """
    Transpiles variable-related constructs (declarations, constants, globals, inc/dec).
    Returns None if the line is not a variable-related construct.
    """
    # Variable declarations (with or without assignment)
    match = re.match(r'^(int|bool|char|float|string|dyn)\s+(\w+)(\s*=\s*.+)?$', line)
    if match:
        var_type, var_name, assignment = match.groups()
        if assignment:
            # Handle boolean value conversion
            assignment_value = assignment.split('=', 1)[1].strip()
            if assignment_value.lower() == 'true':
                assignment_value = 'True'
            elif assignment_value.lower() == 'false':
                assignment_value = 'False'
            return f"{var_name} = {assignment_value}"
        else:
            return f"{var_name} = None"

    # Constant declaration (brick keyword)
    if line.startswith("brick "):
        const_line = line.replace("brick ", "")
        # Handle boolean constants
        const_line = const_line.replace(' true', ' True').replace(' false', ' False')
        return const_line

    # Global variable declaration (universal keyword)
    if line.startswith("universal "):
        return line.replace("universal ", "global ")

    # Increment/decrement operators
    if re.match(r'^\w+\+\+$', line):
        return line[:-2] + ' += 1'
    if re.match(r'^\w+\-\-$', line):
        return line[:-2] + ' -= 1'

    return None