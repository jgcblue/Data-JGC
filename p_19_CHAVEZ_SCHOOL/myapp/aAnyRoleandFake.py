import argparse
from app import create_app, db
from app.models.user import User
from faker import Faker

fake = Faker()

def add_user(username, email, password, role):
    """
    Function to add a user to the database with a specified role.
    
    Parameters:
    - username (str): The desired username for the user.
    - email (str): The email address for the user.
    - password (str): The password for the user.
    - role (str): The role for the user.
    
    Returns:
    - str: A message indicating success or the nature of any error.
    """
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return "Username or Email already exists."
    
    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return f"{role.capitalize()} added successfully!"

def add_fake_students(num_students):
    for _ in range(num_students):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        role = "student"
        result = add_user(username, email, password, role)
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Add a user with a specified role or fake students to the database.")
    parser.add_argument("username", type=str, help="The desired username for the user.", nargs='?', default=None)
    parser.add_argument("email", type=str, help="The email address for the user.", nargs='?', default=None)
    parser.add_argument("password", type=str, help="The password for the user.", nargs='?', default=None)
    parser.add_argument("role", type=str, help="The role for the user.", nargs='?', default=None)
    parser.add_argument("--fake-students", type=int, help="Number of fake students to add.", default=0)

    args = parser.parse_args()

    # Create a minimal Flask app instance
    app = create_app()

    # Establish an app context to perform database operations
    with app.app_context():
        if args.fake_students:
            add_fake_students(args.fake_students)
        else:
            result = add_user(args.username, args.email, args.password, args.role)
            print(result)

if __name__ == "__main__":
    main()

