from laboratories.connections import get_connection_postgres

conn = get_connection_postgres()
cursor = conn.cursor()


cursor.execute("""
   DROP TABLE IF EXISTS students CASCADE;
   DROP TABLE IF EXISTS groups CASCADE;
""")


cursor.execute("""
    CREATE TABLE groups(
        id   SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL
    )
""")


cursor.execute("""
    CREATE TABLE students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        group_id INTEGER REFERENCES groups(id)
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


cursor.executemany("INSERT INTO groups (id, name) VALUES (%s, %s)", groups_data)
cursor.executemany("INSERT INTO students (id, name, group_id) VALUES (%s, %s, %s)", students_data)

conn.commit()

print("=" * 60)
print("Postgres SQL - JOIN operators")
print("=" * 60)


def inner_join():
    print("\n1. INNER JOIN (JOIN)")
    print("-" * 60)
    query = """
    SELECT students.id, students.name, groups.name
    FROM students
    INNER JOIN groups ON students.group_id = groups.id
    ORDER BY students.id
    """
    results = cursor.execute(query)
    print("ID | Name        | Group")
    for result in results:
        print(f"{result[0]:<3}| {result[1]:<10} | {result[2]}")


def left_join():
    print("\n2. LEFT JOIN")
    print("-" * 60)
    query = """
    SELECT students.id, students.name, groups.name
    FROM students
    LEFT JOIN groups ON students.group_id = groups.id
    ORDER BY students.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("ID | Name        | Group")
    for result in results:
        group = result[2] if result[2] else "NULL"
        print(f"{result[0]:<3}| {result[1]:<10} | {group}")


def right_join():
    print("\n3. RIGHT JOIN")
    print("-" * 60)
    query = """
    SELECT students.id, students.name, groups.name
    FROM students
    RIGHT JOIN groups ON students.group_id = groups.id
    ORDER BY groups.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("ID   | Name        | Group")
    for result in results:
        student_id = result[0] if result[0] else "NULL"
        name = result[1] if result[1] else "NULL"
        print(f"{str(student_id):<5}| {name:<10} | {result[2]}")


def full_join():
    print("\n4. FULL JOIN")
    print("-" * 60)
    query = """
    SELECT students.id, students.name, groups.name
    FROM students
    FULL JOIN groups ON students.group_id = groups.id
    students.id, NULLS LAST, groups.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("ID   | Name        | Group")
    for result in results:
        student_id = result[0] if result[0] else "NULL"
        name = result[1] if result[1] else "NULL"
        group = result[2] if result[2] else "NULL"
        print(f"{str(student_id):<5}| {name:<10} | {group}")


inner_join()
left_join()
right_join()
full_join()


cursor.close()
conn.close()
