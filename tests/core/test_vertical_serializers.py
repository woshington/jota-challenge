from rest_framework.test import APITestCase
from core.models import Vertical
from core.serializers import VerticalSerializer

class TestVerticalSerializer(APITestCase):
    def test_vertical_serializer(self):
        instance = Vertical.objects.first()
        serializer = VerticalSerializer(instance=instance)
        data = serializer.data

        self.assertEqual(data['name'], instance.name)
        self.assertNotIn('created_at', data)
        self.assertNotIn('updated_at', data)