from .connection import get_connection
from models.users import User
conn = get_connection()

class PermissionQueries:
    @staticmethod
    def get_user_permissions(role):
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
    def add_permission_to_role(role, permission_name):
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO role_permissions (role, permission_id)
            SELECT ?, p.id FROM permissions p WHERE p.name = ?
        """, (role, permission_name))

        conn.commit()
        conn.close()

    @staticmethod
    def remove_permissions_from_role(role, permissions_name):
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM role_permissions
            WHERE role = ? AND permission_id = (
                SELECT id FROM permissions WHERE name = ?   
            )
        """, (role, permissions_name))

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_permissions():
        cursor = conn.cursor()

        cursor.execute("SELECT name, description FROM permissions")
        permissions = cursor.fetchall()
        conn.close()
        return [{'name': p[0], 'description': p[1]} for p in permissions]


class UserQueries:
    @staticmethod
    def create_user(full_name, phone_number, email, password, role):
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (full_name, phone_number, email, password, role)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, phone_number, email, password, role))

        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id, full_name

    @staticmethod
    def get_user_by_phone(phone_number):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE phone_number = ?
        """, (phone_number,))

        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return User(*user_data)
        return None

    @staticmethod
    def get_all_users():
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
        """)

        users_data = cursor.fetchall()
        conn.close()

        return [User(*user_data) for user_data in users_data]