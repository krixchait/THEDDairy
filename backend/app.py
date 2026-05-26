from flask import Flask, request
import sqlite3

app=Flask(__name__)

conn=sqlite3.connect("diary.db",check_same_thread=False)
cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
)
""")
conn.commit()

@app.route("/")
def home():
    return "DDairy backend running!!"
    

@app.route("/add_todo",methods=["POST"])
def add_todo():
    data=request.get_json()
    task=data.get("task")
    cursor.execute(
        "INSERT INTO todos (task) VALUES (?)",
        (task,)

    )
    conn.commit()

    return {
        "message" : "Todo received successfully"
    }

@app.route("/get_todos", methods=["GET"])
def get_todos():

    cursor.execute("SELECT * FROM todos")

    todos = cursor.fetchall()

    return {
        "todos": todos
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




if __name__=="__main__":
    app.run(debug=True)
