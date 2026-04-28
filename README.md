# Advanced Python To-do List App

An advanced command-line To-do List application built with Python and SQLite.

This project allows users to add, view, search, complete, delete, and export tasks. It is designed to practice Python programming, backend logic, data handling, automation concepts, and GitHub project structure.

## Features

- Add new tasks
- Add task descriptions
- Set priority levels: Low, Medium, High
- Add due dates
- View all tasks
- View pending tasks
- View completed tasks
- Mark tasks as completed
- Delete tasks
- Search tasks by keyword
- View overdue tasks
- View task statistics
- Export tasks to CSV
- Store tasks using SQLite database
- Input validation
- Error handling
- Clean menu-based user interface

## Technologies Used

- Python
- SQLite
- sqlite3
- csv
- os
- datetime
- Git
- GitHub

## Project Structure

```text
todo-list-python/
│
├── todo_app.py
├── README.md
├── .gitignore
└── exports/
```

Note: `tasks.db` and `exports/` are generated automatically when the program runs and are ignored by Git.

## How to Run

1. Clone this repository:

```bash
git clone https://github.com/SteffaniSilva/To-do-list.git
```

2. Go to the project folder:

```bash
cd todo-list-python
```

3. Run the app:

```bash
python todo_app.py
```

Or:

```bash
py todo_app.py
```

## Example Usage

```text
========== MAIN MENU ==========
1. Add task
2. View all tasks
3. View pending tasks
4. View completed tasks
5. Mark task as completed
6. Delete task
7. Search tasks
8. View overdue tasks
9. View statistics
10. Export tasks to CSV
11. Exit
===============================
```

## What I Learned

While building this project, I practiced:

- Python basics
- Functions
- Classes and objects
- SQLite database handling
- CRUD operations
- File handling
- CSV export
- Date validation
- Error handling
- Menu-based application design
- Git and GitHub workflow

## Interview Explanation

This is an advanced Python command-line To-do List application. I used SQLite to store tasks locally and implemented CRUD operations such as creating, reading, updating, and deleting tasks. The program allows users to add task details, set priorities, add due dates, search tasks, view overdue tasks, check task statistics, and export tasks to a CSV file.

I structured the project using a class called `TodoDatabase` to manage database operations. I also used functions to separate the user interface logic from the database logic. This makes the code cleaner, reusable, and easier to maintain.

## Future Improvements

- Add user login system
- Add task categories
- Add reminders
- Add GUI using Tkinter
- Add Flask backend API
- Add web frontend using HTML, CSS, and JavaScript
- Add AI-based task suggestions
- Add natural language task creation

## Author

Created by Steffani Silva
