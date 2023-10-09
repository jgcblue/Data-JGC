from app import db  # Replace 'your_flask_app' with your actual Flask application name
from sqlalchemy import MetaData

metadata = MetaData(bind=db.engine)
metadata.reflect()

# List all tables in the database
tables = metadata.tables.keys()
for table in tables:
    print(table)

