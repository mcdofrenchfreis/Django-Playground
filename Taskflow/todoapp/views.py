"""Views for todoapp."""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Todo
from .forms import TodoForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def todo_list(request):
    """Display all todos for the current user (or all if not authenticated)."""
    if request.user.is_authenticated:
        todos = Todo.objects.filter(owner=request.user)
    else:
        todos = Todo.objects.none()
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
    """Create a new todo for the current user."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.owner = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todoapp/todo_form.html', {'form': form, 'title': 'Create Todo'})


def todo_update(request, pk):
    """Update a todo (only if user is the owner)."""
    todo = get_object_or_404(Todo, pk=pk)
    
    # Check ownership
    if todo.owner != request.user:
        return redirect('todo_list')
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_detail', pk=todo.pk)
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todoapp/todo_form.html', {'form': form, 'todo': todo, 'title': 'Edit Todo'})


def todo_delete(request, pk):
    """Delete a todo (only if user is the owner)."""
    todo = get_object_or_404(Todo, pk=pk)
    
    # Check ownership
    if todo.owner != request.user:
        return redirect('todo_list')
    
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todoapp/todo_confirm_delete.html', {'todo': todo})


@require_http_methods(['POST'])
def toggle_todo(request, pk):
    """Toggle todo completion status (only if user is the owner)."""
    todo = get_object_or_404(Todo, pk=pk)
    
    # Check ownership
    if todo.owner != request.user:
        return redirect('todo_list')
    
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')


def register_view(request):
    """Register a new user via a simple form and log them in."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('todo_list')
    else:
        form = UserCreationForm()
    return render(request, 'todoapp/register.html', {'form': form})


def login_view(request):
    """Login view using Django's AuthenticationForm."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('todo_list')
    else:
        form = AuthenticationForm()
    return render(request, 'todoapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out.')
    return redirect('todo_list')
