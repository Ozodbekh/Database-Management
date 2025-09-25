import secrets
from datetime import datetime, timedelta


class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.current_user = None

    def create_session(self, user):
        token = secrets.token_hex(32)
        expires_at = datetime.now() + timedelta(hours=24)
        self.sessions[token] = {
            'user': user,
            'expires_at': expires_at
        }
        self.current_user = user
        return token

    def get_current_user(self):
        return self.current_user

    def is_logged_in(self):
        return self.current_user is not None

    def logout(self):
        self.current_user = None
        self.sessions.clear()

    def validate_session(self, token):
        if token in self.sessions:
            session = self.sessions[token]
            if session['expires_at'] > datetime.now():
                return session['user']
        return None


session_manager = SessionManager()
