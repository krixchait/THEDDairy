import streamlit as st
import requests

st.title("DDiary")

with st.form("todo_form", clear_on_submit=True):

    task = st.text_input("Enter your todo")

    submitted = st.form_submit_button("Add Todo")

    if submitted:

        response = requests.post(
            "http://127.0.0.1:5000/add_todo",
            json={"task": task}
        )

        st.success("Todo Added Successfully!")

todos_response = requests.get(
    "http://127.0.0.1:5000/get_todos"
)

todos = todos_response.json()

st.subheader("Your Todos")

for todo in todos["todos"]:

    task_id = todo[0]
    task_name = todo[1]

    st.write(f"{task_id}. {task_name}")