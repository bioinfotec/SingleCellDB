from django.urls import path
from .views import execute_r_code

urlpatterns = [
    path('execute/', execute_r_code, name='execute_r_code'),
]