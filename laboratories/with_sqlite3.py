from laboratories.connections import get_connection_sqlite3

conn = get_connection_sqlite3()
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS groups")

cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        group_id INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE groups (
        id INTEGER PRIMARY KEY,
        group_name TEXT
    )
""")


students_data = [
    (1, "John Smith", 1),
    (2, "James Anderson", 2),
    (3, "Emily Johnson", 1),
    (4, "Michael Smith", None),
    (5, "Olivia Brown", 3),
    (6, "William Davis", 2),
    (7, "Sophia Wilson", 1),
    (8, "Benjamin Moore", 4),
    (9, "Emma Taylor", 3),
    (10, "Lucas Martinez", None),
    (11, "Isabella Garcia", 2),
    (12, "Mason Rodriguez", 1),
    (13, "Ava Martinez", 4),
    (14, "Ethan Lee", None),
    (15, "Mia White", 3),
    (16, "Alexander Harris", 1),
    (17, "Charlotte Clark", 2),
    (18, "Daniel Lewis", 4),
    (19, "Amelia Walker", 3),
    (20, "Matthew Hall", 1)
]

groups_data = [
    (1, "Python"),
    (2, "Java"),
    (3, "C++"),
    (4, "Assembly"),
    (5, "JavaScript"),
    (6, "Ruby"),
    (7, "Go"),
    (8, "Rust")
]

cursor.executemany("INSERT INTO students VALUES (?, ?, ?)", students_data)
cursor.executemany("INSERT INTO groups VALUES (?, ?)", groups_data)

conn.commit()

print("=" * 60)
print("SQLite3 - JOIN operators")
print("=" * 60)


def inner_join():
    print("\n1. INNER JOIN (JOIN)")
    print("-" * 60)
    query = """
        SELECT students.id, students.full_name, groups.group_name
        FROM students
        INNER JOIN groups ON students.group_id = groups.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("ID  | Full name              | Group")
    print("-" * 60)
    for result in results:
        print(f"{result[0]:<4}| {result[1]:<22} | {result[2]}")


def left_join():
    print("\n2. LEFT JOIN")
    print("-" * 60)
    query = """
        SELECT students.id, students.full_name, groups.group_name
        FROM students
        LEFT JOIN groups ON students.group_id = groups.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("ID  | Full name              | Group")
    print("-" * 60)
    for result in results:
        group = result[2] if result[2] else "NULL"
        print(f"{result[0]:<4}| {result[1]:<22} | {group}")


def right_join():
    print("\n3. RIGHT JOIN (BY LEFT JOIN)")
    print("-" * 60)
    query = """
        SELECT students.id, students.full_name, groups.group_name
        FROM groups
        LEFT JOIN students ON groups.id = students.group_id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("ID  | Full name              | Group")
    print("-" * 60)
    for result in results:
        student_id = result[0] if result[0] else "NULL"
        full_name = result[1] if result[1] else "NULL"
        print(f"{str(student_id):<4}| {full_name:<22} | {result[2]}")


def full_outer_join():
    print("\n4. FULL OUTER JOIN (BY UNION)")
    print("-" * 60)
    query = """
        SELECT students.id, students.full_name, groups.group_name
        FROM students
        LEFT JOIN groups ON students.group_id = groups.id
        UNION
        SELECT students.id, students.full_name, groups.group_name
        FROM groups
        LEFT JOIN students ON groups.id = students.group_id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("ID  | Full Name              | Group")
    print("-" * 60)
    for result in results:
        student_id = result[0] if result[0] else "NULL"
        full_name = result[1] if result[1] else "NULL"
        group = result[2] if result[2] else "NULL"
        print(f"{str(student_id):<4}| {full_name:<22} | {group}")


inner_join()
left_join()
right_join()
full_outer_join()

conn.close()