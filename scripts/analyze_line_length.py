import os
import sys
from pathlib import Path

def analyze_line_lengths(directory):
    total_lines = 0
    total_length = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in lines:
                            # Skip empty lines and comments
                            if line.strip() and not line.strip().startswith('#'):
                                total_lines += 1
                                total_length += len(line.rstrip())
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    if total_lines > 0:
        average_length = total_length / total_lines
        print(f"Total lines analyzed: {total_lines}")
        print(f"Average line length: {average_length:.2f} characters")
    else:
        print("No Python files found or no valid lines to analyze.")

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    analyze_line_lengths(project_root)
