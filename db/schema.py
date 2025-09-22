from .connection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone_number TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT CHECK(role IN ('admin', 'teacher', 'student')) NOT NULL
    )
    """)
    print("Created user schema.")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)
    print("Created permissions schema.")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS role_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        permissions_id INTEGER NOT NULL,
        FOREIGN KEY (permissions_id) REFERENCES permissions(id),
        UNIQUE(role, permissions_id)
    )
    """)
    print("Created role_permissions schema.")

    conn.commit()
    conn.commit()


def insert_default_permissions():
    conn = get_connection()
    cursor = conn.cursor()

    default_permissions = [
        ('create_user', 'Create new user'),
        ('delete_user', "Delete user"),
        ('view_all_users', 'View all users'),
        ('edit_user', "Edit user information"),
        ('create_course', 'Create new course'),
        ('edit_course', 'Edit course'),
        ('delete_course', "Delete course"),
        ('view_courses', 'View courses'),
        ('grade_students', 'Grade students'),
        ('view_grades', 'View grades'),
        ('submit_assignment', 'Submit assignment'),
        ('manage_system', 'Manage system'),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO permissions (name, description)
        VALUES (?, ?)
    """, default_permissions)

    role_permissions = [
        # Admin permissions
        ('admin', 'create_user'),
        ('admin', 'delete_user'),
        ('admin', 'view_all_users'),
        ('admin', 'edit_user'),
        ('admin', 'create_course'),
        ('admin', 'edit_course'),
        ('admin', 'delete_course'),
        ('admin', 'view_courses'),
        ('admin', 'manage_system'),

        # Teacher permissions
        ('teacher', 'create_course'),
        ('teacher', 'edit_course'),
        ('teacher', 'view_courses'),
        ('teacher', 'grade_students'),
        ('teacher', 'view_grades'),

        # Student permissions
        ('student', 'view_courses'),
        ('student', 'view_grades'),
        ('student', 'submit_assignment'),
    ]

    for role, permission_name in role_permissions:
        cursor.execute("""
            INSERT OR IGNORE INTO role_permissions (role, permission_id)
            SELECT ?, p.id FROM permissions p WHERE p.name = ?
        """, (role, permission_name))

        conn.commit()
        conn.commit()
        print("Default permissions inserted.")