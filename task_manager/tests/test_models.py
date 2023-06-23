from datetime import timedelta

from django.test import TestCase

from django.utils import timezone
from task_manager.models import Position, TaskType, Worker, Task, Project


class ModelsTest(TestCase):

    def setUp(self) -> None:
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

        self.task = Task.objects.create(
            name="TaskTests",
            description="TestDescription",
            created_at=timezone.now().date(),
            deadline=timezone.now().date() + timedelta(days=1),
            is_completed=True,
            priority="Urgent",
            task_type=self.task_type,
            project=self.project

        )
        self.task.assignees.set([self.worker])

    def test_position_str(self):
        self.assertEqual(
            str(self.position), self.position.name
        )

    def test_task_type_str(self):
        self.assertEqual(
            str(self.task_type), self.task_type.name
        )

    def test_worker_str(self):
        expected_object_name = f"{self.worker.last_name} {self.worker.first_name}"

        self.assertEqual(
            str(self.worker), expected_object_name
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), self.project.name)

    def test_task_str(self):
        self.assertEqual(str(self.task), self.task.name)
