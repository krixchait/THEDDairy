from flask import Flask, request
import sqlite3

app=Flask(__name__)

conn=sqlite3.connect("diary.db",check_same_thread=False)
cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        task TEXT NOT NULL,
        completed INTEGER DEFAULT 0
)
""")
conn.commit()

@app.route("/")
def home():
    return "DDairy backend running!!"
    

@app.route("/add_todo",methods=["POST"])
def add_todo():
    data=request.get_json()

    username=data.get("username")
    task=data.get("task")

    cursor.execute(
        "INSERT INTO todos (username,task) VALUES (?,?)",
        (username,task)
    )
    conn.commit()
    return {
        "message": " TODO received successfully"
    }



@app.route("/get_todos/<username>",methods=["GET"])
def get_todos(username):
    cursor.execute(
        "SELECT * FROM todos WHERE username = ?",
        (username,)
    )
    todos=cursor.fetchall()
    return {
        "todos":todos
    }


@app.route("/delete_todo/<int:task_id>", methods=["DELETE"])
def delete_todo(task_id):

    cursor.execute(
        "DELETE FROM todos WHERE id = ?",
        (task_id,)
    )

    conn.commit()

    return {
        "message": "Todo deleted successfully"
    }

@app.route("/complete_todo/<int:task_id>",methods=["PUT"])
def complete_todo(task_id):
    cursor.execute(
        "UPDATE todos SET completed=1 where id=?",
        (task_id,)
    )
    conn.commit()
    return{
        "message":"Todo marked completed"
    }


if __name__=="__main__":
    app.run(debug=True)
