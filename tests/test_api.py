import pytest
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
django.setup()
from django.test import Client


client = Client()

from tasks_app.db import get_connection

@pytest.fixture(scope="function")
def setup_tasks_table():
    conn = get_connection()
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            description TEXT,
            due_date DATE,
            status VARCHAR(50)
        )
    """)
    conn.commit()
    yield
    # Optional: drop table after test
    cursor.execute("DROP TABLE tasks")
    conn.commit()
    conn.close()

@pytest.mark.django_db
def test_get_tasks(setup_tasks_table):
    response = client.get("/api/tasks/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_task(setup_tasks_table):
    payload = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": "2025-11-20",
        "status": "pending"
    }
    response = client.post(
        "/api/tasks/",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Task created"

@pytest.mark.django_db
def test_update_task(setup_tasks_table):
    # Create a task first
    payload = {"title": "Update Test", "description": "Desc", "due_date": "2025-11-21", "status": "pending"}
    create_resp = client.post("/api/tasks/", data=json.dumps(payload), content_type="application/json")

    task_id = 1  # adjust if needed
    update_payload = {"title": "Updated", "description": "Updated", "due_date": "2025-11-22", "status": "completed"}
    response = client.put(f"/api/tasks/{task_id}/", data=json.dumps(update_payload), content_type="application/json")
    assert response.status_code == 200
    assert response.json()["message"] == "Task updated"

@pytest.mark.django_db
def test_delete_task(setup_tasks_table):
    task_id = 1  # adjust if needed
    response = client.delete(f"/api/tasks/{task_id}/")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"
