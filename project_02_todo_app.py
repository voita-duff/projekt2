#import knihoven
import os
from datetime import datetime

 #cesta k souboru
TASKS_FILE = "data/todo_tasks.txt"

############################################

def load_tasks(): ###nacteni ukolu
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(";")
                tasks.append({
                    "id": int(parts[0]),
                    "name": parts[1],
                    "priority": parts[2],
                    "due_date": parts[3],
                    "status": parts[4]
                })
    return tasks
