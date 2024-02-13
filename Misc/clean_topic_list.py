import re

file_path = 'topics1.md'
output_file_path = 'topics2.md'

timestamp_pattern = re.compile(r'^\d+:\d+:\d+\s')

with open(file_path, 'r') as file:
    lines = file.readlines()

cleaned_lines = [timestamp_pattern.sub('', line) for line in lines]

with open(output_file_path, 'w') as file:
    file.writelines(cleaned_lines)