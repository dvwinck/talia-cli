# Talia CLI

Task List CLI - A simple and elegant task management application.

## Features

- 📝 **Task Management**
  - Add tasks to your inbox
  - Mark tasks as completed
  - Archive tasks
  - Move tasks between lists (Inbox, To Do, Review)
  - View task dashboard

- 🔄 **Task Status**
  - Inbox: New tasks
  - To Do: Tasks to be done
  - Review: Tasks under review
  - Completed: Finished tasks
  - Archived: Archived tasks

## Installation

```bash
pip install .
```

## Creating a Shortcut (tl)

You can create a shortcut `tl` for the `talia` command. Here's how to do it:

### macOS/Linux

1. Create a shell script in `/usr/local/bin`:
   ```bash
   sudo sh -c 'echo "#!/bin/bash\nsource /path/to/your/venv/bin/activate\ntalia \"\$@\"" > /usr/local/bin/tl && chmod +x /usr/local/bin/tl'
   ```
   Replace `/path/to/your/venv` with the actual path to your virtual environment.

2. Test the shortcut:
   ```bash
   tl --help
   ```

### Windows

1. Create a batch file named `tl.bat` in a directory that's in your PATH:
   ```batch
   @echo off
   call path\to\your\venv\Scripts\activate.bat
   talia %*
   ```
   Replace `path\to\your\venv` with the actual path to your virtual environment.

2. Test the shortcut:
   ```batch
   tl --help
   ```

## Usage

### Basic Commands

```bash
# Add a new task
talia add "Write documentation"

# List all tasks
talia list

# List tasks by status
talia list --status INBOX
talia list --status TODO
talia list --status REVIEW
talia list --status COMPLETED
talia list --status ARCHIVED

# Mark a task as completed
talia done 1

# Archive a task
talia archive 1

# Move a task to To Do list
talia todo 1

# Move a task to Review list
talia review 1

# View your dashboard
talia dashboard

# Create a backup
talia backup

# Reset your task list
talia reset
```

## Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## License

MIT 