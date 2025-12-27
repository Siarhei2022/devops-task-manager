from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .db import SessionLocal, engine, Base
from .crud import (
    create_task,
    list_tasks,
    update_task_status,
    delete_task,
    ALLOWED_STATUSES,
)

# FastAPI application instance
app = FastAPI(title="DevOps Project - Task Manager")

# Serve static files (frontend)
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve the main UI page
@app.get("/")
def ui():
    return FileResponse(STATIC_DIR / "index.html")

# Create database tables on startup (simple approach for demo project)
# Create tables when the app starts (not during import)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Get list of all tasks
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = list_tasks(db)
    return [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "created_at": t.created_at.isoformat(),
            "updated_at": t.updated_at.isoformat(),
        }
        for t in tasks
    ]

# Create a new task
@app.post("/tasks")
def add_task(title: str, db: Session = Depends(get_db)):
    title = title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    t = create_task(db, title=title)
    return {
        "id": t.id,
        "title": t.title,
        "status": t.status,
        "created_at": t.created_at.isoformat(),
        "updated_at": t.updated_at.isoformat(),
    }

# Update task status
@app.patch("/tasks/{task_id}")
def set_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    if status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"status must be one of {sorted(ALLOWED_STATUSES)}",
        )

    t = update_task_status(db, task_id=task_id, status=status)
    if t is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": t.id,
        "title": t.title,
        "status": t.status,
        "created_at": t.created_at.isoformat(),
        "updated_at": t.updated_at.isoformat(),
    }

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db)):
    ok = delete_task(db, task_id=task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True, "id": task_id}

