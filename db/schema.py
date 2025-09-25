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
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('admin', 'teacher', 'student')) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS role_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        permission_id INTEGER NOT NULL,
        FOREIGN KEY (permission_id) REFERENCES permissions(id),
        UNIQUE(role, permission_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        code TEXT NOT NULL UNIQUE,
        description TEXT,
        credits INTEGER DEFAULT 3
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS group_subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL,
        FOREIGN KEY (group_id) REFERENCES groups(id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id),
        FOREIGN KEY (teacher_id) REFERENCES users(id),
        UNIQUE(group_id, subject_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT CHECK(status IN ('active', 'inactive', 'graduated')) DEFAULT 'active',
        FOREIGN KEY (student_id) REFERENCES users(id),
        FOREIGN KEY (group_id) REFERENCES groups(id),
        UNIQUE(student_id, group_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        date DATE NOT NULL,
        status TEXT CHECK(status IN ('present', 'absent', 'late')) NOT NULL,
        notes TEXT,
        marked_by INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES users(id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id),
        FOREIGN KEY (marked_by) REFERENCES users(id),
        UNIQUE(student_id, subject_id, date)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        subject_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        total_marks INTEGER NOT NULL,
        due_date DATE,
        created_by INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id),
        FOREIGN KEY (group_id) REFERENCES groups(id),
        FOREIGN KEY (created_by) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        assignment_id INTEGER NOT NULL,
        marks_obtained DECIMAL(5,2) NOT NULL,
        feedback TEXT,
        graded_by INTEGER NOT NULL,
        graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES users(id),
        FOREIGN KEY (assignment_id) REFERENCES assignments(id),
        FOREIGN KEY (graded_by) REFERENCES users(id),
        UNIQUE(student_id, assignment_id)
    )
    """)

    conn.commit()
    conn.close()
    print("All tables created successfully.")

def insert_default_permissions():
    conn = get_connection()
    cursor = conn.cursor()

    default_permissions = [
        ('create_user', 'Create new user'),
        ('delete_user', 'Delete user'),
        ('view_all_users', 'View all users'),
        ('edit_user', 'Edit user information'),
        ('create_group', 'Create new group'),
        ('edit_group', 'Edit group'),
        ('delete_group', 'Delete group'),
        ('view_groups', 'View groups'),
        ('assign_teacher', 'Assign teacher to group'),
        ('enroll_student', 'Enroll student to group'),
        ('create_subject', 'Create new subject'),
        ('edit_subject', 'Edit subject'),
        ('delete_subject', 'Delete subject'),
        ('view_subjects', 'View subjects'),
        ('create_assignment', 'Create assignment'),
        ('grade_assignment', 'Grade assignment'),
        ('view_grades', 'View grades'),
        ('view_own_grades', 'View own grades'),
        ('mark_attendance', 'Mark attendance'),
        ('view_attendance', 'View attendance'),
        ('view_own_attendance', 'View own attendance'),
        ('generate_reports', 'Generate reports'),
        ('manage_system', 'Manage system')
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO permissions (name, description)
        VALUES (?, ?)
    """, default_permissions)

    role_permissions = [
        ('admin', 'create_user'),
        ('admin', 'delete_user'),
        ('admin', 'view_all_users'),
        ('admin', 'edit_user'),
        ('admin', 'create_group'),
        ('admin', 'edit_group'),
        ('admin', 'delete_group'),
        ('admin', 'view_groups'),
        ('admin', 'assign_teacher'),
        ('admin', 'enroll_student'),
        ('admin', 'create_subject'),
        ('admin', 'edit_subject'),
        ('admin', 'delete_subject'),
        ('admin', 'view_subjects'),
        ('admin', 'view_grades'),
        ('admin', 'view_attendance'),
        ('admin', 'generate_reports'),
        ('admin', 'manage_system'),

        ('teacher', 'view_groups'),
        ('teacher', 'enroll_student'),
        ('teacher', 'create_assignment'),
        ('teacher', 'grade_assignment'),
        ('teacher', 'view_grades'),
        ('teacher', 'mark_attendance'),
        ('teacher', 'view_attendance'),
        ('teacher', 'generate_reports'),

        ('student', 'view_own_grades'),
        ('student', 'view_own_attendance')
    ]

    for role, permission_name in role_permissions:
        cursor.execute("""
            INSERT OR IGNORE INTO role_permissions (role, permission_id)
            SELECT ?, p.id FROM permissions p WHERE p.name = ?
        """, (role, permission_name))

    conn.commit()
    conn.close()
    print("Default permissions inserted.")