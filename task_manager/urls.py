from django.urls import path

from task_manager.views import (
    index,
    WorkerListView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TaskTypeListView,
    TaskListView, TaskDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
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
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
]

app_name = "task_manager"
