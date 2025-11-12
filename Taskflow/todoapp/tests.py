"""Tests for todoapp."""
from django.test import TestCase
from .models import Todo


class TodoModelTest(TestCase):
    """Test cases for Todo model."""

    def setUp(self):
        """Set up test data."""
        self.todo = Todo.objects.create(
            title='Test Todo',
            description='This is a test todo',
            completed=False
        )

    def test_todo_creation(self):
        """Test todo creation."""
        self.assertEqual(self.todo.title, 'Test Todo')
        self.assertEqual(self.todo.description, 'This is a test todo')
        self.assertFalse(self.todo.completed)

    def test_todo_str(self):
        """Test todo string representation."""
        self.assertEqual(str(self.todo), 'Test Todo')

    def test_todo_completion(self):
        """Test todo completion toggle."""
        self.assertFalse(self.todo.completed)
        self.todo.completed = True
        self.todo.save()
        self.assertTrue(self.todo.completed)
