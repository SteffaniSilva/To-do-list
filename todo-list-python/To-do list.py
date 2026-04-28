import sqlite3
import csv
import os
from datetime import datetime


DATABASE_NAME = "tasks.db"
EXPORT_FOLDER = "exports"


class TodoDatabase:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT NOT NULL,
                due_date TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def add_task(self, title, description, priority, due_date):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
            INSERT INTO tasks (title, description, priority, due_date, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, priority, due_date, "Pending", created_at))

        self.connection.commit()

    def get_all_tasks(self):
        self.cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
        return self.cursor.fetchall()

    def get_tasks_by_status(self, status):
        self.cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY id DESC", (status,))
        return self.cursor.fetchall()

    def mark_completed(self, task_id):
        self.cursor.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id = ?
        """, ("Completed", task_id))

        self.connection.commit()
        return self.cursor.rowcount

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.connection.commit()
        return self.cursor.rowcount

    def search_tasks(self, keyword):
        search_keyword = "%" + keyword + "%"

        self.cursor.execute("""
            SELECT * FROM tasks
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY id DESC
        """, (search_keyword, search_keyword))

        return self.cursor.fetchall()

    def get_overdue_tasks(self):
        today = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute("""
            SELECT * FROM tasks
            WHERE due_date < ? AND status = ?
            ORDER BY due_date ASC
        """, (today, "Pending"))

        return self.cursor.fetchall()

    def get_statistics(self):
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        total = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = ?", ("Pending",))
        pending = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = ?", ("Completed",))
        completed = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE priority = ?", ("High",))
        high_priority = self.cursor.fetchone()[0]

        return total, pending, completed, high_priority

    def close(self):
        self.connection.close()


def validate_date(date_text):
    if date_text == "":
        return True

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def choose_priority():
    while True:
        print()
        print("Choose priority:")
        print("1. Low")
        print("2. Medium")
        print("3. High")

        choice = input("Enter your choice: ")

        if choice == "1":
            return "Low"
        elif choice == "2":
            return "Medium"
        elif choice == "3":
            return "High"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def display_tasks(tasks):
    if len(tasks) == 0:
        print("No tasks found.")
        return

    print()
    print("=" * 90)
    print(f"{'ID':<5}{'Title':<25}{'Priority':<12}{'Due Date':<15}{'Status':<12}{'Created At'}")
    print("=" * 90)

    for task in tasks:
        task_id = task[0]
        title = task[1]
        priority = task[3]
        due_date = task[4] if task[4] else "No due date"
        status = task[5]
        created_at = task[6]

        print(f"{task_id:<5}{title:<25}{priority:<12}{due_date:<15}{status:<12}{created_at}")

    print("=" * 90)


def add_task_menu(database):
    print()
    print("========== ADD NEW TASK ==========")

    title = input("Enter task title: ").strip()

    if title == "":
        print("Task title cannot be empty.")
        return

    description = input("Enter task description: ").strip()
    priority = choose_priority()

    while True:
        due_date = input("Enter due date YYYY-MM-DD or leave empty: ").strip()

        if validate_date(due_date):
            break
        else:
            print("Invalid date format. Please use YYYY-MM-DD.")

    database.add_task(title, description, priority, due_date)
    print("Task added successfully!")


def mark_task_completed_menu(database):
    try:
        task_id = int(input("Enter task ID to mark as completed: "))

        rows_updated = database.mark_completed(task_id)

        if rows_updated == 0:
            print("Task ID not found.")
        else:
            print("Task marked as completed.")

    except ValueError:
        print("Invalid ID. Please enter a number.")


def delete_task_menu(database):
    try:
        task_id = int(input("Enter task ID to delete: "))

        confirm = input("Are you sure you want to delete this task? yes/no: ").lower()

        if confirm == "yes":
            rows_deleted = database.delete_task(task_id)

            if rows_deleted == 0:
                print("Task ID not found.")
            else:
                print("Task deleted successfully.")
        else:
            print("Delete cancelled.")

    except ValueError:
        print("Invalid ID. Please enter a number.")


def search_task_menu(database):
    keyword = input("Enter search keyword: ").strip()

    if keyword == "":
        print("Search keyword cannot be empty.")
        return

    tasks = database.search_tasks(keyword)
    display_tasks(tasks)


def show_statistics(database):
    total, pending, completed, high_priority = database.get_statistics()

    print()
    print("========== TASK STATISTICS ==========")
    print("Total tasks:", total)
    print("Pending tasks:", pending)
    print("Completed tasks:", completed)
    print("High priority tasks:", high_priority)

    if total > 0:
        completion_rate = (completed / total) * 100
        print("Completion rate:", round(completion_rate, 2), "%")

    print("=====================================")


def export_tasks_to_csv(database):
    tasks = database.get_all_tasks()

    if len(tasks) == 0:
        print("No tasks to export.")
        return

    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)

    file_name = "tasks_export.csv"
    file_path = os.path.join(EXPORT_FOLDER, file_name)

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Title",
            "Description",
            "Priority",
            "Due Date",
            "Status",
            "Created At"
        ])

        writer.writerows(tasks)

    print("Tasks exported successfully to:", file_path)


def main():
    database = TodoDatabase()

    print("Welcome to the Advanced Python To-do List App")

    while True:
        print()
        print("========== MAIN MENU ==========")
        print("1. Add task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. Mark task as completed")
        print("6. Delete task")
        print("7. Search tasks")
        print("8. View overdue tasks")
        print("9. View statistics")
        print("10. Export tasks to CSV")
        print("11. Exit")
        print("===============================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task_menu(database)

        elif choice == "2":
            tasks = database.get_all_tasks()
            display_tasks(tasks)

        elif choice == "3":
            tasks = database.get_tasks_by_status("Pending")
            display_tasks(tasks)

        elif choice == "4":
            tasks = database.get_tasks_by_status("Completed")
            display_tasks(tasks)

        elif choice == "5":
            mark_task_completed_menu(database)

        elif choice == "6":
            delete_task_menu(database)

        elif choice == "7":
            search_task_menu(database)

        elif choice == "8":
            tasks = database.get_overdue_tasks()
            display_tasks(tasks)

        elif choice == "9":
            show_statistics(database)

        elif choice == "10":
            export_tasks_to_csv(database)

        elif choice == "11":
            database.close()
            print("Program ended. Thank you!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 11.")


main()
