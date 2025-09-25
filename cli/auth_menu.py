from db.auth import AuthService
from utils.session_manager import session_manager


class AuthMenu:
    @staticmethod
    def show_login_menu():
        while True:
            print("\n" + "=" * 50)
            print("STUDENT RECORD MANAGEMENT SYSTEM")
            print("=" * 50)
            print("1. Login")
            print("2. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                return AuthMenu.login()
            elif choice == '2':
                print("Goodbye!")
                return False
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def login():
        print("\n" + "-" * 30)
        print("LOGIN")
        print("-" * 30)

        phone_number = input("Phone Number: ").strip()
        password = input("Password: ").strip()

        user, token = AuthService.login(phone_number, password)

        if user:
            print(f"\nLogin successful! Welcome, {user.full_name}")
            print(f"Role: {user.role.title()}")
            return True
        else:
            print("Invalid credentials. Please try again.")
            return False

    @staticmethod
    def register_user_menu(current_user):
        print("\n" + "-" * 30)
        print("REGISTER NEW USER")
        print("-" * 30)

        if current_user.role == 'admin':
            print("Available roles: admin, teacher, student")
            role = input("Role: ").strip().lower()
            if role not in ['admin', 'teacher', 'student']:
                print("Invalid role.")
                return
        elif current_user.role == 'teacher':
            role = 'student'
            print("You can only register students.")
        else:
            print("You don't have permission to register users.")
            return

        full_name = input("Full Name: ").strip()
        phone_number = input("Phone Number: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        user_id = AuthService.register_user(full_name, phone_number, email, password, role, current_user)

        if user_id:
            print(f"\nUser registered successfully! User ID: {user_id}")
        else:
            print("Registration failed. Phone number might already exist or you don't have permission.")

    @staticmethod
    def logout():
        AuthService.logout()
        print("\nLogged out successfully!")