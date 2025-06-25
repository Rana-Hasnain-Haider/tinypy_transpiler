import re

def transpile_loop(line):
    """
    Transpiles loop-related constructs (for, while, foreach).
    Returns None if the line is not a loop-related construct.
    """
    for_result = transpile_for_loop(line)
    if for_result is not None:
        return for_result
    
    while_result = transpile_while_loop(line)
    if while_result is not None:
        return while_result

    foreach_result = transpile_foreach_loop(line)
    if foreach_result is not None:
        return foreach_result

    fordict_result = transpile_fordict_loop(line)
    if fordict_result is not None:
        return fordict_result

    if line.strip() == "}":
        return ""

    return None


def transpile_for_loop(line):
    """
    Transpiles for loops.
    Format: repeatFor(int i=0;i<10;i++){
    """
    pattern = r'^repeatFor\s*\(\s*(int|bool|char|float|string|dyn)?\s*(\w+)\s*=\s*([^;]+)\s*;\s*([^;]+)\s*;\s*(\w+)\+\+\s*\)\s*\{$'
    match = re.match(pattern, line)

    if match:
        var_type, var_name, start_value, condition, increment_var = match.groups()

        condition_match = re.match(r'(\w+)\s*(<|<=|!=|>|>=)\s*(.+)', condition.strip())
        if condition_match:
            cond_var, operator, limit = condition_match.groups()
            limit = limit.strip()

            if operator == '<':
                return f"for {var_name} in range({start_value}, {limit}):"
            elif operator == '<=':
                return f"for {var_name} in range({start_value}, ({limit}) + 1):"
            elif operator == '>':
                return f"for {var_name} in range({start_value}, {limit}, -1):"
            elif operator == '>=':
                return f"for {var_name} in range({start_value}, ({limit}) - 1, -1):"
            elif operator == '!=':
                return f"for {var_name} in range({start_value}, {limit}):"  # May need refining

        return f"for {var_name} in range({start_value}, {condition}):"

    return None


def transpile_while_loop(line):
    pattern = r'^repeatWhile\s*\(\s*(.+)\s*\)\s*\{$'
    match = re.match(pattern, line)

    if match:
        condition = match.group(1)
        condition = replace_conditional_operators(condition)
        return f"while {condition}:"

    return None


def transpile_foreach_loop(line):
    pattern = r'^for\s*\(\s*(\w+)\s*:\s*(\w+)\s*\)\s*\{$'
    match = re.match(pattern, line)

    if match:
        item_var, collection_var = match.groups()
        return f"for {item_var} in {collection_var}:"

    return None


def transpile_fordict_loop(line):
    pattern = r'^forDict\s*\(\s*(\w+)\s*,\s*(\w+)\s*:\s*(\w+)\s*\)\s*\{$'
    match = re.match(pattern, line)

    if match:
        key_var, value_var, dict_var = match.groups()
        return f"for {key_var}, {value_var} in {dict_var}.items():"

    return None


def replace_conditional_operators(text):
    text = re.sub(r'\btrue\b', 'True', text)
    text = re.sub(r'\bfalse\b', 'False', text)
    text = re.sub(r'\&\&', ' and ', text)
    text = re.sub(r'\|\|', ' or ', text)
    text = re.sub(r'\!([^=])', r' not \1', text)
    text = re.sub(r'\!\=', ' != ', text)
    text = re.sub(r'\=\=', ' == ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
