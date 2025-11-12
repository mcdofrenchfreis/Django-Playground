"""Models for todoapp."""
from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    """Todo item model."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Todos'

    def __str__(self):
        return self.title
