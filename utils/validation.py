import re
from datetime import datetime

from config import PASSWORD_MIN_LENGTH, ATTENDANCE_STATUSES


def validate_email(email):
    if not email:
        return True

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone_number(phone):
    if not phone or len(phone.strip()) < 3:
        return False

    pattern = r'^[a-zA-Z0-9]+$'
    return re.match(pattern, phone.strip()) is not None


def validate_password(password):
    if not password or len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"

    return True, "Password is valid"


def validate_name(name):
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"

    # Allow letters, spaces, hyphens, and apostrophes
    pattern = r"^[a-zA-Z\s\-']+$"
    if not re.match(pattern, name.strip()):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"

    return True, "Name is valid"


def validate_role(role):
    valid_roles = ['admin', 'teacher', 'student']
    if role.lower() not in valid_roles:
        return False, f"Role must be one of: {', '.join(valid_roles)}"

    return True, "Role is valid"


def validate_date(date_string):
    if not date_string:
        return True, "Date is optional"

    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True, "Date is valid"
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format"


def validate_attendance_status(status):
    if status.lower() not in ATTENDANCE_STATUSES:
        return False, f"Status must be one of: {', '.join(ATTENDANCE_STATUSES)}"

    return True, "Status is valid"


def validate_marks(marks, total_marks):
    try:
        marks_float = float(marks)
        total_float = float(total_marks)

        if marks_float < 0:
            return False, "Marks cannot be negative"

        if marks_float > total_float:
            return False, "Marks cannot exceed total marks"

        return True, "Marks are valid"
    except ValueError:
        return False, "Marks must be a valid number"


def validate_credits(credits):
    try:
        credits_int = int(credits)
        if credits_int < 1 or credits_int > 10:
            return False, "Credits must be between 1 and 10"

        return True, "Credits are valid"
    except ValueError:
        return False, "Credits must be a valid number"


def validate_subject_code(code):
    if not code or len(code.strip()) < 3:
        return False, "Subject code must be at least 3 characters long"

    # Allow alphanumeric codes like CS101, MATH201, etc.
    pattern = r'^[A-Z]{2,4}\d{3}$'
    if not re.match(pattern, code.strip().upper()):
        return False, "Subject code must be in format like CS101, MATH201"

    return True, "Subject code is valid"


def sanitize_input(input_string):
    if not input_string:
        return ""

    return input_string.strip()


def validate_id(id_string, entity_type="ID"):
    try:
        id_int = int(id_string.strip())
        if id_int <= 0:
            return False, f"{entity_type} must be a positive number"

        return True, f"{entity_type} is valid"
    except ValueError:
        return False, f"{entity_type} must be a valid number"


def get_grade_letter(percentage):
    from config import GRADE_LETTERS

    for threshold in sorted(GRADE_LETTERS.keys(), reverse=True):
        if percentage >= threshold:
            return GRADE_LETTERS[threshold]

    return 'F'


def format_percentage(marks_obtained, total_marks):
    try:
        percentage = (float(marks_obtained) / float(total_marks)) * 100
        return round(percentage, 2)
    except (ValueError, ZeroDivisionError):
        return 0.0


def validate_menu_choice(choice, max_options):
    try:
        choice_int = int(choice.strip())
        if 1 <= choice_int <= max_options:
            return True, choice_int
        else:
            return False, f"Please enter a number between 1 and {max_options}"
    except ValueError:
        return False, "Please enter a valid number"
