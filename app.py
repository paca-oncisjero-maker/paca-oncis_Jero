from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student")
def get_student():
    return jsonify({
        "student_id": "24-00115",
        "name": "JERO PACA-ONCIS",
        "program": "BSIT",
        "year": 3,
        "section": "DIJKSTRA"
    })


@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Student")
    return jsonify({
        "message": f"Hello, {name}!"
    })


# Example custom endpoint for the additional task
@app.route("/jero")
def custom_api():
    name = request.args.get("name", "Student")
    return jsonify({
        "message": f"Hello, {name}! Welcome to Jero.",
        "endpoint": "/jero",
        "activity": "Laboratory Activity 6"
    })


if __name__ == "__main__":
    app.run(debug=True)

