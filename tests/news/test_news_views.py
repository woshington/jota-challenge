from django.utils import timezone
from rest_framework.test import APITestCase
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Vertical, Plan
from core.serializers import VerticalSerializer
from news.models import News

User = get_user_model()

class TestViewNews(APITestCase):
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


    def test_get_news_admin(self):
        self.client.force_authenticate(user=self.user_admin)

        instance = News.objects.create(
            title='Test News',
            content='Test Content',
            author=self.user_publisher,
            is_open=False
        )
        verticals = Vertical.objects.all()[:2]
        instance.vertical.add(*verticals)

        url = reverse('news-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['id'] == instance.id
        assert response.json()[0]['title'] == instance.title
        assert response.json()[0]['content'] == instance.content
        assert response.json()[0]['author'] == instance.author.id
        assert response.json()[0]['is_open'] == instance.is_open
        assert response.json()[0]['vertical'] == [VerticalSerializer(v).data for v in verticals]

    def test_get_news_publisher(self):
        self.client.force_authenticate(user=self.user_publisher)

        instance = News.objects.create(
            title='Test News',
            content='Test Content',
            author=self.user_publisher,
            is_open=False
        )
        instance_admin = News.objects.create(
            title='Test News 2',
            content='Test Content 2',
            author=self.user_admin,
            is_open=False
        )
        verticals = Vertical.objects.all()[:2]
        instance.vertical.add(*verticals)

        verticals_admin = Vertical.objects.all()[2:]
        instance_admin.vertical.add(*verticals_admin)

        url = reverse('news-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]['id'] in [instance.id, instance_admin.id]
        assert response.json()[1]['id'] in [instance.id, instance_admin.id]
        assert "vertical" in response.json()[0]
        assert "vertical" in response.json()[1]

    def test_get_news_reader_only_draft(self):
        self.client.force_authenticate(user=self.user_reader)

        instance = News.objects.create(
            title='Test News',
            content='Test Content',
            author=self.user_publisher,
            is_open=False
        )
        instance.vertical.add(*self.user_reader.plan.vertical.all())
        instance_admin = News.objects.create(
            title='Test News 2',
            content='Test Content 2',
            author=self.user_admin,
            is_open=False
        )
        verticals = Vertical.objects.all()[:2]
        instance.vertical.add(*verticals)

        verticals_admin = Vertical.objects.all()[2:]
        instance_admin.vertical.add(*verticals_admin)

        url = reverse('news-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_get_news_reader_only_publisher(self):
        self.client.force_authenticate(user=self.user_reader)

        instance = News.objects.create(
            title='Test News',
            content='Test Content',
            author=self.user_publisher,
            is_open=True,
            published_at=timezone.now(),
            status=News.Status.PUBLISHED
        )
        instance.vertical.add(*self.user_reader.plan.vertical.all())

        instance_admin = News.objects.create(
            title='Test News 2',
            content='Test Content 2',
            author=self.user_admin,
            is_open=False
        )
        verticals = Vertical.objects.all()[:2]
        instance.vertical.add(*verticals)

        verticals_admin = Vertical.objects.all()[2:]
        instance_admin.vertical.add(*verticals_admin)

        url = reverse('news-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_allow_edit_news_admin(self):
        self.client.force_authenticate(user=self.user_admin)

        instance = News.objects.create(
            title='Test News',
            content='Test Content',
            author=self.user_publisher,
            is_open=False
        )
        verticals = Vertical.objects.all()[:2]
        instance.vertical.add(*verticals)

        url = reverse('news-detail', args=[instance.id])
        data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'author': self.user_publisher.id,
            'is_open': True
        }
        response = self.client.put(url, data)

        assert response.status_code == 200
        instance.refresh_from_db()
        assert instance.title == data['title']
        assert instance.content == data['content']
        assert instance.is_open == data['is_open']

    def test_allow_edit_news_publisher(self):
        self.client.force_authenticate(user=self.user_publisher)

        instance = News.objects.create(
            title='Test News',
            content='Test Content',
            author=self.user_publisher,
            is_open=False
        )
        verticals = Vertical.objects.all()[:2]
        instance.vertical.add(*verticals)

        url = reverse('news-detail', args=[instance.id])
        data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'author': self.user_publisher.id,
            'is_open': True
        }
        response = self.client.put(url, data)
        assert response.status_code == 200

    def test_deny_edit_news_publisher(self):
        self.client.force_authenticate(user=self.user_publisher)

        instance = News.objects.create(
            title='Test News',
            content='Test Content',
            author=self.user_admin,
            is_open=False
        )
        verticals = Vertical.objects.all()[:2]
        instance.vertical.add(*verticals)

        url = reverse('news-detail', args=[instance.id])
        data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'author': self.user_publisher.id,
            'is_open': True
        }
        response = self.client.put(url, data)
        assert response.status_code == 403