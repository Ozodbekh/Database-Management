from utils.password_utils import verify_password
from utils.session_manager import session_manager
from .queries import UserQueries


class AuthService:
    @staticmethod
    def login(phone_number, password):
        user = UserQueries.get_user_by_phone(phone_number)
        if user and verify_password(user.password, password):
            token = session_manager.create_session(user)
            return user, token
        return None, None

    @staticmethod
    def register_user(full_name, phone_number, email, password, role, created_by_user):
        if created_by_user.role == 'admin':
            if role in ['admin', 'teacher', 'student']:
                return UserQueries.create_user(full_name, phone_number, email, password, role)
        elif created_by_user.role == 'teacher':
            if role == 'student':
                return UserQueries.create_user(full_name, phone_number, email, password, role)
        return None

    @staticmethod
    def logout():
        session_manager.logout()

    @staticmethod
    def get_current_user():
        return session_manager.get_current_user()

    @staticmethod
    def is_logged_in():
        return session_manager.is_logged_in()
