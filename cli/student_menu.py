from cli.auth_menu import AuthMenu
from db.queries import GroupQueries, SubjectQueries, AttendanceQueries, AssignmentQueries, GradeQueries


class StudentMenu:
    @staticmethod
    def show_menu(user):
        while True:
            print("\n" + "=" * 50)
            print(f"STUDENT PANEL - Welcome {user.full_name}")
            print("=" * 50)
            print("1. My Groups & Subjects")
            print("2. My Attendance")
            print("3. My Assignments")
            print("4. My Grades")
            print("5. Academic Summary")
            print("6. Logout")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                StudentMenu.view_my_groups_subjects(user)
            elif choice == '2':
                StudentMenu.view_my_attendance(user)
            elif choice == '3':
                StudentMenu.view_my_assignments(user)
            elif choice == '4':
                StudentMenu.view_my_grades(user)
            elif choice == '5':
                StudentMenu.academic_summary(user)
            elif choice == '6':
                AuthMenu.logout()
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def view_my_groups_subjects(user):
        print("\n" + "-" * 50)
        print("MY GROUPS & SUBJECTS")
        print("-" * 50)

        groups = GroupQueries.get_student_groups(user.id)

        if not groups:
            print("You are not enrolled in any groups.")
            return

        print("My Groups:")
        for group in groups:
            print(f"- {group[1]}: {group[2]}")

            subjects = SubjectQueries.get_group_subjects(group[0])
            if subjects:
                print("  Subjects:")
                for subject in subjects:
                    print(f"    • {subject[1]} ({subject[2]}) - Teacher: {subject[5]}")
            else:
                print("    No subjects assigned yet.")
            print()

    @staticmethod
    def view_my_attendance(user):
        while True:
            print("\n" + "-" * 30)
            print("MY ATTENDANCE")
            print("-" * 30)
            print("1. View All Attendance")
            print("2. View Attendance by Subject")
            print("3. Attendance Summary")
            print("4. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                StudentMenu.view_all_attendance(user)
            elif choice == '2':
                StudentMenu.view_attendance_by_subject(user)
            elif choice == '3':
                StudentMenu.attendance_summary(user)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def view_all_attendance(user):
        attendance = AttendanceQueries.get_student_attendance(user.id)

        if not attendance:
            print("No attendance records found.")
            return

        print("\n" + "-" * 70)
        print("ALL ATTENDANCE RECORDS")
        print("-" * 70)
        print(f"{'Date':<12} {'Subject':<20} {'Status':<12} {'Notes'}")
        print("-" * 70)

        for record in attendance:
            notes = record[5] or ""
            print(f"{record[3]:<12} {record[6]:<20} {record[4]:<12} {notes}")

    @staticmethod
    def view_attendance_by_subject(user):
        groups = GroupQueries.get_student_groups(user.id)

        if not groups:
            print("You are not enrolled in any groups.")
            return

        all_subjects = []
        for group in groups:
            subjects = SubjectQueries.get_group_subjects(group[0])
            all_subjects.extend(subjects)

        if not all_subjects:
            print("No subjects found.")
            return

        print("\nYour Subjects:")
        for i, subject in enumerate(all_subjects, 1):
            print(f"{i}. {subject[1]} ({subject[2]})")

        try:
            choice = int(input("\nSelect subject (number): ")) - 1
            selected_subject = all_subjects[choice]
            subject_id = selected_subject[0]

            attendance = AttendanceQueries.get_student_attendance(user.id, subject_id)

            print(f"\nAttendance for {selected_subject[1]}")
            print("-" * 50)
            print(f"{'Date':<12} {'Status':<12} {'Notes'}")
            print("-" * 50)

            for record in attendance:
                notes = record[5] or ""
                print(f"{record[3]:<12} {record[4]:<12} {notes}")

        except (ValueError, IndexError):
            print("Invalid selection.")

    @staticmethod
    def attendance_summary(user):
        groups = GroupQueries.get_student_groups(user.id)

        if not groups:
            print("You are not enrolled in any groups.")
            return

        print("\n" + "-" * 60)
        print("ATTENDANCE SUMMARY")
        print("-" * 60)
        print(f"{'Subject':<20} {'Total':<8} {'Present':<8} {'Absent':<8} {'Late':<8} {'Percentage'}")
        print("-" * 60)

        for group in groups:
            subjects = SubjectQueries.get_group_subjects(group[0])
            for subject in subjects:
                summary = AttendanceQueries.get_attendance_summary(user.id, subject[0])
                if summary and summary[0] > 0:
                    print(
                        f"{subject[1]:<20} {summary[0]:<8} {summary[1]:<8} {summary[2]:<8} {summary[3]:<8} {summary[4]}%")
                else:
                    print(f"{subject[1]:<20} {'0':<8} {'0':<8} {'0':<8} {'0':<8} {'N/A'}")

    @staticmethod
    def view_my_assignments(user):
        groups = GroupQueries.get_student_groups(user.id)

        if not groups:
            print("You are not enrolled in any groups.")
            return

        print("\n" + "-" * 80)
        print("MY ASSIGNMENTS")
        print("-" * 80)
        print(f"{'Title':<20} {'Subject':<15} {'Total Marks':<12} {'Due Date':<12} {'Status'}")
        print("-" * 80)

        for group in groups:
            assignments = AssignmentQueries.get_group_assignments(group[0])
            for assignment in assignments:
                grades = GradeQueries.get_assignment_grades(assignment[0])
                student_graded = any(grade[1] == user.id for grade in grades)
                status = "Graded" if student_graded else "Pending"
                due_date = assignment[6] or "N/A"

                print(f"{assignment[1]:<20} {assignment[7]:<15} {assignment[5]:<12} {due_date:<12} {status}")

    @staticmethod
    def view_my_grades(user):
        while True:
            print("\n" + "-" * 30)
            print("MY GRADES")
            print("-" * 30)
            print("1. View All Grades")
            print("2. View Grades by Subject")
            print("3. Grade Summary")
            print("4. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                StudentMenu.view_all_grades(user)
            elif choice == '2':
                StudentMenu.view_grades_by_subject(user)
            elif choice == '3':
                StudentMenu.grade_summary(user)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def view_all_grades(user):
        grades = GradeQueries.get_student_grades(user.id)

        if not grades:
            print("No grades found.")
            return

        print("\n" + "-" * 90)
        print("ALL GRADES")
        print("-" * 90)
        print(f"{'Assignment':<20} {'Subject':<15} {'Marks':<8} {'Total':<8} {'Percentage':<12} {'Date'}")
        print("-" * 90)

        for grade in grades:
            graded_date = grade[10].split()[0] if grade[10] else "N/A"
            print(f"{grade[6]:<20} {grade[8]:<15} {grade[3]:<8} {grade[7]:<8} {grade[9]}%{'':<7} {graded_date}")

    @staticmethod
    def view_grades_by_subject(user):
        groups = GroupQueries.get_student_groups(user.id)

        if not groups:
            print("You are not enrolled in any groups.")
            return

        all_subjects = []
        for group in groups:
            subjects = SubjectQueries.get_group_subjects(group[0])
            all_subjects.extend(subjects)

        if not all_subjects:
            print("No subjects found.")
            return

        print("\nYour Subjects:")
        for i, subject in enumerate(all_subjects, 1):
            print(f"{i}. {subject[1]} ({subject[2]})")

        try:
            choice = int(input("\nSelect subject (number): ")) - 1
            selected_subject = all_subjects[choice]
            subject_id = selected_subject[0]

            grades = GradeQueries.get_student_grades(user.id)
            subject_grades = [g for g in grades if g[8] == selected_subject[1]]

            print(f"\nGrades for {selected_subject[1]}")
            print("-" * 70)
            print(f"{'Assignment':<25} {'Marks':<8} {'Total':<8} {'Percentage':<12} {'Date'}")
            print("-" * 70)

            for grade in subject_grades:
                graded_date = grade[10].split()[0] if grade[10] else "N/A"
                print(f"{grade[6]:<25} {grade[3]:<8} {grade[7]:<8} {grade[9]}%{'':<7} {graded_date}")

            if subject_grades:
                average = GradeQueries.get_student_subject_average(user.id, subject_id)
                if average and average[0] > 0:
                    print("-" * 70)
                    print(f"Subject Average: {average[1]}%")

        except (ValueError, IndexError):
            print("Invalid selection.")

    @staticmethod
    def grade_summary(user):
        groups = GroupQueries.get_student_groups(user.id)

        if not groups:
            print("You are not enrolled in any groups.")
            return

        print("\n" + "-" * 70)
        print("GRADE SUMMARY BY SUBJECT")
        print("-" * 70)
        print(f"{'Subject':<20} {'Assignments':<12} {'Average':<10} {'Total Points'}")
        print("-" * 70)

        overall_total_obtained = 0
        overall_total_possible = 0

        for group in groups:
            subjects = SubjectQueries.get_group_subjects(group[0])
            for subject in subjects:
                average = GradeQueries.get_student_subject_average(user.id, subject[0])
                if average and average[0] > 0:
                    print(f"{subject[1]:<20} {average[0]:<12} {average[1]}%{'':<5} {average[2]}/{average[3]}")
                    overall_total_obtained += average[2]
                    overall_total_possible += average[3]
                else:
                    print(f"{subject[1]:<20} {'0':<12} {'N/A':<10} {'0/0'}")

        if overall_total_possible > 0:
            overall_percentage = round((overall_total_obtained * 100 / overall_total_possible), 2)
            print("-" * 70)
            print(
                f"{'OVERALL':<20} {'':<12} {overall_percentage}%{'':<5} {overall_total_obtained}/{overall_total_possible}")

    @staticmethod
    def academic_summary(user):
        print("\n" + "=" * 60)
        print("ACADEMIC SUMMARY")
        print("=" * 60)

        groups = GroupQueries.get_student_groups(user.id)

        if not groups:
            print("You are not enrolled in any groups.")
            return

        print(f"Student: {user.full_name}")
        print(f"Phone: {user.phone_number}")
        print(f"Email: {user.email or 'N/A'}")
        print()

        for group in groups:
            print(f"Group: {group[1]}")
            subjects = SubjectQueries.get_group_subjects(group[0])

            if subjects:
                print("Subjects and Performance:")
                total_credits = 0
                weighted_average = 0

                for subject in subjects:
                    total_credits += subject[4]

                    average = GradeQueries.get_student_subject_average(user.id, subject[0])
                    attendance_summary = AttendanceQueries.get_attendance_summary(user.id, subject[0])

                    if average and average[0] > 0:
                        grade_avg = average[1]
                        weighted_average += grade_avg * subject[4]
                    else:
                        grade_avg = 0

                    attendance_pct = attendance_summary[4] if attendance_summary and attendance_summary[0] > 0 else 0

                    print(f"  • {subject[1]} ({subject[2]}) - {subject[4]} credits")
                    print(f"    Teacher: {subject[5]}")
                    print(f"    Grade Average: {grade_avg}%")
                    print(f"    Attendance: {attendance_pct}%")
                    print()

                if total_credits > 0:
                    gpa = weighted_average / total_credits
                    print(f"Group GPA: {gpa:.2f}%")
                    print(f"Total Credits: {total_credits}")

            print("-" * 40)
