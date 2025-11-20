from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks_app'

    def ready(self):
        import sys
        if 'runserver' in sys.argv:
            try:
                from .db import init_db
                init_db()
                print("✔ tasks table initialized")
            except Exception as e:
                print("❌ DB INIT ERROR:", e)
