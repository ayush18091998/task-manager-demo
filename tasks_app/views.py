import json
import logging
from datetime import datetime

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from .db import get_connection

# -----------------------------
# Simple Logger
# -----------------------------
logger = logging.getLogger("tasks.views")

# -----------------------------
# API: GET /api/tasks/ , POST /api/tasks/
# -----------------------------
def tasks_list(request):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if request.method == "GET":
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            conn.close()

            tasks = [
                {"id": r[0], "title": r[1], "description": r[2], "due_date": str(r[3]), "status": r[4]}
                for r in rows
            ]
            return JsonResponse(tasks, safe=False)

        elif request.method == "POST":
            try:
                data = json.loads(request.body)
                logger.info(data)
            except json.JSONDecodeError:
                logger.error("Invalid JSON in POST /api/tasks/")
                return HttpResponseBadRequest("Invalid JSON")

            title = data.get("title", "")
            description = data.get("description", "")
            status = data.get("status", "")
            due_date_str = data.get("due_date", None)

            # Convert string to date object
            due_date = None
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

            cursor.execute("""
                INSERT INTO tasks (title, description, due_date, status)
                VALUES (%s, %s, %s, %s)
            """, (title, description, due_date, status))
            conn.commit()
            conn.close()
            return JsonResponse({"message": "Task created"}, status=201)

        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as ex:
        logger.exception("Error in tasks_list API")
        if conn:
            conn.close()
        return JsonResponse({"error": "Something went wrong"}, status=500)


# -----------------------------
# API: GET /api/tasks/<id>/ , PUT /api/tasks/<id>/ , DELETE /api/tasks/<id>/
# -----------------------------
def task_detail(request, task_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if request.method == "GET":
            cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
            row = cursor.fetchone()
            conn.close()

            if not row:
                logger.warning(f"Task not found: {task_id}")
                return JsonResponse({"error": "Task not found"}, status=404)

            task = {"id": row[0], "title": row[1], "description": row[2], "due_date": str(row[3]), "status": row[4]}
            return JsonResponse(task)

        elif request.method == "PUT":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in PUT /api/tasks/{task_id}")
                return HttpResponseBadRequest("Invalid JSON")

            title = data.get("title", "")
            description = data.get("description", "")
            status = data.get("status", "")
            due_date_str = data.get("due_date", None)

            # Convert due_date string to date object
            due_date = None
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

            try:
                cursor.execute("""
                        UPDATE tasks
                        SET title=%s, description=%s, due_date=%s, status=%s
                        WHERE id=%s
                    """, (title, description, due_date, status, task_id))
                conn.commit()
            except Exception as ex:
                logger.exception(f"Failed to update task {task_id}")
                return JsonResponse({"error": "Failed to update task"}, status=500)

            conn.close()
            return JsonResponse({"message": "Task updated"})

        elif request.method == "DELETE":
            try:
                cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
                conn.commit()
                logger.info(f"Task deleted: {task_id}")
            except Exception as ex:
                logger.exception(f"Failed to delete task {task_id}")
                return JsonResponse({"error": "Failed to delete task"}, status=500)

            conn.close()
            return JsonResponse({"message": "Task deleted"})

        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as ex:
        logger.exception(f"Error in task_detail API: {task_id}")
        if conn:
            conn.close()
        return JsonResponse({"error": "Something went wrong"}, status=500)


# -----------------------------
# Template Views
# -----------------------------
def tasks_page(request):
    return render(request, "task_list.html")


def add_task_page(request):
    return render(request, "add_task.html")
