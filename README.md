# Task Manager CLI

A small command-line to-do app written in Python. Tasks are saved in a JSON file, so they are still there the next time you run it.

## Features
- Add, list, complete and delete tasks
- Filter to show only unfinished tasks
- Data saved to `tasks.json`
- Input checks and clear error messages
- Unit tests

## Skills practiced
Python OOP (classes), lists and dictionaries, JSON file handling, `argparse`, error handling, `unittest`, Git and GitHub.

## Requirements
Python 3.8 or newer. No extra packages needed.

## How to use
```bash
python task_manager.py add "Learn Git and GitHub"
python task_manager.py add "Build my AI agent"
python task_manager.py list
python task_manager.py done 1
python task_manager.py list --pending
python task_manager.py delete 2
```

## Run the tests
```bash
python -m unittest -v
```

## Project structure
```
task-manager-cli/
├── task_manager.py        # main program (Task and TaskManager classes)
├── test_task_manager.py   # unit tests
├── README.md
└── .gitignore
```

## Ideas to extend it
- Add due dates and priorities
- Add an `edit` command
- Save to SQLite instead of JSON

## Author
Afan Nasr, BS Computer Science student
