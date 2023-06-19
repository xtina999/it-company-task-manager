from django.contrib.auth.models import AbstractUser
from django.db import models
from it_company_task_manager import settings


class Position(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=False, blank=False)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=6,
        choices=(
            ("Urgent", "Urgent"),
            ("High", "High"),
            ("Normal", "Normal"),
            ("Low", "Low"),
        ),
        default="Normal",
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="assignees"
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
