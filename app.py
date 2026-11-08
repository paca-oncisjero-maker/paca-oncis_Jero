from flask import Flask, jsonify, render_template, request
import sqlite3
import requests
import os
from urllib.parse import urlparse

app = Flask(__name__)

DATABASE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "students.db"
)


# DATABASE CONNECTION
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# CREATE DATABASE TABLE
def create_table():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            year INTEGER NOT NULL,
            section TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_table()


# VALIDATE STUDENT DATA
def validate_data(data):

    if not isinstance(data, dict):
        return None, "Invalid student information."

    fields = [
        "student_id",
        "name",
        "program",
        "year",
        "section"
    ]

    for field in fields:
        if data.get(field) is None or str(data[field]).strip() == "":
            return None, field + " is required."

    try:
        year = int(data["year"])
        if year < 1:
            return None, "Invalid year."
    except (ValueError, TypeError):
        return None, "Year must be a number."

    return {
        "student_id": str(data["student_id"]).strip(),
        "name": str(data["name"]).strip(),
        "program": str(data["program"]).strip(),
        "year": year,
        "section": str(data["section"]).strip()
    }, None


# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")


# LABORATORY ACTIVITY 6
@app.route("/student")
def student():
    return jsonify({
        "student_id": "24-00115",
        "name": "JERO PACA-ONCIS",
        "program": "BSIT",
        "year": 3,
        "section": "DIJKSTRA"
    })


@app.route("/hello")
def hello():
    name = request.args.get("name", "Student")
    return jsonify({
        "message": f"Hello, {name}!"
    })


@app.route("/jero")
def jero():
    name = request.args.get("name", "Student")

    return jsonify({
        "message": f"Hello, {name}! Welcome to Jero.",
        "activity": "Laboratory Activity 8"
    })


# READ ALL STUDENTS
@app.route("/api/students", methods=["GET"])
def get_students():

    conn = get_connection()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# CREATE STUDENT
@app.route("/api/students", methods=["POST"])
def add_student():

    data, error = validate_data(
        request.get_json(silent=True)
    )

    if error:
        return jsonify({"error": error}), 400

    conn = get_connection()

    cursor = conn.execute("""
        INSERT INTO students
        (student_id, name, program, year, section)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["student_id"],
        data["name"],
        data["program"],
        data["year"],
        data["section"]
    ))

    conn.commit()

    student_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "message": "Student added successfully!",
        "id": student_id
    }), 201


# READ ONE STUDENT
@app.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):

    conn = get_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found."
        }), 404

    return jsonify(dict(student))


# UPDATE STUDENT
@app.route("/api/students/<int:id>", methods=["PUT"])
def edit_student(id):

    data, error = validate_data(
        request.get_json(silent=True)
    )

    if error:
        return jsonify({"error": error}), 400

    conn = get_connection()

    existing = conn.execute(
        "SELECT id FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    if existing is None:
        conn.close()
        return jsonify({
            "error": "Student not found."
        }), 404

    conn.execute("""
        UPDATE students
        SET student_id = ?,
            name = ?,
            program = ?,
            year = ?,
            section = ?
        WHERE id = ?
    """, (
        data["student_id"],
        data["name"],
        data["program"],
        data["year"],
        data["section"],
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student updated successfully!"
    })


# DELETE STUDENT
@app.route("/api/students/<int:id>", methods=["DELETE"])
def remove_student(id):

    conn = get_connection()

    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    if deleted == 0:
        return jsonify({
            "error": "Student not found."
        }), 404

    return jsonify({
        "message": "Student deleted successfully!"
    })


# LABORATORY ACTIVITY 7
@app.route("/students", methods=["GET"])
def old_get_students():
    return get_students()


@app.route("/students/<int:id>", methods=["GET"])
def old_get_student(id):
    return get_student(id)


@app.route("/students/program/<path:program>", methods=["GET"])
def search_program(program):

    conn = get_connection()

    students = conn.execute("""
        SELECT * FROM students
        WHERE LOWER(program) = LOWER(?)
        ORDER BY id DESC
    """, (program,)).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# CLASSMATE API - READ ONLY
@app.route("/api/classmate/students", methods=["GET"])
def classmate_students():

    api_url = request.args.get("url", "").strip()

    if not api_url:
        return jsonify({
            "error": "Please enter your classmate's API URL."
        }), 400

    try:
        parsed = urlparse(api_url)

        valid_url = (
            parsed.scheme == "https"
            and parsed.hostname is not None
            and parsed.hostname.lower().endswith(".onrender.com")
            and parsed.username is None
            and parsed.password is None
            and parsed.port in (None, 443)
            and parsed.path.rstrip("/") == "/api/students"
            and not parsed.query
            and not parsed.fragment
        )

    except ValueError:
        valid_url = False

    if not valid_url:
        return jsonify({
            "error": "Please enter a valid Render API URL ending in /api/students."
        }), 400

    try:

        response = requests.get(
            api_url,
            timeout=20,
            allow_redirects=False,
            headers={"Accept": "application/json"}
        )

        response.raise_for_status()

        records = response.json()

        if not isinstance(records, list):
            return jsonify({
                "error": "Invalid classmate API response."
            }), 502

        return jsonify(records)

    except requests.RequestException:
        return jsonify({
            "error": "Unable to connect to classmate's API."
        }), 502

    except ValueError:
        return jsonify({
            "error": "Invalid JSON response."
        }), 502


# RUN APPLICATION
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
