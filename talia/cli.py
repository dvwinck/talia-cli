"""Main CLI module for Talia CLI."""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
from typing import Optional, List
import os
import shutil

from .models import Task, TaskStatus
from .storage import STORAGE_FILE, backup_tasks, remove_storage_file
from .logger import logger
from .repo import TaskRepo

console = Console()

def create_task_table(tasks_to_show: List[Task], title: Optional[str] = None) -> Table:
    """Create a table to display tasks.
    
    Args:
        tasks_to_show: List of tasks to display
        title: Optional title for the table
    
    Returns:
        A rich Table object with the tasks
    """
    table = Table(show_header=True, header_style="bold", title=title)
    table.add_column("ID", style="cyan", width=4)
    table.add_column("Title", style="green")
    table.add_column("Status", style="yellow", width=12)
    table.add_column("Created", style="blue", width=16)
    
    for task in tasks_to_show:
        status_style = "green" if task.status == TaskStatus.COMPLETED else "yellow"
        table.add_row(
            str(task.id),
            task.title,
            f"[{status_style}]{task.status.value}[/{status_style}]",
            task.created_at.strftime("%Y-%m-%d %H:%M")
        )
    
    return table

@click.group()
@click.pass_context
def cli(ctx):
    """Talia CLI - A simple and elegant task management application."""
    if not ctx.obj:
        ctx.obj = TaskRepo(STORAGE_FILE)

@cli.command()
@click.argument('title')
@click.pass_obj
def add(repo: TaskRepo, title: str):
    """Add a new task to your inbox."""
    try:
        task = Task(
            id=repo.get_next_id(),
            title=title,
            status=TaskStatus.INBOX,
            created_at=datetime.now()
        )
        repo.add(task)
        repo.save()
        logger.info(f"Added new task to inbox: {title}")
        console.print(f"✅ Added to inbox: {title}", style="green")
    except ValueError as e:
        logger.error(f"Invalid task data: {e}")
        console.print(f"❌ Failed to add task: {e}", style="red")
    except Exception as e:
        logger.error(f"Failed to add task: {e}")
        console.print("❌ Failed to add task", style="red")

@cli.command()
@click.option('--status', '-s', type=click.Choice([s.name for s in TaskStatus]), help='Filter tasks by status')
@click.pass_obj
def list(repo: TaskRepo, status: Optional[str]):
    """List all tasks, optionally filtered by status."""
    status_msg = f" with status {status}" if status else ""
    filtered_tasks = repo.all
    if status:
        filtered_tasks = [t for t in repo.all if t.status.name == status]
    
    if not filtered_tasks:
        logger.info(f"No tasks found{status_msg}")
        console.print(f"📝 No tasks found{status_msg}", style="yellow")
        return

    try:
        # Sort tasks by ID
        sorted_tasks = sorted(filtered_tasks, key=lambda x: x.id)
        table = create_task_table(sorted_tasks, title=f"Tasks{status_msg}")
        
        logger.debug(f"Displaying {len(filtered_tasks)} tasks")
        console.print(table)
    except Exception as e:
        logger.error(f"Failed to display tasks: {e}")
        console.print("❌ Failed to display tasks", style="red")

@cli.command()
@click.argument('task_id', type=int)
@click.pass_obj
def done(repo: TaskRepo, task_id: int):
    """Mark a task as completed."""
    try:
        task = repo.get(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            console.print(f"❌ Task {task_id} not found", style="red")
            return
        
        if task.status == TaskStatus.COMPLETED:
            logger.info(f"Task {task_id} is already completed")
            console.print(f"ℹ️ Task {task_id} is already completed", style="yellow")
            return
        
        task.complete()
        repo.save()
        logger.info(f"Completed task: {task.title}")
        console.print(f"✅ Completed task: {task.title}", style="green")
    except ValueError as e:
        logger.error(f"Invalid task data: {e}")
        console.print(f"❌ Failed to complete task: {e}", style="red")
    except Exception as e:
        logger.error(f"Failed to complete task: {e}")
        console.print("❌ Failed to complete task", style="red")

@cli.command()
@click.argument('task_id', type=int)
@click.pass_obj
def archive(repo: TaskRepo, task_id: int):
    """Archive a task."""
    try:
        task = repo.get(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            console.print(f"❌ Task {task_id} not found", style="red")
            return
        
        if task.status == TaskStatus.ARCHIVED:
            logger.info(f"Task {task_id} is already archived")
            console.print(f"ℹ️ Task {task_id} is already archived", style="yellow")
            return
        
        task.archive()
        repo.save()
        logger.info(f"Archived task: {task.title}")
        console.print(f"📦 Archived task: {task.title}", style="green")
    except Exception as e:
        logger.error(f"Failed to archive task: {e}")
        console.print("❌ Failed to archive task", style="red")

@cli.command()
@click.argument('task_id', type=int)
@click.pass_obj
def todo(repo: TaskRepo, task_id: int):
    """Move a task to To Do list."""
    try:
        task = repo.get(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            console.print(f"❌ Task {task_id} not found", style="red")
            return
        
        task.move_to_todo()
        repo.save()
        logger.info(f"Moved task to To Do: {task.title}")
        console.print(f"📋 Moved to To Do: {task.title}", style="green")
    except Exception as e:
        logger.error(f"Failed to move task: {e}")
        console.print("❌ Failed to move task", style="red")

@cli.command()
@click.argument('task_id', type=int)
@click.pass_obj
def review(repo: TaskRepo, task_id: int):
    """Move a task to Review list."""
    try:
        task = repo.get(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            console.print(f"❌ Task {task_id} not found", style="red")
            return
        
        task.move_to_review()
        repo.save()
        logger.info(f"Moved task to Review: {task.title}")
        console.print(f"👀 Moved to Review: {task.title}", style="green")
    except Exception as e:
        logger.error(f"Failed to move task: {e}")
        console.print("❌ Failed to move task", style="red")

@cli.command()
@click.pass_obj
def dashboard(repo: TaskRepo):
    """Show your task dashboard."""
    if not repo.all:
        logger.info("No tasks found for dashboard")
        console.print("📝 No tasks found", style="yellow")
        return

    try:
        # Task Statistics
        total_tasks = len(repo.all)
        completed_tasks = len([t for t in repo.all if t.status == TaskStatus.COMPLETED])
        pending_tasks = total_tasks - completed_tasks
        
        # Create statistics panel
        stats = Table.grid()
        stats.add_row("📝 Total Tasks:", str(total_tasks))
        stats.add_row("✅ Completed:", str(completed_tasks))
        stats.add_row("⏳ Pending:", str(pending_tasks))
        
        console.print("\n📊 Task Dashboard\n", style="bold")
        console.print(stats)
        
        # Show recent tasks
        if repo.all:
            console.print("\n📋 Recent Tasks", style="bold")
            # Sort tasks by creation date, most recent first
            sorted_tasks = sorted(repo.all, key=lambda x: x.created_at, reverse=True)
            # Show last 5 tasks or all if less than 5
            table = create_task_table(sorted_tasks[:5])
            console.print(table)
            
            # Show completion rate if there are tasks
            if total_tasks > 0:
                completion_rate = (completed_tasks / total_tasks) * 100
                console.print(f"\n📈 Completion Rate: {completion_rate:.1f}%", style="bold")
        
        logger.debug(f"Displayed dashboard with {total_tasks} tasks ({completed_tasks} completed)")
    except Exception as e:
        logger.error(f"Failed to display dashboard: {e}")
        console.print("❌ Failed to display dashboard", style="red")

@cli.command()
@click.option('--name', '-n', help='Custom name for the backup file')
@click.pass_obj
def backup(repo: TaskRepo, name: Optional[str]):
    """Create a backup of your tasks."""
    try:
        if os.path.exists(STORAGE_FILE):
            backup_file = backup_tasks(name)
            if backup_file:
                logger.info(f"Created backup: {backup_file}")
                console.print(f"📦 Tasks backed up to: {backup_file}", style="green")
        else:
            logger.warning("No tasks found to backup")
            console.print("ℹ️  No tasks found to backup", style="yellow")
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        console.print("❌ Failed to create backup", style="red")

@cli.command()
@click.pass_obj
def reset(repo: TaskRepo):
    """Move current tasks to a backup file and start fresh."""
    try:
        if os.path.exists(repo._path):
            backup_file = backup_tasks("todelete", repo._path)
            if backup_file and remove_storage_file(repo._path):
                logger.info(f"Reset completed, backup at: {backup_file}")
                console.print(f"📦 Tasks backed up to: {backup_file}", style="green")
        else:
            logger.warning("No tasks found to reset")
            console.print("ℹ️  No tasks found to backup", style="yellow")
        
        # Clear the in-memory tasks
        repo._tasks = []
        repo.save()
    except Exception as e:
        logger.error(f"Failed to reset tasks: {e}")
        console.print("❌ Failed to reset tasks", style="red")

def main():
    """Entry point for the CLI."""
    cli() 