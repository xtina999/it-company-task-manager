from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import render
from django.urls import reverse_lazy


from task_manager.forms import (
    WorkerUpdateForm,
    WorkerCreateForm,
    TaskForm,
    TaskSearchForm,
    WorkerAccountsUpdateForm,
    ProjectSearchForm,
    ProjectForm,
)
from task_manager.models import (
    Worker,
    Task,
    TaskType,
    Position, Project
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        project_id = self.request.GET.get("project_id")
        is_completed = self.request.GET.get("is_completed")

        tasks = Task.objects.filter(assignees=worker)

        if project_id:
            tasks = tasks.filter(project_id=project_id)

        if is_completed is not None:
            is_completed = True if is_completed.lower() == "true" else False
            tasks = tasks.filter(is_completed=is_completed)

        context["tasks"] = tasks
        return context


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


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        project_id = self.kwargs['project_id']
        return reverse("task_manager:project-detail", kwargs={"project_id": project_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        return context

    def form_valid(self, form):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        form.instance.project = project
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['project_id']
        return context

    def get_success_url(self):
        task = self.get_object()
        return reverse_lazy(
            "task_manager:project-detail",
            kwargs={"project_id": task.project_id}
        )


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/task_confirm_delete.html"

    def get_success_url(self):
        task = self.get_object()
        return reverse_lazy(
            "task_manager:project-detail",
            kwargs={"project_id": task.project_id}
        )


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


class ProjectMixin:
    @staticmethod
    def get_project(project_id):
        queryset = ProjectMixin.get_project_queryset()
        return get_object_or_404(queryset, id=project_id)

    @staticmethod
    def get_project_queryset():
        return Project.objects.all()


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProjectSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = ProjectMixin.get_project_queryset()
        is_completed = self.request.GET.get("is_completed")
        form = ProjectSearchForm(self.request.GET)

        if is_completed:
            is_completed = True if is_completed == "true" else False
            queryset = queryset.filter(is_completed=is_completed)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = "task_manager/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(self.request.GET)
        context["filtered_tasks"] = self.get_filtered_tasks().prefetch_related('task_type')
        context["task_types"] = TaskType.objects.all()
        return context

    def get_object(self, queryset=None):
        project_id = int(self.kwargs.get("project_id"))
        queryset = ProjectMixin.get_project_queryset()
        return get_object_or_404(queryset, id=project_id)

    def get_filtered_tasks(self):
        project_id = int(self.kwargs.get("project_id"))
        project = ProjectMixin.get_project(project_id)
        tasks = project.tasks.all()
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            tasks = tasks.filter(name__icontains=name)
        priority = self.request.GET.get("priority")
        if priority:
            tasks = tasks.filter(priority=priority)
        task_type_id = self.request.GET.get("task_type_id")
        if task_type_id:
            tasks = tasks.filter(task_type_id=task_type_id)

        is_completed = self.request.GET.get("is_completed")
        if is_completed is not None:
            is_completed = True if is_completed == "true" else False
            tasks = tasks.filter(is_completed=is_completed)
        return tasks.distinct()


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task_manager:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task_manager:project-list")

    def get_object(self, queryset=None):
        project_id = self.kwargs.get("project_id")
        return ProjectMixin.get_project(project_id)


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    template_name = "task_manager/project_confirm_delete.html"
    success_url = reverse_lazy("task_manager:project-list")

    def get_object(self, queryset=None):
        project_id = self.kwargs.get("project_id")
        return ProjectMixin.get_project(project_id)
