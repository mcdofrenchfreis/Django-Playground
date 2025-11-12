"""Views for todoapp."""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Todo
from .forms import TodoForm


def todo_list(request):
    """Display all todos."""
    todos = Todo.objects.all()
    completed_count = todos.filter(completed=True).count()
    pending_count = todos.filter(completed=False).count()
    return render(request, 'todoapp/todo_list.html', {
        'todos': todos,
        'completed_count': completed_count,
        'pending_count': pending_count,
    })


def todo_detail(request, pk):
    """Display a single todo."""
    todo = get_object_or_404(Todo, pk=pk)
    return render(request, 'todoapp/todo_detail.html', {'todo': todo})


def todo_create(request):
    """Create a new todo."""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todoapp/todo_form.html', {'form': form, 'title': 'Create Todo'})


def todo_update(request, pk):
    """Update a todo."""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_detail', pk=todo.pk)
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todoapp/todo_form.html', {'form': form, 'todo': todo, 'title': 'Edit Todo'})


def todo_delete(request, pk):
    """Delete a todo."""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todoapp/todo_confirm_delete.html', {'todo': todo})


@require_http_methods(['POST'])
def toggle_todo(request, pk):
    """Toggle todo completion status."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')
