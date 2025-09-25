#!/usr/bin/env python3
import os
import sys

from db.schema import create_tables, insert_default_permissions
from db.seed_data import seed_sample_data
from utils.display import print_welcome, print_success, print_error, print_info


def check_python_version():
    if sys.version_info < (3, 6):
        print_error("Python 3.6 or higher is required")
        return False
    return True


def setup_database():
    """Initialize database tables and permissions"""
    try:
        print_info("Creating database tables...")
        create_tables()

        print_info("Setting up default permissions...")
        insert_default_permissions()

        print_success("Database initialized successfully!")
        return True
    except Exception as e:
        print_error(f"Database setup failed: {e}")
        return False


def setup_sample_data():
    while True:
        choice = input("\nWould you like to add sample data? (y/n): ").strip().lower()

        if choice in ['y', 'yes']:
            try:
                seed_sample_data()
                print_success("Sample data added successfully!")
                return True
            except Exception as e:
                print_error(f"Sample data setup failed: {e}")
                return False
        elif choice in ['n', 'no']:
            print_info("Skipping sample data setup")
            return True
        else:
            print_error("Please enter 'y' for yes or 'n' for no")


def create_directories():
    directories = ['db', 'models', 'utils', 'cli']

    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print_info(f"Created directory: {directory}")
            except Exception as e:
                print_error(f"Failed to create directory {directory}: {e}")
                return False

    return True


def check_files():
    required_files = [
        'main.py',
        'config.py',
        'db/connection.py',
        'db/schema.py',
        'db/queries.py',
        'db/auth.py',
        'models/users.py',
        'utils/password_utils.py',
        'utils/session_manager.py',
        'cli/menu.py',
        'cli/auth_menu.py',
        'cli/admin_menu.py',
        'cli/teacher_menu.py',
        'cli/student_menu.py'
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print_error("Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False

    print_success("All required files found!")
    return True


def main():
    """Main setup function"""
    print_welcome()
    print("Setting up Student Record Management System...")

    if not check_python_version():
        return False

    if not create_directories():
        return False

    if not check_files():
        print_error("Please ensure all required files are present before running setup")
        return False

    if not setup_database():
        return False

    if not setup_sample_data():
        return False

    print("\n" + "=" * 60)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    print("\nSystem is ready to use!")
    print("\nTo start the application, run:")
    print("  python main.py")

    print("\nDefault login credentials:")
    print("  Phone: admin")
    print("  Password: admin123")

    print("\nFor help and documentation, see README.md")

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed with unexpected error: {e}")
        sys.exit(1)
