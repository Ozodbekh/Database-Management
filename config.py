DATABASE_NAME = "db_management.db"
DATABASE_PATH = "./"

SESSION_TIMEOUT_HOURS = 24
PASSWORD_MIN_LENGTH = 6
SALT_LENGTH = 16
HASH_ITERATIONS = 100000

SYSTEM_NAME = "Student Record Management System"
SYSTEM_VERSION = "1.0.0"
MAX_LOGIN_ATTEMPTS = 3

DEFAULT_SUBJECT_CREDITS = 3
DEFAULT_ATTENDANCE_STATUS = "not_marked"

PASSING_GRADE_PERCENTAGE = 60.0
EXCELLENT_GRADE_PERCENTAGE = 90.0

TABLE_WIDTH = 80
MENU_WIDTH = 50

ATTENDANCE_STATUSES = ['present', 'absent', 'late']

GRADE_LETTERS = {
    90: 'A',
    80: 'B',
    70: 'C',
    60: 'D',
    0: 'F'
}

ROLE_HIERARCHY = {
    'admin': ['admin', 'teacher', 'student'],
    'teacher': ['teacher', 'student'],
    'student': ['student']
}

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

ERROR_MESSAGES = {
    'invalid_credentials': 'Invalid phone number or password.',
    'insufficient_permissions': 'You do not have permission to perform this action.',
    'user_not_found': 'User not found.',
    'group_not_found': 'Group not found.',
    'subject_not_found': 'Subject not found.',
    'assignment_not_found': 'Assignment not found.',
    'duplicate_entry': 'This entry already exists.',
    'invalid_input': 'Invalid input provided.',
    'database_error': 'Database operation failed.',
}

SUCCESS_MESSAGES = {
    'user_created': 'User created successfully!',
    'login_success': 'Login successful!',
    'logout_success': 'Logged out successfully!',
    'data_saved': 'Data saved successfully!',
    'data_updated': 'Data updated successfully!',
    'data_deleted': 'Data deleted successfully!',
}

MAIN_MENU_OPTIONS = {
    'admin': [
        'User Management',
        'Group Management',
        'Subject Management',
        'View Reports',
        'System Overview',
        'Logout'
    ],
    'teacher': [
        'My Groups & Subjects',
        'Attendance Management',
        'Assignment Management',
        'Grade Management',
        'Register Student',
        'View Reports',
        'Logout'
    ],
    'student': [
        'My Groups & Subjects',
        'My Attendance',
        'My Assignments',
        'My Grades',
        'Academic Summary',
        'Logout'
    ]
}
