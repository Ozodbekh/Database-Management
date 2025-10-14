from sqlite3 import connect


class Sqlite:
    def __init__(self):
        self._database = "db_sqlite"
        self._conn = connect(database=self._database)
        self._cursor = self._conn.cursor()

    def db_tables(self):
        teachers = """
                   CREATE TABLE IF NOT EXISTS teachers
                   (
                       id           INTEGER PRIMARY KEY AUTOINCREMENT,
                       full_name    TEXT NOT NULL,
                       phone_number TEXT UNIQUE,
                       email        TEXT UNIQUE,
                       created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   ) \
                   """

        groups = """
                 CREATE TABLE IF NOT EXISTS groups
                 (
                     id          INTEGER PRIMARY KEY AUTOINCREMENT,
                     name        TEXT NOT NULL UNIQUE,
                     course_year INTEGER,
                     created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 ) \
                 """

        students = """
                   CREATE TABLE IF NOT EXISTS students
                   (
                       id         INTEGER PRIMARY KEY AUTOINCREMENT,
                       full_name  TEXT NOT NULL,
                       phone_number TEXT NOT NULL,
                       email      TEXT NOT NULL,
                       group_id   INTEGER,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (group_id) REFERENCES groups (id)
                   ) \
                   """

        subjects = """
                   CREATE TABLE IF NOT EXISTS subjects
                   (
                       id            INTEGER PRIMARY KEY AUTOINCREMENT,
                       name          TEXT NOT NULL,
                       teacher_id    INTEGER,
                       group_id      INTEGER,
                       schedule_day  TEXT,
                       schedule_time TEXT,
                       room_number   TEXT,
                       created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (teacher_id) REFERENCES teachers (id),
                       FOREIGN KEY (group_id) REFERENCES groups (id)
                   ) \
                   """

        attendance = """
                     CREATE TABLE IF NOT EXISTS attendance
                     (
                         id              INTEGER PRIMARY KEY AUTOINCREMENT,
                         student_id      INTEGER NOT NULL,
                         subject_id      INTEGER NOT NULL,
                         attandance_date DATE    NOT NULL  DEFAULT  (date('now')),
                         status          TEXT CHECK ( status IN ('came', 'did not come', 'caused')) DEFAULT 'came',
                         note            TEXT,
                         created_at      TIMESTAMP                                                  DEFAULT CURRENT_TIMESTAMP,
                         FOREIGN KEY (student_id) REFERENCES students (id),
                         FOREIGN KEY (subject_id) REFERENCES subjects (id),
                         UNIQUE (student_id, subject_id, attandance_date)
                     ) \
                     """

        self._cursor.execute(teachers)
        self._cursor.execute(groups)
        self._cursor.execute(students)
        self._cursor.execute(subjects)
        self._cursor.execute(attendance)
        self._cursor.close()
        self._conn.close()
        print("Created all tables")

    def insert_data(self):
        teachers_data = [
            ("Dilnoza Ahmedova", "+998901234567", "dilnoza.ahmedova@example.com"),
            ("Jasur Rasulov", "+998902223344", "jasur.rasulov@example.com"),
            ("Malika To‘xtayeva", "+998903334455", "malika.toxtayeva@example.com"),
            ("Sherzod Qodirov", "+998904445566", "sherzod.qodirov@example.com"),
            ("Nodira Abdug‘anieva", "+998905556677", "nodira.abduganieva@example.com"),
            ("Olimjon Hamidov", "+998906667788", "olimjon.hamidov@example.com"),
            ("Gulbahor To‘laganova", "+998907778899", "gulbahor.tolaganova@example.com"),
            ("Behruz Mahmudov", "+998908889900", "behruz.mahmudov@example.com"),
            ("Shahnoza Nurmatova", "+998909990011", "shahnoza.nurmatova@example.com")
        ]

        groups_data = [
            ("Python", 3),
            ("Java", 2),
            ("Kotlin", 4),
            ("C#", 5),
            ("C++", 2),
            ("C", 5),
            ("Go", 3)
        ]

        students_data = [
            ("Botirov Anvar", "+998910000001", "anvar1@gmail.com", 1),
            ("Karimova Dilnoza", "+998910000002", "dilnoza1@gmail.com", 1),
            ("Xolmatov Sherzod", "+998910000003", "sherzod1@gmail.com", 1),
            ("Usmonova Maftuna", "+998910000004", "maftuna1@gmail.com", 1),
            ("Abduqodirov Bekzod", "+998910000005", "bekzod1@gmail.com", 1),
            ("Tursunova Madina", "+998910000006", "madina1@gmail.com", 1),
            ("Rasulov Ibrohim", "+998910000007", "ibrohim1@gmail.com", 1),
            ("G‘ulomova Shahnoza", "+998910000008", "shahnoza1@gmail.com", 1),
            ("Sodiqov Javohir", "+998910000009", "javohir1@gmail.com", 1),
            ("Qurbonova Sevara", "+998910000010", "sevara1@gmail.com", 1),

            ("Xasanov Nodir", "+998910000011", "nodir2@gmail.com", 2),
            ("Ortiqova Malika", "+998910000012", "malika2@gmail.com", 2),
            ("Abdullayev Doston", "+998910000013", "doston2@gmail.com", 2),
            ("Rustamova Laylo", "+998910000014", "laylo2@gmail.com", 2),
            ("Qodirov Akmal", "+998910000015", "akmal2@gmail.com", 2),
            ("Sobirova Mohira", "+998910000016", "mohira2@gmail.com", 2),
            ("To‘xtayev Aziz", "+998910000017", "aziz2@gmail.com", 2),
            ("Shamsiyeva Nargiza", "+998910000018", "nargiza2@gmail.com", 2),
            ("Bekmurodov Sarvar", "+998910000019", "sarvar2@gmail.com", 2),
            ("Ravshanova Nilufar", "+998910000020", "nilufar2@gmail.com", 2),

            ("Mirzayev Umid", "+998910000021", "umid3@gmail.com", 3),
            ("Abdullayeva Guli", "+998910000022", "guli3@gmail.com", 3),
            ("Jo‘rayev Baxtiyor", "+998910000023", "baxtiyor3@gmail.com", 3),
            ("Yo‘ldosheva Dilrabo", "+998910000024", "dilrabo3@gmail.com", 3),
            ("Rasulova Zilola", "+998910000025", "zilola3@gmail.com", 3),
            ("To‘laganov Otabek", "+998910000026", "otabek3@gmail.com", 3),
            ("Qurbonova Nasiba", "+998910000027", "nasiba3@gmail.com", 3),
            ("Suyunov Jamshid", "+998910000028", "jamshid3@gmail.com", 3),
            ("Matkarimova Maftuna", "+998910000029", "maftuna3@gmail.com", 3),
            ("Ergashev Kamol", "+998910000030", "kamol3@gmail.com", 3),

            ("Toshpo‘latov Islom", "+998910000031", "islom4@gmail.com", 4),
            ("Nurmatova Dildora", "+998910000032", "dildora4@gmail.com", 4),
            ("Qobilov Ravshan", "+998910000033", "ravshan4@gmail.com", 4),
            ("Zokirova Munisa", "+998910000034", "munisa4@gmail.com", 4),
            ("Isroilov Diyor", "+998910000035", "diyor4@gmail.com", 4),
            ("Shomurodova Ziyoda", "+998910000036", "ziyoda4@gmail.com", 4),
            ("Raxmatov Sherzod", "+998910000037", "sherzod4@gmail.com", 4),
            ("Yusupova Mahliyo", "+998910000038", "mahliyo4@gmail.com", 4),
            ("Xudoyberdiyev Asad", "+998910000039", "asad4@gmail.com", 4),
            ("Sattorova Nargiza", "+998910000040", "nargiza4@gmail.com", 4),

            ("Yo‘ldoshev Ulug‘bek", "+998910000041", "ulugbek5@gmail.com", 5),
            ("Toshmatova Go‘zal", "+998910000042", "gozal5@gmail.com", 5),
            ("Abduvaliyev Bobur", "+998910000043", "bobur5@gmail.com", 5),
            ("Matmurodova Laylo", "+998910000044", "laylo5@gmail.com", 5),
            ("Eshmurodov Anvar", "+998910000045", "anvar5@gmail.com", 5),
            ("Kurbanova Dilshoda", "+998910000046", "dilshoda5@gmail.com", 5),
            ("Sodiqova Shahnoza", "+998910000047", "shahnoza5@gmail.com", 5),
            ("Jo‘rayev Rustam", "+998910000048", "rustam5@gmail.com", 5),
            ("Suyunova Zarina", "+998910000049", "zarina5@gmail.com", 5),
            ("Shavkatov Azizbek", "+998910000050", "azizbek5@gmail.com", 5),

            ("Abdurahmonov Kamron", "+998910000051", "kamron6@gmail.com", 6),
            ("Jumayeva Mohinur", "+998910000052", "mohinur6@gmail.com", 6),
            ("Shukurov Doston", "+998910000053", "doston6@gmail.com", 6),
            ("Rustamova Nilufar", "+998910000054", "nilufar6@gmail.com", 6),
            ("Karimov Alisher", "+998910000055", "alisher6@gmail.com", 6),
            ("Abdullayeva Madina", "+998910000056", "madina6@gmail.com", 6),
            ("To‘xtasinov Jasur", "+998910000057", "jasur6@gmail.com", 6),
            ("Rasulova Sevara", "+998910000058", "sevara6@gmail.com", 6),
            ("Xolmatov Shuxrat", "+998910000059", "shuxrat6@gmail.com", 6),
            ("G‘aniyeva Dildora", "+998910000060", "dildora6@gmail.com", 6),

            ("Yuldashev Sherzod", "+998910000061", "sherzod7@gmail.com", 7),
            ("Abdug‘afurova Maftuna", "+998910000062", "maftuna7@gmail.com", 7),
            ("Rasulov Bekzod", "+998910000063", "bekzod7@gmail.com", 7),
            ("O‘rozova Laylo", "+998910000064", "laylo7@gmail.com", 7),
            ("Tursunov Aziz", "+998910000065", "aziz7@gmail.com", 7),
            ("Jo‘rayeva Nargiza", "+998910000066", "nargiza7@gmail.com", 7),
            ("Saidov Diyor", "+998910000067", "diyor7@gmail.com", 7),
            ("Matkarimova Zilola", "+998910000068", "zilola7@gmail.com", 7),
            ("Rustamov Shaxzod", "+998910000069", "shaxzod7@gmail.com", 7),
            ("Kurbanova Nilufar", "+998910000070", "nilufar7@gmail.com", 7)
        ]

        subjects_data = [
            ("Matematika", 1, 1, "Dushanba", "09:00", "101"),
            ("Geometriya", 1, 2, "Payshanba", "10:00", "102"),

            ("Fizika", 2, 3, "Seshanba", "11:00", "201"),
            ("Astronomiya", 2, 4, "Juma", "12:00", "202"),

            ("Informatika", 3, 5, "Chorshanba", "09:00", "301"),
            ("Robototexnika", 3, 6, "Shanba", "11:00", "302"),

            ("Kimyo", 4, 7, "Dushanba", "13:00", "401"),
            ("Biologiya", 4, 1, "Payshanba", "14:00", "402"),

            ("Tarix", 5, 2, "Seshanba", "09:00", "501"),
            ("Huquq", 5, 3, "Juma", "10:00", "502"),

            ("Ona tili", 6, 4, "Chorshanba", "08:00", "601"),
            ("Adabiyot", 6, 5, "Shanba", "10:00", "602"),

            ("Ingliz tili", 7, 6, "Dushanba", "09:00", "701"),
            ("Nemis tili", 7, 7, "Payshanba", "11:00", "702"),

            ("Iqtisod", 8, 1, "Seshanba", "13:00", "801"),
            ("Buxgalteriya", 8, 2, "Juma", "14:00", "802"),

            ("Rasm", 9, 3, "Chorshanba", "15:00", "901"),
            ("Musiqa", 9, 4, "Shanba", "16:00", "902")
        ]

        attendance_data = [
            (1, 1, "2025-10-01", "came", None),
            (2, 1, "2025-10-01", "did not come", "kasal bo'lgan"),
            (3, 2, "2025-10-01", "came", None),
            (4, 2, "2025-10-02", "came", None),
            (5, 3, "2025-10-02", "caused", "kechikkan"),
            (6, 3, "2025-10-02", "came", None),
            (7, 4, "2025-10-03", "did not come", "sababsiz"),
            (8, 4, "2025-10-03", "came", None),
            (9, 5, "2025-10-03", "came", None),
            (10, 5, "2025-10-03", "came", None),
            (11, 6, "2025-10-04", "caused", "kechikdi"),
            (12, 6, "2025-10-04", "came", None),
            (13, 7, "2025-10-04", "did not come", "uyda ish bo'lgan"),
            (14, 7, "2025-10-04", "came", None),
            (15, 8, "2025-10-05", "came", None),
            (16, 8, "2025-10-05", "caused", "kechikdi"),
            (17, 9, "2025-10-05", "came", None),
            (18, 9, "2025-10-06", "did not come", "sababsiz"),
            (19, 10, "2025-10-06", "came", None),
            (20, 10, "2025-10-06", "came", None),
            (21, 11, "2025-10-07", "came", None),
            (22, 11, "2025-10-07", "did not come", "kasal bo'lgan"),
            (23, 12, "2025-10-07", "caused", "kechikdi"),
            (24, 12, "2025-10-08", "came", None),
            (25, 13, "2025-10-08", "did not come", "uyda mehmon"),
            (26, 13, "2025-10-08", "came", None),
            (27, 14, "2025-10-09", "caused", "kechikkan"),
            (28, 14, "2025-10-09", "came", None),
            (29, 15, "2025-10-09", "came", None),
            (30, 15, "2025-10-09", "did not come", "sababsiz")
        ]

        self._cursor.executemany("""
            INSERT INTO teachers (full_name, phone_number, email)
                VALUES (?, ?, ?)
        """, teachers_data)

        for data in groups_data:
            self._cursor.execute("""
                INSERT INTO groups (name, course_year)
                    VALUES (?, ?)
            """, data)

        self._cursor.executemany("""
            INSERT INTO students (full_name, phone_number, email, group_id)
                VALUES (?, ?, ?, ?)
        """, students_data)

        self._cursor.executemany("""
            INSERT INTO subjects (name, teacher_id, group_id, schedule_day, schedule_time, room_number)
                VALUES (?, ?, ?, ?, ?, ?)
        """, subjects_data)

        self._cursor.executemany("""
            INSERT INTO attendance (student_id, subject_id, attandance_date, status, note)
                VALUES (?, ?, ?, ?, ?)
        """, attendance_data)


        self._cursor.close()
        self._conn.commit()
        self._conn.close()

    def update_data(self):
        self._cursor.execute("""
            UPDATE teachers SET created_at = CURRENT_TIMESTAMP
        """)

        self._cursor.execute("""
            UPDATE students SET full_name = 'Ozodbek Gofurov' WHERE id = 2
        """)

        self._conn.commit()
        self._cursor.close()
        self._conn.close()

    def delete_data(self):
        # self._cursor.execute("""
        #     DELETE FROM attendance WHERE id = 1
        # """)

        # self._cursor.execute("""
        #     DELETE FROM attendance
        # """)

        self._conn.commit()
        self._cursor.close()
        self._conn.close()


if __name__ == "__main__":
    obj = Sqlite()
    # obj.db_tables()
    # obj.insert_data()
    # obj.update_data()
    # obj.delete_data()