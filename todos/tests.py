from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Todo


class TodoAccessTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='TestPass123!')
        self.other_user = User.objects.create_user(username='other', password='TestPass123!')
        self.todo = Todo.objects.create(
            owner=self.owner,
            title='Owner task',
            description='Visible only to the owner.',
        )

    def test_todo_list_requires_login(self):
        response = self.client.get(reverse('todo-list'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('todo-list')}",
        )

    def test_user_only_sees_owned_todos(self):
        Todo.objects.create(owner=self.other_user, title='Other task')
        self.client.login(username='owner', password='TestPass123!')

        response = self.client.get(reverse('todo-list'))

        self.assertContains(response, 'Owner task')
        self.assertNotContains(response, 'Other task')

    def test_user_cannot_edit_other_users_todo(self):
        self.client.login(username='other', password='TestPass123!')

        response = self.client.get(reverse('todo-update', args=[self.todo.pk]))

        self.assertEqual(response.status_code, 404)

    def test_create_view_assigns_logged_in_user_as_owner(self):
        self.client.login(username='owner', password='TestPass123!')

        response = self.client.post(
            reverse('todo-create'),
            {
                'title': 'Fresh task',
                'description': 'Created in a test.',
                'priority': Todo.Priority.HIGH,
            },
        )

        self.assertRedirects(response, reverse('todo-list'))
        created_todo = Todo.objects.get(title='Fresh task')
        self.assertEqual(created_todo.owner, self.owner)


class SignUpTests(TestCase):
    def test_signup_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'newuser',
                'email': 'new@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertRedirects(response, reverse('todo-list'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        follow_up = self.client.get(reverse('todo-list'))
        self.assertEqual(follow_up.status_code, 200)
