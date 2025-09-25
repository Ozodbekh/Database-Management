from datetime import date

from cli.auth_menu import AuthMenu
from db.queries import UserQueries, GroupQueries, SubjectQueries


class AdminMenu:
    @staticmethod
    def show_menu(user):
        while True:
            print("\n" + "=" * 50)
            print(f"ADMIN PANEL - Welcome {user.full_name}")
            print("=" * 50)
            print("1. User Management")
            print("2. Group Management")
            print("3. Subject Management")
            print("4. View Reports")
            print("5. System Overview")
            print("6. Logout")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                AdminMenu.user_management_menu(user)
            elif choice == '2':
                AdminMenu.group_management_menu(user)
            elif choice == '3':
                AdminMenu.subject_management_menu(user)
            elif choice == '4':
                AdminMenu.reports_menu(user)
            elif choice == '5':
                AdminMenu.system_overview()
            elif choice == '6':
                AuthMenu.logout()
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def user_management_menu(user):
        while True:
            print("\n" + "-" * 30)
            print("USER MANAGEMENT")
            print("-" * 30)
            print("1. Register New User")
            print("2. View All Users")
            print("3. View Users by Role")
            print("4. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                AuthMenu.register_user_menu(user)
            elif choice == '2':
                AdminMenu.view_all_users()
            elif choice == '3':
                AdminMenu.view_users_by_role()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def view_all_users():
        users = UserQueries.get_all_users()
        print("\n" + "-" * 70)
        print("ALL USERS")
        print("-" * 70)
        print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Role':<10} {'Email':<25}")
        print("-" * 70)
        for user in users:
            print(
                f"{user.id:<5} {user.full_name:<25} {user.phone_number:<15} {user.role:<10} {user.email or 'N/A':<25}")

    @staticmethod
    def view_users_by_role():
        role = input("Enter role (admin/teacher/student): ").strip().lower()
        if role not in ['admin', 'teacher', 'student']:
            print("Invalid role.")
            return

        users = UserQueries.get_users_by_role(role)
        print(f"\n{role.upper()}S")
        print("-" * 50)
        for user in users:
            print(f"ID: {user.id}, Name: {user.full_name}, Phone: {user.phone_number}")

    @staticmethod
    def group_management_menu(user):
        while True:
            print("\n" + "-" * 30)
            print("GROUP MANAGEMENT")
            print("-" * 30)
            print("1. Create New Group")
            print("2. View All Groups")
            print("3. Enroll Student to Group")
            print("4. View Group Students")
            print("5. Assign Teacher to Subject")
            print("6. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                AdminMenu.create_group()
            elif choice == '2':
                AdminMenu.view_all_groups()
            elif choice == '3':
                AdminMenu.enroll_student_to_group()
            elif choice == '4':
                AdminMenu.view_group_students()
            elif choice == '5':
                AdminMenu.assign_teacher_to_subject()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def create_group():
        name = input("Group Name: ").strip()
        description = input("Description: ").strip()

        group_id = GroupQueries.create_group(name, description)
        print(f"Group created successfully! Group ID: {group_id}")

    @staticmethod
    def view_all_groups():
        groups = GroupQueries.get_all_groups()
        print("\n" + "-" * 50)
        print("ALL GROUPS")
        print("-" * 50)
        for group in groups:
            print(f"ID: {group[0]}, Name: {group[1]}, Description: {group[2]}")

    @staticmethod
    def enroll_student_to_group():
        students = UserQueries.get_users_by_role('student')
        groups = GroupQueries.get_all_groups()

        print("\nStudents:")
        for student in students:
            print(f"{student.id}: {student.full_name}")

        print("\nGroups:")
        for group in groups:
            print(f"{group[0]}: {group[1]}")

        student_id = input("\nEnter Student ID: ").strip()
        group_id = input("Enter Group ID: ").strip()

        try:
            GroupQueries.enroll_student(int(student_id), int(group_id))
            print("Student enrolled successfully!")
        except Exception as e:
            print(f"Error enrolling student: {e}")

    @staticmethod
    def view_group_students():
        groups = GroupQueries.get_all_groups()
        print("\nGroups:")
        for group in groups:
            print(f"{group[0]}: {group[1]}")

        group_id = input("\nEnter Group ID: ").strip()

        try:
            students = GroupQueries.get_group_students(int(group_id))
            print(f"\nStudents in Group:")
            print("-" * 40)
            for student in students:
                print(f"{student.id}: {student.full_name} - {student.phone_number}")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def assign_teacher_to_subject():
        teachers = UserQueries.get_users_by_role('teacher')
        groups = GroupQueries.get_all_groups()
        subjects = SubjectQueries.get_all_subjects()

        print("\nTeachers:")
        for teacher in teachers:
            print(f"{teacher.id}: {teacher.full_name}")

        print("\nGroups:")
        for group in groups:
            print(f"{group[0]}: {group[1]}")

        print("\nSubjects:")
        for subject in subjects:
            print(f"{subject[0]}: {subject[1]} ({subject[2]})")

        teacher_id = input("\nEnter Teacher ID: ").strip()
        group_id = input("Enter Group ID: ").strip()
        subject_id = input("Enter Subject ID: ").strip()

        try:
            SubjectQueries.assign_teacher_to_subject(int(group_id), int(subject_id), int(teacher_id))
            print("Teacher assigned to subject successfully!")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def subject_management_menu(user):
        while True:
            print("\n" + "-" * 30)
            print("SUBJECT MANAGEMENT")
            print("-" * 30)
            print("1. Create New Subject")
            print("2. View All Subjects")
            print("3. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                AdminMenu.create_subject()
            elif choice == '2':
                AdminMenu.view_all_subjects()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def create_subject():
        name = input("Subject Name: ").strip()
        code = input("Subject Code: ").strip()
        description = input("Description: ").strip()
        credits = input("Credits (default 3): ").strip() or "3"

        try:
            subject_id = SubjectQueries.create_subject(name, code, description, int(credits))
            print(f"Subject created successfully! Subject ID: {subject_id}")
        except Exception as e:
            print(f"Error creating subject: {e}")

    @staticmethod
    def view_all_subjects():
        subjects = SubjectQueries.get_all_subjects()
        print("\n" + "-" * 70)
        print("ALL SUBJECTS")
        print("-" * 70)
        print(f"{'ID':<5} {'Name':<20} {'Code':<10} {'Credits':<8} {'Description'}")
        print("-" * 70)
        for subject in subjects:
            print(f"{subject[0]:<5} {subject[1]:<20} {subject[2]:<10} {subject[4]:<8} {subject[3] or 'N/A'}")

    @staticmethod
    def reports_menu(user):
        print("\n" + "-" * 30)
        print("REPORTS")
        print("-" * 30)
        print("1. User Statistics")
        print("2. Group Statistics")
        print("3. Subject Statistics")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            AdminMenu.user_statistics()
        elif choice == '2':
            AdminMenu.group_statistics()
        elif choice == '3':
            AdminMenu.subject_statistics()

    @staticmethod
    def user_statistics():
        all_users = UserQueries.get_all_users()
        admins = len([u for u in all_users if u.role == 'admin'])
        teachers = len([u for u in all_users if u.role == 'teacher'])
        students = len([u for u in all_users if u.role == 'student'])

        print("\n" + "-" * 30)
        print("USER STATISTICS")
        print("-" * 30)
        print(f"Total Users: {len(all_users)}")
        print(f"Admins: {admins}")
        print(f"Teachers: {teachers}")
        print(f"Students: {students}")

    @staticmethod
    def group_statistics():
        groups = GroupQueries.get_all_groups()
        print(f"\nTotal Groups: {len(groups)}")

        for group in groups:
            students = GroupQueries.get_group_students(group[0])
            print(f"Group '{group[1]}': {len(students)} students")

    @staticmethod
    def subject_statistics():
        subjects = SubjectQueries.get_all_subjects()
        print(f"\nTotal Subjects: {len(subjects)}")

        total_credits = sum(subject[4] for subject in subjects)
        print(f"Total Credits Available: {total_credits}")

    @staticmethod
    def system_overview():
        print("\n" + "=" * 50)
        print("SYSTEM OVERVIEW")
        print("=" * 50)

        all_users = UserQueries.get_all_users()
        groups = GroupQueries.get_all_groups()
        subjects = SubjectQueries.get_all_subjects()

        print(f"Total Users: {len(all_users)}")
        print(f"Total Groups: {len(groups)}")
        print(f"Total Subjects: {len(subjects)}")
        print(f"System Date: {date.today()}")
