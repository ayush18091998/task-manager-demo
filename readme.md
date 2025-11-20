# Task Manager (Django + MySQL, No ORM)

A simple task manager built using **Django** with **raw SQL** (no Django ORM), connected to **MySQL**, and tested with **pytest**.  
The project includes both REST API endpoints and basic HTML templates for frontend interaction.

---

## 📌 Features
- CRUD API for tasks (Create, Read, Update, Delete)
- Uses **PyMySQL + manual SQL queries** instead of Django ORM
- Auto-creates the `tasks` table on server start
- HTML frontend for viewing and adding tasks
- Complete unit tests using pytest
- Clean MVC separation


## ⚙️ Setup Instructions

### 1️⃣ Create & activate a virtual environment
- python -m venv venv
- venv\Scripts\activate(windows)
- source venv/bin/activate(MAC/Linux)

### 2️⃣ Install dependencies
 - pip install -r requirements.txt

### 3️⃣ Configure MySQL connection
Update `tasks/db.py` if needed:

```python
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="todo_db",
)
```
### 4️⃣ Run Django server

 - python manage.py runserver

## 🧪 Running Tests 

Run a specific test:
- pytest tasks/tests/test_api.py::test_get_tasks

Run all tests:
- pytest

## 🚀 API Endpoints

| Method | Endpoint         | Description      |
|--------|------------------|------------------|
| GET    | /api/tasks/      | List all tasks   |
| POST   | /api/tasks/      | Create a task    |
| GET    | /api/tasks/{id}/ | Get a task       |
| PUT    | /api/tasks/{id}/ | Update a task    |
| DELETE | /api/tasks/{id}/ | Delete a task    |

## Notes

- Project intentionally avoids Django ORM as required.

- All SQL queries are executed using PyMySQL.

- Safe against CSRF using Django’s built-in token.