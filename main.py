import os
from db.schema import create_tables, insert_default_permissions
from db.auth import AuthService
from cli.menu import MainMenu
from utils.display import print_welcome, print_success, print_error, print_info
from config import DATABASE_NAME


def initialize_system():
    print_info("Initializing Student Record Management System...")

    try:
        create_tables()
        insert_default_permissions()

        current_user = AuthService.get_current_user()
        if not current_user or not current_user.is_admin():
            create_default_admin()

        print_success("System initialized successfully!")
        return True
    except Exception as e:
        print_error(f"System initialization failed: {e}")
        return False


def create_default_admin():
    from db.queries import UserQueries

    print_info("Creating default admin user...")
    admin_password = "admin123"

    try:
        existing_admin = UserQueries.get_user_by_phone("admin")
        if existing_admin:
            print_info("Default admin user already exists")
            return True

        UserQueries.create_user(
            full_name="System Administrator",
            phone_number="admin",
            email="admin@system.com",
            password=admin_password,
            role="admin"
        )

        print_success("Default admin created successfully!")
        print("\nDefault Login Credentials:")
        print("  Phone: admin")
        print("  Password: admin123")
        print("  IMPORTANT: Change password after first login!")

        return True
    except Exception as e:
        print_error(f"Failed to create default admin: {e}")
        return False


def check_system_health():
    try:
        if not os.path.exists(DATABASE_NAME):
            return False, "Database file not found"

        from db.connection import get_connection
        conn = get_connection()
        conn.close()

        return True, "System is healthy"
    except Exception as e:
        return False, f"System health check failed: {e}"


def main():
    try:
        print_welcome()

        healthy, message = check_system_health()
        if not healthy:
            print_info(f"System check: {message}")
            if not initialize_system():
                print_error("Failed to initialize system")
                return False

        print_info("Starting application...")
        MainMenu.run()

        print_info("Application closed successfully")
        return True

    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
        return True
    except Exception as e:
        print_error(f"Application error: {e}")
        print("Please check your system configuration and try again.")
        return False


if __name__ == "__main__":
    main()