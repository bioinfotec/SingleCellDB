from django.shortcuts import render
from celery.result import AsyncResult
from celery import current_task
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .task import add_numbers

@api_view(['POST'])
@permission_classes([AllowAny])
def add_two_numbers(request):
    # Get the two numbers from the request data
    a = int(request.data.get('a', 0))
    b = int(request.data.get('b', 0))

    # Call the Celery task to calculate the sum (in the background)
    result = add_numbers.delay(a, b)
    
    current_task.update_state(meta={'metadata': {'user_account': '123'}})
    return Response({'task_id': result.id}, status=200)

# Some other view or endpoint to get the task result
@api_view(['GET'])
@permission_classes([AllowAny])
def get_task_result(request, task_id):
    # Get the AsyncResult object for the task using the task_id
    result = AsyncResult(task_id)

    # Check if the task is ready and get the result
    if result.ready():
        try:
            # If the task is completed, get the result using the .get() method with a timeout
            # In this example, we set the timeout to 10 seconds (adjust it according to your requirements)
            task_result = result.get(timeout=2)
            response_data = {
                "task_id": task_id,
                "task_status": result.status,
                "task_result": task_result
            }
            return Response(response_data, status=200)
        except TimeoutError:
            # If the task is not ready within the timeout, return a response indicating the task is still running
            return Response({'status': 'Task is still running'}, status=202)
    else:
        # If the task is not ready, return a response indicating the task is still running
        return Response({'status': 'Task is still running'}, status=202)