import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create the students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
""")

# Clear previous sample records
cursor.execute("DELETE FROM students")

# Insert five sample student records
students = [
    ("24-00115", "JERO PACA-ONCIS", "BSIT", 3, "DIJKSTRA"),
    ("24-00116", "MISSY MIRANDA", "BSIT", 3, "DIJKSTRA"),
    ("25-00121", "RUBY JOY MOLINA", "BSIT", 3, "DIJKSTRA"),
    ("25-00122", "SHARAMAINE JOYCE PALENCIA", "BSIT", 3, "DIJKSTRA"),
    ("26-00130", "Mark Villanueva", "BSIT", 1, "RIZAL")
]

cursor.executemany("""
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
""", students)

conn.commit()
conn.close()

print("Database created successfully.")
