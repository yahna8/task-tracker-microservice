from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import Task
from utils.auth import get_current_user

# Initialize router
router = APIRouter()

# Pydantic models for request/response validation
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int
    deadline: str  # ISO format (e.g., "2025-01-30")

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    deadline: str
    completed: bool

    class Config:
        orm_mode = True

# Routes

@router.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        deadline=task.deadline,
        completed=False,
        user_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/tasks", response_model=List[TaskResponse])
def get_active_tasks(db: Session = Depends(get_db)):
    """
    Retrieve all active (incomplete) tasks.
    """
    tasks = db.query(Task).filter(Task.completed == False).all()
    return tasks


@router.put("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Mark a task as completed.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks/history", response_model=List[TaskResponse])
def get_completed_tasks(db: Session = Depends(get_db)):
    """
    Retrieve a history of completed tasks.
    """
    tasks = db.query(Task).filter(Task.completed == True).all()
    return tasks