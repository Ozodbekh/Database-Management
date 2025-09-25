from datetime import date

from cli.auth_menu import AuthMenu
from db.queries import GroupQueries, SubjectQueries, AttendanceQueries, AssignmentQueries, GradeQueries


class TeacherMenu:
    @staticmethod
    def show_menu(user):
        while True:
            print("\n" + "=" * 50)
            print(f"TEACHER PANEL - Welcome {user.full_name}")
            print("=" * 50)
            print("1. My Groups & Subjects")
            print("2. Attendance Management")
            print("3. Assignment Management")
            print("4. Grade Management")
            print("5. Register Student")
            print("6. View Reports")
            print("7. Logout")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                TeacherMenu.view_my_groups_subjects(user)
            elif choice == '2':
                TeacherMenu.attendance_menu(user)
            elif choice == '3':
                TeacherMenu.assignment_menu(user)
            elif choice == '4':
                TeacherMenu.grade_menu(user)
            elif choice == '5':
                AuthMenu.register_user_menu(user)
            elif choice == '6':
                TeacherMenu.reports_menu(user)
            elif choice == '7':
                AuthMenu.logout()
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def view_my_groups_subjects(user):
        print("\n" + "-" * 50)
        print("MY GROUPS & SUBJECTS")
        print("-" * 50)

        groups = GroupQueries.get_teacher_groups(user.id)
        subjects = SubjectQueries.get_teacher_subjects(user.id)

        print("My Groups:")
        for group in groups:
            print(f"- {group[1]}: {group[2]}")

        print("\nMy Subjects:")
        for subject in subjects:
            print(f"- {subject[1]} ({subject[2]}) - Group: {subject[6]}")

    @staticmethod
    def attendance_menu(user):
        while True:
            print("\n" + "-" * 30)
            print("ATTENDANCE MANAGEMENT")
            print("-" * 30)
            print("1. Mark Attendance")
            print("2. View Group Attendance")
            print("3. View Student Attendance Summary")
            print("4. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                TeacherMenu.mark_attendance(user)
            elif choice == '2':
                TeacherMenu.view_group_attendance(user)
            elif choice == '3':
                TeacherMenu.view_student_attendance_summary()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def mark_attendance(user):
        subjects = SubjectQueries.get_teacher_subjects(user.id)
        if not subjects:
            print("You are not assigned to any subjects.")
            return

        print("\nYour Subjects:")
        for i, subject in enumerate(subjects, 1):
            print(f"{i}. {subject[1]} - Group: {subject[6]}")

        try:
            choice = int(input("\nSelect subject (number): ")) - 1
            selected_subject = subjects[choice]
            subject_id = selected_subject[0]
            group_name = selected_subject[6]

            attendance_date = input(f"Date (YYYY-MM-DD, press Enter for today): ").strip() or str(date.today())

            group_id = None
            groups = GroupQueries.get_all_groups()
            for group in groups:
                if group[1] == group_name:
                    group_id = group[0]
                    break

            if group_id is None:
                print("Group not found.")
                return

            attendance_data = AttendanceQueries.get_group_attendance(group_id, subject_id, attendance_date)

            print(f"\nMarking attendance for {selected_subject[1]} - {group_name} on {attendance_date}")
            print("-" * 60)

            for student_data in attendance_data:
                student_id, student_name, current_status, notes = student_data
                print(f"\nStudent: {student_name}")
                print(f"Current status: {current_status}")

                status = input("Status (p=present, a=absent, l=late, s=skip): ").strip().lower()
                if status == 's':
                    continue

                status_map = {'p': 'present', 'a': 'absent', 'l': 'late'}
                if status in status_map:
                    notes = input("Notes (optional): ").strip()
                    AttendanceQueries.mark_attendance(student_id, subject_id, attendance_date, status_map[status],
                                                      notes, user.id)
                    print("Attendance marked!")
                else:
                    print("Invalid status, skipping...")

        except (ValueError, IndexError):
            print("Invalid selection.")

    @staticmethod
    def view_group_attendance(user):
        subjects = SubjectQueries.get_teacher_subjects(user.id)
        if not subjects:
            print("You are not assigned to any subjects.")
            return

        print("\nYour Subjects:")
        for i, subject in enumerate(subjects, 1):
            print(f"{i}. {subject[1]} - Group: {subject[6]}")

        try:
            choice = int(input("\nSelect subject (number): ")) - 1
            selected_subject = subjects[choice]
            subject_id = selected_subject[0]
            group_name = selected_subject[6]

            attendance_date = input(f"Date (YYYY-MM-DD, press Enter for today): ").strip() or str(date.today())

            group_id = None
            groups = GroupQueries.get_all_groups()
            for group in groups:
                if group[1] == group_name:
                    group_id = group[0]
                    break

            if group_id:
                attendance_data = AttendanceQueries.get_group_attendance(group_id, subject_id, attendance_date)

                print(f"\nAttendance for {selected_subject[1]} - {group_name} on {attendance_date}")
                print("-" * 60)
                print(f"{'Student Name':<25} {'Status':<12} {'Notes'}")
                print("-" * 60)

                for student_data in attendance_data:
                    student_name = student_data[1]
                    status = student_data[2]
                    notes = student_data[3] or ""
                    print(f"{student_name:<25} {status:<12} {notes}")

        except (ValueError, IndexError):
            print("Invalid selection.")

    @staticmethod
    def view_student_attendance_summary():
        student_id = input("Enter Student ID: ").strip()
        subject_id = input("Enter Subject ID (optional): ").strip()

        try:
            student_id = int(student_id)
            subject_id = int(subject_id) if subject_id else None

            if subject_id:
                summary = AttendanceQueries.get_attendance_summary(student_id, subject_id)
                if summary and summary[0] > 0:
                    print(f"\nAttendance Summary:")
                    print(f"Total Classes: {summary[0]}")
                    print(f"Present: {summary[1]}")
                    print(f"Absent: {summary[2]}")
                    print(f"Late: {summary[3]}")
                    print(f"Attendance Percentage: {summary[4]}%")
                else:
                    print("No attendance data found.")
            else:
                attendance = AttendanceQueries.get_student_attendance(student_id)
                print(f"\nAll Attendance Records:")
                print("-" * 70)
                for record in attendance:
                    print(f"Subject: {record[6]}, Date: {record[3]}, Status: {record[4]}")

        except ValueError:
            print("Invalid input.")

    @staticmethod
    def assignment_menu(user):
        while True:
            print("\n" + "-" * 30)
            print("ASSIGNMENT MANAGEMENT")
            print("-" * 30)
            print("1. Create Assignment")
            print("2. View My Assignments")
            print("3. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                TeacherMenu.create_assignment(user)
            elif choice == '2':
                TeacherMenu.view_my_assignments(user)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def create_assignment(user):
        subjects = SubjectQueries.get_teacher_subjects(user.id)
        if not subjects:
            print("You are not assigned to any subjects.")
            return

        print("\nYour Subjects:")
        for i, subject in enumerate(subjects, 1):
            print(f"{i}. {subject[1]} - Group: {subject[6]}")

        try:
            choice = int(input("\nSelect subject (number): ")) - 1
            selected_subject = subjects[choice]
            subject_id = selected_subject[0]
            group_name = selected_subject[6]

            group_id = None
            groups = GroupQueries.get_all_groups()
            for group in groups:
                if group[1] == group_name:
                    group_id = group[0]
                    break

            if group_id is None:
                print("Group not found.")
                return

            title = input("Assignment Title: ").strip()
            description = input("Description: ").strip()
            total_marks = int(input("Total Marks: ").strip())
            due_date = input("Due Date (YYYY-MM-DD, optional): ").strip() or None

            assignment_id = AssignmentQueries.create_assignment(title, description, subject_id, group_id, total_marks,
                                                                due_date, user.id)
            print(f"Assignment created successfully! ID: {assignment_id}")

        except (ValueError, IndexError):
            print("Invalid input.")

    @staticmethod
    def view_my_assignments(user):
        assignments = AssignmentQueries.get_teacher_assignments(user.id)

        print("\n" + "-" * 70)
        print("MY ASSIGNMENTS")
        print("-" * 70)
        print(f"{'ID':<5} {'Title':<20} {'Subject':<15} {'Group':<15} {'Due Date':<12} {'Marks'}")
        print("-" * 70)

        for assignment in assignments:
            due_date = assignment[6] or "N/A"
            print(
                f"{assignment[0]:<5} {assignment[1]:<20} {assignment[7]:<15} {assignment[8]:<15} {due_date:<12} {assignment[5]}")

    @staticmethod
    def grade_menu(user):
        while True:
            print("\n" + "-" * 30)
            print("GRADE MANAGEMENT")
            print("-" * 30)
            print("1. Grade Assignment")
            print("2. View Assignment Grades")
            print("3. View Student Grades")
            print("4. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                TeacherMenu.grade_assignment(user)
            elif choice == '2':
                TeacherMenu.view_assignment_grades()
            elif choice == '3':
                TeacherMenu.view_student_grades()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def grade_assignment(user):
        assignments = AssignmentQueries.get_teacher_assignments(user.id)
        if not assignments:
            print("You have no assignments.")
            return

        print("\nYour Assignments:")
        for i, assignment in enumerate(assignments, 1):
            print(f"{i}. {assignment[1]} - {assignment[7]} ({assignment[8]})")

        try:
            choice = int(input("\nSelect assignment (number): ")) - 1
            selected_assignment = assignments[choice]
            assignment_id = selected_assignment[0]

            students = GroupQueries.get_group_students(selected_assignment[4])

            print(f"\nGrading: {selected_assignment[1]}")
            print(f"Total Marks: {selected_assignment[5]}")
            print("-" * 50)

            for student in students:
                print(f"\nStudent: {student.full_name} (ID: {student.id})")
                marks = input(f"Marks obtained (out of {selected_assignment[5]}): ").strip()
                feedback = input("Feedback (optional): ").strip()

                if marks:
                    try:
                        marks = float(marks)
                        if 0 <= marks <= selected_assignment[5]:
                            GradeQueries.grade_assignment(student.id, assignment_id, marks, feedback, user.id)
                            print("Grade recorded!")
                        else:
                            print("Invalid marks range.")
                    except ValueError:
                        print("Invalid marks format.")

        except (ValueError, IndexError):
            print("Invalid selection.")

    @staticmethod
    def view_assignment_grades():
        assignment_id = input("Enter Assignment ID: ").strip()

        try:
            grades = GradeQueries.get_assignment_grades(int(assignment_id))

            print(f"\nGrades for Assignment ID: {assignment_id}")
            print("-" * 60)
            print(f"{'Student Name':<25} {'Marks':<10} {'Total':<8} {'Percentage'}")
            print("-" * 60)

            for grade in grades:
                percentage = round((grade[3] * 100 / grade[5]), 2)
                print(f"{grade[4]:<25} {grade[3]:<10} {grade[5]:<8} {percentage}%")

        except ValueError:
            print("Invalid assignment ID.")

    @staticmethod
    def view_student_grades():
        student_id = input("Enter Student ID: ").strip()

        try:
            grades = GradeQueries.get_student_grades(int(student_id))

            print(f"\nGrades for Student ID: {student_id}")
            print("-" * 80)
            print(f"{'Assignment':<20} {'Subject':<15} {'Marks':<8} {'Total':<8} {'Percentage'}")
            print("-" * 80)

            for grade in grades:
                print(f"{grade[6]:<20} {grade[8]:<15} {grade[3]:<8} {grade[7]:<8} {grade[9]}%")

        except ValueError:
            print("Invalid student ID.")

    @staticmethod
    def reports_menu(user):
        print("\n" + "-" * 30)
        print("REPORTS")
        print("-" * 30)
        print("1. My Groups Summary")
        print("2. My Subjects Summary")
        print("3. Class Performance")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            TeacherMenu.my_groups_summary(user)
        elif choice == '2':
            TeacherMenu.my_subjects_summary(user)
        elif choice == '3':
            TeacherMenu.class_performance(user)

    @staticmethod
    def my_groups_summary(user):
        groups = GroupQueries.get_teacher_groups(user.id)

        print("\n" + "-" * 50)
        print("MY GROUPS SUMMARY")
        print("-" * 50)

        for group in groups:
            students = GroupQueries.get_group_students(group[0])
            print(f"Group: {group[1]}")
            print(f"Total Students: {len(students)}")
            print(f"Description: {group[2]}")
            print("-" * 30)

    @staticmethod
    def my_subjects_summary(user):
        subjects = SubjectQueries.get_teacher_subjects(user.id)

        print("\n" + "-" * 50)
        print("MY SUBJECTS SUMMARY")
        print("-" * 50)

        for subject in subjects:
            print(f"Subject: {subject[1]} ({subject[2]})")
            print(f"Group: {subject[6]}")
            print(f"Credits: {subject[4]}")
            print("-" * 30)

    @staticmethod
    def class_performance(user):
        subjects = SubjectQueries.get_teacher_subjects(user.id)

        if not subjects:
            print("You are not assigned to any subjects.")
            return

        print("\nYour Subjects:")
        for i, subject in enumerate(subjects, 1):
            print(f"{i}. {subject[1]} - Group: {subject[6]}")

        try:
            choice = int(input("\nSelect subject (number): ")) - 1
            selected_subject = subjects[choice]
            subject_id = selected_subject[0]
            group_name = selected_subject[6]

            group_id = None
            groups = GroupQueries.get_all_groups()
            for group in groups:
                if group[1] == group_name:
                    group_id = group[0]
                    break

            if group_id:
                students = GroupQueries.get_group_students(group_id)

                print(f"\nClass Performance - {selected_subject[1]} ({group_name})")
                print("-" * 60)

                for student in students:
                    average = GradeQueries.get_student_subject_average(student.id, subject_id)
                    if average and average[0] > 0:
                        print(f"{student.full_name}: {average[1]}% average ({average[0]} assignments)")
                    else:
                        print(f"{student.full_name}: No grades yet")

        except (ValueError, IndexError):
            print("Invalid selection.")