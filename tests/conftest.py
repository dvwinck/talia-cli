"""Shared pytest fixtures."""

import pytest
from datetime import datetime
import os
from talia.models import Task, TaskStatus
from talia.repo import TaskRepo

@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task(
        id=1,
        title="Test task",
        status=TaskStatus.INBOX,
        created_at=datetime.now()
    )

@pytest.fixture
def sample_tasks():
    """Create a list of sample tasks for testing."""
    return [
        Task(id=1, title="Task 1", status=TaskStatus.INBOX, created_at=datetime.now()),
        Task(id=2, title="Task 2", status=TaskStatus.TODO, created_at=datetime.now()),
        Task(id=3, title="Task 3", status=TaskStatus.COMPLETED, created_at=datetime.now())
    ] 