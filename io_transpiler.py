import re

def transpile_io(line):
    """
    Transpiles I/O-related constructs including individual data structure input operations.
    Returns None if the line is not recognized.
    """
    
    # Handle display/print: disp << "hello"; or disp<<"hello", var;
    if line.strip().startswith("disp"):
        # Remove 'disp <<' or 'disp<<' with any spacing, and optional trailing semicolon
        normalized_line = re.sub(r'^disp\s*<<\s*', '', line.strip())
        normalized_line = normalized_line.rstrip(';')
        
        # Match string literals, variables, or numbers
        parts = re.findall(r'"[^"]*"|\w+|\d+', normalized_line)
        if parts:
            return "print(" + ", ".join(parts) + ")"
        return None
    
    # Handle single variable input: enter("%i", x)
    if line.strip().startswith("enter(") and not '[' in line:
        match = re.match(r'enter\(\s*"%(\w+)"\s*,\s*(\w+)\s*\)', line.strip().rstrip(';'))
        if match:
            fmt, var = match.groups()
            if fmt == 'i': return f"{var} = int(input())"
            if fmt == 'f': return f"{var} = float(input())"
            if fmt == 'b': return f"{var} = input().lower() in ['true', '1']"
            if fmt == 'c': return f"{var} = input()[0]"
            if fmt == 's' or fmt == 'dy': return f"{var} = input()"
    
    # Handle array element input: enter("%i", arr[index])
    array_input_result = transpile_array_input(line)
    if array_input_result:
        return array_input_result
    
    # Handle dictionary element input: enter("%i", dict[key])
    dict_input_result = transpile_dict_input(line)
    if dict_input_result:
        return dict_input_result
    
    return None

def transpile_array_input(line):
    """
    Handle input into specific array elements.
    Format: enter("%i", arr[index]);
    """
    match = re.match(r'enter\(\s*"%(\w+)"\s*,\s*(\w+)\[([^\]]+)\]\s*\)', line.strip().rstrip(';'))
    if match:
        fmt, array_name, index = match.groups()
        
        if fmt == 'i':
            return f"{array_name}[{index}] = int(input())"
        elif fmt == 'f':
            return f"{array_name}[{index}] = float(input())"
        elif fmt == 'b':
            return f"{array_name}[{index}] = input().lower() in ['true', '1']"
        elif fmt == 'c':
            return f"{array_name}[{index}] = input()[0]"
        elif fmt == 's' or fmt == 'dy':
            return f"{array_name}[{index}] = input()"
    
    return None

def transpile_dict_input(line):
    """
    Handle input into specific dictionary elements.
    Format: enter("%i", dict[key]);
    """
    match = re.match(r'enter\(\s*"%(\w+)"\s*,\s*(\w+)\[([^\]]+)\]\s*\)', line.strip().rstrip(';'))
    if match:
        fmt, dict_name, key = match.groups()
        
        # Handle string keys (remove quotes if present for the key lookup)
        if key.startswith('"') and key.endswith('"'):
            key_for_access = key
        elif key.isdigit():
            key_for_access = key
        else:
            # Variable key
            key_for_access = key
        
        if fmt == 'i':
            return f"{dict_name}[{key_for_access}] = int(input())"
        elif fmt == 'f':
            return f"{dict_name}[{key_for_access}] = float(input())"
        elif fmt == 'b':
            return f"{dict_name}[{key_for_access}] = input().lower() in ['true', '1']"
        elif fmt == 'c':
            return f"{dict_name}[{key_for_access}] = input()[0]"
        elif fmt == 's' or fmt == 'dy':
            return f"{dict_name}[{key_for_access}] = input()"
    
    return None