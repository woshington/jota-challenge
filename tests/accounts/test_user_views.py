from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from core.models import Plan

User = get_user_model()

class TestUserViews(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create_user(
            username='testuser_admin',
            password='testpass',
            email='testemail@gmail.com',
            role=CustomUser.ADMIN
        )
        self.user_publisher = User.objects.create_user(
            username='testuser_publisher',
            password='testpass',
            role=CustomUser.PUBLISHER,
            email='testemail_publisher@gmail.com',
        )
        self.user_reader = User.objects.create_user(
            username='testuser_reader',
            password='testpass',
            role=CustomUser.READER,
            email='testemail_reader@gmail.com',
            plan=Plan.objects.get(name='JOTA Info')
        )

    def test_user_registration_admin_success(self):
        self.client.force_authenticate(user=self.user_admin)
        data = {
            'username': 'newuser',
            'email': 'newemail@gmail.com',
            'password': 'newpassword',
            'role': CustomUser.PUBLISHER,
        }
        response = self.client.post('/api/v1/accounts/register/', data)
        self.assertEqual(response.status_code, 201)

    def test_user_registration_denied_publisher(self):
        self.client.force_authenticate(user=self.user_publisher)
        data = {
            'username': 'newuser',
            'email': 'newemail@gmail.com',
            'password': 'newpassword',
            'role': CustomUser.PUBLISHER,
        }
        response = self.client.post('/api/v1/accounts/register/', data)
        self.assertEqual(response.status_code, 403)

    def test_user_registration_denied_reader(self):
        self.client.force_authenticate(user=self.user_reader)
        data = {
            'username': 'newuser',
            'email': 'newemail@gmail.com',
            'password': 'newpassword',
            'role': CustomUser.PUBLISHER,
        }
        response = self.client.post('/api/v1/accounts/register/', data)
        self.assertEqual(response.status_code, 403)


    def test_user_registration_admin_failed_create_reader(self):
        self.client.force_authenticate(user=self.user_admin)
        data = {
            'username': 'newuser',
            'email': 'newemail@gmail.com',
            'password': 'newpassword',
            'role': CustomUser.READER,
        }
        response = self.client.post('/api/v1/accounts/register/', data)
        self.assertEqual(response.status_code, 400)

    def test_user_registration_admin_success_create_reader(self):
        self.client.force_authenticate(user=self.user_admin)
        plan = Plan.objects.get(name='JOTA Info')
        data = {
            'username': 'newuser',
            'email': 'newemail@gmail.com',
            'password': 'newpassword',
            'role': CustomUser.READER,
            "plan": plan.id
        }
        response = self.client.post('/api/v1/accounts/register/', data)
        self.assertEqual(response.status_code, 201)

    def test_user_me_info(self):
        self.client.force_authenticate(user=self.user_reader)
        response = self.client.get('/api/v1/accounts/me/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.user_reader.username)
        self.assertEqual(response.data['email'], self.user_reader.email)
        self.assertEqual(response.data['role'], CustomUser.READER)
        self.assertEqual(response.data['plan'], self.user_reader.plan_id)

    def test_user_me_update(self):
        self.client.force_authenticate(user=self.user_reader)
        response = self.client.patch('/api/v1/accounts/me/', data={"username": "updated_username"})
        self.assertEqual(response.status_code, 200)
        self.user_reader.refresh_from_db()
        self.assertEqual(response.data['username'], "updated_username")
        self.assertEqual(response.data['email'], self.user_reader.email)
        self.assertEqual(response.data['role'], CustomUser.READER)
        self.assertEqual(response.data['plan'], self.user_reader.plan_id)