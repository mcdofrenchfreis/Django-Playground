"""API views (DRF viewsets) for todoapp.

Enhancements:
- support filtering by `completed` and `search` via query params
- add a `toggle` action to flip the `completed` state
- enforce per-user todos: users can only see/modify their own todos
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allows users to read all todos, but only modify their own."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class TodoViewSet(viewsets.ModelViewSet):
    """CRUD viewset for Todo with filtering, search, and per-user permissions.

    Query params supported:
    - completed=true|false  -> filter by completion state
    - search=<text>         -> case-insensitive title contains
    
    Authenticated users can create and modify only their own todos.
    """
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Filter todos: if authenticated, return only user's todos; else return empty queryset."""
        # Only authenticated users can see todos
        if not self.request.user.is_authenticated:
            return Todo.objects.none()
        
        qs = Todo.objects.filter(owner=self.request.user)
        
        # Apply query parameter filters
        params = self.request.query_params
        completed = params.get('completed')
        if completed is not None:
            c = completed.lower()
            if c in ('true', '1', 't', 'yes'):
                qs = qs.filter(completed=True)
            elif c in ('false', '0', 'f', 'no'):
                qs = qs.filter(completed=False)

        search = params.get('search')
        if search:
            qs = qs.filter(title__icontains=search)

        return qs

    def perform_create(self, serializer):
        """Automatically set owner to current user on create."""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """Toggle the `completed` boolean for a single Todo.

        POST /api/todos/{id}/toggle/
        Returns the updated object.
        """
        todo = self.get_object()
        todo.completed = not todo.completed
        todo.save()
        serializer = self.get_serializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
