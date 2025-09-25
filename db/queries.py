from .connection import get_connection
from models.users import User
from utils.password_utils import hash_password

class PermissionQueries:
    @staticmethod
    def get_user_permissions(role):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, p.description
            FROM permissions p 
            JOIN role_permissions rp ON p.id = rp.permission_id
            WHERE rp.role = ?
        """, (role,))
        permissions = cursor.fetchall()
        conn.close()
        return [{"name": p[0], "description": p[1]} for p in permissions]

    @staticmethod
    def has_permission(role, permission_name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM permissions p 
            JOIN role_permissions rp ON p.id = rp.permission_id
            WHERE rp.role = ? AND p.name = ?
        """, (role, permission_name))
        result = cursor.fetchone()[0] > 0
        conn.close()
        return result

    @staticmethod
    def get_all_permissions():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, description FROM permissions")
        permissions = cursor.fetchall()
        conn.close()
        return [{'name': p[0], 'description': p[1]} for p in permissions]

class UserQueries:
    @staticmethod
    def create_user(full_name, phone_number, email, password, role):
        conn = get_connection()
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute("""
            INSERT INTO users (full_name, phone_number, email, password, role)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, phone_number, email, hashed_password, role))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id

    @staticmethod
    def get_user_by_phone(phone_number):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return User(*user_data)
        return None

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return User(*user_data)
        return None

    @staticmethod
    def get_all_users():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users_data = cursor.fetchall()
        conn.close()
        return [User(*user_data) for user_data in users_data]

    @staticmethod
    def get_users_by_role(role):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE role = ?", (role,))
        users_data = cursor.fetchall()
        conn.close()
        return [User(*user_data) for user_data in users_data]

class GroupQueries:
    @staticmethod
    def create_group(name, description):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO groups (name, description) VALUES (?, ?)", (name, description))
        group_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return group_id

    @staticmethod
    def get_all_groups():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups ORDER BY name")
        groups = cursor.fetchall()
        conn.close()
        return groups

    @staticmethod
    def get_group_by_id(group_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE id = ?", (group_id,))
        group = cursor.fetchone()
        conn.close()
        return group

    @staticmethod
    def enroll_student(student_id, group_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO student_groups (student_id, group_id) VALUES (?, ?)", (student_id, group_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_group_students(group_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.* FROM users u
            JOIN student_groups sg ON u.id = sg.student_id
            WHERE sg.group_id = ? AND sg.status = 'active'
            ORDER BY u.full_name
        """, (group_id,))
        students = cursor.fetchall()
        conn.close()
        return [User(*student) for student in students]

    @staticmethod
    def get_student_groups(student_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.* FROM groups g
            JOIN student_groups sg ON g.id = sg.group_id
            WHERE sg.student_id = ? AND sg.status = 'active'
        """, (student_id,))
        groups = cursor.fetchall()
        conn.close()
        return groups

    @staticmethod
    def get_teacher_groups(teacher_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT g.* FROM groups g
            JOIN group_subjects gs ON g.id = gs.group_id
            WHERE gs.teacher_id = ?
        """, (teacher_id,))
        groups = cursor.fetchall()
        conn.close()
        return groups

class SubjectQueries:
    @staticmethod
    def create_subject(name, code, description, credits):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subjects (name, code, description, credits) VALUES (?, ?, ?, ?)",
                      (name, code, description, credits))
        subject_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return subject_id

    @staticmethod
    def get_all_subjects():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subjects ORDER BY name")
        subjects = cursor.fetchall()
        conn.close()
        return subjects

    @staticmethod
    def assign_teacher_to_subject(group_id, subject_id, teacher_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO group_subjects (group_id, subject_id, teacher_id) VALUES (?, ?, ?)",
                      (group_id, subject_id, teacher_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_group_subjects(group_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, u.full_name as teacher_name FROM subjects s
            JOIN group_subjects gs ON s.id = gs.subject_id
            JOIN users u ON gs.teacher_id = u.id
            WHERE gs.group_id = ?
        """, (group_id,))
        subjects = cursor.fetchall()
        conn.close()
        return subjects

    @staticmethod
    def get_teacher_subjects(teacher_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, g.name as group_name FROM subjects s
            JOIN group_subjects gs ON s.id = gs.subject_id
            JOIN groups g ON gs.group_id = g.id
            WHERE gs.teacher_id = ?
        """, (teacher_id,))
        subjects = cursor.fetchall()
        conn.close()
        return subjects

class AttendanceQueries:
    @staticmethod
    def mark_attendance(student_id, subject_id, date, status, notes, marked_by):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO attendance (student_id, subject_id, date, status, notes, marked_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, subject_id, date, status, notes, marked_by))
        conn.commit()
        conn.close()

    @staticmethod
    def get_student_attendance(student_id, subject_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        if subject_id:
            cursor.execute("""
                SELECT a.*, s.name as subject_name FROM attendance a
                JOIN subjects s ON a.subject_id = s.id
                WHERE a.student_id = ? AND a.subject_id = ?
                ORDER BY a.date DESC
            """, (student_id, subject_id))
        else:
            cursor.execute("""
                SELECT a.*, s.name as subject_name FROM attendance a
                JOIN subjects s ON a.subject_id = s.id
                WHERE a.student_id = ?
                ORDER BY a.date DESC
            """, (student_id,))
        attendance = cursor.fetchall()
        conn.close()
        return attendance

    @staticmethod
    def get_group_attendance(group_id, subject_id, date):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.full_name, COALESCE(a.status, 'not_marked') as status, a.notes
            FROM users u
            JOIN student_groups sg ON u.id = sg.student_id
            LEFT JOIN attendance a ON u.id = a.student_id AND a.subject_id = ? AND a.date = ?
            WHERE sg.group_id = ? AND sg.status = 'active'
            ORDER BY u.full_name
        """, (subject_id, date, group_id))
        attendance = cursor.fetchall()
        conn.close()
        return attendance

    @staticmethod
    def get_attendance_summary(student_id, subject_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_classes,
                SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_count,
                SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_count,
                SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late_count,
                ROUND((SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) as attendance_percentage
            FROM attendance
            WHERE student_id = ? AND subject_id = ?
        """, (student_id, subject_id))
        summary = cursor.fetchone()
        conn.close()
        return summary

class AssignmentQueries:
    @staticmethod
    def create_assignment(title, description, subject_id, group_id, total_marks, due_date, created_by):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO assignments (title, description, subject_id, group_id, total_marks, due_date, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, description, subject_id, group_id, total_marks, due_date, created_by))
        assignment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return assignment_id

    @staticmethod
    def get_group_assignments(group_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.name as subject_name, u.full_name as created_by_name
            FROM assignments a
            JOIN subjects s ON a.subject_id = s.id
            JOIN users u ON a.created_by = u.id
            WHERE a.group_id = ?
            ORDER BY a.due_date
        """, (group_id,))
        assignments = cursor.fetchall()
        conn.close()
        return assignments

    @staticmethod
    def get_teacher_assignments(teacher_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.name as subject_name, g.name as group_name
            FROM assignments a
            JOIN subjects s ON a.subject_id = s.id
            JOIN groups g ON a.group_id = g.id
            WHERE a.created_by = ?
            ORDER BY a.due_date
        """, (teacher_id,))
        assignments = cursor.fetchall()
        conn.close()
        return assignments

class GradeQueries:
    @staticmethod
    def grade_assignment(student_id, assignment_id, marks_obtained, feedback, graded_by):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO grades (student_id, assignment_id, marks_obtained, feedback, graded_by)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, assignment_id, marks_obtained, feedback, graded_by))
        conn.commit()
        conn.close()

    @staticmethod
    def get_student_grades(student_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.*, a.title as assignment_title, a.total_marks, s.name as subject_name,
                   ROUND((g.marks_obtained * 100.0 / a.total_marks), 2) as percentage
            FROM grades g
            JOIN assignments a ON g.assignment_id = a.id
            JOIN subjects s ON a.subject_id = s.id
            WHERE g.student_id = ?
            ORDER BY g.graded_at DESC
        """, (student_id,))
        grades = cursor.fetchall()
        conn.close()
        return grades

    @staticmethod
    def get_assignment_grades(assignment_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.*, u.full_name as student_name, a.total_marks
            FROM grades g
            JOIN users u ON g.student_id = u.id
            JOIN assignments a ON g.assignment_id = a.id
            WHERE g.assignment_id = ?
            ORDER BY u.full_name
        """, (assignment_id,))
        grades = cursor.fetchall()
        conn.close()
        return grades

    @staticmethod
    def get_student_subject_average(student_id, subject_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_assignments,
                ROUND(AVG(g.marks_obtained * 100.0 / a.total_marks), 2) as average_percentage,
                SUM(g.marks_obtained) as total_marks_obtained,
                SUM(a.total_marks) as total_possible_marks
            FROM grades g
            JOIN assignments a ON g.assignment_id = a.id
            WHERE g.student_id = ? AND a.subject_id = ?
        """, (student_id, subject_id))
        average = cursor.fetchone()
        conn.close()
        return average