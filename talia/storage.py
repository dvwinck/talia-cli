"""Storage module for TaskListAI."""

import json
import os
from datetime import datetime
import shutil
from typing import List, Dict, Any, Optional

from .models import Task, TaskStatus
from .logger import logger

# Storage file path
STORAGE_DIR = os.path.expanduser("~/.tasklistai")
STORAGE_FILE = os.path.join(STORAGE_DIR, "tasks.json")

def ensure_storage_dir(path: str):
    """Ensure the storage directory exists."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except PermissionError as e:
        logger.error(f"Permission denied when creating storage directory: {e}")
        raise
    except OSError as e:
        logger.error(f"Failed to create storage directory: {e}")
        raise

def task_to_dict(task: Task) -> Dict[str, Any]:
    """Convert a Task object to a dictionary."""
    return {
        "id": task.id,
        "title": task.title,
        "status": task.status.value,
        "created_at": task.created_at.isoformat()
    }

def dict_to_task(data: Dict[str, Any]) -> Task:
    """Convert a dictionary to a Task object."""
    try:
        return Task(
            id=data["id"],
            title=data["title"],
            status=TaskStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"])
        )
    except KeyError as e:
        logger.error(f"Missing required field in task data: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid value in task data: {e}")
        raise

def save_tasks(tasks: List[Task], path: str = STORAGE_FILE):
    """Save tasks to storage."""
    try:
        ensure_storage_dir(path)
        data = [task_to_dict(task) for task in tasks]
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        logger.debug(f"Saved {len(tasks)} tasks to storage")
    except PermissionError as e:
        logger.error(f"Permission denied when saving tasks: {e}")
        raise
    except OSError as e:
        logger.error(f"Failed to save tasks: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Failed to encode tasks to JSON: {e}")
        raise

def load_tasks(path: str = STORAGE_FILE) -> List[Task]:
    """Load tasks from storage."""
    if not os.path.exists(path):
        logger.debug("No storage file found, returning empty list")
        return []
    
    try:
        with open(path, "r") as f:
            data = json.load(f)
        tasks = [dict_to_task(task_data) for task_data in data]
        logger.debug(f"Loaded {len(tasks)} tasks from storage")
        return tasks
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from task file: {e}")
        return []
    except FileNotFoundError:
        logger.warning("No task file found, returning empty task list")
        return []
    except KeyError as e:
        logger.error(f"Missing key in task data: {e}")
        return []
    except ValueError as e:
        logger.error(f"Invalid value in task data: {e}")
        return []
    except PermissionError as e:
        logger.error(f"Permission denied when reading task file: {e}")
        return []
    except OSError as e:
        logger.error(f"Failed to read task file: {e}")
        return []

def backup_tasks(name: Optional[str] = None, path: str = STORAGE_FILE) -> str:
    """Create a backup of the tasks file.
    
    Args:
        name: Optional custom name for the backup. If not provided, uses timestamp.
        path: Path to the tasks file to backup.
    
    Returns:
        Path to the backup file.
    """
    if not os.path.exists(path):
        logger.warning("No storage file found to backup")
        return ""
    
    try:
        if name:
            backup_file = f"{path}.{name}"
        else:
            timestamp = datetime.now().strftime("%Y%m%d%H%M")
            backup_file = f"{path}.{timestamp}"
        
        shutil.copy2(path, backup_file)
        logger.info(f"Created backup at: {backup_file}")
        return backup_file
    except PermissionError as e:
        logger.error(f"Permission denied when creating backup: {e}")
        return ""
    except OSError as e:
        logger.error(f"Failed to create backup: {e}")
        return ""

def remove_storage_file(path: str = STORAGE_FILE) -> bool:
    """Remove the storage file.
    
    Args:
        path: Path to the storage file to remove.
    
    Returns:
        True if the file was removed, False if it didn't exist.
    """
    if not os.path.exists(path):
        logger.warning("No storage file found to remove")
        return False
    
    try:
        os.remove(path)
        logger.info(f"Removed storage file: {path}")
        return True
    except PermissionError as e:
        logger.error(f"Permission denied when removing storage file: {e}")
        return False
    except OSError as e:
        logger.error(f"Failed to remove storage file: {e}")
        return False 