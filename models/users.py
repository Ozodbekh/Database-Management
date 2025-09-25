from db.queries import PermissionQueries

class User:
    def __init__(self, id, full_name, phone_number, email, password, role, created_at):
        self.id = id
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at

    def __repr__(self):
        return f"<User {self.id}: {self.full_name} ({self.role})>"

    def has_permission(self, permission_name):
        return PermissionQueries.has_permission(self.role, permission_name)

    def get_permissions(self):
        return PermissionQueries.get_user_permissions(self.role)

    def can_create_user(self):
        return self.has_permission('create_user')

    def can_delete_user(self):
        return self.has_permission('delete_user')

    def can_manage_groups(self):
        return self.has_permission('create_group')

    def can_assign_teacher(self):
        return self.has_permission('assign_teacher')

    def can_enroll_student(self):
        return self.has_permission('enroll_student')

    def can_create_assignment(self):
        return self.has_permission('create_assignment')

    def can_grade_assignment(self):
        return self.has_permission('grade_assignment')

    def can_mark_attendance(self):
        return self.has_permission('mark_attendance')

    def can_view_all_grades(self):
        return self.has_permission('view_grades')

    def can_view_all_attendance(self):
        return self.has_permission('view_attendance')

    def can_generate_reports(self):
        return self.has_permission('generate_reports')

    def is_admin(self):
        return self.role == 'admin'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'