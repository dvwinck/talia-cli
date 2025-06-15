"""Models for TaskListAI."""

from enum import Enum
from datetime import datetime
from typing import Optional

class TaskStatus(Enum):
    """Possible statuses for a task."""
    INBOX = "📥 Inbox"
    TODO = "📋 To Do"
    REVIEW = "👀 To Review"
    COMPLETED = "✅ Completed"
    ARCHIVED = "📦 Archived"

class Task:
    """A task in the system."""
    
    def __init__(
        self,
        id: int,
        title: str,
        status: TaskStatus = TaskStatus.INBOX,
        created_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.status = status
        self.created_at = created_at or datetime.now()
        self.completed_at = completed_at
    
    def complete(self):
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def archive(self):
        """Archive the task."""
        self.status = TaskStatus.ARCHIVED
    
    def move_to_todo(self):
        """Move the task to To Do list."""
        self.status = TaskStatus.TODO
    
    def move_to_review(self):
        """Move the task to Review list."""
        self.status = TaskStatus.REVIEW 