from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to Jero API!"


@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00115",
        "name": "Jero Paca-oncis",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })

@app.route('/about')
def about():
    return jsonify({
        "api_name": "My First API",
        "description": "A simple Flask REST API",
        "developer": "Jero Paca-oncis",
        "version": "1.0"
    })

@app.route('/jero')
def say_jero():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Gwapo si, {name}!"
    })


if __name__ == '__main__':
    app.run(debug=True)
