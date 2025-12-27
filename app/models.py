from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .db import OrmModelBase

# Database model representing a task in the system
class Task(OrmModelBase):
    __tablename__ = "tasks"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Task title / description
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # Task status: todo / in_progress / done
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="todo",
    )

    # Timestamp when task was created
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Timestamp of last update
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )