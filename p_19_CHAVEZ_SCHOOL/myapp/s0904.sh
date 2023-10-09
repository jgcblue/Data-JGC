#!/bin/bash

# Define the path to your project
PROJECT_PATH="."

# Define the output file
OUTPUT_FILE="$PROJECT_PATH/search_results.txt"

# Clear the output file if it exists
> $OUTPUT_FILE

# Searching for Imports
echo "Searching for Admin imports..." >> $OUTPUT_FILE
grep -r "from app.models.user import Admin" $PROJECT_PATH >> $OUTPUT_FILE

echo "Searching for Staff imports..." >> $OUTPUT_FILE
grep -r "from app.models.user import Staff" $PROJECT_PATH >> $OUTPUT_FILE

echo "Searching for Student imports..." >> $OUTPUT_FILE
grep -r "from app.models.user import Student" $PROJECT_PATH >> $OUTPUT_FILE

# Searching for Queries
echo "Searching for Admin.query..." >> $OUTPUT_FILE
grep -r "Admin.query" $PROJECT_PATH >> $OUTPUT_FILE

echo "Searching for Staff.query..." >> $OUTPUT_FILE
grep -r "Staff.query" $PROJECT_PATH >> $OUTPUT_FILE

echo "Searching for Student.query..." >> $OUTPUT_FILE
grep -r "Student.query" $PROJECT_PATH >> $OUTPUT_FILE

# Print completion message
echo "Search completed. Results stored in $OUTPUT_FILE"

