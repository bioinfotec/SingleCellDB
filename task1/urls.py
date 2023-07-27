from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_two_numbers, name="add"),
    path('result/<str:task_id>/', views.get_task_result, name='get-task-result'),
]
