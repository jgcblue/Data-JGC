import argparse
from app import create_app, db
from app.models.user import User

def add_admin(username, email, password):
    """
    Function to add an admin to the database.
    
    Parameters:
    - username (str): The desired username for the admin.
    - email (str): The email address for the admin.
    - password (str): The password for the admin.
    
    Returns:
    - str: A message indicating success or the nature of any error.
    """
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return "Username or Email already exists."
    
    new_admin = User(username=username, email=email, role='admin')
    new_admin.set_password(password)
    db.session.add(new_admin)
    db.session.commit()
    return "Admin added successfully!"

def main():
    parser = argparse.ArgumentParser(description="Add an admin to the database.")
    parser.add_argument("username", type=str, help="The desired username for the admin.")
    parser.add_argument("email", type=str, help="The email address for the admin.")
    parser.add_argument("password", type=str, help="The password for the admin.")

    args = parser.parse_args()

    # Create a minimal Flask app instance
    app = create_app()

    # Establish an app context to perform database operations
    with app.app_context():
        result = add_admin(args.username, args.email, args.password)
        print(result)

if __name__ == "__main__":
    main()

