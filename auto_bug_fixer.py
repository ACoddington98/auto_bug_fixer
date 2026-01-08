# auto_bug_fixer.py
import os
import ast

def check_syntax(file_path):
    """
    Checks Python file for syntax errors.
    Returns a list of errors or empty list if none.
    """
    errors = []
    with open(file_path, "r") as f:
        code = f.read()
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append(f"{file_path}: {e}")
    return errors

def scan_folder(folder_path):
    """
    Scan all .py files in a folder for syntax errors.
    """
    all_errors = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                errors = check_syntax(file_path)
                all_errors.extend(errors)
    return all_errors

if __name__ == "__main__":
    folder = input("Enter folder path to scan: ")
    errors = scan_folder(folder)
    if errors:
        print("Syntax errors found:")
        for e in errors:
            print(e)
    else:
        print("No syntax errors found!")
