from django.views import generic
from django.shortcuts import render

from task_manager.models import (
    Worker,
    Task,
    TaskType,
    Position
)


def index(request):
    num_workers = Worker.objects.count()

    context = {
        "num_workers": num_workers,
    }

    return render(request, "task_manager/index.html", context=context)


class WorkerListView(generic.ListView):
    model = Worker


class TaskListView(generic.ListView):
    model = Task


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees")


class PositionListView(generic.ListView):
    model = Position


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
