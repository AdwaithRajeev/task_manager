from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB table if not exists
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "<h1>WELCOME TO Task Manager</h1><p>Use /add to add tasks and /tasks to view tasks.</p>"

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()
        return redirect("/tasks")
    return render_template("add.html")

@app.route("/tasks")
def view_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template("tasks.html", tasks=tasks)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
