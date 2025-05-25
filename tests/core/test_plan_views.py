from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import Vertical, Plan
from django.contrib.auth import get_user_model

class TestViewCore(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.plan_info = Plan.objects.get(name='JOTA Info')
        self.plan_pro = Plan.objects.get(name='JOTA PRO')


    def test_plan_list_view(self):
        url = reverse('core-plan-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_plan_retrieve_view(self):
        url = reverse('core-plan-detail', args=[self.plan_info.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], self.plan_info.name)
