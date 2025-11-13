from .models import Todo


def task_count(request):
    """Provide the number of todos for the authenticated user for navbar badges."""
    if request.user.is_authenticated:
        count = Todo.objects.filter(owner=request.user).count()
    else:
        count = 0
    return {
        'nav_task_count': count
    }
