import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# Database connection
def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Original Student Information API, now using SQLite
@app.route("/student")
def get_student():
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        ("24-00115",)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "student_id": student["student_id"],
        "name": student["name"],
        "program": student["program"],
        "year": student["year"],
        "section": student["section"]
    })


# Original Greeting API
@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Student")

    return jsonify({
        "message": f"Hello, {name}!"
    })


# Original custom API
@app.route("/jero")
def custom_api():
    name = request.args.get("name", "Student")

    return jsonify({
        "message": f"Hello, {name}! Welcome to Jero.",
        "endpoint": "/jero",
        "activity": "Laboratory Activity 7"
    })


# API: Get all students from the database
@app.route("/students")
def get_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# API: Get one student by database ID
@app.route("/students/<int:id>")
def get_student_by_id(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# Additional task: Get students by program
@app.route("/students/program/<string:program>")
def get_students_by_program(program):
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students WHERE program = ? ORDER BY id",
        (program,)
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == "__main__":
    app.run(debug=True)
