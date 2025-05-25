from rest_framework.test import APITestCase
from core.models import Vertical, Plan
from core.serializers import VerticalSerializer, PlanSerializer

class TestPlanSerializer(APITestCase):
    def test_plan_serializer_success(self):
        instance = Plan.objects.first()
        verticals = Vertical.objects.all()[:2]
        instance.vertical.add(*verticals)
        serializer = PlanSerializer(instance=instance)
        data = serializer.data

        self.assertEqual(data['name'], instance.name)
        self.assertEqual(len(data['vertical']), 2)
        self.assertNotIn('created_at', data)
        self.assertNotIn('updated_at', data)


        vertical_names = {v['name'] for v in data['vertical']}
        self.assertIn(verticals[0].name, vertical_names)
        self.assertIn(verticals[1].name, vertical_names)