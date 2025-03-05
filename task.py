import sys
import json
from datetime import datetime

TASK_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            tasks = json.load(f)
            # Retrofit old tasks: calculate duration for done tasks missing it
            for task in tasks:
                if task["done"] and task.get("duration") is None and task["completed"]:
                    task["duration"] = (datetime.fromisoformat(task["completed"]) - datetime.fromisoformat(task["created"])).total_seconds()
            return tasks
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "description": description,
        "created": datetime.now().isoformat(),
        "done": False,
        "completed": None,
        "duration": None
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task {task['id']}: {description}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return
    
    # Calculate average duration of completed tasks
    completed_tasks = [t for t in tasks if t["done"] and t.get("duration") is not None]
    avg_duration = sum(t["duration"] for t in completed_tasks) / len(completed_tasks) if completed_tasks else float("inf")
    
    # Assign priority: lower number = higher priority
    for task in tasks:
        if task["done"]:
            priority = 0  # Done tasks
        else:
            desc = task["description"].lower()
            if "urgent" in desc:
                priority = 1  # Urgent tasks
            elif "important" in desc:
                priority = 2  # Important tasks
            elif task.get("duration") is not None:
                priority = 1 if task["duration"] < avg_duration else 2
            else:
                priority = 3  # Default for undone tasks
        task["priority"] = priority
    
    # Display sorted by priority
    for task in sorted(tasks, key=lambda x: x["priority"]):
        status = "✓" if task["done"] else " "
        print(f"[{task['id']}] [{status}] {task['description']} (Priority: {task['priority']})")

def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"Task {task_id} already marked done!")
            else:
                task["done"] = True
                task["completed"] = datetime.now().isoformat()
                duration = (datetime.fromisoformat(task["completed"]) - datetime.fromisoformat(task["created"])).total_seconds()
                task["duration"] = duration
                save_tasks(tasks)
                print(f"Marked task {task_id} as done! (Took {duration:.2f} seconds)")
            return
    print(f"Task {task_id} not found!")

def show_stats():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return
    completed = [t for t in tasks if t["done"]]
    avg_duration = sum(t["duration"] for t in completed) / len(completed) if completed else 0
    print(f"Total tasks: {len(tasks)}, Completed: {len(completed)}, Avg duration: {avg_duration:.2f} seconds")

def main():
    if len(sys.argv) < 2:
        print("Usage: task <add|list|done|stats> [args]")
        return

    command = sys.argv[1].lower()
    if command == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif command == "list":
        list_tasks()
    elif command == "done" and len(sys.argv) == 3:
        try:
            task_id = int(sys.argv[2])
            mark_done(task_id)
        except ValueError:
            print("Please provide a valid task ID!")
    elif command == "stats":
        show_stats()
    else:
        print("Unknown command. Use: task add <description> | task list | task done <id> | task stats")

if __name__ == "__main__":
    main()