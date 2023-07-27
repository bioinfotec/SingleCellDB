# calculator/tasks.py

from celery import shared_task
import time
@shared_task
def add_numbers(a, b):
    time.sleep(10)
    return a + b
