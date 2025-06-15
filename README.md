# Talia CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/dvwinck/talia-cli)

A simple and elegant task management CLI application built with Python. Features include task creation, status tracking, archiving, and a beautiful dashboard interface.

---

## Table of Contents
- [Talia CLI](#talia-cli)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Basic Commands](#basic-commands)
    - [Verbose Output](#verbose-output)
  - [Creating a Shortcut (`tl`)](#creating-a-shortcut-tl)
    - [macOS/Linux](#macoslinux)
    - [Windows](#windows)
  - [Development](#development)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)

---

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
- 📦 **Backup & Reset**
  - Backup and reset your task list
- 🖥️ **Beautiful CLI**
  - Rich output with tables and colors
- 🐍 **Pythonic & Tested**
  - 100% test coverage for core modules

---

## Installation

```bash
# Clone the repository
git clone https://github.com/dvwinck/talia-cli.git
cd talia-cli

# (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install .
```

---

## Usage

### Basic Commands

```bash
# Add a new task
talia add "Write documentation"

# List all tasks
talia list

# List tasks by status (case-insensitive, now positional)
talia list inbox
talia list todo
talia list review
talia list completed
talia list archived

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

### Verbose Output

Enable debug/verbose output for any command:

```bash
talia -v list inbox
talia --verbose add "My new task"
```

---

## Creating a Shortcut (`tl`)

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
   tl list inbox
   tl -v dashboard
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
   tl list inbox
   ```

---

## Development

1. Clone the repository and set up a virtual environment (see Installation).
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Make your changes and ensure all tests pass before submitting a pull request.

---

## Testing

Run all tests and check coverage:

```bash
pytest -v --cov=talia --cov-report=term-missing
```

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

---

## License

[MIT](LICENSE)

---

## Acknowledgements

- Built with [Click](https://click.palletsprojects.com/), [Rich](https://rich.readthedocs.io/), and Python 3.8+
- Inspired by productivity and simplicity 