# TaskTrackerAI
A command-line task manager with AI-driven prioritization.

## Features
- Add, list, and mark tasks as done via command prompt.
- AI prioritizes tasks based on completion time and keywords ("urgent", "important").
- Stats command for task summary.
- Built with Python in a Conda environment.

## Usage
- `python task.py add "task name"` - Add a task.
- `python task.py list` - List tasks with priorities.
- `python task.py done <id>` - Mark task done.
- `python task.py stats` - Show task stats.

## Installation
1. Clone repo: `git clone https://github.com/yourusername/TaskTrackerAI.git`
2. Set up Conda env: `conda create -n TaskTrackerAI python=3.11`
3. Activate: `conda activate TaskTrackerAI`
4. Run: `python task.py`