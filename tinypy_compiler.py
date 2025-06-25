import sys
from file_transpiler import transpile_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tinypy_compiler.py <input.tpy>")
    else:
        transpile_file(sys.argv[1])