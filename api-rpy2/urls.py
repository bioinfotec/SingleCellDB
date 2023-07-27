from django.urls import path
from .views import anaylse, execute_r_code, test

urlpatterns = [
    path('execute/', execute_r_code, name='execute_r_code'),
    path("analyse/", anaylse, name="analyse_r_code"),
    path("test/", test, name="test")
]