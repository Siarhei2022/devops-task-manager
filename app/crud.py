from datetime import datetime, timezone
from sqlalchemy.orm import Session

from .models import Task

# Allowed task statuses
ALLOWED_STATUSES = {"todo", "in_progress", "done"}

# Create a new task with default status "todo"
def create_task(db: Session, title: str) -> Task:
    now = datetime.now(timezone.utc)
    task = Task(
        title=title,
        status="todo",
        created_at=now,
        updated_at=now,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# Return all tasks ordered by creation date
def list_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.created_at.desc()).all()

# Update task status by id
def update_task_status(db: Session, task_id: int, status: str) -> Task | None:
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status: {status}")

    task = db.get(Task, task_id)
    if task is None:
        return None

    task.status = status
    task.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    task = db.get(Task, task_id)
    if task is None:
        return False
    db.delete(task)
    db.commit()
    return True
