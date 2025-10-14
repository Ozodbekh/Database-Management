from mysql.connector import connect

class MySql:
    def __init__(self):
        self._conn = connect(
            host="localhost",
            user="root",
            password="6236",
            database="db_mg",
            port=3306
        )
        self._cursor = self._conn.cursor()

    def db_tables(self):
        teachers = """
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                full_name VARCHAR(255) NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                email VARCHAR(255) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """

        groups_ = """
            CREATE TABLE IF NOT EXISTS groups_ (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                course_year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """

        students = """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                phone_number VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                group_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES groups_(id)
            )
        """

        subjects = """
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                teacher_id INTEGER,
                group_id INTEGER,
                schedule_day VARCHAR(255),
                schedule_time VARCHAR(255),
                room_number VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers(id),
                FOREIGN KEY (group_id) REFERENCES groups_(id)
            )
        """

        attendance = """
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                attendance_date DATE DEFAULT (CURRENT_DATE),
                status ENUM('came', 'did not come', 'caused') DEFAULT 'came',
                note VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            )
        """

        self._cursor.execute(teachers)
        self._cursor.execute(groups_)
        self._cursor.execute(students)
        self._cursor.execute(subjects)
        self._cursor.execute(attendance)
        self._cursor.close()
        self._conn.close()
        print("Created all tables")


if __name__ == "__main__":
    obj = MySql()
    obj.db_tables()