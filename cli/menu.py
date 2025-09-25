from cli.admin_menu import AdminMenu
from cli.auth_menu import AuthMenu
from cli.student_menu import StudentMenu
from cli.teacher_menu import TeacherMenu
from db.auth import AuthService


class MainMenu:
    @staticmethod
    def run():
        while True:
            if not AuthService.is_logged_in():
                if not AuthMenu.show_login_menu():
                    break
                continue

            user = AuthService.get_current_user()

            if user.is_admin():
                AdminMenu.show_menu(user)
            elif user.is_teacher():
                TeacherMenu.show_menu(user)
            elif user.is_student():
                StudentMenu.show_menu(user)

            if not AuthService.is_logged_in():
                continue
