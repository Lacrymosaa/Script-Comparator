import os
import re
from difflib import unified_diff

def strip_comments_and_strings(line):
    line = re.sub(r'"[^"]*"', '', line)
    line = re.split(r'#', line)[0]
    return line.strip()

def extract_functions(file_path):
    functions = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_func = None
    func_lines = []
    func_start_line = 0

    for i, line in enumerate(lines):
        stripped_line = strip_comments_and_strings(line)
        if stripped_line.startswith('def '):
            if current_func:
                functions[current_func] = (func_start_line, func_lines)
            current_func = stripped_line[4:].split('(')[0].strip()
            func_lines = [strip_comments_and_strings(line)]
            func_start_line = i + 1
        elif current_func:
            func_lines.append(strip_comments_and_strings(line))
            if stripped_line == 'end':
                functions[current_func] = (func_start_line, func_lines)
                current_func = None
                func_lines = []

    return functions

def compare_functions(file1_path, file2_path):
    func1 = extract_functions(file1_path)
    func2 = extract_functions(file2_path)

    changes = []

    all_funcs = set(func1.keys()).union(set(func2.keys()))
    for func in all_funcs:
        if func not in func1:
            changes.append(f"Function '{func}' missing in {os.path.basename(file1_path)}")
        elif func not in func2:
            changes.append(f"Function '{func}' missing in {os.path.basename(file2_path)}")
        else:
            _, lines1 = func1[func]
            _, lines2 = func2[func]
            diff = list(unified_diff(lines1, lines2, lineterm='', fromfile=file1_path, tofile=file2_path))
            if diff:
                changes.append(f"\nFunction '{func}' differs:")
                changes.extend(diff)

    return changes

def compare_folders(folder1, folder2):
    changelog = []
    files1 = {f for f in os.listdir(folder1) if f.endswith('.rb')}
    files2 = {f for f in os.listdir(folder2) if f.endswith('.rb')}
    common_files = files1 & files2

    for file in sorted(common_files):
        file1_path = os.path.join(folder1, file)
        file2_path = os.path.join(folder2, file)
        changes = compare_functions(file1_path, file2_path)
        if changes:
            changelog.append(f"\n### Changes in file: {file}")
            changelog.extend(changes)

    return '\n'.join(changelog)

if __name__ == "__main__":
    folder1 = "19.1"
    folder2 = "21.1"
    log = compare_folders(folder1, folder2)

    output_path = "changelog.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(log if log else "No differences found.")
    print(f"Changelog exported to {output_path}")
