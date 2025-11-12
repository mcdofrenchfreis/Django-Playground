"""Minimal API tests for the Todo endpoints."""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Todo
from django.urls import reverse


class TodoAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        # Create tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        # Create todos for user1
        self.todo1 = Todo.objects.create(title='User1 Todo', description='desc', owner=self.user1)
        self.todo2 = Todo.objects.create(title='User1 Todo 2', description='desc2', owner=self.user1)
        # Create todo for user2
        self.todo3 = Todo.objects.create(title='User2 Todo', description='user2desc', owner=self.user2)

    def test_list_todos_unauthenticated(self):
        """Unauthenticated users should see empty list."""
        resp = self.client.get('/api/todos/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 0)

    def test_list_todos_authenticated(self):
        """Authenticated users should see only their own todos."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        resp = self.client.get('/api/todos/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # user1 should see only their 2 todos
        self.assertEqual(len(data), 2)
        ids = {item['id'] for item in data}
        self.assertIn(self.todo1.id, ids)
        self.assertIn(self.todo2.id, ids)
        self.assertNotIn(self.todo3.id, ids)

    def test_create_todo(self):
        data = {'title': 'New from test', 'description': 'd'}
        # unauthenticated should be forbidden for writes
        resp = self.client.post('/api/todos/', data, format='json')
        self.assertIn(resp.status_code, (401, 403))

        # authenticate as user1 and create
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        resp = self.client.post('/api/todos/', data, format='json')
        self.assertEqual(resp.status_code, 201)
        created = resp.json()
        # verify owner is set to user1
        self.assertEqual(created['owner'], self.user1.id)

    def test_toggle_todo_permission(self):
        """User can only toggle their own todos."""
        # user1 tries to toggle their own todo (should succeed)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        resp = self.client.post(f'/api/todos/{self.todo1.id}/toggle/')
        self.assertEqual(resp.status_code, 200)
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.completed)

        # user2 tries to toggle user1's todo (should fail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        resp = self.client.post(f'/api/todos/{self.todo1.id}/toggle/')
        self.assertIn(resp.status_code, (403, 404))

    def test_filter_completed(self):
        """Filter by completed status only returns user's todos."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        # Mark one of user1's todos as completed
        self.todo1.completed = True
        self.todo1.save()
        
        resp = self.client.get('/api/todos/?completed=true')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # should only see user1's completed todo
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.todo1.id)

    def test_search(self):
        """Search only returns user's todos matching search."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        resp = self.client.get('/api/todos/?search=User1')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # user1 should see their matching todos
        self.assertTrue(any('User1' in item['title'] for item in data))
        # user2's todo should not appear
        self.assertFalse(any('User2' in item['title'] for item in data))

    def test_register_and_login(self):
        # register new user
        url = '/api/auth/register/'
        data = {'username': 'newuser', 'password': 'pw1234', 'email': 'a@b.com'}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        self.assertIn('token', body)

        # login via login endpoint
        login_url = '/api/auth/login/'
        resp2 = self.client.post(login_url, {'username': 'newuser', 'password': 'pw1234'}, format='json')
        self.assertEqual(resp2.status_code, 200)
        body2 = resp2.json()
        self.assertIn('token', body2)
