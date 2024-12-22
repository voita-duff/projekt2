import os
import csv
from datetime import datetime

# Cesta k souboru, kde budou ulozeny ulohy
data_file = "data/todo_tasks.txt"

# Funkce pro nacteni uloh ze souboru
def load_tasks():
    tasks = []
    # Overime, zda existuje soubor, pokud ne, vytvorime jej
    if not os.path.exists(data_file):
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        open(data_file, 'w').close()
    else:
        # Pokud soubor existuje, otevreme jej a precteme ulohy
        with open(data_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                # Zkontrolujeme, zda radek obsahuje spravny pocet sloupcu
                if len(row) == 5:
                    tasks.append({
                        "id": row[0],
                        "name": row[1],
                        "priority": row[2],
                        "deadline": row[3],
                        "status": row[4]
                    })
    return tasks

# Funkce pro ulozeni uloh do souboru
def save_tasks(tasks):
    with open(data_file, mode="w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        # Pro kazdy ulozeny ukol zapiseme jeho hodnoty do radku souboru
        for task in tasks:
            writer.writerow([task["id"], task["name"], task["priority"], task["deadline"], task["status"]])

# Funkce pro pridani noveho ukolu
def add_task(tasks):
    # Automaticky vygenerujeme ID ukolu podle poctu ulozenych uloh
    task_id = str(len(tasks) + 1)
    name = input("Zadejte název úkolu: ").strip()
    priority = input("Zadejte prioritu (Nízká, Střední, Vysoká, výchozí Střední): ").strip() or "Střední"
    deadline = input("Zadejte termín splnění (YYYY-MM-DD, volitelné): ").strip()
    status = "Ne"
    # Vytvorime novy ukol jako slovnik
    task = {"id": task_id, "name": name, "priority": priority, "deadline": deadline, "status": status}
    tasks.append(task)  # Pridame ukol do seznamu
    print(f"Úkol '{name}' byl přidán!")

# Funkce pro zobrazeni uloh, s moznosti filtrovani
def list_tasks(tasks, filter_by=None):
    filtered_tasks = tasks
    # Pokud je nastaven filtr, aplikujeme jej
    if filter_by:
        if "priority" in filter_by:
            filtered_tasks = [task for task in tasks if task["priority"].lower() == filter_by["priority"].lower()]
        if "status" in filter_by:
            filtered_tasks = [task for task in tasks if task["status"].lower() == filter_by["status"].lower()]

    # Vypiseme hlavicku tabulky
    print("\nID | Úkol               | Priorita  | Termín       | Stav")
    print("-" * 60)
    # Pro kazdy ukol vypiseme jeho detaily
    for task in filtered_tasks:
        print(f"{task['id']:2} | {task['name']:18} | {task['priority']:9} | {task['deadline']:12} | {task['status']}")

# Funkce pro odstraneni ukolu podle ID nebo nazvu
def remove_task(tasks):
    identifier = input("Zadejte ID nebo název úkolu pro odstranění: ").strip()
    for task in tasks:
        # Pokud najdeme ukol odpovidajici zadanemu ID nebo nazvu
        if task["id"] == identifier or task["name"] == identifier:
            tasks.remove(task)  # Odstranime ukol ze seznamu
            print(f"Úkol '{task['name']}' byl odstraněn.")
            return
    print("Úkol nenalezen.")

# Funkce pro oznaceni ukolu jako dokoncenych
def complete_task(tasks):
    identifier = input("Zadejte ID nebo název úkolu k označení jako hotový: ").strip()
    for task in tasks:
        # Pokud najdeme ukol odpovidajici zadanemu ID nebo nazvu
        if task["id"] == identifier or task["name"] == identifier:
            task["status"] = "Ano"  # Nastavime status na Ano
            print(f"Úkol '{task['name']}' byl označen jako dokončený.")
            return
    print("Úkol nenalezen.")

# Funkce pro editaci existujiciho ukolu
def edit_task(tasks):
    identifier = input("Zadejte ID nebo název úkolu pro úpravu: ").strip()
    for task in tasks:
        # Pokud najdeme ukol odpovidajici zadanemu ID nebo nazvu
        if task["id"] == identifier or task["name"] == identifier:
            # Umoznuje uzivateli upravit jednotlive vlastnosti
            task["name"] = input(f"Zadejte nový název úkolu (aktuální: {task['name']}): ").strip() or task["name"]
            task["priority"] = input(f"Zadejte novou prioritu (aktuální: {task['priority']}): ").strip() or task["priority"]
            task["deadline"] = input(f"Zadejte nový termín (aktuální: {task['deadline']}): ").strip() or task["deadline"]
            task["status"] = input(f"Zadejte nový stav (Ano/Ne, aktuální: {task['status']}): ").strip() or task["status"]
            print(f"Úkol '{task['name']}' byl aktualizován.")
            return
    print("Úkol nenalezen.")

# Hlavni funkce aplikace
def main():
    tasks = load_tasks()  # Nacteni uloh pri spusteni aplikace
    while True:
        # Nabidka prikazu pro uzivatele
        print("=== ToDo List Manager ===")
        print("Nápověda: použijte příkazy 'add', 'list', 'remove', 'complete', 'edit', 'save', 'exit'.")
        command = input("> ").strip().lower()
        if command == "add":
            add_task(tasks)
        elif command == "list":
            filter_choice = input("Chcete filtrovat? (priority/stav/ne): ").strip().lower()
            if filter_choice == "priority":
                priority = input("Zadejte prioritu (Nízká, Střední, Vysoká): ")
                list_tasks(tasks, filter_by={"priority": priority})
            elif filter_choice == "stav":
                status = input("Zadejte stav (Ano/Ne): ")
                list_tasks(tasks, filter_by={"status": status})
            else:
                list_tasks(tasks)
        elif command == "remove":
            remove_task(tasks)
        elif command == "complete":
            complete_task(tasks)
        elif command == "edit":
            edit_task(tasks)
        elif command == "save":
            save_tasks(tasks)
            print("Úkoly byly uloženy do souboru.")
        elif command == "exit":
            save_tasks(tasks)  # Automaticke ulozeni pred ukoncenim
            print("Úkoly byly uloženy. Ukončuji aplikaci.")
            break
        else:
            print("Neplatný příkaz. Použijte 'add', 'list', 'remove', 'complete', 'edit', 'save', 'exit'.")

# Spusteni aplikace
if __name__ == "__main__":
    main()
