from db.queries import PermissionQueries


class User:
    def __init__(
            self,
            id: int,
            full_name: str,
            phone_number: str,
            email: str,
            password: str,
            role: str
    ):
        self.id = id
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return f"<User {self.id}: {self.full_name} ({self.role})>"

    def has_permission(self, permission_name):
        return PermissionQueries.has_permission(self.role, permission_name)

    def get_permissions(self):
        return PermissionQueries.get_user_permissions(self.role)

    def can_create_user(self):
        return self.has_permission('create_user')

    def can_delete_user(self):
        return self.has_permission("delete_user")

    def can_manage_courses(self):
        return self.has_permission("create_course")
