from .auth import AuthService
from .queries import UserQueries, GroupQueries, SubjectQueries


def seed_sample_data():
    print("Seeding sample data...")

    admin_user = UserQueries.get_user_by_phone("admin")
    if not admin_user:
        UserQueries.create_user("System Admin", "admin", "admin@school.com", "admin123", "admin")
        print("Default admin created")

    try:
        teacher1_id = UserQueries.create_user("John Smith", "teacher001", "john@school.com", "teacher123", "teacher")
        teacher2_id = UserQueries.create_user("Sarah Johnson", "teacher002", "sarah@school.com", "teacher123",
                                              "teacher")
        teacher3_id = UserQueries.create_user("Mike Brown", "teacher003", "mike@school.com", "teacher123", "teacher")
        print("Sample teachers created")
    except:
        print("Teachers might already exist")

    sample_students = [
        ("Alice Wilson", "student001", "alice@email.com", "student123"),
        ("Bob Davis", "student002", "bob@email.com", "student123"),
        ("Carol Miller", "student003", "carol@email.com", "student123"),
        ("David Garcia", "student004", "david@email.com", "student123"),
        ("Emma Martinez", "student005", "emma@email.com", "student123"),
        ("Frank Thompson", "student006", "frank@email.com", "student123"),
        ("Grace Lee", "student007", "grace@email.com", "student123"),
        ("Henry Wang", "student008", "henry@email.com", "student123"),
    ]

    student_ids = []
    for name, phone, email, password in sample_students:
        try:
            student_id = UserQueries.create_user(name, phone, email, password, "student")
            student_ids.append(student_id)
        except:
            pass

    print("Sample students created")

    try:
        group1_id = GroupQueries.create_group("Computer Science 2024", "CS students batch 2024")
        group2_id = GroupQueries.create_group("Mathematics 2024", "Math students batch 2024")
        group3_id = GroupQueries.create_group("Physics 2024", "Physics students batch 2024")
        print("Sample groups created")
    except:
        print("Groups might already exist")

    sample_subjects = [
        ("Python Programming", "CS101", "Introduction to Python programming", 4),
        ("Data Structures", "CS201", "Data structures and algorithms", 4),
        ("Database Systems", "CS301", "Database design and management", 3),
        ("Calculus I", "MATH101", "Differential and integral calculus", 4),
        ("Linear Algebra", "MATH201", "Vectors, matrices, and linear transformations", 3),
        ("Statistics", "MATH301", "Statistical analysis and probability", 3),
        ("Classical Mechanics", "PHYS101", "Newton's laws and mechanics", 4),
        ("Electromagnetics", "PHYS201", "Electric and magnetic fields", 4),
    ]

    subject_ids = []
    for name, code, desc, credits in sample_subjects:
        try:
            subject_id = SubjectQueries.create_subject(name, code, desc, credits)
            subject_ids.append(subject_id)
        except:
            pass

    print("Sample subjects created")

    try:

        for i in range(min(4, len(student_ids))):
            GroupQueries.enroll_student(student_ids[i], group1_id)

        for i in range(4, min(6, len(student_ids))):
            GroupQueries.enroll_student(student_ids[i], group2_id)

        for i in range(6, len(student_ids)):
            GroupQueries.enroll_student(student_ids[i], group3_id)

        print("Students enrolled in groups")
    except:
        print("Enrollment might already exist")

    try:
        teachers = UserQueries.get_users_by_role("teacher")
        if len(teachers) >= 3 and len(subject_ids) >= 8:
            SubjectQueries.assign_teacher_to_subject(group1_id, subject_ids[0], teachers[0].id)
            SubjectQueries.assign_teacher_to_subject(group1_id, subject_ids[1], teachers[0].id)
            SubjectQueries.assign_teacher_to_subject(group1_id, subject_ids[2], teachers[0].id)

            SubjectQueries.assign_teacher_to_subject(group2_id, subject_ids[3], teachers[1].id)
            SubjectQueries.assign_teacher_to_subject(group2_id, subject_ids[4], teachers[1].id)
            SubjectQueries.assign_teacher_to_subject(group2_id, subject_ids[5], teachers[1].id)

            SubjectQueries.assign_teacher_to_subject(group3_id, subject_ids[6], teachers[2].id)
            SubjectQueries.assign_teacher_to_subject(group3_id, subject_ids[7], teachers[2].id)

        print("Teachers assigned to subjects")
    except Exception as e:
        print(f"Teacher assignment failed: {e}")

    print("\nSample data seeding completed!")
    print("\nSample Login Credentials:")
    print("=" * 40)
    print("Admin:")
    print("  Phone: admin")
    print("  Password: admin123")
    print("\nTeachers:")
    print("  Phone: teacher001, Password: teacher123")
    print("  Phone: teacher002, Password: teacher123")
    print("  Phone: teacher003, Password: teacher123")
    print("\nStudents:")
    print("  Phone: student001, Password: student123")
    print("  Phone: student002, Password: student123")
    print("  (and so on...)")


if __name__ == "__main__":
    from schema import create_tables, insert_default_permissions

    create_tables()
    insert_default_permissions()
    seed_sample_data()
