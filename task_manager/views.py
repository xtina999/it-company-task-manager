from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

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


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")
    template_name = "task_manager/position_form.html"


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")
    template_name = "task_manager/position_form.html"


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "task_manager/position_confirm_delete.html"
    success_url = reverse_lazy("task_manager:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")
    template_name = "task_manager/task_type_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")
    template_name = "task_manager/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task-type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-type-list")

