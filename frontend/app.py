import streamlit as st
import requests

st.title("DDiary")

username=st.text_input("Enter your username")

if not username:
    st.warning("Please enter username")
    st.stop()

with st.form("todo_form", clear_on_submit=True):

    task = st.text_input("Enter your todo")

    submitted = st.form_submit_button("Add Todo")

    if submitted:

        response = requests.post(
            "http://127.0.0.1:5000/add_todo",
            json={
                "username":username,
                "task":task
            }
        )

        st.success("Todo Added Successfully!")

todos_response = requests.get(
    f"http://127.0.0.1:5000/get_todos/{username}"
)

todos = todos_response.json()



st.subheader("Current TO-DO")

for todo in todos["todos"]:
    task_id=todo[0]
    task_name=todo[2]
    completed=todo[3]
    
    if completed==0:
        col1,col2=st.columns([4,1])
        with col1:
            checked=st.checkbox(
                task_name,
                key=f"check_{task_id}"
            )
            
            if checked:
                requests.put(
                    f"http://127.0.0.1:5000/complete_todo/{task_id}"
                )
                st.rerun()
            
        with col2:
            if st.button("Delete",key=f"delete_{task_id}"):
                requests.delete(
                    f"http://127.0.0.1:5000/delete_todo/{task_id}"
                )
                st.rerun()

st.subheader("Completed Tasks")
for todo in todos["todos"]:
    task_id=todo[0]
    task_name=todo[2]
    completed=todo[3]

    if completed==1:
        st.write(f"✅ {task_name}")
