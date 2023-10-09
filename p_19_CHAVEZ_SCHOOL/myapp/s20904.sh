#!/bin/bash

# Define the files to be modified
FILES="./app/blueprints/admin/routes.py ./app/blueprints/crud/routes.py ./app/blueprints/staff/routes.py"

# Replace imports
for file in $FILES; do
    sed -i '' 's/from app.models.user import Admin, Student/from app.models.user import User/g' $file
done

# Replace Admin queries
sed -i '' 's/Admin.query.filter_by(username=/User.query.filter_by(role='"'"'admin'"'"', username=/g' ./app/blueprints/admin/routes.py

# Replace Student queries in crud/routes.py
sed -i '' 's/Student.query.all()/User.query.filter_by(role='"'"'student'"'"').all()/g' ./app/blueprints/crud/routes.py
sed -i '' 's/Student.query.get_or_404(id)/User.query.filter_by(role='"'"'student'"'"').get_or_404(id)/g' ./app/blueprints/crud/routes.py

echo "Replacements done!"


