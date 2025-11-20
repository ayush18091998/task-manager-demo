from django.urls import path
from . import views

urlpatterns = [
    # API ROUTES
    path("api/tasks/", views.tasks_list),
    path("api/tasks/<int:task_id>/", views.task_detail),

    # FRONTEND ROUTES
    path("", views.tasks_page, name="tasks_page"),
    path("add/", views.add_task_page, name="add_task_page"),
]
