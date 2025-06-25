import re

def transpile_conditional(line):
    """
    Transpiles conditional-related constructs (operators, if/else statements).
    Returns None if the line is not a conditional-related construct.
    
    Note: This function now only handles operator replacements in regular expressions.
    Control flow structures are handled at the file level.
    """
    
    # Skip control flow keywords - these are handled by file transpiler
    if (line.startswith("thereBe{") or line.startswith("}if(") or 
        line.startswith("}else if(") or line.startswith("alas{") or
        line == "}"):
        return None
    
    # Apply conditional operator replacements to regular expressions
    original_line = line
    line = replace_conditional_operators(line)
    
    # Only return the modified line if changes were made
    if line != original_line:
        return line
    
    return None

def replace_conditional_operators(text):
    """
    Replace TinyPy conditional operators with Python equivalents.
    """
    # Replace boolean values
    text = re.sub(r'\btrue\b', 'True', text)
    text = re.sub(r'\bfalse\b', 'False', text)
    
    # Replace logical operators
    text = re.sub(r'\&\&', ' and ', text)
    text = re.sub(r'\|\|', ' or ', text)
    text = re.sub(r'\!([^=])', r' not \1', text)  # ! but not !=
    
    # Replace comparison operators  
    text = re.sub(r'\!\=', ' != ', text)
    text = re.sub(r'\=\=', ' == ', text)
    
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text