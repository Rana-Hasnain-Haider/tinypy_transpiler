import re

def transpile_datastructure(line):
    """
    Transpiles data structure constructs (arrays and dictionaries).
    Returns None if the line is not a data structure construct.
    """
    
    # Handle array declarations
    array_result = transpile_array(line)
    if array_result is not None:
        return array_result
    
    # Handle dictionary declarations
    dict_result = transpile_dictionary(line)
    if dict_result is not None:
        return dict_result
    
    return None

def transpile_array(line):
    """
    Transpiles array declarations.
    Formats:
    - int a[10];
    - int a[10] = {1,2,3,4,5,6,7,8,9,10};
    - dyn a[2] = {1,"S"};
    """
    
    # Pattern for array declaration with optional initialization
    # Matches: type name[size] or type name[size] = {values}
    pattern = r'^(int|bool|char|float|string|dyn)\s+(\w+)\[(\w+|\d+)\](\s*=\s*\{([^}]*)\})?$'
    match = re.match(pattern, line)
    
    if match:
        array_type, var_name, size, assignment_part, values = match.groups()
        
        if assignment_part:  # Array with initialization
            if values:
                # Parse the values
                value_list = parse_array_values(values, array_type)
                return f"{var_name} = {value_list}"
            else:
                # Empty initialization
                return f"{var_name} = []"
        else:  # Array without initialization
            if array_type == 'dyn':
                # Dynamic array - just create empty list
                return f"{var_name} = []"
            else:
                # Typed array - create list with default values based on size
                default_value = get_default_value(array_type)
                if size.isdigit():
                    return f"{var_name} = [{default_value}] * {size}"
                else:
                    # Size is a variable
                    return f"{var_name} = [{default_value}] * {size}"
    
    return None

def transpile_dictionary(line):
    """
    Transpiles dictionary declarations.
    Format: dict var <key_type,value_type>[size] = { key : value, key : value }
    """
    
    # Pattern for dictionary declaration
    # Matches: dict name <key_type,value_type>[size] = {key:value, key:value}
    pattern = r'^dict\s+(\w+)\s*<(\w+)\s*,\s*(\w+)>\s*\[(\w+|\d+)\](\s*=\s*\{([^}]*)\})?$'
    match = re.match(pattern, line)
    
    if match:
        var_name, key_type, value_type, size, assignment_part, pairs = match.groups()
        
        if assignment_part:  # Dictionary with initialization
            if pairs:
                # Parse the key-value pairs
                dict_content = parse_dict_pairs(pairs, key_type, value_type)
                return f"{var_name} = {dict_content}"
            else:
                # Empty initialization
                return f"{var_name} = {{}}"
        else:  # Dictionary without initialization
            return f"{var_name} = {{}}"
    
    return None

def parse_array_values(values_str, array_type):
    """
    Parse array values from string format to Python list format.
    """
    values = []
    
    # Split by comma, handling quoted strings
    parts = split_preserving_quotes(values_str)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Convert value based on array type
        if array_type == 'dyn':
            # Dynamic type - keep as is but handle strings and booleans
            values.append(convert_value(part))
        elif array_type == 'string':
            # String array - ensure all values are strings
            if not (part.startswith('"') and part.endswith('"')):
                part = f'"{part}"'
            values.append(part)
        elif array_type == 'bool':
            # Boolean array
            if part.lower() == 'true':
                values.append('True')
            elif part.lower() == 'false':
                values.append('False')
            else:
                values.append(part)
        else:
            # Numeric types (int, float, char)
            values.append(part)
    
    return '[' + ', '.join(values) + ']'

def parse_dict_pairs(pairs_str, key_type, value_type):
    """
    Parse dictionary key-value pairs from string format to Python dict format.
    """
    pairs = {}
    
    # Split by comma, handling quoted strings and nested structures
    parts = split_preserving_quotes(pairs_str)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Split by colon to get key and value
        if ':' in part:
            key_part, value_part = part.split(':', 1)
            key = convert_value(key_part.strip())
            value = convert_value(value_part.strip())
            pairs[key] = value
    
    # Format as Python dictionary
    pair_strings = []
    for key, value in pairs.items():
        pair_strings.append(f"{key}: {value}")
    
    return '{' + ', '.join(pair_strings) + '}'

def split_preserving_quotes(text):
    """
    Split text by comma while preserving quoted strings.
    """
    parts = []
    current = ""
    in_quotes = False
    quote_char = None
    
    for char in text:
        if char in ['"', "'"] and not in_quotes:
            in_quotes = True
            quote_char = char
            current += char
        elif char == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
            current += char
        elif char == ',' and not in_quotes:
            if current.strip():
                parts.append(current.strip())
            current = ""
        else:
            current += char
    
    if current.strip():
        parts.append(current.strip())
    
    return parts

def convert_value(value_str):
    """
    Convert a string value to appropriate Python representation.
    """
    value_str = value_str.strip()
    
    # Handle boolean values
    if value_str.lower() == 'true':
        return 'True'
    elif value_str.lower() == 'false':
        return 'False'
    
    # Handle string literals (keep quotes)
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return value_str
    
    # Handle numeric values
    if value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
        return value_str
    
    # Handle float values
    try:
        float(value_str)
        return value_str
    except ValueError:
        pass
    
    # Default: treat as variable name or string
    return value_str

def get_default_value(data_type):
    """
    Get default value for a given data type.
    """
    defaults = {
        'int': '0',
        'float': '0.0',
        'bool': 'False',
        'char': "''",
        'string': '""',
        'dyn': 'None'
    }
    return defaults.get(data_type, 'None')