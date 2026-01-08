# auto_bug_fixer.py
"""
Auto Bug Fixer

A Python automation tool to scan Python files or folders for syntax errors.
Detects syntax issues and saves results in text, CSV, and JSON formats.
"""

import os
import csv
import json

def check_syntax(file_path):
    """
    Checks a Python file for syntax errors.
    Returns a list of errors or empty list if none.
    """
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        compile(code, file_path, "exec")  # This checks all syntax errors
    except SyntaxError as e:
        errors.append(f"{file_path}: {e}")
    except Exception as e:  # Catches file reading issues
        errors.append(f"{file_path}: {e}")
    return errors

def scan_folder(folder_path):
    """
    Scan all .py files in a folder (and subfolders) for syntax errors.
    """
    all_errors = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                errors = check_syntax(file_path)
                all_errors.extend(errors)
    return all_errors

def save_results(errors):
    """
    Save errors in text, CSV, and JSON formats.
    """
    # Save as text
    with open("scan_results.txt", "w", encoding="utf-8") as f:
        for e in errors:
            f.write(e + "\n")

    # Save as CSV
    with open("scan_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["File", "Error"])  # Header
        for e in errors:
            if ": " in e:
                file, error = e.split(": ", 1)
                writer.writerow([file, error])
            else:
                writer.writerow([e, "Unknown"])

    # Save as JSON
    json_data = {}
    for e in errors:
        if ": " in e:
            file, error = e.split(": ", 1)
            json_data[file] = error
        else:
            json_data[e] = "Unknown"
    with open("scan_results.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

    print("Results saved to scan_results.txt, scan_results.csv, and scan_results.json")

if __name__ == "__main__":
    folder = input("Enter folder path to scan: ")
    errors = scan_folder(folder)

    if errors:
        print("Syntax errors found:")
        for e in errors:
            print(e)
        save_results(errors)
    else:
        print("No syntax errors found!")

