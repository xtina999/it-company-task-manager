from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import timedelta

from django.utils import timezone
from task_manager.models import Position, TaskType, Worker, Task, Project


POSITION_URL = reverse("task_manager:position-list")
TASK_TYPE_URL = reverse("task_manager:task-type-list")
PROJECT_URL = reverse("task_manager:project-list")
WORKER_URL = reverse("task_manager:worker-list")
INDEX_URL = reverse("task_manager:index")


class PublicTests(TestCase):

    def test_index_required(self):
        res = self.client.get(INDEX_URL)

        self.assertNotEqual(res.status_code, 300)

    def test_position_login_required(self):
        res = self.client.get(POSITION_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_task_type_login_required(self):
        res = self.client.get(TASK_TYPE_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_project_login_required(self):
        res = self.client.get(PROJECT_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_worker_login_required(self):
        res = self.client.get(WORKER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivatePositionTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)
        self.position = Position.objects.create(name="PositionTests")
        self.task_type = TaskType.objects.create(name="TaskTypeTests")
        self.worker = Worker.objects.create(
            username="TestUser",
            password="test1234",
            first_name="TestFirst",
            last_name="TestLast",
            position=self.position
        )
        self.project = Project.objects.create(
            name="ProjectTests",
            description="ProjectDescription",
            deadline=timezone.now().date() + timedelta(days=1),
            is_completed=True,
        )
        self.project.assignees.set([self.worker])
        self.project1 = Project.objects.create(
            name="Project1Tests",
            description="Project1Description",
            deadline=timezone.now().date() + timedelta(days=1),
            is_completed=False,
        )
        self.project1.assignees.set([self.worker])
        self.project2 = Project.objects.create(
            name="Project2Tests",
            description="Project2Description",
            deadline=timezone.now().date() + timedelta(days=1),
            is_completed=False,
        )
        self.project2.assignees.set([self.worker])

        self.task1 = Task.objects.create(
            name="Task1Tests",
            description="Test1Description",
            created_at=timezone.now().date(),
            deadline=timezone.now().date() + timedelta(days=1),
            is_completed=True,
            priority="Low",
            task_type=self.task_type,
            project=self.project

        )
        self.task1.assignees.set([self.worker])
        self.task2 = Task.objects.create(
            name="Task2Tests",
            description="Test2Description",
            created_at=timezone.now().date(),
            deadline=timezone.now().date() + timedelta(days=1),
            is_completed=False,
            priority="Urgent",
            task_type=self.task_type,
            project=self.project

        )
        self.task2.assignees.set([self.worker])

    def test_retrieve_index(self):
        response = self.client.get(INDEX_URL)
        num_workers = Worker.objects.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_workers"], num_workers)
        self.assertTemplateUsed(response, "task_manager/index.html")

    def test_project_search_form_initial_value(self):
        response = self.client.get(PROJECT_URL)
        form = response.context["search_form"]

        self.assertEqual(form.initial["name"], "")

    def test_project_search_results(self):
        project1 = Project.objects.get(id=1)
        project2 = Project.objects.get(id=2)
        project3 = Project.objects.get(id=3)

        form_data = {"name": "ProjectTests"}

        response = self.client.get(PROJECT_URL, form_data)

        self.assertContains(response, project1.name)
        self.assertNotContains(response, project2.name)
        self.assertNotContains(response, project3.name)

    def test_project_no_search_results(self):
        form_data = {"name": "Project5"}
        response = self.client.get(PROJECT_URL, form_data)

        self.assertContains(
            response,
            "The are no project in company"
        )

    def test_project_search_few_results(self):
        project1 = Project.objects.get(id=1)
        project2 = Project.objects.get(id=2)
        project3 = Project.objects.get(id=3)

        form_data = {"name": "Project"}
        response = self.client.get(PROJECT_URL, form_data)

        expected_names = [
            project1.name,
            project2.name,
            project3.name
        ]
        for name in expected_names:
            self.assertContains(response, name)

    def test_project_filter_py_is_completed(self):
        project1 = Project.objects.get(id=1)
        project2 = Project.objects.get(id=2)
        project3 = Project.objects.get(id=3)

        response = self.client.get(PROJECT_URL, {"is_completed": "true"})

        self.assertContains(response, project1.name)
        self.assertNotContains(response, project2.name)
        self.assertNotContains(response, project3.name)

    def test_project_tasks_search_results(self):
        project1 = Project.objects.get(id=1)
        project_id = project1.id
        url = reverse("task_manager:task-list", args=[project_id])
        data = {"name": "Task1Tests"}
        response = self.client.get(url, data)
        self.assertContains(response, "Task1Tests")

    def test_project_tasks_no_search_results(self):
        project_id = self.project.id
        url = reverse("task_manager:task-list", args=[project_id])
        data = {"name": "ProTask"}
        response = self.client.get(url, data)
        self.assertNotContains(response, "Task1Tests")

    def test_project_tasks_search_few_results(self):
        project_id = self.project.id
        url = reverse("task_manager:task-list", args=[project_id])
        data = {"name": "Task"}
        response = self.client.get(url, data)

        expected_names = [
            self.task1.name,
            self.task2.name,
        ]

        for name in expected_names:
            self.assertContains(response, name)

    def test_project_tasks_filter_by_is_completed(self):
        project_id = self.project.id
        url = reverse("task_manager:task-list", args=[project_id])

        response = self.client.get(url, {"is_completed": "true"})

        self.assertContains(response, self.task1.name)

    def test_project_tasks_filter_by_priority(self):
        project_id = self.project.id
        url = reverse("task_manager:task-list", args=[project_id])

        response = self.client.get(url, {"priority": "Low"})

        self.assertContains(response, self.task1.name)

    def test_project_tasks_filter_by_task_type(self):
        project_id = self.project.id
        url = reverse("task_manager:task-list", args=[project_id])

        response = self.client.get(url, {"task_type": self.task_type})
        expected_names = [
            self.task1.name,
            self.task2.name,
        ]

        for name in expected_names:
            self.assertContains(response, name)
