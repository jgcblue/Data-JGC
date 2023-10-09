#!/bin/bash

# Start directory
start_directory="./app"

# Output file
output_file="combined_output.txt"

# Empty the output file first
> $output_file

# Avoid these directories and files
avoid_list="tags venv logs .git __pycache__ migrations"

# Add top-level .py files first
for file in ./*.py; do
    echo "==== $file ====" >> $output_file
    cat "$file" >> $output_file
    echo -e "\n\n" >> $output_file
done

# Find and concatenate Python and Jinja HTML template files from the app directory
find $start_directory -type f \( -name "*.py" -o -name "*.html" \) | while read file; do
    skip=false
    for avoid in $avoid_list; do
        if [[ $file == *$avoid* ]]; then
            skip=true
            break
        fi
    done
    if ! $skip; then
        echo "==== $file ====" >> $output_file
        cat "$file" >> $output_file
        echo -e "\n\n" >> $output_file
    fi
done

echo "Files concatenated into $output_file"

