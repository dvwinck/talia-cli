"""Unit tests for the CLI commands."""

import pytest
from click.testing import CliRunner
from datetime import datetime
import os
from talia.cli import cli
from talia.models import Task, TaskStatus
from talia.repo import TaskRepo

@pytest.fixture
def runner():
    """Create a Click CLI test runner."""
    return CliRunner()

@pytest.fixture
def temp_storage(tmp_path):
    """Create a temporary storage file for testing."""
    return tmp_path / "tasks.json"

def test_add_command(runner, temp_storage):
    """Test the add command."""
    result = runner.invoke(cli, ['add', 'Test task'], obj=TaskRepo(str(temp_storage)))
    assert result.exit_code == 0
    assert "Added to inbox: Test task" in result.output

def test_list_command_empty(runner, temp_storage):
    """Test the list command with no tasks."""
    result = runner.invoke(cli, ['list'], obj=TaskRepo(str(temp_storage)))
    assert result.exit_code == 0
    assert "📝 No tasks found" in result.output

def test_list_command_with_tasks(runner, temp_storage):
    """Test the list command with tasks."""
    repo = TaskRepo(str(temp_storage))
    task = Task(id=1, title="Test task", status=TaskStatus.INBOX, created_at=datetime.now())
    repo.add(task)
    repo.save()
    
    result = runner.invoke(cli, ['list'], obj=repo)
    assert result.exit_code == 0
    assert "Test task" in result.output
    assert "📥 Inbox" in result.output

def test_list_command_with_status_filter(runner, temp_storage):
    """Test the list command with status filter."""
    repo = TaskRepo(str(temp_storage))
    task1 = Task(id=1, title="Task 1", status=TaskStatus.INBOX, created_at=datetime.now())
    task2 = Task(id=2, title="Task 2", status=TaskStatus.TODO, created_at=datetime.now())
    repo.add(task1)
    repo.add(task2)
    repo.save()
    
    result = runner.invoke(cli, ['list', '--status', 'TODO'], obj=repo)
    assert result.exit_code == 0
    assert "Task 2" in result.output
    assert "Task 1" not in result.output

def test_done_command(runner, temp_storage):
    """Test the done command."""
    repo = TaskRepo(str(temp_storage))
    task = Task(id=1, title="Task 1", status=TaskStatus.INBOX, created_at=datetime.now())
    repo.add(task)
    repo.save()
    
    result = runner.invoke(cli, ['done', '1'], obj=repo)
    assert result.exit_code == 0
    assert "✅ Completed task: Task 1" in result.output
    
    # Verify task was marked as completed
    assert repo.get(1).status == TaskStatus.COMPLETED

def test_archive_command(runner, temp_storage):
    """Test the archive command."""
    repo = TaskRepo(str(temp_storage))
    task = Task(id=1, title="Task 1", status=TaskStatus.INBOX, created_at=datetime.now())
    repo.add(task)
    repo.save()
    
    result = runner.invoke(cli, ['archive', '1'], obj=repo)
    assert result.exit_code == 0
    assert "📦 Archived task: Task 1" in result.output
    
    # Verify task was archived
    assert repo.get(1).status == TaskStatus.ARCHIVED

def test_todo_command(runner, temp_storage):
    """Test the todo command."""
    repo = TaskRepo(str(temp_storage))
    task = Task(id=1, title="Task 1", status=TaskStatus.INBOX, created_at=datetime.now())
    repo.add(task)
    repo.save()
    
    result = runner.invoke(cli, ['todo', '1'], obj=repo)
    assert result.exit_code == 0
    assert "📋 Moved to To Do: Task 1" in result.output
    
    # Verify task was moved to todo
    assert repo.get(1).status == TaskStatus.TODO

def test_review_command(runner, temp_storage):
    """Test the review command."""
    repo = TaskRepo(str(temp_storage))
    task = Task(id=1, title="Task 1", status=TaskStatus.INBOX, created_at=datetime.now())
    repo.add(task)
    repo.save()
    
    result = runner.invoke(cli, ['review', '1'], obj=repo)
    assert result.exit_code == 0
    assert "👀 Moved to Review: Task 1" in result.output
    
    # Verify task was moved to review
    assert repo.get(1).status == TaskStatus.REVIEW

def test_dashboard_command_empty(runner, temp_storage):
    """Test the dashboard command with no tasks."""
    result = runner.invoke(cli, ['dashboard'], obj=TaskRepo(str(temp_storage)))
    assert result.exit_code == 0
    assert "📝 No tasks found" in result.output

def test_dashboard_command_with_tasks(runner, temp_storage):
    """Test the dashboard command with tasks."""
    repo = TaskRepo(str(temp_storage))
    task1 = Task(id=1, title="Task 1", status=TaskStatus.COMPLETED, created_at=datetime.now())
    task2 = Task(id=2, title="Task 2", status=TaskStatus.INBOX, created_at=datetime.now())
    repo.add(task1)
    repo.add(task2)
    repo.save()
    
    result = runner.invoke(cli, ['dashboard'], obj=repo)
    assert result.exit_code == 0
    assert "📝 Total Tasks:2" in result.output
    assert "✅ Completed:  1" in result.output
    assert "⏳ Pending:    1" in result.output

def test_reset_command(runner, temp_storage):
    """Test the reset command."""
    repo = TaskRepo(str(temp_storage))
    task = Task(id=1, title="Task 1", status=TaskStatus.INBOX, created_at=datetime.now())
    repo.add(task)
    repo.save()
    
    result = runner.invoke(cli, ['reset'], obj=repo)
    assert result.exit_code == 0
    assert "📦 Tasks backed up to:" in result.output
    
    # Create a new repo instance to verify tasks were cleared
    new_repo = TaskRepo(str(temp_storage))
    assert len(new_repo.all) == 0 