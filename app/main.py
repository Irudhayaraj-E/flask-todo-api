from flask import Flask, request, jsonify
from db import init_db, get_db

app = Flask(__name__)
init_db()

@app.route("/todos", methods=["GET"])
def get_todos():
    db = get_db()
    todos = db.execute("SELECT id, task FROM todos").fetchall()
    return jsonify([{"id": row["id"], "task": row["task"]} for row in todos])

@app.route("/todos", methods=["POST"])
def add_todo():
    task = request.json.get("task")
    if not task:
        return jsonify({"error": "Task required"}), 400

    db = get_db()
    db.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    db.commit()
    return jsonify({"message": "Todo added"}), 201

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    return jsonify({"message": "Todo deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
