"""Tests for the storage module."""

import os
import json
import pytest
from datetime import datetime
from pathlib import Path
from talia.storage import (
    ensure_storage_dir,
    task_to_dict,
    dict_to_task,
    save_tasks,
    load_tasks,
    backup_tasks,
    remove_storage_file,
    STORAGE_DIR,
    STORAGE_FILE
)
from talia.models import Task, TaskStatus
import shutil

@pytest.fixture
def temp_storage(tmp_path):
    """Create a temporary storage directory."""
    storage_dir = tmp_path / ".tasklistai"
    storage_file = storage_dir / "tasks.json"
    return storage_file

@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task(
        id=1,
        title="Test task",
        status=TaskStatus.INBOX,
        created_at=datetime.now()
    )

def test_ensure_storage_dir(temp_storage):
    """Test creating storage directory."""
    ensure_storage_dir(str(temp_storage))
    assert os.path.exists(os.path.dirname(temp_storage))

def test_ensure_storage_dir_permission_error(tmp_path):
    """Test storage directory creation with permission error."""
    # Create a directory that we can't write to
    os.chmod(tmp_path, 0o444)  # Read-only
    with pytest.raises(PermissionError):
        ensure_storage_dir(str(tmp_path / "test" / "file.txt"))

def test_ensure_storage_dir_os_error(tmp_path, monkeypatch):
    """Test storage directory creation with OSError."""
    def mock_makedirs(*args, **kwargs):
        raise OSError("Mock OSError")
    
    monkeypatch.setattr(os, 'makedirs', mock_makedirs)
    with pytest.raises(OSError):
        ensure_storage_dir(str(tmp_path / "test" / "file.txt"))

def test_task_to_dict(sample_task):
    """Test converting task to dictionary."""
    task_dict = task_to_dict(sample_task)
    assert task_dict["id"] == sample_task.id
    assert task_dict["title"] == sample_task.title
    assert task_dict["status"] == sample_task.status.value
    assert task_dict["created_at"] == sample_task.created_at.isoformat()

def test_dict_to_task(sample_task):
    """Test converting dictionary to task."""
    task_dict = task_to_dict(sample_task)
    task = dict_to_task(task_dict)
    assert task.id == sample_task.id
    assert task.title == sample_task.title
    assert task.status == sample_task.status
    assert task.created_at.isoformat() == sample_task.created_at.isoformat()

def test_dict_to_task_missing_field():
    """Test converting dictionary with missing field to task."""
    with pytest.raises(KeyError):
        dict_to_task({"id": 1, "title": "Test"})  # Missing status and created_at

def test_dict_to_task_invalid_status():
    """Test converting dictionary with invalid status to task."""
    with pytest.raises(ValueError):
        dict_to_task({
            "id": 1,
            "title": "Test",
            "status": "INVALID_STATUS",
            "created_at": datetime.now().isoformat()
        })

def test_save_and_load_tasks(temp_storage, sample_task):
    """Test saving and loading tasks."""
    # Save tasks
    save_tasks([sample_task], str(temp_storage))
    assert os.path.exists(temp_storage)
    
    # Load tasks
    loaded_tasks = load_tasks(str(temp_storage))
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].id == sample_task.id
    assert loaded_tasks[0].title == sample_task.title
    assert loaded_tasks[0].status == sample_task.status

def test_save_tasks_permission_error(tmp_path):
    """Test saving tasks with permission error."""
    # Create a directory that we can't write to
    os.chmod(tmp_path, 0o444)  # Read-only
    with pytest.raises(PermissionError):
        save_tasks([Task(id=1, title="Test")], str(tmp_path / "test.json"))

def test_save_tasks_json_error(temp_storage, sample_task, monkeypatch):
    """Test saving tasks with JSON encoding error."""
    def mock_json_dump(*args, **kwargs):
        raise json.JSONDecodeError("Mock JSON Error", "", 0)
    
    monkeypatch.setattr(json, 'dump', mock_json_dump)
    with pytest.raises(json.JSONDecodeError):
        save_tasks([sample_task], str(temp_storage))

def test_save_tasks_os_error(temp_storage, sample_task, monkeypatch):
    """Test saving tasks with OSError."""
    def mock_open(*args, **kwargs):
        raise OSError("Mock OSError")
    
    monkeypatch.setattr('builtins.open', mock_open)
    with pytest.raises(OSError):
        save_tasks([sample_task], str(temp_storage))

def test_load_tasks_empty_file(temp_storage):
    """Test loading tasks from empty file."""
    # Create empty file
    ensure_storage_dir(str(temp_storage))
    with open(temp_storage, "w") as f:
        f.write("[]")
    
    tasks = load_tasks(str(temp_storage))
    assert len(tasks) == 0

def test_load_tasks_invalid_json(temp_storage):
    """Test loading tasks from invalid JSON file."""
    # Create file with invalid JSON
    ensure_storage_dir(str(temp_storage))
    with open(temp_storage, "w") as f:
        f.write("invalid json")
    
    tasks = load_tasks(str(temp_storage))
    assert len(tasks) == 0

def test_load_tasks_file_not_found(temp_storage):
    """Test loading tasks when file doesn't exist."""
    tasks = load_tasks(str(temp_storage))
    assert len(tasks) == 0

def test_load_tasks_key_error(temp_storage):
    """Test loading tasks with missing key in data."""
    ensure_storage_dir(str(temp_storage))
    with open(temp_storage, "w") as f:
        json.dump([{"id": 1}], f)  # Missing required fields
    
    tasks = load_tasks(str(temp_storage))
    assert len(tasks) == 0

def test_load_tasks_value_error(temp_storage):
    """Test loading tasks with invalid value in data."""
    ensure_storage_dir(str(temp_storage))
    with open(temp_storage, "w") as f:
        json.dump([{
            "id": 1,
            "title": "Test",
            "status": "INVALID_STATUS",
            "created_at": "invalid-date"
        }], f)
    
    tasks = load_tasks(str(temp_storage))
    assert len(tasks) == 0

def test_load_tasks_permission_error(temp_storage, monkeypatch):
    """Test loading tasks with permission error."""
    def mock_open(*args, **kwargs):
        raise PermissionError("Mock PermissionError")
    
    monkeypatch.setattr('builtins.open', mock_open)
    tasks = load_tasks(str(temp_storage))
    assert len(tasks) == 0

def test_load_tasks_os_error(temp_storage, monkeypatch):
    """Test loading tasks with OSError."""
    def mock_open(*args, **kwargs):
        raise OSError("Mock OSError")
    
    monkeypatch.setattr('builtins.open', mock_open)
    tasks = load_tasks(str(temp_storage))
    assert len(tasks) == 0

def test_backup_tasks(temp_storage, sample_task):
    """Test creating backup of tasks."""
    # Save some tasks
    save_tasks([sample_task], str(temp_storage))
    
    # Create backup with custom name
    backup_path = backup_tasks("test_backup", str(temp_storage))
    assert os.path.exists(backup_path)
    
    # Create backup with timestamp
    backup_path = backup_tasks(path=str(temp_storage))
    assert os.path.exists(backup_path)

def test_backup_tasks_no_file(temp_storage):
    """Test creating backup when no file exists."""
    backup_path = backup_tasks(path=str(temp_storage))
    assert backup_path == ""

def test_backup_tasks_permission_error(temp_storage, sample_task, monkeypatch):
    """Test creating backup with permission error."""
    # Save some tasks
    save_tasks([sample_task], str(temp_storage))
    
    def mock_copy2(*args, **kwargs):
        raise PermissionError("Mock PermissionError")
    
    monkeypatch.setattr(shutil, 'copy2', mock_copy2)
    backup_path = backup_tasks(path=str(temp_storage))
    assert backup_path == ""

def test_backup_tasks_os_error(temp_storage, sample_task, monkeypatch):
    """Test creating backup with OSError."""
    # Save some tasks
    save_tasks([sample_task], str(temp_storage))
    
    def mock_copy2(*args, **kwargs):
        raise OSError("Mock OSError")
    
    monkeypatch.setattr(shutil, 'copy2', mock_copy2)
    backup_path = backup_tasks(path=str(temp_storage))
    assert backup_path == ""

def test_remove_storage_file(temp_storage, sample_task):
    """Test removing storage file."""
    # Create and save some tasks
    save_tasks([sample_task], str(temp_storage))
    assert os.path.exists(temp_storage)
    
    # Remove file
    assert remove_storage_file(str(temp_storage))
    assert not os.path.exists(temp_storage)

def test_remove_storage_file_no_file(temp_storage):
    """Test removing non-existent storage file."""
    assert not remove_storage_file(str(temp_storage))

def test_remove_storage_file_permission_error(tmp_path):
    """Test removing storage file with permission error."""
    # Create a file that we can't remove
    test_file = tmp_path / "test.json"
    test_file.touch()
    os.chmod(tmp_path, 0o444)  # Read-only directory
    assert not remove_storage_file(str(test_file))

def test_remove_storage_file_os_error(temp_storage, sample_task, monkeypatch):
    """Test removing storage file with OSError."""
    # Create and save some tasks
    save_tasks([sample_task], str(temp_storage))
    
    def mock_remove(*args, **kwargs):
        raise OSError("Mock OSError")
    
    monkeypatch.setattr(os, 'remove', mock_remove)
    assert not remove_storage_file(str(temp_storage))

def test_save_tasks_json_error_with_message(temp_storage, sample_task, monkeypatch):
    """Test saving tasks with JSON encoding error with message."""
    def mock_json_dump(*args, **kwargs):
        raise json.JSONDecodeError("Mock JSON Error", "test", 0)
    
    monkeypatch.setattr(json, 'dump', mock_json_dump)
    with pytest.raises(json.JSONDecodeError):
        save_tasks([sample_task], str(temp_storage))

def test_load_tasks_json_error_with_message(temp_storage, monkeypatch):
    """Test loading tasks with JSON decode error with message."""
    ensure_storage_dir(str(temp_storage))
    with open(temp_storage, "w") as f:
        f.write("invalid json")
    
    def mock_json_load(*args, **kwargs):
        raise json.JSONDecodeError("Mock JSON Error", "test", 0)
    
    monkeypatch.setattr(json, 'load', mock_json_load)
    tasks = load_tasks(str(temp_storage))
    assert len(tasks) == 0

def test_remove_storage_file_with_message(temp_storage, sample_task, monkeypatch):
    """Test removing storage file with error message."""
    # Create and save some tasks
    save_tasks([sample_task], str(temp_storage))
    
    def mock_remove(*args, **kwargs):
        raise OSError("Mock OSError with message")
    
    monkeypatch.setattr(os, 'remove', mock_remove)
    assert not remove_storage_file(str(temp_storage)) 