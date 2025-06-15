"""Repository module for managing task state."""

from typing import List, Optional
from .models import Task
from .storage import load_tasks, save_tasks

class TaskRepo:
    """Repository for managing task state."""
    
    def __init__(self, path: str):
        """Initialize the repository with a storage path.
        
        Args:
            path: Path to the storage file
        """
        self._path = path
        self._tasks = load_tasks(path)
    
    @property
    def all(self) -> List[Task]:
        """Get all tasks.
        
        Returns:
            List of all tasks
        """
        return self._tasks
    
    def save(self):
        """Save all tasks to storage."""
        save_tasks(self._tasks, self._path)
    
    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.
        
        Args:
            task_id: ID of the task to get
            
        Returns:
            Task if found, None otherwise
        """
        return next((t for t in self._tasks if t.id == task_id), None)
    
    def add(self, task: Task):
        """Add a new task.
        
        Args:
            task: Task to add
        """
        self._tasks.append(task)
    
    def get_next_id(self) -> int:
        """Get the next available task ID.
        
        Returns:
            Next available task ID
        """
        if not self._tasks:
            return 1
        return max(task.id for task in self._tasks) + 1 