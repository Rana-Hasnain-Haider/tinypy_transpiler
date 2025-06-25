# 🐍 TinyPy Transpiler

TinyPy is a statically and dynamically typed, C++-style language designed for educational and experimental purposes. This project includes a **TinyPy-to-Python transpiler**, which translates TinyPy source code into executable Python code.

## 📜 Overview

TinyPy aims to make learning programming fun and structured. It features:
- Familiar C/C++-like syntax
- Static and dynamic typing
- Support for arrays, dictionaries, and basic I/O
- Auto-detection of `main()` function
- Seamless Python transpilation

This repository includes:
- 💻 Language Syntax Guide
- 🔧 Transpilation Logic for Each Construct
- 📂 Transpiler Modules (organized by language features)
- 🧪 Sample Programs and Test Cases

---

## 📦 Features

### ✅ Language Syntax
- **Data Types:** `int`, `float`, `bool`, `char`, `string`, `dyn`
- **Variables & Constants:** `brick` for constants, `universal` for global vars
- **Control Flow:** `thereBe { } if (...)`, `} else if (...)`, `alas { }`
- **Loops:** `repeatFor(...)`, `repeatWhile(...)`, `for(...)`, `forDict(...)`
- **I/O:** `disp << ...`, `enter(...)`
- **Functions:** Defined with typed return and parameters using `ret`
- **Arrays & Dictionaries:** First-class support with static/dynamic types

### 🧠 Transpilation Highlights
Each TinyPy feature is transpiled to Python using custom modules:
- `function_transpiler.py` for functions and return statements
- `variable_transpiler.py` for variable, constant, and global declarations
- `loop_transpiler.py` for `for`, `while`, `foreach`, and `fordict` loops
- `conditional_transpiler.py` for conditions, comparisons, and booleans
- `io_transpiler.py` for handling input/output operations
- `datastructure_transpiler.py` for arrays and dictionaries
- `file_transpiler.py` manages block structure, indentation, and main function injection

---

## 🚀 Getting Started
#####refer to readme.txt in this repositry

### 🔧 Requirements
- Python 3.8+
- `re` (standard library)
- Works on Windows, Linux, and macOS

### 📁 Project Structure
