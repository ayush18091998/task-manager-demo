from django.contrib import admin
from django.urls import path, include  # <--- include is needed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks_app.urls')),  # <--- this connects your app's urls
]
