from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestViewCore(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_vertical_list_view(self):
        url = reverse('core-vertical-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 5)