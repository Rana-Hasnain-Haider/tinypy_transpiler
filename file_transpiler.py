import os
import re
from line_transpiler import transpile_line
from function_transpiler import FUNC_DEF_PATTERN
from conditional_transpiler import replace_conditional_operators

def find_matching_condition(lines, start_index):
    brace_count = 1
    i = start_index + 1

    while i < len(lines) and brace_count > 0:
        line = lines[i].strip()

        if line.startswith("}if(") or line.startswith("}else if(") or line.startswith("alas{"):
            return i, line
        elif line == "}":
            brace_count -= 1
            if brace_count == 0 and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith("if(") or next_line.startswith("else if("):
                    return i + 1, next_line
        elif line.endswith("{"):
            brace_count += 1

        i += 1

    return None, None

def transpile_file(input_path, output_path=None):
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".py"

    with open(input_path, 'r') as f:
        lines = f.readlines()

    output_lines = []
    indent_level = 0
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Handle thereBe{ ... }if(...) and }else if(...) and alas{
        if line.startswith("thereBe{"):
            condition_index, condition_line = find_matching_condition(lines, i)

            if condition_index is not None and condition_line:
                block_lines = []
                j = i + 1
                while j < condition_index:
                    current_line = lines[j].strip()
                    if current_line and current_line != "}":
                        block_lines.append(lines[j])
                    j += 1

                if condition_line.startswith("}if("):
                    match = re.match(r'^}if\s*\(\s*(.+)\s*\)$', condition_line)
                    if match:
                        condition = replace_conditional_operators(match.group(1))
                        output_lines.append("    " * indent_level + f"if {condition}:")
                        indent_level += 1
                        for block_line in block_lines:
                            py_line = transpile_line(block_line)
                            if py_line:
                                output_lines.append("    " * indent_level + py_line)
                        indent_level -= 1
                        i = condition_index + 1
                        continue

                elif condition_line.startswith("}else if("):
                    match = re.match(r'^}else\s+if\s*\(\s*(.+)\s*\)$', condition_line)
                    if match:
                        condition = replace_conditional_operators(match.group(1))
                        output_lines.append("    " * indent_level + f"elif {condition}:")
                        indent_level += 1
                        for block_line in block_lines:
                            py_line = transpile_line(block_line)
                            if py_line:
                                output_lines.append("    " * indent_level + py_line)
                        indent_level -= 1
                        i = condition_index + 1
                        continue

            i += 1
            continue

        # Handle alas{
        if line.startswith("alas{"):
            output_lines.append("    " * indent_level + "else:")
            indent_level += 1
            j = i + 1
            while j < len(lines):
                current_line = lines[j].strip()
                if current_line == "}":
                    indent_level -= 1
                    i = j + 1
                    break
                py_line = transpile_line(lines[j])
                if py_line:
                    output_lines.append("    " * indent_level + py_line)
                j += 1
            continue

        # Handle function definitions
        if re.match(FUNC_DEF_PATTERN, line):
            output_lines.append("    " * indent_level + transpile_line(lines[i]))
            indent_level += 1
            i += 1
            continue

        # Handle line ending with '{' (like loops or custom blocks)
        if line.endswith("{"):
            py_line = transpile_line(line)
            if py_line:
                output_lines.append("    " * indent_level + py_line)
            indent_level += 1
            i += 1
            continue

        # Handle closing brace
        if line == "}" and indent_level > 0:
            indent_level -= 1
            i += 1
            continue

        # Skip redundant TinyPy-style condition tokens
        if line.startswith("}if(") or line.startswith("}else if(") or line.startswith("if(") or line.startswith("else if("):
            i += 1
            continue

        # Normal line
        py_line = transpile_line(lines[i])
        if py_line:
            output_lines.append("    " * indent_level + py_line)
        i += 1

    # Auto-insert main() call if main() is defined
    if any("def main(" in l for l in output_lines):
        output_lines.append("")
        output_lines.append('if __name__ == "__main__":')
        output_lines.append("    main()")

    with open(output_path, 'w') as f:
        f.write("\n".join(output_lines))

    print(f"✅ Transpiled to {output_path}")
    return output_path
