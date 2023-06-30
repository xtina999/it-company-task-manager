from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="Test_position")
        self.worker = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            position=self.position
        )

    def test_worker_detailed_position_listed(self):
        """Tests that worker's position
        is in on worker detail admin page"""
        url = reverse(
            "admin:task_manager_worker_change",
            args=[self.worker.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

