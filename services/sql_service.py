import pyodbc
from config import SQL_DRIVER, SQL_SERVER, SQL_DATABASE, SQL_TRUSTED_CONNECTION

def get_conn():
    return pyodbc.connect(
        f"DRIVER={{{SQL_DRIVER}}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"Trusted_Connection={SQL_TRUSTED_CONNECTION};"
    )

def clear_sql_tables():
    """
    Clears data in FK-safe order.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM Enrollments;")
    cur.execute("DELETE FROM Courses;")
    cur.execute("DELETE FROM Instructors;")
    cur.execute("DELETE FROM Students;")
    cur.execute("DELETE FROM Departments;")
    conn.commit()
    conn.close()

def insert_normalized(records: list[dict]):
    """
    Inserts flattened row-like dictionaries into normalized SQL tables.
    """
    conn = get_conn()
    cur = conn.cursor()

    departments = {}
    students = {}
    instructors = {}
    courses = {}
    enrollments = []

    for r in records:
        dept_id = str(r.get("department_id", "")).strip()
        dept_name = str(r.get("department_name", "")).strip()
        if dept_id:
            departments[dept_id] = dept_name

        sid = str(r.get("student_id", "")).strip()
        if sid:
            students[sid] = (
                str(r.get("student_name", "")).strip(),
                str(r.get("email", "")).strip(),
                str(r.get("phone", "")).strip(),
                dept_id
            )

        iid = str(r.get("instructor_id", "")).strip()
        if iid:
            instructors[iid] = (
                str(r.get("instructor_name", "")).strip(),
                dept_id
            )

        cid = str(r.get("course_id", "")).strip()
        if cid:
            courses[cid] = (
                str(r.get("course_title", "")).strip(),
                safe_int(r.get("credit_hours", 0)),
                dept_id,
                iid
            )

        # each record is one enrollment row
        if sid and cid:
            enrollments.append((
                sid,
                cid,
                str(r.get("semester", "")).strip(),
                str(r.get("enroll_date", "")).strip(),  # date string YYYY-MM-DD
                str(r.get("grade", "")).strip()
            ))

    # Optional: clear tables before inserting (demo-friendly)
    clear_sql_tables()

    # Insert Departments
    for dept_id, dept_name in departments.items():
        cur.execute(
            "INSERT INTO Departments(department_id, department_name) VALUES (?, ?);",
            dept_id, dept_name
        )

    # Insert Students
    for sid, (name, email, phone, dept_id) in students.items():
        cur.execute(
            "INSERT INTO Students(student_id, student_name, email, phone, department_id) VALUES (?, ?, ?, ?, ?);",
            sid, name, email, phone, dept_id
        )

    # Insert Instructors
    for iid, (iname, dept_id) in instructors.items():
        cur.execute(
            "INSERT INTO Instructors(instructor_id, instructor_name, department_id) VALUES (?, ?, ?);",
            iid, iname, dept_id
        )

    # Insert Courses
    for cid, (title, credit_hours, dept_id, iid) in courses.items():
        cur.execute(
            "INSERT INTO Courses(course_id, course_title, credit_hours, department_id, instructor_id) VALUES (?, ?, ?, ?, ?);",
            cid, title, credit_hours, dept_id, iid
        )

    # Insert Enrollments
    for (sid, cid, semester, enroll_date, grade) in enrollments:
        cur.execute(
            "INSERT INTO Enrollments(student_id, course_id, semester, enroll_date, grade) VALUES (?, ?, ?, ?, ?);",
            sid, cid, semester, enroll_date, grade
        )

    conn.commit()
    conn.close()

    return {
        "departments": len(departments),
        "students": len(students),
        "instructors": len(instructors),
        "courses": len(courses),
        "enrollments": len(enrollments),
    }

def safe_int(x) -> int:
    try:
        return int(str(x).strip())
    except Exception:
        return 0

def status():
    conn = get_conn()
    cur = conn.cursor()
    tables = ["Departments", "Students", "Instructors", "Courses", "Enrollments"]
    counts = {}
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t};")
        counts[t] = cur.fetchone()[0]
    conn.close()
    return counts
def delete_all_sql_data():
    """
    Deletes all rows from all tables (FK-safe order).
    """
    clear_sql_tables()

def delete_one_student_sql(student_id: str):
    """
    Deletes a student and their enrollments (FK-safe).
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM Enrollments WHERE student_id=?;", student_id)
    cur.execute("DELETE FROM Students WHERE student_id=?;", student_id)
    conn.commit()
    conn.close()
