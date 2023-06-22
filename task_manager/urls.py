from django.urls import path
from task_manager.views import (
    index,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerAccountsUpdateView,
    WorkerDeleteView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,

)

urlpatterns = [
    path("", index, name="index"),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "workers/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "workers/<int:pk>/update",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/accounts/<int:pk>/update",
        WorkerAccountsUpdateView.as_view(),
        name="worker-accounts-update"
    ),
    path(
        "workers/<int:pk>/delete",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="positions-create"
    ),
    path(
        "positions/<int:pk>/update",
        PositionUpdateView.as_view(),
        name="positions-update"
    ),
    path(
        "positions/<int:pk>/delete",
        PositionDeleteView.as_view(),
        name="positions-delete"
    ),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path(
        "task-types/create/",
        TaskTypeCreateView.as_view(),
        name="task-types-create"
    ),
    path(
        "task-types/<int:pk>/update",
        TaskTypeUpdateView.as_view(),
        name="task-types-update"
    ),
    path(
        "task-types/<int:pk>/delete",
        TaskTypeDeleteView.as_view(),
        name="task-types-delete"
    ),
    path(
        "projects/<int:project_id>/tasks/",
        ProjectDetailView.as_view(),
        name="task-list"
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "projects/<int:project_id>/tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"),

    path(
        "projects/<int:project_id>/tasks/<int:pk>/delete",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "projects/",
        ProjectListView.as_view(),
        name="project-list"
    ),
    path(
        "projects/<int:project_id>/",
        ProjectDetailView.as_view(),
        name="project-detail"
    ),
    path(
        "projects/create/",
        ProjectCreateView.as_view(),
        name="project-create"
    ),
    path(
        "projects/<int:project_id>/update",
        ProjectUpdateView.as_view(),
        name="project-update"
    ),
    path(
        "projects/<int:project_id>/delete",
        ProjectDeleteView.as_view(),
        name="project-delete"
    ),
]

app_name = "task_manager"
