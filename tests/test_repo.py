"""Unit tests for the TaskRepo class."""

import pytest
from datetime import datetime
import os
from talia.repo import TaskRepo
from talia.models import Task, TaskStatus

@pytest.fixture
def temp_storage(tmp_path):
    """Create a temporary storage file for testing."""
    return tmp_path / "tasks.json"

@pytest.fixture
def repo(temp_storage):
    """Create a TaskRepo instance with temporary storage."""
    return TaskRepo(str(temp_storage))

@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task(
        id=1,
        title="Test task",
        status=TaskStatus.INBOX,
        created_at=datetime.now()
    )

def test_repo_initialization(repo):
    """Test that repo initializes with empty task list."""
    assert len(repo.all) == 0

def test_repo_add_task(repo, sample_task):
    """Test adding a task to the repo."""
    repo.add(sample_task)
    assert len(repo.all) == 1
    assert repo.all[0] == sample_task

def test_repo_get_task(repo, sample_task):
    """Test getting a task by ID."""
    repo.add(sample_task)
    task = repo.get(1)
    assert task == sample_task
    assert repo.get(999) is None

def test_repo_get_next_id(repo):
    """Test getting the next available task ID."""
    assert repo.get_next_id() == 1
    
    task1 = Task(id=1, title="Task 1", status=TaskStatus.INBOX, created_at=datetime.now())
    task2 = Task(id=2, title="Task 2", status=TaskStatus.INBOX, created_at=datetime.now())
    
    repo.add(task1)
    repo.add(task2)
    assert repo.get_next_id() == 3

def test_repo_save_and_load(temp_storage):
    """Test saving and loading tasks."""
    # Create and save tasks
    repo1 = TaskRepo(str(temp_storage))
    task1 = Task(id=1, title="Task 1", status=TaskStatus.INBOX, created_at=datetime.now())
    task2 = Task(id=2, title="Task 2", status=TaskStatus.TODO, created_at=datetime.now())
    
    repo1.add(task1)
    repo1.add(task2)
    repo1.save()
    
    # Load tasks in a new repo instance
    repo2 = TaskRepo(str(temp_storage))
    assert len(repo2.all) == 2
    assert repo2.get(1).title == "Task 1"
    assert repo2.get(2).title == "Task 2"
    assert repo2.get(1).status == TaskStatus.INBOX
    assert repo2.get(2).status == TaskStatus.TODO 