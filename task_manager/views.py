from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from task_manager.forms import WorkerUpdateForm, WorkerCreateForm, TaskForm, TaskSearchForm, WorkerAccountsUpdateForm
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
    queryset = Worker.objects.select_related("position")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related("position")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerAccountsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerAccountsUpdateForm
    success_url = reverse_lazy("task_manager:index")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "task_manager/worker_confirm_delete.html"
    success_url = reverse_lazy("task_manager:worker-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["task_types"] = TaskType.objects.all()
        context["search_form"] = TaskSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        priority = self.request.GET.get("priority")
        task_type = self.request.GET.get("task_type")
        is_completed = self.request.GET.get("is_completed")
        form = TaskSearchForm(self.request.GET)

        if priority:
            queryset = queryset.filter(priority=priority)
        if task_type:
            queryset = queryset.filter(task_type=task_type)
        if is_completed:
            is_completed = True if is_completed == "true" else False
            queryset = queryset.filter(is_completed=is_completed)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/task_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-list")


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
