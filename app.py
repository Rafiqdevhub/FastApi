from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

# initialize FastAPI
app=FastAPI()

# Task model
class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# list of tasks
tasks=[]

# route (home)
@app.get("/")
def root():
    return {"message": "Welcome to the Bookstore"}

# route (create tasks)
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    task.id=uuid4()
    tasks.append(task)
    return task

# route (read tasks)
@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks

# route (read task by id)
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# route (update task by id)
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task: Task):
    for t in tasks:
        if t.id == task_id:
            t.title = task.title
            t.description = task.description
            t.completed = task.completed
            return t
    raise HTTPException(status_code=404, detail="Task not found")

# route (delete task by id)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: UUID):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


# run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)